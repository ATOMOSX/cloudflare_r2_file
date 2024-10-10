from flask import Flask, request, jsonify
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración de las variables de entorno
CLOUDFLARE_R2_ACCESS_KEY_ID = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
CLOUDFLARE_R2_SECRET_ACCESS_KEY = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')
CLOUDFLARE_R2_ENDPOINT_URL = os.getenv('CLOUDFLARE_R2_ENDPOINT_URL')
CLOUDFLARE_R2_BUCKET_NAME = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')


# Función para configurar el cliente boto3 para Cloudflare R2
def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=CLOUDFLARE_R2_ACCESS_KEY_ID,
        aws_secret_access_key=CLOUDFLARE_R2_SECRET_ACCESS_KEY,
        endpoint_url=CLOUDFLARE_R2_ENDPOINT_URL
    )


# Función para subir el archivo a Cloudflare R2
def upload_file_to_r2(file, filename):
    s3_client = get_s3_client()

    # Sube el archivo a R2
    s3_client.upload_fileobj(file, CLOUDFLARE_R2_BUCKET_NAME, filename)

    # Retorna la URL del archivo
    file_url = f"{CLOUDFLARE_R2_ENDPOINT_URL}/{CLOUDFLARE_R2_BUCKET_NAME}/{filename}"
    return file_url


# Ruta para manejar la subida de archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file.'}), 400

    try:
        # Sube el archivo a Cloudflare R2
        file_url = upload_file_to_r2(file, file.filename)
        return jsonify({'success': True, 'file_url': file_url}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
