import re
import jsonlpendec

def parse(b):
    s = strip(b)
    sa = re.split('\n', s)
    def splitcolumn(i):
        v = re.sub(r'\\:', r'-', i)
        return tuple(re.split(r':', v))

    r = [splitcolumn(x) for x in sa if len(x) > 0] 
    return r

def strip(b):
    s = jsonlpendec.from_bytes(b)
    return s.replace("\n\n", "\n").rstrip('\n')
