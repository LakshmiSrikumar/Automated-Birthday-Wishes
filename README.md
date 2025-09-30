# Birthday Wisher

A Python script to send personalized birthday wishes via Gmail SMTP.

## Features

- Reads user data from a CSV file (`birthdays.csv`)
- Checks if today is a user's birthday
- Sends personalized emails using Gmail SMTP with app password
- Loads sensitive credentials securely from `.env`
- Error handling for file, parsing, and SMTP errors

## Setup

1. **Clone the repo or download files**

2. **Create a Gmail App Password**

- Go to your Google Account -> Security -> App passwords
- Generate an app password for "Mail" and device "Other"
- Copy the 16-character password

3. **Create `.env` file**

Copy `.env.example` to `.env` and add your Gmail address and app password

4. **Install dependencies & run **

```bash
pip install -r requirements.txt
python birthday_wish.py

