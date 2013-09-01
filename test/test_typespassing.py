#!/usr/bin/env python
##
## Author(s):
##  - Vincent Barbaresi <vbarbaresi@aldebaran-robotics.com>
##
## Copyright (C) 2013 Aldebaran Robotics

import time
import qi
from qi import ServiceDirectory
from qi import Session


class TestService:
    def display(self, t):
        return t


def test_throwing_callback():
    def raising(f):
        raise Exception("woops")

    local = "tcp://127.0.0.1:5555"
    sd = ServiceDirectory()
    sd.listen(local)

    s = Session()
    s.connect(local)
    f = s.service("ServiceDirectory", _async=True)

    f.addCallback(raising)
    time.sleep(0.01)
    s.close()


def test_unicode_strings():
    local = "tcp://127.0.0.1:5555"
    sd = ServiceDirectory()
    sd.listen(local)

    s = Session()
    s.connect(local)

    m = TestService()
    s.registerService("TestService", m)
    service = s.service("TestService")
    # ASCII range
    unicode_string = ''.join([unichr(i) for i in range(1, 128)])
    mystring = service.display(unicode_string)
    assert type(mystring) == str
    assert mystring == unicode_string.encode("ascii")

    # Wide unicode
    wide_string = "\U00010000" * 39 + "\uffff" * 4096
    mystring = service.display(wide_string)
    assert mystring == wide_string

    # String with many unicode chars
    unicode_string = ''.join([unichr(i) for i in range(1, 50000)])
    service.display(unicode_string)
    time.sleep(0.01)
    s.close()


def test_builtin_types():
    local = "tcp://127.0.0.1:5555"
    sd = ServiceDirectory()
    sd.listen(local)

    s = Session()
    s.connect(local)

    m = TestService()
    s.registerService("TestService", m)
    service = s.service("TestService")

    # None
    assert service.display(None) is None
    # bool
    t, f = service.display(True), service.display(False)
    assert t == 1L  # is True ?
    assert f == 0L  # is False ?

    # int
    assert type(service.display(42)) == long
    assert service.display(42) == 42

    # float
    assert service.display(0.1337) == 0.1337

    # long (32b)
    assert service.display(2 ** 31 - 1) == 2147483647

    # list
    assert service.display([]) == []
    assert service.display([1]) == [1]
    assert service.display(["bla", "bli"]) == ["bla", "bli"]

    # sets
    assert service.display(set([1, 2])) == (1, 2)
    assert service.display(frozenset([1, 2])) == (1, 2)
    assert service.display(frozenset([frozenset("a"), frozenset("b")])) \
     == (("b",), ("a",))

    # tuple
    assert service.display(()) == ()
    assert service.display((1)) == (1)
    assert service.display((1, 2)) == (1, 2)

    # dict
    assert service.display({}) == {}
    assert service.display({1: "bla", 3: []}) == {1: "bla", 3: []}

    # bytearray
    assert service.display(bytearray("lol")) == "lol"

    # buffer (not implemented)
    try:
        service.display(buffer("lol"))
    except RuntimeError:
        pass  # OK
    # complex (why not)
    assert service.display(complex(1.5, 2)) == 1.5

    time.sleep(0.01)
    s.close()


def test_object_types():
    local = "tcp://127.0.0.1:5555"
    sd = ServiceDirectory()
    sd.listen(local)

    s = Session()
    s.connect(local)

    m = TestService()
    s.registerService("TestService", m)
    service = s.service("TestService")

    # new style
    class A(object):
        pass
    obj = A()

    service.display(A)
    service.display(obj)

    # old style
    class Aold:
        pass
    objold = Aold()

    try:
        service.display(Aold)
    except RuntimeError:
        pass

    service.display(objold)


def test_qi_object_instance():
    local = "tcp://127.0.0.1:5555"
    sd = ServiceDirectory()
    sd.listen(local)

    s = Session()
    s.connect(local)

    m = s.service("ServiceDirectory")
    assert isinstance(m, qi.Object)


def main():
    test_throwing_callback()
    test_unicode_strings()
    test_builtin_types()
    test_object_types()
    test_qi_object_instance()

if __name__ == "__main__":
    main()
