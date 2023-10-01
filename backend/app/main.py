from core.youtube import Youtube

yt = Youtube()
yt.read_videos_from_file("backend/data/videos.json")

yt.fetch_video("ku7uAFfdejc")

yt.save_videos_to_file("backend/data/videos.json")
