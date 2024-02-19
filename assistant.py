import pyttsx3
import speech_recognition as sr
import boto3
from google.oauth2.service_account import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document


def initialize_google_drive_api(service_account_file, scopes):
    credentials = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    service = build('drive', 'v3', credentials=credentials)
    return service

def append_text_to_docx(file_path, text):
    doc = Document(file_path)
    doc.add_paragraph(text)
    doc.save(file_path)

def update_file_on_google_drive(service, FILE_ID, file_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
    media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)
    updated_file = service.files().update(fileId=FILE_ID, media_body=media).execute()
    return updated_file

def download_file_as_docx(service, FILE_ID, output_file_name):
    request = service.files().export_media(fileId=FILE_ID, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    with open(output_file_name, 'wb') as f:
        f.write(fh.getbuffer())
    print(f"Le fichier a été exporté et sauvegardé en tant que '{output_file_name}'.")


# Initialiser l'objet recognizer
r = sr.Recognizer()

with sr.Microphone() as source:

    print("Dites quelque chose...")


    try:
        audio = r.listen(source, timeout=5)

    except sr.WaitTimeoutError:
        print("La durée d'attente maximale de 5 secondes est écoulée. Aucune commande vocale détectée.")
        exit()


try:


    # Chemin vers vos credentials du compte de service
    SERVICE_ACCOUNT_FILE = '/home/emal2090/perso/google.json'
    OUTPUT_FILE_NAME = 'test course.docx'
    # L'ID du fichier sur Google Drive que vous souhaitez modifier
    FILE_ID = '1xfc5bpGMFMst_kHQUhS_5_eHsCgBIKAXjf9hoieYcfE'
    # Définir les scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = initialize_google_drive_api(SERVICE_ACCOUNT_FILE, SCOPES)


    # Reconnaître la commande vocale
    command = r.recognize_google(audio, language='fr-fr')

    append_text_to_docx(OUTPUT_FILE_NAME, command)

    update_file_on_google_drive(service, FILE_ID,OUTPUT_FILE_NAME)

    download_file_as_docx(service, FILE_ID, OUTPUT_FILE_NAME)


    # Préparer le fichier pour le téléversement
    media = MediaFileUpload('test course.docx',
                        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        resumable=True)

    # Mettre à jour le fichier
    updated_file = service.files().update(fileId=FILE_ID,
                                          media_body=media).execute()






except sr.UnknownValueError:
    print("Impossible de comprendre la commande vocal.")

