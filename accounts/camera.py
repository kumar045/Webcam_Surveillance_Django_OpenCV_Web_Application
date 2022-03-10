from imutils.video import VideoStream
import imutils
import cv2, os, urllib.request
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import time
from django.conf import settings
from threading import Thread

ip2 = 'rtsp://Admin:sveltetech123@10.5.1.10:554/h264'
# Load Yolo
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
#net = cv2.dnn.readNet("drone/yolo-drone.weights", "drone/yolov3.cfg")
classes = []
#with open("drone/dota.names", "r") as f:
with open("dota.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


class VideoCamera(object):
    def __init__(self):
        self.video = VideoStream(0).start()

    def __del__(self):
        self.video.stop()

    def get_frame(self):
        img = self.video.read()
        
        # img = imutils.resize(img, width=800,height=800)
        height, width, channels = img.shape
        #print(height)
        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]

                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3,color, 3)
        # fps.update()
        ret, jpeg = cv2.imencode('.jpg', img)

        return jpeg.tobytes()

class LiveWebCam(object):
    def __init__(self):
        self.url = VideoStream(0).start()
        

    def __del__(self):
         self.url.stop()

    def get_frame(self):
        imgNp = self.url.read()
        #resize = cv2.resize(imgNp, (640, 480), interpolation = cv2.INTER_LINEAR) 
        ret, jpeg = cv2.imencode('.jpg', imgNp)
        return jpeg.tobytes()