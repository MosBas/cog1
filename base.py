"""Base class for the Emitter and Reciver, just for some common properties"""

class Base:
    """Base class for common properties"""
    def __init__(self, pipe, frequency, stop_event, noise_mode):
        self.pipe = pipe
        self.frequency = frequency
        self.stop_event = stop_event
        self.noise_mode = noise_mode
