# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Variant_8: Dictionary based on hash-map, open address
import threading
from threading import Lock


class Next:
    def __init__(self, myDictionary):
        self.data = myDictionary
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        x = self.index
        self.index += 1
        if self.data.top < x:
            raise StopIteration
        a = self.data.que[x]
        if a is None:
            return None
        b = self.data.get(self.data.que[x])
        if a == self.data.none_default:
            a = None
        entry = (a, b)
        return entry


class HMOpenAddressDict:
    none_default = "2611556444074013268L"

    def __init__(self, size=0):
        self.dic_size = size
        self.store = [i for i in range(2 * size)]
        self.keys = [i for i in range(2 * size)]
        # que is used to record the seq of inserts
        self.que = [i for i in range(size)]
        self.top = -1
        # init que、store、keys
        for i in range(size):
            self.que[i] = None
        for i in range(2 * size):
            self.store[i] = None
            self.keys[i] = None

    def __str__(self):
        ret = "{"
        for item in self:
            a = str(item[0])
            if a != "None":
                if not str.isdigit(a):
                    a = "'" + a + "'"

            b = str(item[1])
            if b != "None":
                if not str.isdigit(b):
                    b = "'" + b + "'"

            ret = ret + a + ":" + b + ","
        ret = ret.strip(',') + "}"
        return ret

    def __eq__(self, other):
        if self.top != other.top:
            return False
        for i in range(len(self.que)):
            if self.que[i] is None:
                break
            else:
                a = self.que[i]
                if not other.contains_key(a):
                    return False
                b = self.get(self.que[i])
                if other.get(a) != b:
                    return False
        return True

    def __iter__(self):
        return Next(self)

    # model hash(modular arithmetic) :: f( key ) = key mod p ( p ≤ m )
    def compute_index(self, key):
        if key is None:
            key = self.none_default
        hash_value = hash(key)
        if hash_value < 0:
            hash_value = hash_value * -1
        return hash_value % self.dic_size

    # to update the que
    def delete_que_by_key(self, key):
        t = 0
        for i in range(self.dic_size):
            if self.que[i] == key:
                t += 1
            if self.que[i] is None:
                break
            if i + 1 >= self.dic_size:
                self.que[i] = None
                break
            self.que[i] = self.que[i + t]
        if t > 0:
            self.top -= 1

    # transform key to index
    # open address
    def find(self, key):
        index = self.compute_index(key)
        if self.keys[index] == key:
            return index
        else:
            index += 1
            while index < len(self.keys):
                if self.keys[index] == key:
                    return index
                if self.keys[index] is None:
                    return -1
                index += 1
            return -1

    def add(self, key, value):
        self.set(key, value)
        return self

    # when set ,the object should be locked
    def set(self, key, value):
        if key is None:
            key = self.none_default
        if value is None:
            value = self.none_default
        lock = Lock()
        lock.acquire()
        try:
            old_index = self.find(key)
            if old_index > -1:
                # there is a the same key in this dictionary, and replace it
                self.store[old_index] = value
                # update the seq of key-value insert
                self.delete_que_by_key(key)
                self.top += 1
                self.que[self.top] = key
                return True
            if self.top + 1 >= self.dic_size:
                # table is full
                return False
            index = self.compute_index(key)
            if self.keys[index] is None:
                self.keys[index] = key
                self.store[index] = value
                self.top += 1
                self.que[self.top] = key
                return True
            else:
                index += 1
                while index < len(self.keys):
                    if self.keys[index] is None:
                        break
                    index += 1
                if index < len(self.keys):
                    self.keys[index] = key
                    self.store[index] = value
                    self.top += 1
                    self.que[self.top] = key
                    return True
        finally:
            lock.release()

    def get(self, key):
        if key is None:
            key = self.none_default
        index = self.find(key)
        if index > -1:
            a = self.store[index]
            if a == self.none_default:
                a = None
            return a
        else:
            return None

    def contains_key(self, item):
        if item is None:
            item = self.none_default
        for i in self.keys:
            if i == item:
                return True
        return False


def cons(key, value, m):
    ret = HMOpenAddressDict(length(m) + 1)
    for e in m:
        ret.add(e[0], e[1])
    ret.add(key, value)
    return ret


def remove(m, key):
    ret = HMOpenAddressDict(length(m))
    for item in m:
        if item[0] != key:
            ret.add(item[0], item[1])
    return ret


def length(m):
    return m.dic_size


def member(key, m):
    return m.contains_key(key)


def reverse(li):
    ret = HMOpenAddressDict(length(li))
    for i in range(li.top + 1):
        ret.add(li.que[li.top - i], li.get(li.que[li.top - i]))
    return ret


def to_list(m):
    ret = []
    for i in m:
        ret.append(i)
    return ret


def from_list(li):
    m = HMOpenAddressDict(len(li))
    for entry in li:
        a = entry[0]
        b = entry[1]
        if a is None:
            a = m.none_default
        if b is None:
            b = m.none_default
        m.add(a, b)
    return m


def find(li, key):
    if key is None:
        key = li.none_default
    index = li.find(key)
    if index > -1:
        a = li.store[index]
        if a == li.none_default:
            a = None
        return a
    else:
        return None


def filter(li, f):
    ret = HMOpenAddressDict(li.dic_size)
    for i in range(len(li.que)):
        if li.que[i] is None:
            break
        a = li.que[i]
        if a == li.none_default:
            a = None
        if f(a):
            ret.add(a, li.get(a))
    return ret


def mmap(li, p):
    ret = HMOpenAddressDict(li.dic_size)
    for i in li:
        a = p(i)
        ret.add(a[0], a[1])
    return ret


def reduce(self, p):
    ret = 0
    for i in range(len(self.store)):
        if self.store[i] is not None:
            ret = p(ret, self.store[i])
    return ret


def iterator(li):
    return Next(li)


def mempty():
    return HMOpenAddressDict()


def mconcat(m, o):
    ret = HMOpenAddressDict(m.dic_size + o.dic_size)
    for item in m:
        ret.add(item[0], item[1])
    for item in o:
        ret.add(item[0], item[1])
    return ret


def exchangeDic2Tuples(d):
    test = []
    for item in d.items():
        a = item[0]
        b = item[1]
        t = (a, b)
        test.append(t)
    return test
