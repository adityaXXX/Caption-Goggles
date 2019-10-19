import cv2
from captionbot import CaptionBot
import numpy as np
import urllib.request as urllib2

url = 'http://10.42.0.244/media/?action=stream'
username = 'admin'
password = ''
p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

stream = urllib2.urlopen(url)
byte = bytes()
c = CaptionBot()

while True:
	byte += stream.read(32768)
	a = byte.find(b'\xff\xd8')
	b = byte.find(b'\xff\xd9')
	if a != -1 and b != -1:
		jpg = byte[a:b+2]
		byte = byte[b+2:]
		img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
		img = cv2.resize(img,(640,480))
		cv2.imshow('Stream', img)
		key = cv2.waitKey(1)
		if key == ord('a'):
			print("Generating Caption...")
			cv2.imwrite('image.jpg',img)
			caption = c.file_caption('/home/aditya/Hack-a-bit2019/' + 'image.jpg')
			print(caption)
		elif key == 27:
			break
		else:
			continue
cv2.destroyAllWindows()



#     r, f = stream.read()
#     if r==True:
#         cv2.imshow("Stream", f)
#         key = cv2.waitKey(1)
#         if key == ord('a'):
#             print("Generating Caption...")
#             cv2.imwrite('image.jpg',f)
#             caption = c.file_caption('/home/aditya/Hack-a-bit2019/' + 'image.jpg')
#             print(caption)
#         elif key == 27:
#             break
#     else :
#         continue
# cv2.destroyAllWindows()
# cap.release()
