from imageai.Detection.Custom import CustomObjectDetection
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from . import app
import secrets
import json
import base64

# Path: engine_ppe/views.py

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/v1/get/token', methods=['GET'])
def get_token():
    api_token = secrets.token_hex(16)

    with open("engine_ppe/config.json", "r") as f:
        config = json.load(f)

    config["api_token"] = api_token

    with open("engine_ppe/config.json", "w") as f:
        json.dump(config, f)
    
    return jsonify({'status': 200, 'message': 'Token generated successfully', 'token': api_token})


@app.route('/api/v1/process/image', methods=['POST', 'GET'])
def get_image():

    authorization = request.headers.get('Authorization')
    with open("engine_ppe/config.json", "r") as f:
        config = json.load(f)
    
    if authorization != config["api_token"]:
        return jsonify({'status': 403, 'message': 'Invalid Api Key'})
    elif authorization is None:
        return jsonify({'status': 401, 'message': 'Unauthorized'})


    if 'file_image' not in request.files:
        return jsonify({'status': 400, 'message': 'No file part'})

    file = request.files['file_image']
    # file = request.data

    if file.filename == '':
        return jsonify({'status': 400, 'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # return jsonify({'status': 200 ,'message': 'Image saved successfully'})

    # authorization = request.headers.get('Authorization')
    # with open("engine_ppe/config.json", "r") as f:
    #     config = json.load(f)
    
    # if authorization != config["api_token"]:
    #     return jsonify({'status': 401, 'message': 'Unauthorized'})

    # nama_img = request.form.get('nama_img')
    nama_img = file.filename
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("engine_ppe/models/yolov3_ppe_train2_mAP-0.77405_epoch-24.pt")
    detector.setJsonPath("engine_ppe/json/ppe_train2_yolov3_detection_config.json")
    detector.loadModel()
    detector.useCPU()
    detections = detector.detectObjectsFromImage(input_image="engine_ppe/images/{}".format(nama_img),
                                    output_image_path="engine_ppe/output/{}".format(nama_img),)
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
    
    with open("engine_ppe/output/{}".format(nama_img), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    response = jsonify({'status': 200, 'message': 'Image processed successfully', 'image': encoded_string})

    response.headers.set('Content-Type', 'application/json')
    response.headers.set('Content-Disposition', 'attachment', filename='output/{}'.format(nama_img))

    return response
    # send_file("output/{}".format(nama_img), mimetype='image/jpg', as_attachment=True)
    
    # time.sleep(5)
    
    # output_img = "engine_ppe/output/{}".format(nama_img)

# @app.route('/api/v1.upload/<path:filename>', methods=['GET'])
# def upload_image(filename):
#     authorization = request.headers.get('Authorization')
#     with open("engine_ppe/config.json", "r") as f:
#         config = json.load(f)
    
#     if authorization != config["api_token"]:
#         return jsonify({'status': 401, 'message': 'Unauthorized'})
    
#     try:
#         return send_file("engine_ppe/output/{}".format(filename), mimetype='image/jpg', as_attachment=True)
#     except FileNotFoundError:
#         return jsonify({'status': 404, 'message': 'File not found'})

    




    
    

