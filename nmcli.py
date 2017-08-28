import re
import jsonlpendec

def parse(b):
    s = strip(b)
    sa = re.split('\n', s)
    return map(lambda i: re.split(":", i), sa)

def strip(b):
    s = jsonlpendec.from_bytes(b)
    return s.rstrip('\n')
