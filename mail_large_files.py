import base64
import io
import json
import os
from email import utils, encoders
from email.message import EmailMessage
from email.mime import application, multipart, text, base, image, audio
import mimetypes
import datetime
from apiclient import errors
from googleapiclient import discovery, http
from google.oauth2 import service_account


def get_environment_variables():
    """ Retrieves the environment variables and returns them in
        a dictionary object.
    """
    env_var_dict = {
        'to': os.environ.get('TO'),
        'subject': os.environ.get('SUBJECT'),
        'body': os.environ.get('BODY'),
        'file': os.environ.get('FILE')
    }

    return env_var_dict


def send_email(email_subject, email_body, email_sender='', email_to='', email_cc='', email_bcc='', files=None):

    # Pulling in the string value of the service key from the parameter
    with open(r'C:\Users\___.json') as f:
        service_account_info = json.loads(f.read())

    # Define which scopes we're trying to access
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Setting up credentials using the gmail api
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    # This allows us to assign an alias account to the message so that the messages aren't coming from 'ServiceDriod-8328balh blah blah'
    delegated_credentials = credentials.with_subject(email_sender)
    # 'Building' the service instance using the credentials we've passed
    service = discovery.build(serviceName='gmail', version='v1', credentials=delegated_credentials)

    # Building out the email
    message = multipart.MIMEMultipart()
    message['to'] = email_to
    message['from'] = email_sender
    message['date'] = utils.formatdate(localtime=True)
    message['subject'] = email_subject
    message['cc'] = email_cc
    message['bcc'] = email_bcc
    message.attach(text.MIMEText(email_body, 'plain'))

    for f in files or []:
        f = f.strip(' ')
        mimetype, encoding = mimetypes.guess_type(f)

        # If the extension is not recognized it will return: (None, None)
        # If it's an .mp3, it will return: (audio/mp3, None) (None is for the encoding)
        # For an unrecognized extension we set mimetype to 'application/octet-stream' so it won't return None again.
        if mimetype is None or encoding is not None:
            mimetype = 'application/octet-stream'
        main_type, sub_type = mimetype.split('/', 1)

        # Creating the attachement:
        # This part is used to tell how the file should be read and stored (r, or rb, etc.)
        if main_type == 'text':
            print('text')
            with open(f, 'rb') as outfile:
                attachement = text.MIMEText(outfile.read(), _subtype=sub_type)
        elif main_type == 'image':
            print('image')
            with open(f, 'rb') as outfile:
                attachement = image.MIMEImage(outfile.read(), _subtype=sub_type)
        elif main_type == 'audio':
            print('audio')
            with open(f, 'rb') as outfile:
                attachement = audio.MIMEAudio(outfile.read(), _subtype=sub_type)
        elif main_type == 'application' and sub_type == 'pdf':
            with open(f, 'rb') as outfile:
                attachement = application.MIMEApplication(outfile.read(), _subtype=sub_type)
        else:
            attachement = base.MIMEBase(main_type, sub_type)
            with open(f, 'rb') as outfile:
                attachement.set_payload(outfile.read())

        encoders.encode_base64(attachement)
        attachement.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f))
        message.attach(attachement)

    media_body = http.MediaIoBaseUpload(io.BytesIO(message.as_bytes()), mimetype='message/rfc822', resumable=True)
    body_metadata = {} # no thread, no labels in this example

    try:
        print('Uploading file...')
        response = service.users().messages().send(userId='me', body=body_metadata, media_body=media_body).execute()
        print(response)
    except errors.HttpError as error:
        print('An error occurred when sending the email:\n{}'.format(error))


if __name__ == '__main__':

    env_var_dict = get_environment_variables()
    print("Sending email...")
    send_email(email_subject='test',
               email_body='Hi.',
               email_to= ','.join(['']),
               files=[r'C:\Users\___.csv'])

    print("Email sent!")