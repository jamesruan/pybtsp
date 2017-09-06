import re
import jsonlpendec

def parse(b):
    s = strip(b)
    sa = re.split('\n', s)
    def splitcolumn(i):
        v = re.sub(r'\\:', r'-', i)
        return re.split(r':', v)
    return map(lambda i: splitcolumn(i), sa)

def strip(b):
    s = jsonlpendec.from_bytes(b)
    return s.replace("\n\n", "\n").rstrip('\n')
