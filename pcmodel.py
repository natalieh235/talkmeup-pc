from queue import Queue
from threading import Thread
import time
import random

MAX_ITEMS = 100

class Producer(Thread):
    def __init__(self, name, queues, max_items):
        super().__init__(name=name)
        self.queues = queues
        self.max_items = max_items

    def run(self):
        for i in range(self.max_items):
            #find (approxmiate) shortest queue
            shortest = sorted(self.queues, key=lambda x: x.qsize())[0]  

            #put item
            shortest.put(i)

class Consumer(Thread):
    def __init__(self, name, queue):
        #run as daemon to exit the infinite loop
        super().__init__(name=name, daemon=True)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            print(f'{self.name} getting {item} from queue')
            time.sleep(random.random())
            self.queue.task_done()

if __name__ == "__main__":
    queues = [Queue(), Queue(), Queue()]
    producer = Producer("producer", queues, MAX_ITEMS)

    #initialize consumer threads w/ name and queue
    consumers = [Consumer(f'consumer {i}', queues[i]) for i in range(len(queues))]

    producer.start()
    for c in consumers:
        c.start()

    for q in queues:
        q.join()

    