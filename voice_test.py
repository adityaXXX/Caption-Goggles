import pyaudio
from porcupine import Porcupine
import struct
import cv2
from captionbot import CaptionBot
import numpy as np

c = CaptionBot()
cap = cv2.VideoCapture(0)

library_path = 'E:/Hack-a-bit_2019/porcupine/lib/windows/amd64/libpv_porcupine.dll' 
model_file_path = 'E:/Hack-a-bit_2019/porcupine/lib/common/porcupine_params.pv'
keyword_file_path = ['alexa_windows.ppn','describe.ppn','hey pico_windows.ppn','blueberry_windows.ppn',
						'bumblebee_windows.ppn','grasshopper_windows.ppn','picovoice_windows.ppn','porcupine_windows.ppn',
						'terminator_windows.ppn']
sensitivity = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

handle = Porcupine(library_path, 
				   model_file_path, 
	               keyword_file_paths=keyword_file_path, 
	               sensitivities=sensitivity)

def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate,
    					   channels=1,
    					   format=pyaudio.paInt16,
    					   input=True,
    					   frames_per_buffer=handle.frame_length)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm
r=True
while r:
	r,f = cap.read()
	cv2.imshow('Stream', f)
	key=cv2.waitKey(1)
	if key==27:
		break
	pcm = get_next_audio_frame()
	keyword_index = handle.process(pcm)
	if keyword_index==2:
		print(keyword_file_path[keyword_index])
		print("Generating Caption...")
		cv2.imwrite('image.jpg',f)
		caption = c.file_caption('image.jpg')
		print(caption)
