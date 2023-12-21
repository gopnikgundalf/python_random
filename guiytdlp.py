import tkinter as tk
import subprocess
import requests
from bs4 import BeautifulSoup

########## Scraper ###########

# Extract redirect/tag
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

            print("Found Video-Tag!\n")

        else:

            print("Video-Tag not found.\n")

    else:

        print(f"Fehler beim Abrufen der Seite. Statuscode: {response.status_code}\n")

    video_tag = soup.find('video')

    if video_tag:

        source_tag = video_tag.find('source')

        if source_tag and 'src' in source_tag.attrs:

            video_src = source_tag['src']

            return video_src
        
        else:

            print("Source tag or src attribute not found.")

            return "Error"

def fuckOnePiece(urlstring, seasoncount, episodecount):

    i=0
    j=0
    k=0
    m=0
    for i in range(0,seasoncount):

        for j in range(0,episodecount[i]):

            scraper_urls.append(f"https://aniworld.to/anime/stream/{urlstring}/staffel-{i+1}/episode-{j+1}")
            redirectURL=getRightURL(scraper_urls[k])
            videoURL=getVideoTagFromRightURL(redirectURL)
            videoURLLists.append(videoURL)

            k+=1
    for url in videoURLLists:
        result = subprocess.run(["yt-dlp","--output", f"AttackOnTitan_Episode{m+1}.mp4","--compat-options","filename", url], capture_output=True, text=True)
        print(f"Episode{m+1} downloaded!")
        m+=1

scraper_urls=[]  #Liste aller URLS
videoURLLists=[] #Liste der Video URLS

def main():
    window = tk.Tk()

    urlstring_label = tk.Label(window, text="URL String")
    urlstring_label.pack()
    urlstring_entry = tk.Entry(window)
    urlstring_entry.pack()

    seasoncount_label = tk.Label(window, text="Season Count")
    seasoncount_label.pack()
    seasoncount_entry = tk.Entry(window)
    seasoncount_entry.pack()

    episodecount_label = tk.Label(window, text="Episode Counts (comma-separated)")
    episodecount_label.pack()
    episodecount_entry = tk.Entry(window)
    episodecount_entry.pack()

    run_button = tk.Button(window, text="Run Program", command=lambda: fuckOnePiece(urlstring_entry.get(), int(seasoncount_entry.get()), [int(e) for e in episodecount_entry.get().split(',')]))
    run_button.pack()

    window.mainloop()

if __name__ == "__main__":
    main()

# death-note
# jujutsu-kaisen
# demon-slayer-kimetsu-no-yaiba
# 
# 
# 