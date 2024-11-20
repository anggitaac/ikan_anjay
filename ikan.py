from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load model dengan format .keras
model = tf.keras.models.load_model('ikan.keras')

# Fungsi untuk memproses gambar
def preprocess_image(image_data):
    image = Image.open(io.BytesIO(image_data)).resize((150, 150))  # Resize gambar ke ukuran yang sesuai dengan model
    image = np.array(image) / 255.0  # Normalisasi gambar ke rentang [0, 1]
    return np.expand_dims(image, axis=0)  # Menambah dimensi untuk batch size

# Fungsi untuk mendecode hasil prediksi
def decode_prediction(prediction):
    labels = ["Ikan Badut", "Yellow Tang", "Blue Tang", "Betok Zebra", "Butterfly Fish", "Moonrish Idol", "Neon Tetra", "Ribonned Sweetlips"]  # Label yang sesuai dengan kelas model Anda
    predicted_index = np.argmax(prediction)  # Dapatkan indeks dengan probabilitas tertinggi
    return labels[predicted_index]

@app.route('/prediction', methods=['POST'])
def predict():
    try:
        # Mengambil file gambar dari request
        file = request.files['image']
        
        # Memproses gambar dan prediksi
        image_data = file.read()  # Membaca data gambar
        image = preprocess_image(image_data)  # Memproses gambar
        prediction = model.predict(image)  # Membuat prediksi dengan model
        
        # Decode prediksi menjadi label yang lebih mudah dipahami
        label = decode_prediction(prediction)
        
        return jsonify({'prediction': label})  # Mengembalikan label hasil prediksi
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Menjalankan aplikasi pada port yang ditentukan di Railway atau pada 5000 sebagai default
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)