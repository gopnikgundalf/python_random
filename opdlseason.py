import subprocess
import requests
from bs4 import BeautifulSoup

# Extrahiere redirect/tag
def getRightURL(url):

    response = requests.get(url)
    html_string = response.text
    soup = BeautifulSoup(html_string, 'html.parser')
    watch_episode_vidoza = soup.find_all(lambda tag: tag.name == 'a' and 'watchEpisode' in tag.get('class', []) and 'Vidoza' in tag.text)
    redirectNumber=watch_episode_vidoza[0].get('href')
    print("Check Video: "+url)
    urlFinal="https://aniworld.to"+redirectNumber
    
    return urlFinal

# Convert redirect-URL to Source-URL
def getVideoTagFromRightURL(url):
    
    response = requests.get(url)

    if response.status_code == 200:

        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        video_tag = soup.find('video')
        
        if video_tag:

            print("Gefundenes Video-Tag!\n")

        else:

            print("Video-Tag nicht gefunden.")

    else:

        print(f"Fehler beim Abrufen der Seite. Statuscode: {response.status_code}")

    video_tag = soup.find('video')

    if video_tag:

        source_tag = video_tag.find('source')

        if source_tag and 'src' in source_tag.attrs:

            video_src = source_tag['src']

            return video_src
        
        else:

            print("Source tag or src attribute not found.")

            return "Fehler"

########### YT-DLP ###########

def fuckOnePiece(videoURLLists):   

    i=195
    
    # Execute Command in cmd
    for url in videoURLLists:
        result = subprocess.run(["yt-dlp","--output", f"OnePiece_Folge{i}.mp4","--compat-options","filename", url], capture_output=True, text=True)
        print(i)
        i+=1

    # Display output
    print("Command Output:")
    print(result.stdout)

    # Display any errors, if any
    if result.stderr:
        print("Errors:")
        print(result.stderr)

########### Listen ################

scraper_urls=[]  #Liste aller one piece URLS
videoURLLists=[] #Liste der Video URLS
episodeCount=[61,16,14,39,13,52,33,35,73,45,26,14,101,58,62,50,56,55,74,14,193] #Anzahl aller Episoden pro Staffel

i=6
j=0
k=0

for j in range(0,episodeCount[i]):

    scraper_urls.append(f"https://aniworld.to/anime/stream/one-piece/staffel-{i+1}/episode-{j+1}")
    redirectURL=getRightURL(scraper_urls[k])
    videoURL=getVideoTagFromRightURL(redirectURL)
    videoURLLists.append(videoURL)

    k+=1

fuckOnePiece(videoURLLists)
