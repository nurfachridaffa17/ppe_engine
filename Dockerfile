FROM python:3.9
WORKDIR /code
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install imageai --upgrade
COPY . .
CMD [ "python", "run.py"]