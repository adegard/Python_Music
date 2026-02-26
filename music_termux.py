import yt_dlp
import subprocess

def search_youtube(query):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": "in_playlist"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=False)
        if "entries" in result and result["entries"]:
            return result["entries"][0]["url"]
        return None

def get_audio_url(video_url):
    ydl_opts = {
        "quiet": True,
        "format": "bestaudio/best",
        "extractor_args": {
            "youtube": {
                "player_client": ["tv_embedded"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info["url"]

def play_audio(url):
    subprocess.run([
        "mpv",
        "--no-video",
        "--really-quiet",
        url
    ])

if __name__ == "__main__":
    query = input("Search song: ")
    print("Searching...")
    video_url = search_youtube(query)

    if not video_url:
        print("No results found.")
        exit()

    print("Found:", video_url)
    print("Getting audio stream...")
    audio_url = get_audio_url(video_url)

    print("Playing...")
    play_audio(audio_url)
