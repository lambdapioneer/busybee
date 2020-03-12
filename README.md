# BusyBee 🐝

 - Simple, interactive multiprocessing for slow I/O and calculation in your notebook
 - Simple to use as a drop-in replacement for the standard `map` function
 - Prints the current progress and remaining time estimate
 - No external dependencies and 100% test coverage

The PyPI project page is here: https://pypi.org/project/busybee/

[![CircleCI](https://circleci.com/gh/lambdapioneer/busybee.svg?style=svg)](https://circleci.com/gh/lambdapioneer/busybee)

## Quick start

Install the BusyBee module via `pip` and use it as a replacement for your current `map` function. As BusyBee needs to know to total number of items the data must expose its length to `len()` calls. The best approach is to provide it as a `list`.

**Install:**

```bash
$ pip3 install busybee
```

**Code:**

```python
import busybee
result = busybee.map(func, data)
```

**Output:**

```C
BusyBee: Start processing 42 items with 8 processes...
BusyBee:  1/42,  2.4% (avg: 3.2s cpu, rem: 16.5s)
BusyBee: 15/42, 35.7% (avg: 2.4s cpu, rem: 8.1s)
BusyBee: 21/42, 50.0% (avg: 2.5s cpu, rem: 6.5s)
BusyBee: 24/42, 57.1% (avg: 2.6s cpu, rem: 5.8s)
BusyBee: 34/42, 81.0% (avg: 2.5s cpu, rem: 2.5s)
BusyBee: Finished processing 42 items in 16.1s (avg: 2.6s cpu)
```

## Advanced usage 👩‍💻 👨‍💻

You can configure the amount of cores to be used using the `processes` argument. For this you can either provide a number (e.g. 1, 8) or a simple formula such as `n/2` or `n-1`. The `n` refers to the logical number of CPU cores returned by the `multiprocessing` module.

Further, you can configure the output by providing a custom `stdout` sink and configuring how often you want to receive an update. You can do so by using the arguments `update_every_n_seconds` (default: 10) and `update_every_n_percent` (default: 50).

If you do not want any output, just set `quiet=False`.

**Example:**


```python
import busybee
result = busybee.map(
    func, data
    processes='n-1',
    update_every_n_seconds=10,
    update_every_n_percent=25,
)
```

## Q&A 🤔

**Why did you built it? And why shouldn't I just use the `multiprocessing` module**

I started building BusyBee when I was working with a lot of I/O and pre-processing in Python Notebooks. Parallelizing these cells made it much faster, but it was often more involved than a one-line change.

More importantly, it was hard to predict the remaining time and whether it was worth to avoid context switching or actually making some tea/coffee ☕.

**I want a different output!**

I want to allow choosing from certain output styles. This is on my roadmap, but I do not have any certain date in mind. To maintain the simplicity I do not envision supporting custom output formatting. However, I am happy to be convinced otherwise.

## Contribute 👋

Awesome that you are interested in improving this code! When contributing, please follow the following (common-sense) steps:

 - Create an issue before you write any code. This allows to guide you in the right direction.
    - If you are after a simple 1-5 line fix, you might ignore this.
 - In the pull-request explain the high-level goal and your approach. That provides valuable context.
 - Convince others (and yourself) that the change is safe and sound.
    - Run `python3 -m unittest tests/test*` after you added test cases for your changes
    - Run `coverage3 run --source busybee setup.py test && coverage3 report` to ensure that the code is actually fully covered

## Reference/BibTex 📚

If you want to reference BusyBee in documentation or articles, feel free to use this suggested BibTex snippet:

```
@misc{hugenroth2020busybee,
  author={{Daniel Hugenroth}},
  title={BusyBee Python Software Library},
  year={2020},
  url={https://github.com/lambdapioneer/busybee},
}
```
