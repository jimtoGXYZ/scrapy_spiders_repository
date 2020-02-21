import threading
import time
from queue import Queue

q = Queue()


def pe():
    while True:
        try:
            print(q.get(timeout=2))
        except Exception as e:
            print(repr(e))
            print('[队列无元素 准备正常退出]')
            return

if __name__ == '__main__':
    for i in range(10):
        q.put(i)

    t1 = threading.Thread(target=pe)
    t1.start()

    while True:
        time.sleep(1)
        q.put(2)
