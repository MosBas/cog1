"""Receives vectors and outputs some statistics"""

import threading
import time
from multiprocessing.connection import Connection
from multiprocessing import Event
import numpy as np
from base import Base

class Receiver(Base):
    """Receiver class. Responsible for processing the vectors and doing some stats"""
    def __init__(self, pipe: Connection, frequency: int, stop_event: Event, noise_mode: bool):
        super().__init__(pipe, frequency, stop_event, noise_mode)
        self.message_counter = 0
        self.prev_counter = 0
        self.matrix = None
        self.time_window_start = None
        self.outfile = None


    def process_vector(self, vector: np.array) -> None:
        """Group 100 vectors and compute std and mean"""
        output = None
        if self.matrix is None:
            self.matrix = np.array([vector])
            self.time_window_start = time.time()
        elif self.matrix.shape[0] < 100:
            self.matrix = np.append(self.matrix, [vector], axis=0)
        if self.matrix.shape[0] == 100:
            now = time.time()
            output = f"{self.time_window_start},{now},{self.matrix.mean()},{self.matrix.std()}"
            self.matrix = None
        return output


    def write_vector_stats(self, vector: np.array) -> None:
        """Write the vector processing output to a file"""
        output = self.process_vector(vector)
        if output:
            self.outfile.write(output + "\n")


    def receive_message(self) -> None:
        """Main message receiving loop"""
        while True:
            if self.stop_event.is_set():
                break
            if self.pipe.poll():
                vector = self.pipe.recv()
                self.message_counter += 1
                self.write_vector_stats(vector)


    def stats(self) -> None:
        """stats thread entry point"""
        rates = []
        # start collecting stats only after the first few second, letting the system stabilize
        seconds_to_wait = 2
        while True:
            if self.stop_event.is_set():
                break
            start_time = time.process_time()
            messages_aquired = self.message_counter - self.prev_counter
            self.prev_counter = self.message_counter # TODO: this isn't thread safe, need a lock
            if seconds_to_wait > 0:
                seconds_to_wait -= 1
                time.sleep(1)
                continue
            rates.append(messages_aquired)
            output = 'Rate of data acquisition: {count} vectors/sec, mean={mean:.2f}, std={std:.2f}'.format(
                count=messages_aquired, mean=np.mean(rates), std=np.std(rates))
            print(output)
            if self.noise_mode and messages_aquired < self.frequency:
                print('Packet loss detected')
            self.outfile.write(output + "\n")
            time.sleep(1 - (time.process_time() - start_time))


    def receive(self) -> None:
        """Main entry point for the Receiver class"""
        self.outfile = open('results.txt', 'w')
        receiver_thread = threading.Thread(target=self.receive_message)
        receiver_thread.start()
        stats_thread = threading.Thread(target=self.stats)
        stats_thread.start()
        stats_thread.join()
        receiver_thread.join()
        self.pipe.close()
        self.outfile.close()
