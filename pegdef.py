import re

integer = re.compile(r"[\d]+")

HWAddr = re.compile(r"([0-9a-zA-Z]{2}:){5}[0-9a-zA-Z]{2}")

PhyName = re.compile(r"phy#\d")

FreqMHz = re.compile(r"\d+ MHz")

InterfaceName = re.compile(r"wlan\d")

dBm = re.compile(r"-\d+.\d+ dBm")

Time = re.compile(r"\d{2}:\d{2}:\d{2}")

def thing2obj(thing):
    import pypeg2
    try:
        v = thing.to_obj()
        return v
    except AttributeError:
        pass

    if isinstance(thing, str):
        obj = str(thing)
        return obj

    try:
        l = thing.list
        obj = []
        for i in l:
            obj.append(thing2obj(i))
        return obj
    except AttributeError:
        obj = {}
        if isinstance(thing, list):
            l = thing
        elif isinstance(thing, pypeg2.Namespace):
            l = thing.values()
        else:
            l = []

        for i in l:
            try:
                k = type(i).type
            except AttributeError:
                k = type(i).__name__
            obj[k] = thing2obj(i)
        return obj
