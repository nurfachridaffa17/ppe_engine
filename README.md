# ppe_engine


- STEP TO INSTALL

1. Create folder models, json, output inside folder engine_ppe
2. Insert your models which is already your trainning inside folder models
3. In folder image, after you post an image in another platform it will receipt here
4. After you add the folders you have to add config.py
5. Create config.json for save your api key if you don't want to save it in your code or your database
6. Create static folder, inside the static folder you have to create folder image_in and image_out
7. Build your docker image
8. Run your docker image "docker-compose build"
9. after you build your docker image you can run it "docker-compose up"

- Inside config.py

```
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '{your secret key}'
    UPLOAD_FOLDER = '{your folder to receive the image}'
    ALLOWED_EXTENSIONS = {type file to allow inside your engine like .jpeg or .jpg}
``` 

- File structure

- ppe_recognition
    - [] engine_ppe
        - [] json
            - [] ppe_training.json
        - [] models
            - [] models_training.pt
        - [] static
            - [] image_in
            - [] image_out
        - templates
            - [] 404.html
        - [] __init__.py
        - [] models.py
        - [] views.py
    - [] config.py
    - [] Dockerfile
    - [] docker-compose.yml
    - [] README.md
    - [] requirements.txt
    - [] run.py