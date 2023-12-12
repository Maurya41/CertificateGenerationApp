import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow



if not os.path.exists("./token.json"):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send'];
    flow = InstalledAppFlow.from_client_secrets_file('./assets/token.json', SCOPES);
    credentials = flow.run_local_server(port=0);

    # Save the credentials for future use
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

def gmail_send_mail_with_attachment(From ,TO, name, file_name,url):
    try:
    # create gmail api client
        service = build("gmail", "v1", credentials=
                        Credentials.from_authorized_user_file('token.json'));

        mime_message = EmailMessage();

        # headers
        mime_message["To"] = TO;
        mime_message["From"] = "mgor9198@gmail.com";
        mime_message["Subject"] = "Congratulations on Completing \
            the Software Engineering Program";

        # text
        mime_message.add_alternative(
            f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congratulations on Completing the Software Engineering Program</title>
</head>
<body>
    <p>Dear {name},</p>

    <p>I hope this message finds you well. We are thrilled to inform you that you have successfully completed the Software Engineering Program! Your dedication and hard work throughout the program have truly paid off.</p>

    <p>Attached to this email, you will find your official certificate recognizing your achievement in Software Engineering. This certificate is a testament to your commitment to excellence in the field.</p>

    <p>We commend you on reaching this significant milestone and hope that this accomplishment opens new doors of opportunities for your professional journey.</p>

    <p>Should you have any questions or require further information, feel free to reach out.</p>

    <p>Congratulations once again, and we wish you continued success in all your future endeavors!</p>

    <p>Best regards,<br>{From}</p>

    <p>In order to see Certificate on portal <a href="{url.decode('utf-8')}">click here</a></p>
</body>
</html>

""",subtype='html');

        # attachment
        attachment_filename = os.path.basename(file_name);
        # guessing the MIME type
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split("/")

        with open(file_name, "rb") as fp:
            attachment_data = fp.read()
        mime_message.add_attachment(attachment_data, maintype, subtype)

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode('utf-8')

        create_message = {"raw": encoded_message};
        # pylint: disable=E1101

        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

    except HttpError as error:
        print(f"An error occurred: {error}")
        draft = None

    print(f"mail is sent to {name}");

    return send_message;


if __name__ == "__main__":
  gmail_send_mail_with_attachment("Destroyer","dippatel3102001@gmail.com","Dip",'./tmp/Dip_certificate.jpg')