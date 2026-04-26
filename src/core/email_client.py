import os
from dotenv import load_dotenv
from imap_tools import MailBox

def get_email_credentials():
    """Loads email credentials from the .env file."""
    load_dotenv()
    return os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS")

def fetch_emails():
    """
    Connects to an IMAP server and fetches the 50 most recent emails.
    Returns a list of emails or an error message string.
    """
    user, password = get_email_credentials()
    if not user or not password:
        return "Credentials not found. Please configure your settings."

    # Using Gmail as an example. Change for other providers (e.g., 'outlook.office.com')
    try:
        with MailBox('imap.gmail.com').login(user, password, 'INBOX') as mailbox:
            emails = []
            # Fetch the 50 most recent emails
            for msg in mailbox.fetch(limit=50, reverse=True):
                emails.append({
                    "from": msg.from_,
                    "subject": msg.subject,
                    "date": msg.date_str
                })
            return emails
    except Exception as e:
        # Catching a general exception is more robust across library versions.
        # We can check the error text to see if it was a login problem.
        error_message = str(e).lower()
        # This check is more specific to the error you saw
        if 'authenticationfailed' in error_message or 'invalid credentials' in error_message:
            return "Login failed. Please double-check your email and the 16-digit App Password."
        
        return f"An unknown error occurred: {e}"

