import imaplib
import email
import os
from dotenv import load_dotenv
import time
from datetime import datetime

from database import SessionLocal, LeadEmail

load_dotenv()

IMAP_SERVER=os.getenv("IMAP_SERVER")
IMAP_USERNAME=os.getenv("IMAP_USERNAME")
IMAP_PASSWORD=os.getenv("IMAP_PASSWORD")

def get_email_body(msg):
    """Extract the plain text body from an email message"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and "attachment" not in part.get("Content-Disposition", ""):
                try:
                    return part.get_payload(decode=True).decode('utf-8')
                except UnicodeDecodeError:
                    return part.get_payload(decode=True).decode('latin-1', 'ignore')
                
    else:
        if msg.get_content_type() == "text/plain":
            try:
                return msg.get_payload(decode=True).decode('utf-8')
            except UnicodeDecodeError:
                    return msg.get_payload(decode=True).decode('latin-1', 'ignore')
    return ""


def save_email_to_db(email_message):
    """Saves a parsed email messages to the database"""
    db = SessionLocal()
    try:
        existing_email = db.query(LeadEmail).filter(LeadEmail.message_id == email_message["Message-ID"]).first()
        if existing_email:
            print(f"Email with message id {email_message["Message-ID"]} already exists. Skipping")
            return
        
        new_lead = LeadEmail(
            message_id = email_message["Message-ID"],
            sender=email_message["From"],
            subject = email_message["Subject"],
            body=get_email_body(email_message),
            received_at=datetime.utcnow()
        )

        db.add(new_lead)
        db.commit()
        print(f"Successfully save email from {new_lead.sender} to DB.")
    except Exception as e:
        print(f"Error saving email to DB: {e}")
        db.rollback()
    finally:
        db.close()



def fetch_unread_emails():
    """Connects to the IMAP server and fetches unread emails"""

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(IMAP_USERNAME, IMAP_PASSWORD)

        mail.select('inbox')

        status, messages = mail.search(None, "UNSEEN")

        if status == "OK":
            email_ids = messages[0].split()
            if not email_ids:
                print("No new unread emails")
                return []
            print(f"Found {len(email_ids)} new emails")

            fetched_emails = []

            for email_id in email_ids:
                _, msg_data = mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        fetched_emails.append(msg)
        
            return fetched_emails
        else:
            print("Failed to search for emails")
            return []
    except Exception as e:
        print(f"An Error occured: {e}")
        return []

if __name__ == '__main__':
    while True:
        print("Checking for new emails")
        new_emails = fetch_unread_emails()
        for email_message in new_emails:
            save_email_to_db(email_message)

        print("Waiting for 10 seconds")
        time.sleep(10)
                
