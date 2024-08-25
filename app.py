from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

BUNNY_STORAGE_ZONE = os.getenv('BUNNY_STORAGE_ZONE')
BUNNY_API_KEY = os.getenv('BUNNY_API_KEY')
BUNNY_API_KEY_READ_ONLY = os.getenv('BUNNY_API_KEY_READ_ONLY')
BUNNY_STORAGE_URL = f'https://storage.bunnycdn.com/{BUNNY_STORAGE_ZONE}'
BUNNY_STORAGE_URL_LIST = f'https://storage.bunnycdn.com/{BUNNY_STORAGE_ZONE}/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['video']
        file_name = file.filename
        url = f'{BUNNY_STORAGE_URL}/{file_name}'

        response = requests.put(url, data=file.read(), headers={
            'AccessKey': BUNNY_API_KEY,
            'Content-Type': file.content_type,
        })

        if response.status_code == 201:
            return jsonify({'success': True, 'message': 'File uploaded successfully', 'url': url}), 201
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/videos', methods=['GET'])
def get_videos():
    try:
        if not BUNNY_STORAGE_ZONE or not BUNNY_API_KEY_READ_ONLY:
            return jsonify({'error': 'BUNNY_STORAGE_ZONE or BUNNY_API_KEY_READ_ONLY is not defined'}), 500

        response = requests.get(BUNNY_STORAGE_URL_LIST, headers={
            'AccessKey': BUNNY_API_KEY_READ_ONLY,
        })

        if response.status_code != 200:
            return jsonify({'error': 'Error al obtener la lista de videos'}), 500

        # Verificar que la respuesta tenga el formato esperado
        if not isinstance(response.json(), list):
            return jsonify({'error': 'Formato de respuesta inesperado'}), 500

        video_list = [{'filename': file['ObjectName']} for file in response.json()]

        return render_template('videos.html', videos=video_list)
    except Exception as e:
        print(f"Error al obtener la lista de videos: {e}")
        return jsonify({'error': 'Error al obtener la lista de videos'}), 500

if __name__ == '__main__':
    app.run(debug=True)