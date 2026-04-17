from time import time

import requests
import smtplib
import os
from dotenv import load_dotenv
import paramiko
import linode_api4
import schedule

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
LINODE_TOKEN = os.getenv('LINODE_TOKEN')
SSH_KEY_PATH = os.getenv('SSH_KEY_PATH')

def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f'Subject: Website Down Alert\n\n{email_msg}'
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

def restart_linode_and_container():
    print('Rebooting server...')
    client = linode_api4.LinodeClient(token=LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 96160147)
    nginx_server.reboot()

    # restart application on linode server

    while True:
        nginx_server = client.load(linode_api4.Instance, 96160147)
        if nginx_server.status == 'running':
            restart_application()
            break
        else:
            print('Waiting for server to reboot...')
            time.sleep(10)

def restart_application():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('172.105.121.174', username='root', key_filename=SSH_KEY_PATH)
    print("Connected?")
    transport = ssh.get_transport()
    print(transport is not None and transport.is_active())
    stdin, stdout, stderr = ssh.exec_command('docker start 7220444ee984')
    stdout.channel.recv_exit_status()

    print("STDOUT:")
    print(stdout.read().decode())

    print("STDERR:")
    print(stderr.read().decode())
        
    ssh.close()

def monitor_application():
    try :
        response = requests.get('http://172-105-121-174.ip.linodeusercontent.com:8080')
        if response.status_code == 200:
            print('Website is up and running!')
        else:
            print('Website is down. Status code:', response.status_code)
            msg = f'Subject: Website Down Alert\n\nThe website is down. Status code: {response.status_code}'
            send_notification(msg)
            restart_application()
    except Exception as e:
        msg = f'An error occurred while checking the website: {str(e)}'
        send_notification(msg)

        # restart linode server

        restart_linode_and_container()

        print('Rebooting application...')

schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()

