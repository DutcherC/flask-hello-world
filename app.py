from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def get_stream():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"status": "ok", "message": "yt-dlp proxy online. Pass ?id=VIDEO_ID"}), 200

    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        # Pass extractor arguments to force client types that bypass bot checks on cloud IPs
        cmd = [
            "yt-dlp",
            "-g",
            "-f", "best[ext=mp4]/best",
            "--no-warnings",
            "--extractor-args", "youtube:player_client=ios,android_vr,tv",
            url
        ]
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
