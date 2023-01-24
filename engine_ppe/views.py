from imageai.Detection.Custom import CustomObjectDetection
from flask import Flask, request, jsonify, make_response, render_template, send_from_directory
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
    
    return make_response(jsonify({'status': 200, 'message': 'Token generated successfully', 'api_token': api_token}), 200)

@app.route('/api/v1/upload/<path:filename>', methods=['GET'])
def upload_image(filename):
    authorization = request.headers.get('Authorization')
    with open("engine_ppe/config.json", "r") as f:
        config = json.load(f)
    
    if authorization != config["api_token"]:
        return make_response(jsonify({'status': 401, 'message': 'Unauthorized'}), 401)
    
    try:
        return send_from_directory('static/image_out', filename, as_attachment=True)
    except FileNotFoundError:
        return make_response(jsonify({'status': 404, 'message': 'File not found'}), 404)


@app.route('/api/v1/process/image', methods=['POST', 'GET'])
def get_image():

    authorization = request.headers.get('Authorization')
    with open("engine_ppe/config.json", "r") as f:
        config = json.load(f)
    
    if authorization != config["api_token"]:
        return make_response(jsonify({'status': 401, 'message': 'Unauthorized'}), 401)
    elif authorization is None:
        return make_response(jsonify({'status': 401, 'message': 'Unauthorized'}), 401)


    if 'file_image' not in request.files:
        return jsonify({'status': 400, 'message': 'No file part'})

    file = request.files['file_image']
    # file = request.data

    if file.filename == '':
        return make_response(jsonify({'status': 400, 'message': 'No selected file'}), 400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    nama_img = file.filename

    model_path = app.config['MODELS_PPE']
    json_path = app.config['JSON_PPE']

    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.setJsonPath(json_path)
    detector.loadModel()
    detector.useCPU()
    detections = detector.detectObjectsFromImage(input_image="engine_ppe/static/image_in/{}".format(nama_img),
                                    output_image_path="engine_ppe/static/image_out/{}".format(nama_img),)
    
    safety_list = []

    for detection in detections:
        safety = detection["name"]
        safety_list.append(safety)
    
    os.remove("engine_ppe/static/image_in/{}".format(nama_img))

    link = app.config['SERVER_SAVE'] + "/api/v1/upload/{}".format(nama_img)

    safety_helmet = "safety_helmet" in safety_list
    safety_shoes = "safety_shoes" in safety_list
    not_safety_helmet = "safety_helmet" not in safety_list
    not_safety_shoes = "safety_shoes" not in safety_list
    
    if safety_helmet and safety_shoes:
        return make_response(jsonify({'status': 200, 'message': 'Image processed successfully', "safety_helmet": True, "safety_shoes": True, "link" : link}),200)
    elif not_safety_helmet and safety_shoes:
        return make_response(jsonify({'status': 200, 'message': 'Image processed successfully', "safety_helmet": False, "safety_shoes": True, "link" : link}),200)
    elif safety_helmet and not_safety_shoes:
        return make_response(jsonify({'status': 200, 'message': 'Image processed successfully', "safety_helmet": True, "safety_shoes": False, "link" : link}),200)
    else:
        return make_response(jsonify({'status': 200, 'message': 'Image processed successfully', "safety_helmet": False, "safety_shoes": False, "link" : link}),200)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(status="error", error_code=500, message="Internal Server Error"), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify(status="error", error_code=400, message="Bad Request"), 400

    




    
    

