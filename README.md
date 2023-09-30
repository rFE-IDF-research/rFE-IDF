# rFE-IDF
This is a demo for rFE-IDF that is used to evaluate its performance.

## Library required
fhipe (available [here](https://github.com/kevinlewi/fhipe)) <br>
numpy (available by running `sudo apt-get install python3-numpy`)

## Running steps
1. Copy two Python functions `decrypt_new` and `solve_dlog_bsgs_new` in [ipe_new.py](https://github.com/rFE-IDF-research/rFE-IDF/blob/main/ipe_new.py) to the file in `/fhipe/fhipe/ipe.py`.
2. Copy the file [rFE-IDF.py](https://github.com/rFE-IDF-research/rFE-IDF/blob/main/rFE-IDF.py) to the directory `/fhipe/tests/`.
3. Run the command `sudo python3 rFE-IDF.py`.

## Running result
![running result](https://github.com/rFE-IDF-research/rFE-IDF/blob/main/running%20result.png "Running Result")
