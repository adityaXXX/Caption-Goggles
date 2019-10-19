import pyaudio
from porcupine import Porcupine
import struct
import sounddevice as sd
from porcupine import Porcupine
import struct
import cv2
from captionbot import CaptionBot
import numpy as np
import queue
c = CaptionBot()
cap = cv2.VideoCapture(0)

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata)

library_path = 'F:/Caption-Goggles/porcupine/lib/windows/amd64/libpv_porcupine.dll' 
model_file_path = 'F:/Caption-Goggles/porcupine/lib/common/porcupine_params.pv'
keyword_file_path = ['alexa_windows.ppn','hey pico_windows.ppn','porcupine_windows.ppn','terminator_windows.ppn']
sensitivity = [0.5,0.5,0.5,0.5]

handle = Porcupine(library_path, model_file_path, keyword_file_paths=keyword_file_path, sensitivities=sensitivity)

audio_stream = sd.InputStream(channels=1,device='Microsoft Sound Mapper - Input',
	samplerate=handle.sample_rate,blocksize=handle.frame_length, callback=audio_callback)


# def get_next_audio_frame():
#     # pa = pyaudio.PyAudio()
#     pcm =[]
#     while len(pcm)<=handle.frame_length:
#     	if not q.empty():
#     		pcm.append(q.get_nowait())
#     pcm=bytearray(pcm)
#     pcm = struct.unpack_from("h" * handle.frame_length, pcm)
#     return pcm

while True:
	print(q.qsize())

# r=True
# while r:
# 	r,f = cap.read()
# 	cv2.imshow('Stream', f)
# 	key=cv2.waitKey(1)
# 	if key==27:
# 		break
# 	pcm = get_next_audio_frame()
# 	print('Got_data !')
# 	keyword_index = handle.process(pcm)
# 	if keyword_index==1:
# 		print(keyword_file_path[keyword_index])
# 		print("Generating Caption...")
# 		cv2.imwrite('image.jpg',f)
# 		caption = c.file_caption('image.jpg')
# 		print(caption)
