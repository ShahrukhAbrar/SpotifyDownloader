from pprint import pprint
import eyed3
from eyed3.id3.frames import ImageFrame
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pytube
import os.path
import os
import requests
import math
import re

path=os.path.abspath(os.getcwd()) 
# where to save 
savepath = f"{path}" #to_do 

'''Search Fuction for YT'''
def ytsearch(name:str, lenght):
    videoIncrement=0
    yt=pytube.Search(name)
    ytresult=yt.results[0]
    #while(int(lenght/1000)>ytresult.length):
    spotifySongTime=round(lenght/1000)
    ytSongTime=ytresult.length
    while(math.isclose(spotifySongTime,ytSongTime, rel_tol=5)) is False:

        try:
            ytresult=yt.results[videoIncrement]
            videoIncrement += 1
    
        except Exception as e:
            print(e)
            return 1    

    return ytresult

'''Converts from YT(.mp4) to Mp3'''
def convert(name:str, new_name:str, audioQuality:str):
    audQual=audioQuality
    os.rename(name, 'input.mp4')
    os.system(f'ffmpeg -loglevel panic -i input.mp4 -vn -f mp3 -ab {audQual} output.mp3')
    os.rename('output.mp3', new_name)
    os.remove('input.mp4')

'''Adds MetaData to Song'''
def metadata(song_name:str,artist_name:str, pic_name:str, albumName:str, trackName:str):
    audiofile = eyed3.load(song_name)
    if (audiofile.tag == None):
        audiofile.initTag()

    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(pic_name,'rb').read(), 'image/jpeg')
    audiofile.tag.artist=artist_name
    audiofile.tag.album=albumName
    audiofile.tag.title=trackName

    audiofile.tag.save()
    os.remove(pic_name)


'''Main Function'''

def track(link:str):
    


    if len(sys.argv) > 1:   
        urn = sys.argv[1]
    else:
        urn = 'spotify:track:0Svkvt5I79wficMFgaqEQJ'

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="[ADD ID HERE]", client_secret="[ADD PASSWORD HERE]"))

    track = sp.track(link)



    
    try:
        #gets required Song Info
        albumArt=track['album']['images'][0]['url']
        albumName=track['album']['name']
        trackName=str(track['name'])

        #replaces illegal characters from File name
        trackName=re.sub('[^A-Za-z0-9 ]+', '', trackName)

        artist=track['artists'][0]['name']
        lenght=track['duration_ms']
        name=str(trackName+".mp4")
        name2=str(trackName+".mp3")
        imagename=str(trackName+'.jpg')
        query=str(trackName+" By "+artist)

        #replaces illegal characters from File name


        file_exists= os.path.exists(name2)
        
        if file_exists == True:
            return name2                 #If file is already downloaded and is available in cwd
        
        
           
        result=ytsearch(name=query, lenght=lenght)
        if result==1:
            return 'Error'
    
        
        
    except Exception as e:
        print(e)
        return 'Error' 
        

    

    #Downloads Highest Quality Audio 
    stream=result.streams.filter(only_audio=True).order_by('abr').desc().first() 
    audioQual=str(stream.abr).replace("bps","")
    
    #Album Art Download
    url = albumArt
    r = requests.get(url, allow_redirects=True)
    open(imagename, 'wb').write(r.content)
   
    
    try:
        
        stream.download(filename=name)
        convert(name=name, new_name=name2,audioQuality=audioQual)
        metadata(name2, artist, imagename, albumName, trackName)
        return name2
          
    except Exception as e:
        print(e)
        return 'Error'
