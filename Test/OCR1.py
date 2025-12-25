from flask import Flask, request, jsonify
from flask_cors import CORS
import pymupdf as fitz  
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/extract', methods=['POST'])
def extract_data():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier trouvé"}), 400
        
        file = request.files['file']
        doc = fitz.open(stream=file.read(), filetype="pdf")
        
        text = ""
        images_list = []

        for page in doc:
            text += page.get_text()

            # 2. Extraction des images
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Encodage en Base64 pour l'affichage HTML
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                image_data = f"data:image/{base_image['ext']};base64,{image_base64}"
                images_list.append(image_data)

        return jsonify({
            "text": text,
            "images": images_list
        })

    except Exception as e:
        print(f"Erreur lors de l'extraction : {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)