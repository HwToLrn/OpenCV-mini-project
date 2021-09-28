import threading as trd
import time as t

# Thread Name이 같으면 중복 Error가 발생할 줄 알았지만
# Name이 같아도 잘 동작한다.
# is_alive OR getName을 이용하여 중복을 방지하는 코드를 작성해야할 것 같다.
def CurrentTime1(term: int):
    while True:
        sec = t.localtime().tm_sec
        print("sec : ", sec)
        t.sleep(term)

def CurrentTime2(term: int):
    while True:
        sec = t.localtime().tm_sec
        print("sec : ", sec)
        t.sleep(term)

def main():
    thread1 = trd.Thread(target=CurrentTime1, name='CT1', args=(2, ))
    thread2 = trd.Thread(target=CurrentTime2, name='CT1', args=(6, ))

    # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
    thread1.daemon = True 
    thread2.daemon = True 

    print('Thread 1 Name : ', thread1.getName())
    print('Thread 2 Name : ', thread2.getName())

    print('Start Thread 1')
    print('Before : ', thread1.is_alive())
    thread1.start()
    print('After : ', thread1.is_alive())

    print('Start Thread 2')
    thread2.start()

if __name__ == '__main__':
    main()