import threading as trd
import time as t

# CurrentTime2 함수에서 stop_flag 변수를 이용하여
# CurrentTime1를 종료한다.
def CurrentTime1(term: int):
    global stop_flag
    # Event를 발생시킬 때 사용하는 method이다.
    # set(Event 발생)과 is_set(Event 확인)을 이용해 발생시킨다.
    stop_flag = trd.Event()

    while not stop_flag.is_set():
        sec = t.localtime().tm_sec
        print("T1 sec : ", sec)
        t.sleep(term)
    print('Stop Thread 1')

def CurrentTime2(term: int):
    while True:
        sec = t.localtime().tm_sec
        print("T2 sec : ", sec)
        if sec >= 55:
            stop_flag.set()
            print('Stop Thread 2')
            break
        t.sleep(term)

def main():
    thread1 = trd.Thread(target=CurrentTime1, name='CT1', args=(2, ))
    thread2 = trd.Thread(target=CurrentTime2, name='CT2', args=(3, ))

    thread1.daemon = True
    thread2.daemon = True

    thread1.start()
    thread2.start()

    # join method는 부모자식 관계에 있는 Thread일 때 종료 시간을 기다리기 위해 사용
    # 종료 순서를 지정하는 기능이라고 볼 수 있다.
    # child thread를 종료 후 parent thread가 종료할 때 사용한다.
    thread1.join()
    thread2.join()


if __name__ == '__main__':
    main()