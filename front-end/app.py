from flask import Flask, render_template, request, jsonify
from backend.image_processing.led_classifier import LEDClassifier
from backend.cache_system.cache_manager import CacheManager
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializa componentes
classifier = LEDClassifier('models/led_classifier.h5')
cache = CacheManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Salva arquivo temporariamente
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Verifica cache primeiro
    cache_id = f"file_{file.filename}"
    cached = cache.get_from_cache(cache_id)
    if cached:
        return jsonify(cached)
    
    # Processamento se não estiver em cache
    is_led = classifier.predict(filepath)
    
    # OCR e extração de dados (simplificado)
    extracted_data = {
        'image_path': filepath,
        'extracted_text': "Extraído via OCR",  # Implementar OCR real
        'is_led': is_led,
        'potency': None,
        'model': None
    }
    
    # Adiciona ao cache
    cache.add_to_cache(cache_id, extracted_data)
    
    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)