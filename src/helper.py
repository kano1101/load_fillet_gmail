import base64
import os
import pickle
import quopri

import gspread
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery as client


def get_soups_with_gmail_labels(labels: [str]) -> object:
    """"""
    scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
    ]
    creds = get_credentials_cover(scopes)
    soups = get_soups_for_labels(creds=creds, labels=labels)
    return soups


def get_soups_for_labels(creds, labels):
    soups = []
    for label in labels:
        service, messages = get_emails(creds, label)
        for message in messages:
            soups.append(get_soup_from_message(service=service, message=message))
    return soups


def open_spreadsheet_on_default_account(spreadsheet_id):
    gc = gspread.service_account(filename='service_account.json')
    ss = gc.open_by_key(spreadsheet_id)
    return ss


def get_emails(creds, label):
    """Gmailからメールを取得する"""
    service = client.build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=f"label:{label}",
                                              maxResults=30).execute()
    messages = results.get('messages', [])
    return service, messages


def get_credentials_cover(scopes):
    return get_credentials('token.pickle', 'credentials.json', scopes=scopes)


def get_credentials(pickle_file, creds_file, scopes):
    # 保存された認証情報を読み込む
    creds = None
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)

    # 保存された認証情報が無効か、スコープが変更されている場合は再認証
    if not creds or not creds.valid or creds.scopes != scopes:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, scopes=scopes)
            creds = flow.run_local_server(port=0)
        with open(pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_soup_from_message(service, message):
    msg_raw = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
    msg_body = base64.urlsafe_b64decode(msg_raw['raw'].encode('ASCII'))
    decoded_table = quopri.decodestring(msg_body).decode("utf-8", errors='ignore')
    soup = BeautifulSoup(decoded_table, 'html.parser')
    return soup


def get_list_subject_and_from_email(creds, labels):
    list_subject_and_from_email = []
    for label in labels:
        service, messages = get_emails(creds, label)
        for message in messages:
            subject_and_from_email = get_subject_and_from_email(service=service, message=message)
            list_subject_and_from_email.append(subject_and_from_email)
    return list_subject_and_from_email


def get_subject_and_from_email(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='metadata',
                                         metadataHeaders=['From', 'Subject']).execute()
    from_email = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), None)
    subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
    return subject, from_email


def get_list_subject_and_from_email_with_gmail_label(labels):
    """"""
    scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
    ]
    creds = get_credentials_cover(scopes)
    list_subject_and_from_email = get_list_subject_and_from_email(creds=creds, labels=labels)
    return list_subject_and_from_email


def get_recipe_support_spreadsheet():
    """"""
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')
    ss = open_spreadsheet_on_default_account(spreadsheet_id)
    return ss


def get_worksheet_in_recipe_support(ss, sheet_name):
    return ss.worksheet(sheet_name)
