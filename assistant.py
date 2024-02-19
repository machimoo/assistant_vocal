import pyttsx3
import speech_recognition as sr
import boto3
from google.oauth2.service_account import Credentials
import io
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document

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

    # Définir les scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    # L'ID du fichier sur Google Drive que vous souhaitez modifier
    file_id = '1xfc5bpGMFMst_kHQUhS_5_eHsCgBIKAXjf9hoieYcfE'

    # Demander à l'API d'exporter le fichier en format Microsoft Word (.docx)
    request = service.files().export_media(fileId=file_id,
                                           mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    fh = io.BytesIO()
    # Télécharger le fichier
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Téléchargement %d%%." % int(status.progress() * 100))

    # Écrire le contenu dans un fichier .docx
    with open('test course.docx', 'wb') as f:
        f.write(fh.getbuffer())
    print("Le fichier a été exporté et sauvegardé en tant que 'votre_fichier.docx'.")

    doc = Document('test course.docx')

    # Reconnaître la commande vocale
    command = r.recognize_google(audio, language='fr-fr')

    # Ajouter un paragraphe avec du texte
    doc.add_paragraph(command)

    # Sauvegarder les modifications dans le fichier
    doc.save('test course.docx')

    # Préparer le fichier pour le téléversement
    media = MediaFileUpload('test course.docx',
                        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        resumable=True)

    # Mettre à jour le fichier
    updated_file = service.files().update(fileId=file_id,
                                          media_body=media).execute()





except sr.UnknownValueError:
    print("Impossible de comprendre la commande vocal.")

