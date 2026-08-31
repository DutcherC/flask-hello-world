import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Write environment variable cookies to a temporary file if present
COOKIE_FILE = "/tmp/cookies.txt"
if "YOUTUBE_COOKIES" in os.environ:
    with open(COOKIE_FILE, "w") as f:
        f.write(os.environ["YOUTUBE_COOKIES"])

@app.route('/')
def get_stream():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"status": "ok", "message": "yt-dlp proxy online. Pass ?id=VIDEO_ID"}), 200

    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        cmd = [
            "yt-dlp",
            "-g",
            "-f", "best[ext=mp4]/best",
            "--no-warnings",
            url
        ]

        # Use cookies file if present
        if os.path.exists(COOKIE_FILE):
            cmd.extend(["--cookies", COOKIE_FILE])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0 and result.stdout.strip():
            stream_url = result.stdout.strip().split('\n')[0]
            return jsonify({"url": stream_url}), 200
        else:
            return jsonify({"error": "yt-dlp failed to extract stream", "details": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
