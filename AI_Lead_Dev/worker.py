import time
from database import SessionLocal, LeadEmail
from intelligence import classify_intent

def process_new_emails():
    """
    - Fetches email with status 'new'
    - Classified their intent using the intelligence module
    - Updates the database with the results.
    """

    db = SessionLocal()
    try:
        email_to_process = db.query(LeadEmail).filter(LeadEmail.status=='new').all()

        if not email_to_process:
            print("No new emails to process. Waiting....")
            return

        print(f"Found {len(email_to_process)} new emails to process")

        for email in email_to_process:
            print(f"Processing email ID : {email.id} from {email.sender}")

            try:
                classification_result = classify_intent(email.body)

                email.intent = classification_result.intent_type
                email.is_sales_lead = classification_result.is_sales_lead
                email.summary = classification_result.summary
                email.status = 'classified'

                print(f"-> Classified as: {email.intent}")

                db.commit()

            except Exception as e:
                print(f"!! Error processing email ID {email.id}: {e}")
                email.status = 'error'
                db.commit()

    finally:
        db.close()


if __name__ == '__main__':
    print("Starting the classification worker.....")

    while True:
        process_new_emails()
        time.sleep(10)
