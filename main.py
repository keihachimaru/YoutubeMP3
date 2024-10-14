from pytube import Playlist
import yt_dlp
from pydub import AudioSegment
import os, re

def sanitize_directory_name(dir_name):
    return re.sub(r'[<>:"/\\|?*]', ' ', dir_name)

def download_audio_as_mp3(url, save_dir):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_dir, 'temp_audio.%(ext)s'),
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print(f"Downloading: {info_dict['title']}")

        audio = AudioSegment.from_file(os.path.join(save_dir, "temp_audio.webm"))
        mp3_filename = os.path.join(save_dir, f"{info_dict['title']}.mp3")
        audio.export(mp3_filename, format="mp3")

        print(f"Downloaded and converted to MP3: {mp3_filename}")

        os.remove(os.path.join(save_dir, "temp_audio.webm"))
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def extract_urls_from_playlist(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        print(f"Extracting URLs from playlist: {playlist.title}")
        return playlist.video_urls, playlist.title
    except Exception as e:
        print(f"Error extracting URLs from playlist: {e}")
        return [], None

def create_directory(dir_name):
    sanitized_name = sanitize_directory_name(dir_name)
    if not os.path.exists(sanitized_name):
        os.makedirs(sanitized_name)
        print(f"Created directory: {sanitized_name}")
    return sanitized_name

def process_urls_from_file(filename="urls.txt"):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return

    with open(filename, "r") as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            if "playlist" in url:
                video_urls, playlist_title = extract_urls_from_playlist(url)
                playlist_title = sanitize_directory_name(playlist_title)
                if playlist_title:
                    create_directory(playlist_title)
                    
                    for video_url in video_urls:
                        print(video_url)
                        download_audio_as_mp3(video_url, playlist_title)
            else:
                single_video_dir = "Single_Videos"
                create_directory(single_video_dir)
                download_audio_as_mp3(url, single_video_dir)

if __name__ == "__main__":
    process_urls_from_file()
