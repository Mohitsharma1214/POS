import yt_dlp

def extract_heatmap():
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'extract_flat': True,
        'dump_single_json': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
        heatmap = info.get('heatmap')
        if heatmap:
            most_replayed = max(heatmap, key=lambda x: x.get('value', 0))
            print(f"Most replayed: {most_replayed}")
        else:
            print("No heatmap found")

if __name__ == "__main__":
    extract_heatmap()
