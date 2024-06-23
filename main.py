import time
import random
from threading import Thread, Lock

class Process(Thread):
    def __init__(self, process_id, max_time_interval):
        super().__init__()
        self.process_id = process_id
        self.clock = 0
        self.max_time_interval = max_time_interval
        self.lock = Lock()

    def run(self):
        while True:
            self.internal_event()
            time.sleep(random.uniform(0.5, 2))

    def internal_event(self):
        time_interval = random.randint(1, self.max_time_interval)
        with self.lock:
            self.clock += time_interval
            print(f"Proces {self.process_id}: Zdarzenie wewnętrzne, czas = {self.clock}")

    def send_message(self, recipient):
        with self.lock:
            message_time = self.clock
            print(f"Proces {self.process_id}: Wysłano wiadomość, czas = {self.clock}")
        recipient.receive_message(message_time)

    def receive_message(self, message_time):
        with self.lock:
            self.clock = max(self.clock, message_time)
            print(f"Proces {self.process_id}: Otrzymano wiadomość, synchronizacja czasu = {self.clock}")

def simulate_processes(num_processes, max_time_interval, num_messages):
    processes = [Process(process_id, max_time_interval) for process_id in range(num_processes)]

    for process in processes:
        process.start()

    for _ in range(num_messages):
        sender = random.choice(processes)
        recipient = random.choice(processes)
        if sender != recipient:
            sender.send_message(recipient)


            time.sleep(random.uniform(1, 3))

    for process in processes:
        process.join()


if __name__ == "__main__":
    simulate_processes(num_processes=5, max_time_interval=5, num_messages=10)