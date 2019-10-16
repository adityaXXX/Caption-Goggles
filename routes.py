from pynput import keyboard
from flask import Flask, render_template, Response
import cv2
from captionbot import CaptionBot

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = {'username':"Deepak"}
    return render_template('index.html' , user= user)

def on_press(key):
    try:
        if key.char == 'a':
            print(key.char == 'a')
            print("Generating Caption...")
            cv2.imwrite('image.jpg',f)
            caption = c.file_caption('/home/aditya/Hack-a-bit2019/' + 'image.jpg')
            # caption = c.file_caption("C:/Users/Bharat/Desktop/Caption-Goggles/image.jpg")
            print(caption)
    except:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def gen():
    cap = cv2.VideoCapture(0)
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    listener.start()
    while True:
        ret ,frame =  cap.read()
        if ret == True:
            flag, encodedImage = cv2.imencode(".jpg" , frame)
            if not flag:
                continue
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        else:
            continue
    cv2.destroyAllWindows()
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
