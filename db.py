import pymysql
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tkinter import filedialog
from googleapiclient.http import MediaFileUpload
import os.path
import google.auth
import io

def obtener_conexion():
    return pymysql.connect(host='bd2341mktthoeb7zplfj-mysql.services.clever-cloud.com',
                          user='u6ayukwzc92exyfv',
                          password='woEJDljV8aeJwbhrspYE',
                          db='bd2341mktthoeb7zplfj',
                          port=3306)

def PostImgDrive(img):

    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    TOKEN_PATH = "token.json"
    CREDENTIALS_PATH = "credenciales.json"
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        API_NAME ="drive"
        DRIVE_VERSION = "v3"
        service = build(API_NAME, DRIVE_VERSION, credentials=creds)

        file_metadata = {"name": img,
                         'parents': ['128AT6WK_l9CecKnMgwGpVeo3rarLJSJ9']}
        
        media = MediaFileUpload("templates/img/"+img, mimetype="application/octet-stream",resumable=True)
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
    
        print(f'File ID: {file.get("id")}')
        
    except HttpError as error:
        print(f"An error occurred: {error}")

def getImg(img):

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = None
    TOKEN_PATH = "token.json"
    CREDENTIALS_PATH = "credenciales.json"

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("drive", "v3", credentials=creds)
        files = []
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            
            for file in response.get("files", []):
                if file.get("name") == img:
                    print(f'Found file: {file.get("name")}, {file.get("id")}')
                    idimg = file.get("id")

            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
            
    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None
    
    return idimg

def deleteImg(idimg):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    TOKEN_PATH = "token.json"
    CREDENTIALS_PATH = "credenciales.json"

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        API_NAME ="drive"
        DRIVE_VERSION = "v3"
        service = build(API_NAME, DRIVE_VERSION, credentials=creds)

        body_value = {'trashed': True}

        response = service.files().delete(fileId=idimg).execute()
        
    except HttpError as error:
        print(f"An error occurred: {error}")

global file