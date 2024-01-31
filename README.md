# yolo on docker container

A simple project with a yolov5 model running on a flask server and a simple web ui in html and css.

## usage

### build the container and send it to the server

```bash
docker build -t yolo_container .
docker save -o yolo_container.tar yolo_container
scp C:\Users\ninja\Desktop\yolo_on_docker\yolo_container.tar ninja_server@100.100.100.100:
```

### run it on the server

```bash
docker run yolo_container.tar
```

Now open the `UI.html` file with ur browser choose an image add the server ip address and upload the image to the
server.
You will see you get the image back with bounding boxes of the items in the image.

<p align="left">
  <img width="500" src="https://github.com/matan-chan/yolo_on_docker/blob/main/images/yolo_container.jpg?raw=true">
</p>

