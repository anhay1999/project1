import cv2
import numpy as np
import pafy # pip install pafy, pip install youtube-dl

net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg') # phải sửa code này
classes = []
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()


class Video():
    count = 0
    delay =0
    def __init__(self):
        self.url = "https://www.youtube.com/watch?v=vX9GPhdOLZw"
        self.video = pafy.new(self.url)
        self.best = self.video.getbest(preftype = "mp4")
        self.cap = cv2.VideoCapture()
        self.cap.open(self.best.url)

        # self.video=cv2.VideoCapture('camera.mp4')
    def __del__(self):
        self.video.release()
    def get_frame(self, a):
        # _, img = self.video.read()
        _, img = self.cap.read()
        if Video.delay > 510 and Video.delay<515:
            height, width, _ = img.shape
            blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
            net.setInput(blob)

            output_layers_names = net.getUnconnectedOutLayersNames()
            layerOutputs = net.forward(output_layers_names)

            boxes = []
            confidences = []
            class_ids = []


            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append((float(confidence)))
                        class_ids.append(class_id)
            # print(len(boxes))
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            # print(indexes.flatten())
            font = cv2.FONT_HERSHEY_PLAIN
            colors = np.random.uniform(0, 255, size=(len(boxes), 3))
            if len(indexes) > 0:
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = str(round(confidences[i], 2))
                    color = colors[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label + "" + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)
                    if (label == "motorbike" or label == "car"):
                        # self.count = self.count + 1
                        Video.count +=1
            if Video.delay == 514:
                Video.delay = 0
        Video.delay += 1
        print(Video.delay)
        # if Video.delay == 50:
        #     Video.delay = 0

        if a==1:
            return Video.count
        if a==0:
            ret, jpg = cv2.imencode('.jpg', img)
            return jpg.tobytes()


