from multiprocessing import Process, Queue
import cv2
import os
import time

import sys
sys.path.append('./ECCV2022-RIFE')


input_q = Queue()
output_q = Queue()



# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FPS, 15)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def _interpolate(input_q, output_q):
    # To avoid loading the model in all 3 subprocesses
    from interpolation_wrapper import interpolate_wrapper
    interpolate_wrapper(input_q, output_q)


def capture_frames(q):
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FPS, 15)
    capture_secs = 20
    time_start = time.time()
    while time.time() - time_start <= capture_secs:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        q.put(frame)
    cam.release()
    cv2.destroyAllWindows()


def display_frames(q):
    while True:
        img = q.get()
        cv2.imshow("Display Window", img)
        cv2.waitKey(5)


def main():
    interpolate_worker = Process(
            target=_interpolate,
            args=(input_q, output_q)
        )

    capture_worker = Process(
            target=capture_frames,
            args=(input_q, )
        )

    display_worker = Process(
            target=display_frames,
            args=(output_q, )
        )

    interpolate_worker.start()
    capture_worker.start()
    display_worker.start()

    time.sleep(40)
    interpolate_worker.terminate()
    capture_worker.terminate()
    display_worker.terminate()
    interpolate_worker.join(timeout=30)
    capture_worker.join(timeout=30)
    display_worker.join(timeout=30)


if __name__ == '__main__':
    main()
