from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    converted_image = None
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            converted_image = convert_to_png(uploaded_file)

    return render_template('index.html', converted_image=converted_image)

@app.route('/convert', methods=['POST'])
def convert():
    uploaded_file = request.files['file']
    if uploaded_file and allowed_file(uploaded_file.filename):
        converted_image_path = convert_to_png(uploaded_file)
        return render_template('index.html', converted_image=converted_image_path)
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    filename = request.args.get('filename')
    return send_file(filename, as_attachment=True, download_name="converted_image.png")

def convert_to_png(image_file):
    img = Image.open(image_file)
    img_png = img.convert("RGBA")
    
    img_bytes = BytesIO()
    img_png.save(img_bytes, format="PNG")

    # Save the BytesIO content to a temporary file
    temp_filename = "/tmp/converted_image.png"
    with open(temp_filename, "wb") as temp_file:
        temp_file.write(img_bytes.getvalue())

    return temp_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'webp'}

if __name__ == '__main__':
    app.run(debug=True)
