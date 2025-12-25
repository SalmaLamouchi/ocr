from flask import Flask, request, jsonify
from flask_cors import CORS
import pymupdf as fitz
import base64

app = Flask(__name__)
# Configuration CORS la plus permissive possible
CORS(app, resources={r"/*": {"origins": "*"}}) 

@app.route('/extract', methods=['POST', 'OPTIONS'])
def extract_data():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier"}), 400
        
        file = request.files['file']
        doc = fitz.open(stream=file.read(), filetype="pdf")
        
        text = ""
        for page in doc:
            text += page.get_text()
            
        return jsonify({"text": text, "images": []})
    except Exception as e:
        print(f"Erreur serveur: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Force l'écoute sur toutes les interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)