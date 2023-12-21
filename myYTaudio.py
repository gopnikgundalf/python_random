from googleapiclient.discovery import build
from moviepy.editor import VideoFileClip
from pytube import YouTube
import os
from pydub import AudioSegment
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import re
import subprocess


def download_youtube_video(video_url, output_path):
    #video_url='https://www.youtube.com/watch?v='+video_id
    try:
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path)
        print("Das Video wurde erfolgreich heruntergeladen!")
    except Exception as e:
        print("Beim Herunterladen des Videos ist ein Fehler aufgetreten:", str(e))
    
    
def download_youtube_video_as_mp3(video_url, output_path):
    try:
        # YouTube-Video herunterladen
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        video_file_path = video.download(output_path)

        # Öffne das heruntergeladene Video mit moviepy
        video_clip = VideoFileClip(video_file_path)

        # Extrahiere die Audiospur und speichere sie als MP3
        audio_file_path = video_file_path.replace(".mp4", ".mp3")
        video_clip.audio.write_audiofile(audio_file_path)
        video_clip.close()

        # Video-Datei löschen
        os.remove(video_file_path)
        print(f"Das Video wurde erfolgreich als MP3 heruntergeladen: {audio_file_path}")
    except Exception as e:
        print("Beim Herunterladen des Videos als MP3 ist ein Fehler aufgetreten:", str(e))

def get_video_metadata(video_id):
    try:
        # Video-Metadaten abrufen
        response = youtube.videos().list(part='snippet', id=video_id).execute()
        video_info = response['items'][0]['snippet']

        # Ausgabe der Metadaten
        #print(f"Titel: {video_info['title']}")
        #print(f"Beschreibung: {video_info['description']}")
        #print(f"Veröffentlicht am: {video_info['publishedAt']}")
        #print(f"Kategorien: {video_info['categoryId']}")
        #print(f"Tags: {', '.join(video_info.get('tags', []))}")
        # Weitere Metadaten können hier ausgegeben werden]
        
        return video_info['title'], video_info['description']

    except Exception as e:
        print("Fehler beim Abrufen der Metadaten:", e)

def audio_has_timepatterns(text):
    # Muster für Zeitangaben (Stunden:Minuten:Sekunden)
    time_pattern = r'\d+:\d+:\d+'

    # Überprüfe, ob die Beschreibung Zeiten im Muster der Zeitangabe enthält
    if re.search(time_pattern, text):
        return True
    else:
        return False

def get_chapter_times(video_info):
    # Regulärer Ausdruck, um die Zeiten im Format Stunden:Minuten:Sekunden zu extrahieren
    time_pattern = r"\d+:\d+:\d+"
    chapter_times_str = re.findall(time_pattern, video_info)

    # Konvertiere die extrahierten Zeiten in das gewünschte Format (Stunde, Minute, Sekunde) als Tupel
    chapter_times = []
    for time_str in chapter_times_str:
        h, m, s = map(int, time_str.split(':'))  # Zerlege die Zeit in Stunden, Minuten, Sekunden
        chapter_times.append((h, m, s))  # Füge das Tupel zur Liste hinzu

    return chapter_times

def createTitleFolder(title):
    folder_name = title
    folder_path = os.path.join(os.getcwd(), folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        #print(f"Folder '{folder_name}' created.")
    else:
        print("")
        #print(f"Folder '{folder_name}' already exists.")

def get_audio_length(file_path):
    # Verwende ffmpeg, um die Länge der Audiodatei zu ermitteln
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path], stdout=subprocess.PIPE, text=True)
    duration = float(result.stdout)
    return duration

def split_audio_by_chapters(input_file, output_prefix, chapter_times, title):
    original_path=os.getcwd()
    
    os.chdir(original_path+"\\audiofiles")
    createTitleFolder(title)
    
    folder_name = title
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.chdir(folder_path)
   
    audio_length = get_audio_length(input_file)  # Ermittle die Länge der Ausgangs-Audiodatei
    
    for i, (h, m, s) in enumerate(chapter_times):
        start_time = f"{h:02d}:{m:02d}:{s:02d}"
        if i < len(chapter_times) - 1:
            next_h, next_m, next_s = chapter_times[i + 1]
            end_time = f"{next_h:02d}:{next_m:02d}:{next_s:02d}"
        else:
            # Falls es sich um das letzte Kapitel handelt, nehme das Ende der Datei
            end_time = f"{int(audio_length // 3600):02d}:{int((audio_length % 3600) // 60):02d}:{int(audio_length % 60):02d}"

        output_file = f"{output_prefix} {i + 1}.mp3"
        subprocess.run(["ffmpeg", "-i", input_file, "-ss", start_time, "-to", end_time, "-c", "copy", output_file])
        
    os.chdir(original_path)    
    


def remove_text_full_Audiobook(description):
    pattern_to_remove = " - Full Audiobook"
    cleaned_description = description.replace(pattern_to_remove, '')
    return cleaned_description


def create_audiofiles_folder():
    folder_name = "audiofiles"
    folder_path = os.path.join(os.getcwd(), folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")


# Dein YouTube Data API-Schlüssel hier
api_key = 'AIzaSyChagKfy7CG_B_VY1rcFCbmsL8I4Gh5KqM'

# Erstelle ein YouTube-Service-Objekt
youtube = build('youtube', 'v3', developerKey=api_key)

# Hier die Video-ID einsetzen
video_id = 'y4if5uWqj64' #y4if5uWqj64, Q8iikX5YYzU, Ld2GMtkPgVI, IhimQKBuhB0, ZyRUzgx4pjI
video_id = input("Welche Video-ID soll heruntergeladen werden: ")

video_url = "https://www.youtube.com/watch?v="+video_id


# Funktion aufrufen, um Metadaten abzurufen
title, video_info=get_video_metadata(video_id)

#erhalte Titel des Audio_files
correct_title = title.replace("'", '')
audio_file=correct_title+'.mp3'
new_title=remove_text_full_Audiobook(correct_title)

# Aufruf der Funktion zum Erstellen des Ordners
create_audiofiles_folder()
output_folder = os.getcwd()+'\\audiofiles\\' + new_title

download_youtube_video_as_mp3(video_url, output_folder)


#generiere die Kapitelzeiten
chapter_times=get_chapter_times(video_info)
print(chapter_times)

if audio_has_timepatterns(video_info):
    new_title=remove_text_full_Audiobook(correct_title)
    split_audio_by_chapters(audio_file, new_title+' Chapter', chapter_times, new_title)



