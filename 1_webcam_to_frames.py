import cv2
import os
import time

CAM_STREAM_DIR = 'E:\\4_GithubProjects\\fps-webcam-demo\\cam_stream'

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 15)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

img_counter = 0

capture_secs = 5
time_start = time.time()
while time.time() - time_start <= capture_secs:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    img_name = f"{img_counter}.png"
    img_path = os.path.join(CAM_STREAM_DIR, img_name)
    cv2.imwrite(img_path, frame)
    img_counter += 1


cam.release()
cv2.destroyAllWindows()
