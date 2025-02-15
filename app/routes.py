from flask import Blueprint, Flask, render_template, request, jsonify
import bencodepy
import os

app = Flask(__name__ , template_folder="app/templates")
main = Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"})
    
    try:
        torrent_data = bencodepy.decode(file.read())
        tracker_url = torrent_data.get(b'announce', b'').decode()
        file_info = torrent_data.get(b'info', {})
        return jsonify({"success": True, "tracker": tracker_url, "info": file_info})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
