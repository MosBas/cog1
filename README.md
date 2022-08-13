## How to run this code
This project assumes a supported version of Python, so 3.8 or above.
Write permissions on the working directory are needed in order for the output file to be generated.
1. create a new virtualenv (`virtualenv venv`), and activate it (`source venv/bin/activate`)
2. install dependencies using `pip install -r requirements.txt`
3. run `./exercise1.py`. Press any key (e.g Enter) to terminate.
4. run `./exercise1.py --noise_mode` for noise mode...
5. observe `results.txt` for the output.

## Design decisions

### Using virtualenv (or pipenv)
A far nicer way to bundle the code together would've been Docker, but that would add a requirement for 
Windows and MacOS machines. For the exercise I assumed it'll be tested on a machine that has nothing but some
Python distribution.

### Multiprocessing
The `multiprocessing` lib is the quickest way to get 
multiple processes along with communication channels (e.g an OS pipe) between them, set-up "for free".

Given the fact pipe sizes are limited by the OS, we can optimize the app by tweaking the underlying system.
Obviously this is out of scope in the exercise, at least as long as it's unclear which underlying system will be used.

An alternative could be using `mmap` and fork child processes manually.

### Unit tests
Run `python -m pytest`

### Linting and static code analysis
I've used `pylint` without any customizations. Simply run `pylint *.py`.

### Trying to be temporally accurate
At the time of writing this README, it wasn't clear whether vectors should be emitted in bursts, at the beginning of
every second (1000/s), or should emulate how an actual sensor would sample an input (brain or other device).

I went with the first approach, since it's simpler, but the `Emitter` class contains methods demonstrating how
the latter could be implemented.

For the latter:
The Emitter process tries to figure out how much CPU time is spent on sending a single message, in order to reach
the requested frequency (1000Hz, but could be whatever). It isn't accurate or scientific in any way. A better approach
would've been to learn from a larger sample (e.g make 10K attempts and avg the results). An even better approach would've
been if the process would constantly learn. The reason for why it would be more accurate, is because it depends, among
other things, on system load.

## Sample output
YMMV
```
❯ ./exercise1.py --noise_mode
noise mode is True
press any key to terminate
Rate of data acquisition: 1000 vectors/sec, mean=1000.00, std=0.00
Rate of data acquisition: 1000 vectors/sec, mean=1000.00, std=0.00
Rate of data acquisition: 1000 vectors/sec, mean=1000.00, std=0.00
Rate of data acquisition: 1000 vectors/sec, mean=1000.00, std=0.00
Rate of data acquisition: 998 vectors/sec, mean=999.60, std=0.80
Packet loss detected
Rate of data acquisition: 1000 vectors/sec, mean=999.67, std=0.75
Rate of data acquisition: 1000 vectors/sec, mean=999.71, std=0.70
Rate of data acquisition: 999 vectors/sec, mean=999.62, std=0.70
Packet loss detected
Rate of data acquisition: 1000 vectors/sec, mean=999.67, std=0.67
Rate of data acquisition: 1000 vectors/sec, mean=999.70, std=0.64
Rate of data acquisition: 890 vectors/sec, mean=989.73, std=31.54
Packet loss detected
Rate of data acquisition: 1109 vectors/sec, mean=999.67, std=44.71
Rate of data acquisition: 1000 vectors/sec, mean=999.69, std=42.95
Rate of data acquisition: 495 vectors/sec, mean=963.64, std=136.41
Packet loss detected
Rate of data acquisition: 1286 vectors/sec, mean=985.13, std=154.38
Rate of data acquisition: 744 vectors/sec, mean=970.06, std=160.47
Packet loss detected
```