import yt_dlp
import subprocess
import curses
import time

# -----------------------------
# YOUTUBE SEARCH (TOP 5 RESULTS)
# -----------------------------
def search_youtube(query):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": "in_playlist"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch5:{query}", download=False)
        if "entries" in result:
            return result["entries"]
        return []

# -----------------------------
# GET DIRECT AUDIO URL
# -----------------------------
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

# -----------------------------
# PLAY AUDIO WITH FFPLAY
# -----------------------------
def play_audio(url):
    subprocess.run([
        "ffplay",
        "-nodisp",
        "-autoexit",
        url
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# -----------------------------
# CURSES UI
# -----------------------------
def menu(stdscr, items, title):
    curses.curs_set(0)
    idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title, curses.A_BOLD)

        for i, item in enumerate(items):
            if i == idx:
                stdscr.addstr(i+2, 2, "> " + item, curses.A_REVERSE)
            else:
                stdscr.addstr(i+2, 2, "  " + item)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(items)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(items)
        elif key in (10, 13):  # Enter
            return idx
        elif key == ord('q'):
            return None

# -----------------------------
# MAIN PLAYER LOOP
# -----------------------------
def main(stdscr):
    queue = []

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Press 's' to search, 'q' to quit.", curses.A_BOLD)
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            break

        if key == ord('s'):
            curses.echo()
            stdscr.addstr(2, 0, "Search: ")
            query = stdscr.getstr(2, 8, 60).decode()
            curses.noecho()

            results = search_youtube(query)
            if not results:
                stdscr.addstr(4, 0, "No results found.")
                stdscr.getch()
                continue

            titles = [f"{r['title']}" for r in results]
            idx = menu(stdscr, titles, "Select a song:")

            if idx is None:
                continue

            queue.append(results[idx]["url"])

        # PLAY QUEUE
        while queue:
            url = queue.pop(0)
            audio = get_audio_url(url)

            stdscr.clear()
            stdscr.addstr(0, 0, "Playing...", curses.A_BOLD)
            stdscr.refresh()

            play_audio(audio)

            # After each song, check if user wants to search again
            stdscr.clear()
            stdscr.addstr(0, 0, "Song finished. Press 's' to search, 'q' to quit, Enter to continue queue.")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('q'):
                return
            if key == ord('s'):
                break  # go back to search
            # Enter continues queue

curses.wrapper(main)
