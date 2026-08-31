from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def get_stream():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"status": "ok", "message": "Pass ?id=VIDEO_ID"}), 200

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info.get('url')

            if stream_url:
                return jsonify({"url": stream_url}), 200
            else:
                return jsonify({"error": "No URL found in info dict"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
