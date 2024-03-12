import cv2
import socketio
from ultralytics import YOLO
import cvzone
import pandas as pd
import time

sio = socketio.Client()

# ... (socketio connection events)

if __name__ == "__main__":
    server_url = 'http://127.0.0.1:5000'
    sio.connect(server_url)
    model = YOLO('best.pt')

    def RGB(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            point = [x, y]
            print(point)

    cv2.namedWindow('RGB')
    cv2.setMouseCallback('RGB', RGB)

    cap = cv2.VideoCapture("vid.mp4")

    my_file = open("coco1.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")

    count = 0
    last_detection_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            # Break the loop if the video ends
            break

        count += 1
        if count % 3 != 0:
            continue

        frame = cv2.resize(frame, (1020, 500))
        results = model.predict(frame)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")

        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            c = class_list[d]
            if 'accident' in c:
                current_time = time.time()
                if current_time - last_detection_time >= 5:
                    # Send "accident_detected" message
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)
                    sio.emit('accident', "Accident_Detected : Latitude: 21° 11' 29.29\" N, Longitude: 81° 16' 34.28\" E")
                    last_detection_time = current_time
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)

        cv2.imshow("RGB", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
