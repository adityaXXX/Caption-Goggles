import os
import time
import tarfile
import glob
import six.moves.urllib as urllib
import cv2
from tqdm import tqdm
import numpy as np
import tensorflow as tf
from ssd_mobilenet_utils import *
from captionbot import CaptionBot
import urllib.request as urllib2
import pyttsx3

url = 'http://10.42.0.244/media/?action=stream'
username = 'admin'
password = ''
p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

c = CaptionBot()

def run_detection(image, interpreter):
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])
    classes = interpreter.get_tensor(output_details[1]['index'])
    scores = interpreter.get_tensor(output_details[2]['index'])
    num = interpreter.get_tensor(output_details[3]['index'])

    boxes, scores, classes = np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes + 1).astype(np.int32)
    out_scores, out_boxes, out_classes = non_max_suppression(scores, boxes, classes)

    # Print predictions info
    #print('Found {} boxes for {}'.format(len(out_boxes), 'images/dog.jpg'))

    return out_scores, out_boxes, out_classes

def real_time_object_detection(interpreter, colors):
	stream = urllib2.urlopen(url)
	byte = bytes()
	engine = pyttsx3.init()
	while True:
		start = time.time()
		byte += stream.read(32768)
		a = byte.find(b'\xff\xd8')
		b = byte.find(b'\xff\xd9')
		if a != -1 and b != -1:
			jpg = byte[a:b+2]
			byte = byte[b+2:]
			frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
			frame = cv2.resize(frame,(640,480))
			cv2.imwrite('image.jpg',frame)
			image_data = preprocess_image_for_tflite(frame, model_image_size=300)
			out_scores, out_boxes, out_classes = run_detection(image_data, interpreter)
			result = draw_boxes(frame, out_scores, out_boxes, out_classes, class_names, colors)
			end = time.time()
			t = end - start
			fps  = "Fps: {:.2f}".format(1 / t)
			cv2.putText(result, fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
			cv2.imshow("Object detection - ssdlite_mobilenet_v2", frame)
			key = cv2.waitKey(1)
			if key == ord('a'):
				print("Generating Caption...")
				caption = c.file_caption('/home/aditya/Hack-a-bit2019/' + 'image.jpg')
				print(caption)
				engine.setProperty('rate', 150)
				engine.say(caption)
				engine.runAndWait()
			elif key == 27:
				break

	cv2.destroyAllWindows()



interpreter = tf.lite.Interpreter(model_path="model_data/ssdlite_mobilenet_v2.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
class_names = read_classes('model_data/coco_classes.txt')
colors = generate_colors(class_names)
real_time_object_detection(interpreter, colors)
