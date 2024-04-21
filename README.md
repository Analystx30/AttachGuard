# AttachGuard

## AttachGuard is a standalone Service for cleaning mailattachments if you're not sure if it's malicious or not.

AttachGuard is a standalone service implemented as a continuously running Python script. It retrieves email attachments from a web mailbox, extracts the RGB pixels in a container, and converts them into a PDF. Afterwards, the script sends the attachment back to the sender and deletes the email along with the downloaded attachment.

The script can be easily operated on a Linux distribution, such as a Raspberry Pi, or similar devices in a separate network. It only requires access to the webmail. This provides a simple solution, for example, to offer your employees a way to neutralize suspicious attachments.

**IMPORTANT:** This is not a 100% protection against malware or phishing attempts. While it may increase security measures, the risk and responsibility of using this service solely lie with the user.


This service is inspired by Qubes trusted PDF and Micah Lee's "Dangerzone".
https://dangerzone.rocks/about.html
https://blog.invisiblethings.org/2013/02/21/converting-untrusted-pdfs-into-trusted.html

## Installation

1. Install the Dangerzone-Tool from this repo (select your OS)

    https://github.com/freedomofpress/dangerzone

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/AttachGuard.git
    ```

2. Navigate to the directory:

    ```bash
    cd AttachGuard
    ```

3. Change Mailbox Credentials in AttachGuard.py:

    ```Edit:
    server = smtplib.SMTP('imap.google.com', 587)

    # IMAP settings
    email_address = 'mail@mail.com'
    password = 'password'
    imap_server = 'imap.google.com

    # Sender and recipient details for the reply email
    sender_email = 'mail@mail.com'
    sender_password = 'password'
     
    ```

4. Let's try:

    ```bash
    python3 AttachGuard.py
    ```

    
## Usage

1. The Python script now runs and queries the mailbox every 3 seconds until the script is stopped. It can also be configured as a service.


## Features

- Cleans documents within a very short time.
- Can be operated on a Raspberry Pi.
- Can currently clean the following data types:
PDF (.pdf)
Microsoft Word (.docx, .doc)
Microsoft Excel (.xlsx, .xls)
Microsoft PowerPoint (.pptx, .ppt)
ODF Text (.odt)
ODF Spreadsheet (.ods)
ODF Presentation (.odp)
ODF Graphics (.odg)
Hancom HWP (Hangul Word Processor) (.hwp, .hwpx)
Not supported on Qubes OS
EPUB (.epub)
Jpeg (.jpg, .jpeg)
GIF (.gif)
PNG (.png)
SVG (.svg)
other image formats (.bmp, .pnm, .pbm, .ppm)

## Contributing

- For issues or suggestions, please create an issue.
- Pull requests are welcome.

## License

This project is licensed under the MIT License. For mor
