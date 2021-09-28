import threading as trd
import cv2
import tensorflow as tf
import numpy as np

import time as t


# 해야할 일 2개
# 1. cam 변수 input 값을 넣어주는 reshape - 완료
# not image, 바로 변수형태로 해서 넣어주는게 처리속도가 빠름
# 2. Thread 이용 - 완료
def play_video(winname: str):
    global moment_image
    video = cv2.VideoCapture(0)
    
    anythread = trd.Thread(target=PredictionPicturesCount, name='CountThread', args=())
    anythread.daemon = True
    anythread.start()

    while True:
        # CheckActVideo : Video 활성화 여부
        CheckActVideo, moment_image = video.read() 

        if CheckActVideo:
            cv2.imshow(winname, moment_image)
            
        if cv2.waitKey(1) & 0xFF == 27:
            break

    video.release()
    cv2.destroyAllWindows()

def Timer(time_sec: int):
    # 일단 10초 
    # 운동별로 일정한 시간? -> 추후 논의하는 걸로
    # 특정 시간 어떻게 정함? -> 운동별로 다르다.
    for _ in time_sec:
        t.sleep(1)

def PredictionPicturesCount():
    # Cam이 켜지는 시간을 잠깐 기다리기
    t.sleep(1)
    path = 'C:\\Users\\pksmb\\Desktop\\Project\\SavedModel\\keras_model.h5'
    model = tf.keras.models.load_model(path)
    
    shape = (224, 224, 3)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    count = 0
    end_sec = t.time() + 10
    # 일시정지 기능 - 추후 구현하는걸로
    while True: # t.time() <= end_sec
        temp_img = moment_image.copy()
        temp_img.resize(shape, refcheck=False)
        # Normalize the image
        normalized_image_array = (temp_img.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

        # Prediction and Result print
        prediction = model.predict(data)
        if np.argmax(prediction) == 0:
            print(f'Knee Up : {np.round(prediction[0][0] * 100, 3)} %')
        elif np.argmax(prediction) == 1:
            print(f'일자바 이두컬 : {np.round(prediction[0][1] * 100, 3)} %')
        elif np.argmax(prediction) == 2:
            print(f'Base pose : {np.round(prediction[0][2] * 100, 3)} %')
        t.sleep(1) # 0.1 : 36장, 0.5 : 9장
    #     count += 1
    # print('Count : ', count)
    

def main():
    videothread = trd.Thread(target=play_video, name='VideoThread', args=('MyWindow1',))
    videothread.start()

if __name__ == '__main__':
    main()