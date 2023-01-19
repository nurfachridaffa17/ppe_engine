from imageai.Detection.Custom import CustomObjectDetection
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from . import app

# Path: engine_ppe/views.py

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/v1/dowloads/image', methods=['POST'])
def get_image():
    if 'file_image' not in request.files:
        return jsonify({'status': 400, 'message': 'No file part'})

    file = request.files['file_image']

    if file.filename == '':
        return jsonify({'status': 400, 'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return jsonify({'status': 200 ,'message': 'Image saved successfully'})


@app.route('/api/v1/ppe', methods=['GET', 'POST'])
def get_ppe():
    nama_img = request.form.get('nama_img')
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("models/yolov3_ppe_train2_mAP-0.77405_epoch-24.pt")
    detector.setJsonPath("json/ppe_train2_yolov3_detection_config.json")
    detector.loadModel()
    detector.useCPU()
    detections = detector.detectObjectsFromImage(input_image="images/images.jpeg",
                                    output_image_path="output/images.jpeg",)
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])



    
    

