from flask import Flask, Response
import cv2

app = Flask(__name__)

# 使用 OpenCV 捕获摄像头视频
camera = cv2.VideoCapture(0)  # 0 表示默认摄像头，可以根据需要更改为其他摄像头索引

def generate_frames():
    while True:
        success, frame = camera.read()  # 读取摄像头画面
        if not success:
            break
        else:
            # 将每一帧转换为 JPEG 格式，然后编码为 Bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # 使用 yield 语句输出 JPEG 格式的视频流
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # 返回一个生成器对象作为视频流响应
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
