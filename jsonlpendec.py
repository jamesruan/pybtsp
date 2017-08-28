import json

def to_bytes(s):
    return bytes(s, encoding='utf-8')

def from_bytes(b):
    return str(b, encoding='utf-8')

def encodebytes(o):
    s = json.dumps(o, ensure_ascii=False)
    t = to_bytes(s)
    l = len(t)
    return l.to_bytes(2, 'big') + t

def encodeTo(sink, s):
    t = encodebytes(s)
    return sink.send(t)

def decodebytes(b):
    head = b[0:2]
    l = int.from_bytes(head, 'big')
    tail = b[2:2+l]
    s = from_bytes(tail)
    return json.loads(s)

def decodeFrom(s):
    head = s.recv(2)
    l = int.from_bytes(head, 'big')
    tail = s.recv(l)
    return decodebytes(head + tail)

if __name__ == '__main__':
    a = {'a':'a', 'b': 'b', 'c': 123}
    print(a)
    binary = encodebytes(a)
    print(binary)
    b = decodebytes(binary)
    print(b)
    print(a == b)

    import os
    import threading
    class fdFile(object):
        def __init__(self, fd):
            self.fd = fd

        def recv(self, n):
            return os.read(self.fd, n)

        def send(self, b):
            return os.write(self.fd, b)

    pipe = os.pipe()
    def readf():
        f = fdFile(pipe[0])
        o = decodeFrom(f)
        print("from pipe:", o)

    def writef():
        f = fdFile(pipe[1])
        print("to pipe:", a)
        encodeTo(f, a)

    ta = threading.Thread(target = readf)
    tb = threading.Thread(target = writef)
    ta.start()
    tb.start()
    ta.join()
    tb.join()

