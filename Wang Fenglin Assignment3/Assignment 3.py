from diffusers import DiffusionPipeline
import torch
from flask import Flask, render_template, request,send_file
from PIL import Image
import io
import base64
import random

model = "runwayml/stable-diffusion-v1-5"

pipe = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float32)
pipe.to("cpu")

app = Flask(__name__)

def generate_image():
    img = Image.new('RGB', (200, 300), color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    prompt = request.form['text']
    images = pipe(prompt, num_inference_steps=20).images
    img = images[0]
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)  
    return send_file(img_io, mimetype='image/png')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,port=8080)
