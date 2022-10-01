from pywebio.input import input, TEXT
from pywebio.output import put_file, put_html,put_text,popup
from pywebio.platform import start_server
from spotify import track
import os


path=os.path.abspath(os.getcwd()) 


    

def trackname():
    
    songURL= input("Enter Spotify URL")
    
    try:
        songname= str(track(songURL))
    except Exception as e:
        print(e)
    popup('Something Went Wrong', 'Please Refresh the Page')        
    content = open(f'{songname}', 'rb').read()    
    put_file(f'{songname}', content, 'Download')

if __name__ == '__main__':
    
    start_server(trackname, port=80, host= '127.0.0.1', debug=False)