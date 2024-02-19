import pyttsx3
import speech_recognition as sr
import boto3
from pydub import AudioSegment
from pydub.playback import play

# Initialiser l'objet recognizer
r = sr.Recognizer()
# Initialiser le client Transcribe


# Créer un client Polly
polly_client = boto3.client('polly')

with sr.Microphone() as source:

    print("Dites quelque chose...")


    try:
        audio = r.listen(source, timeout=5)

    except sr.WaitTimeoutError:
        print("La durée d'attente maximale de 5 secondes est écoulée. Aucune commande vocale détectée.")
        exit()

try:
    # Reconnaître la commande vocale
    command = r.recognize_google(audio, language='fr-fr')
    print(f"Vous avez dit: {command}")
    # Appeler Amazon Polly
    response = polly_client.synthesize_speech(VoiceId='Celine',
                                          OutputFormat='mp3',
                                          Text=command,
                                          LanguageCode='fr-FR')

    # Sauvegarder le fichier audio
    file_name = 'speech.mp3'
    with open(file_name, 'wb') as file:
        file.write(response['AudioStream'].read())
        print(f"Le fichier audio a été sauvegardé sous : {file_name}")
    # Après avoir sauvegardé le fichier audio
    song = AudioSegment.from_mp3(file_name)
    play(song)
except sr.UnknownValueError:
    print("Impossible de comprendre la commande vocal.")

