import yt_dlp
import pandas as pd
from datetime import datetime


def get_youtube_videos(query, max_results=20, start_dt=None, end_dt=None):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'ignoreerrors': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # yt-dlp’s search does not support date filters directly.
        search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

    videos = []
    if search_results and 'entries' in search_results:
        for item in search_results['entries']:
            title = item.get("title", "Unknown Title")
            video_id = item.get("id", None)
            timestamp = item.get("timestamp")  # Unix timestamp (if available)

            # Only include videos with a valid timestamp
            if not timestamp:
                continue

            # Convert timestamp to datetime
            video_datetime = datetime.fromtimestamp(timestamp)

            # Filter out videos outside the specified date/time range
            if start_dt and end_dt and not (start_dt <= video_datetime <= end_dt):
                continue

            videos.append({
                "Video Title": title,
                "Upload Date": video_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "YouTube Link": f"https://www.youtube.com/watch?v={video_id}" if video_id else "No URL"
            })

    return pd.DataFrame(videos)
