# ppe_engine


- STEP TO INSTALL

1. Create folder models, json, output inside folder engine_ppe
2. Insert your models which is already your trainning inside folder models
3. In folder image, after you post an image in another platform it will receipt here
4. After you add the folders you have to add config.py

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


5. Build your docker image
6. Run your docker image "docker-compose build"
7. after you build your docker image you can run it "docker-compose up"