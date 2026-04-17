# Website Monitoring Script

This Python script:
- Checks website status
- Sends email alerts if down
- SSH into server and runs Docker commands

## Setup

1. Install dependencies:
pip install -r requirements.txt

2. Create .env file:
EMAIL_ADDRESS=
EMAIL_PASSWORD=
SSH_KEY_PATH=

3. Run:
`python monitor-website.py`