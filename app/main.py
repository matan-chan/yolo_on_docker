from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import numpy as np
import torch
import cv2
import io

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
app = Flask(__name__, template_folder='app/templates')
CORS(app)


def predict(image):
    results = model(image)
    return draw_bounding_boxes(image[0], results)


def draw_bounding_boxes(image, results):
    boxes = results.xyxy[0].cpu().numpy()
    for box in boxes:
        x_min, y_min, x_max, y_max, confidence, class_id = box
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

        thickness = 2
        image[y_min:y_min + thickness, x_min:x_max, :] = [255, 0, 0]  # Top side
        image[y_max:y_max + thickness, x_min:x_max, :] = [255, 0, 0]  # Bottom side
        image[y_min:y_max, x_min:x_min + thickness, :] = [255, 0, 0]  # Left side
        image[y_min:y_max, x_max:x_max + thickness, :] = [255, 0, 0]  # Right side

        label = f'{model.names[int(class_id)]} {confidence:.2f}'
        cv2.putText(image, label, (int(x_min), int(y_min) - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return image


@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']
    img = Image.open(file)
    img = [(np.array(img))]
    processed_img = predict(img)
    processed_img = Image.fromarray(processed_img)
    processed_img_pil = Image.fromarray(np.uint8(processed_img))
    output_buffer = io.BytesIO()
    processed_img_pil.save(output_buffer, format='JPEG')
    output_buffer.seek(0)
    return send_file(output_buffer, mimetype='image/jpeg')

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    app.run(port=76, host='0.0.0.0')
