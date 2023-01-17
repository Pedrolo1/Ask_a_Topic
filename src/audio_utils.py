# THIS FILES WILL HAVE ALL THE FUNCTIONS RELATED TO AUDIO DOWNLOADING AND PROCESSING
import os
from pytube import YouTube, Playlist
from tqdm import tqdm

# a funcion that download a youtube video and convert to wav
def download_youtube_video_wav(url, path):
    # download the video audio
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download(output_path=path)
    # return the path of the downloaded file
    return path + '/' + yt.title + '.mp4'

def download_youtube_playlist_wav(url, path):
    # create the directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    
    lista_paths = []
    # download the playlist
    playlist = Playlist(url)
    for video in tqdm(playlist):
        lista_paths.append(download_youtube_video_wav(video, path))
        
    return lista_paths
    