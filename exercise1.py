#!/usr/bin/env python

""" Cogntiv Exercise 1 - main program """

import sys
from multiprocessing import Process, Pipe, Event
from emitter import Emitter
from receiver import Receiver


def main():
    """main"""
    # layman command line parsing
    noise_mode = bool('--noise_mode' in sys.argv)
    print(f"noise mode is {noise_mode}")
    frequency = 1000
    stop_event = Event()
    receiver_pipe, emitter_pipe = Pipe(duplex=False)
    emitter = Process(target=Emitter(emitter_pipe, frequency, stop_event, noise_mode).emit)
    emitter.start()
    receiver = Process(target=Receiver(receiver_pipe, frequency, stop_event, noise_mode).receive)
    receiver.start()
    input("press any key to terminate\n")
    stop_event.set()
    emitter.join()
    receiver.join()

if __name__ == '__main__':
    main()
