import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv


def load_env_variables():
    """
    Loads environment variables from a .env file.

    Returns:
        tuple: (email_address, app_password)
    """
    load_dotenv()
    email_address = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not email_address or not app_password:
        raise EnvironmentError(
            "GMAIL_ADDRESS or GMAIL_APP_PASSWORD not found in environment variables."
        )
    return email_address, app_password


def read_birthdays(csv_file):
    """
    Reads the CSV file and returns a DataFrame.

    Args:
        csv_file (str): Path to CSV file.

    Returns:
        pd.DataFrame: DataFrame with user data.

    Raises:
        FileNotFoundError: If CSV file is not found.
        pd.errors.ParserError: If CSV parsing fails.
        ValueError: If required columns are missing.
    """
    try:
        df = pd.read_csv(csv_file, parse_dates=["DateOfBirth"])
    except FileNotFoundError as e:
        raise FileNotFoundError(f"CSV file not found: {csv_file}") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error parsing CSV file: {csv_file}") from e

    required_columns = {"Name", "DateOfBirth", "Email"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV file must contain columns: {required_columns}")

    return df


def get_todays_birthday_people(df):
    """
    Filters the DataFrame to find users whose birthday is today.

    Args:
        df (pd.DataFrame): DataFrame with user data.

    Returns:
        pd.DataFrame: Filtered DataFrame with today's birthday users.
    """
    today = datetime.now()
    # Compare month and day only
    birthday_people = df[
        (df["DateOfBirth"].dt.month == today.month) & (df["DateOfBirth"].dt.day == today.day)
    ]
    return birthday_people


def create_birthday_email(sender_email, recipient_email, recipient_name):
    """
    Composes a personalized birthday email.

    Args:
        sender_email (str): Sender's email address.
        recipient_email (str): Recipient's email address.
        recipient_name (str): Recipient's name.

    Returns:
        EmailMessage: Composed email message object.
    """
    msg = EmailMessage()
    msg["Subject"] = "Happy Birthday! 🎉"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    body = f"""\
    Dear {recipient_name},

    Wishing you a very Happy Birthday! May your day be filled with joy, laughter, and unforgettable moments.

    Best wishes,
    Your Friendly Birthday Bot
    """
    msg.set_content(body)
    return msg


def send_email(message, email_address, app_password):
    """
    Sends an email using Gmail SMTP server.

    Args:
        message (EmailMessage): The email message to send.
        email_address (str): Sender's Gmail address.
        app_password (str): Gmail app password.

    Raises:
        smtplib.SMTPException: If SMTP connection or sending fails.
    """
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, app_password)
            smtp.send_message(message)
    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(f"Failed to send email to {message['To']}: {e}")


def main():
    """
    Main function to read birthday data, filter today's birthdays,
    and send personalized birthday wishes via email.
    """
    try:
        sender_email, app_password = load_env_variables()
        df = read_birthdays("birthdays.csv")
        birthday_people = get_todays_birthday_people(df)

        if birthday_people.empty:
            print("No birthdays today. Have a nice day!")
            return

        for _, person in birthday_people.iterrows():
            try:
                email_msg = create_birthday_email(sender_email, person["Email"], person["Name"])
                send_email(email_msg, sender_email, app_password)
                print(f"Successfully sent birthday email to {person['Name']} ({person['Email']})")
            except smtplib.SMTPException as e:
                print(e)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
