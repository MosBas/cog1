"""Sends vectors in a given frquency, supporting noise-mode"""

# system imports
import time
import multiprocessing
from multiprocessing.connection import Connection
from multiprocessing import Event
# 3rd party imports
import numpy as np
# project imports
from base import Base

class Emitter(Base):
    """Emitter claass. Responsible for sending the vectors"""
    def __init__(self, pipe: Connection, frequency: int, stop_event: Event, noise_mode: bool):
        super().__init__(pipe, frequency, stop_event, noise_mode)
        self.rng = np.random.default_rng()


    def estimate_sending_time_simple(self) -> float:
        '''
        Timing how long it takes to send a random vector
        for this to be scientific, it requires calibration on many more samples.
        Enable this in order to use the more "realistic" sample sending.
        '''
        start = time.process_time()
        self.pipe.send(self.rng.normal(size=50))
        sending_time = time.process_time() - start
        return sending_time


    def estimate_sending_time_heavy(self, num_samples: int = 100) -> float:
        '''
        Unused. Demonstrates how one could try and evaluate the time it takes their
        machine to produce messages
        '''
        _, pipe = multiprocessing.Pipe(duplex=False)
        start = time.process_time_ns()
        for _ in range(num_samples):
            pipe.send(self.rng.normal(size=50))
        duration = (time.process_time_ns() - start) / (1000.0 * 1000.0) # nanoseconds -> seconds
        result = float(duration) / num_samples
        pipe.close()
        return result


    def sample_sender_realistic(self) -> None:
        '''
        Unused.
        This emulates a sensor that measures some value in a given frequency
        and emits the measurement.
        '''
        sleep_time = (1.0 / self.frequency) - self.estimate_sending_time_simple()
        while True:
            if self.stop_event.is_set():
                break
            self.pipe.send(self.rng.normal(size=50)) # in a real system, this would've been async
            time.sleep(sleep_time)

    def sample_sender(self) -> None:
        '''
        Silly sample sender. It's equivalent for getting all of the samples at once
        and sending them in bursts at the beginning of every second, while sleeping
        for the rest of the time.
        '''
        while True:
            if self.stop_event.is_set():
                break
            start = time.process_time()
            for _ in range(self.frequency):
                if not self.should_drop():
                    self.pipe.send(self.rng.normal(size=50))
            time.sleep(1 - (time.process_time() - start))


    def should_drop(self) -> bool:
        '''
        The instructions say:
        > according to a uniform distribution, in the interval of [2, 3] seconds.
        So I'm guessting the intention was 1 out of the thousand vectors could get
        dropped, and only in the window of [2, 3] seconds. So in second [2, 3],
        then in [5, 6], [8, 9], etc.
        '''
        # Taking the seconds, mod 3, and checking if we're in the 2->3 window
        # Getting a random number between 0 and 1000 (exclusive)
        if (self.noise_mode
            and int(time.time() % 60 % 3) == 2
            and int(self.rng.uniform(0, 1000)) == 0):
            return True
        return False


    def emit(self) -> None:
        '''
        Use this method as the "entry point" of the Emitter class
        '''
        self.sample_sender()
        self.pipe.close()
