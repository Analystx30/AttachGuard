import os
import imaplib
import email
from email.header import decode_header
import subprocess
import smtplib
import time
import random
import string
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import calendar



# Function to generate a random folder name
def generate_random_folder_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to process attachments using dangerzone
def process_attachments(msg, output_path):
    generated_pdfs = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        folder_name = generate_random_folder_name()
        folder_path = os.path.join(output_path, folder_name)
        os.makedirs(folder_path)

        filename = part.get_filename()
        data = part.get_payload(decode=True)

        # Save the attachment
        attachment_path = os.path.join(folder_path, filename)
        with open(attachment_path, 'wb') as f:
            f.write(data)

        # Run dangerzone command line
        output_pdf_path = os.path.join(folder_path, f"{filename}-safe.pdf")
        subprocess.run(["dangerzone-cli", "--output-filename", output_pdf_path, attachment_path])

        generated_pdfs.append(output_pdf_path)

    return generated_pdfs

# Function to send email with PDF attachments
def send_email_with_attachments(sender_email, sender_password, recipient_email, subject, body, attachments):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEApplication(body, 'plain'))

    for attachment in attachments:
        with open(attachment, "rb") as file:
            attach_part = MIMEApplication(file.read(), Name=attachment)
            attach_part['Content-Disposition'] = f'attachment; filename="{attachment}"'
            message.attach(attach_part)

    server = smtplib.SMTP('imap.google.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    server.quit()

# Function to delete the processed email
def delete_email(email_address, password, mail_id):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, password)
    mail.select("inbox")

    mail.store(mail_id, '+FLAGS', '(\Deleted)')
    mail.expunge()
    mail.close()
    mail.logout()

# Function to clean generated folders and their contents
def clean_folders(folder_paths):
    for folder_path in folder_paths:
        shutil.rmtree(folder_path)

# IMAP settings
email_address = 'mail@mail.com'
password = 'password'
imap_server = 'imap.google.com

# Function to update and save email statistics to a text file
def update_email_statistics(sender_email, statistics_file):
    if not os.path.exists(statistics_file):
        with open(statistics_file, 'w') as file:
            file.write("Sender Email\tEmail Count\n")

    with open(statistics_file, 'a') as file:
        file.write(f"{sender_email}\t1\n")

# Function to check for new emails and process them
def check_and_process_email():
    sender_counts = {}
    email_statistics_file = 'email_statistics.txt'

    while True:
        current_month = datetime.now().month
        current_year = datetime.now().year

        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        mail.select("inbox")

        # Search for unseen emails
        result, data = mail.search(None, "UNSEEN")

        if data[0]:
            for num in data[0].split():
                result, message_data = mail.fetch(num, "(RFC822)")
                raw_email = message_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Check if sender has reached the email limit for the current month
                sender_email = msg['From']
                if sender_email not in sender_counts:
                    sender_counts[sender_email] = 1
                    update_email_statistics(sender_email, email_statistics_file)
                else:
                    sender_counts[sender_email] += 1
                    # Update email statistics
                    with open(email_statistics_file, 'r') as file:
                        lines = file.readlines()
                    with open(email_statistics_file, 'w') as file:
                        for line in lines:
                            if sender_email in line:
                                email_count = int(line.split('\t')[1]) + 1
                                line = f"{sender_email}\t{email_count}\n"
                            file.write(line)

                if sender_counts[sender_email] > 3:
                    # Send quota exceeded email
                    quota_exceeded_subject = 'Quota Exceeded'
                    quota_exceeded_body = 'Sorry, deine Quota ist aufgebraucht.'
                    send_email(sender_email, password, quota_exceeded_subject, quota_exceeded_body)

                    # Delete the processed email from the inbox
                    delete_email(email_address, password, num)

                    continue

                # Create a folder to store attachments and generated PDFs
                output_path = 'generated_pdfs/'
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                # Process attachments using dangerzone
                generated_pdfs = process_attachments(msg, output_path)

                # Sender and recipient details for the reply email
                sender_email = 'mail@mail.com'
                sender_password = 'password'
                recipient_email = msg['From']
                reply_subject = 'Ihre Anhänge wurden bereinigt!'
                reply_body = 'Attached are the processed PDFs.'

                # Send the reply email with processed PDF attachments
                send_email_with_attachments(sender_email, sender_password, recipient_email, reply_subject, reply_body, generated_pdfs)

                # Delete the processed email from the inbox
                delete_email(email_address, password, num)

                # Clean generated folders and their contents
                clean_folders([os.path.dirname(pdf_path) for pdf_path in generated_pdfs])

        mail.close()
        mail.logout()

        time.sleep(3)  # Check for new emails every 3 seconds

# Start the continuous email checking and processing loop
check_and_process_email()
