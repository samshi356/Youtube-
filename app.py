from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            yt = YouTube(url)
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            return render_template('index.html', streams=streams, video_title=yt.title, video_url=url)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

@app.route('/download/<itag>')
def download(itag):
    url = request.args.get('url')
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        filename = f"{yt.title[:40].replace(' ', '_')}_{uuid.uuid4().hex}.mp4"
        filepath = stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Download error: {e}", 400

# ✅ Render.com fix: Use PORT from environment variable
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host='0.0.0.0', port=port)
        
