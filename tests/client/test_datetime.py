import datetime
import time

import pytest

import xmlrpc2.client


def test_default():
    xmlrpc2.client.DateTime()


def test_time():
    d = 1181399930.036952
    t = xmlrpc2.client.DateTime(d)

    assert str(t) == time.strftime("%Y%m%dT%H:%M:%S", time.localtime(d))


def test_time_tuple():
    d = (2007, 6, 9, 10, 38, 50, 5, 160, 0)
    t = xmlrpc2.client.DateTime(d)

    assert str(t) == "20070609T10:38:50"


def test_time_struct():
    d = time.localtime(1181399930.036952)
    t = xmlrpc2.client.DateTime(d)

    assert str(t) == time.strftime("%Y%m%dT%H:%M:%S", d)


def test_datetime_datetime():
    d = datetime.datetime(2007, 1, 2, 3, 4, 5)
    t = xmlrpc2.client.DateTime(d)

    assert str(t) == "20070102T03:04:05"


def test_repr():
    d = datetime.datetime(2007, 1, 2, 3, 4, 5)
    t = xmlrpc2.client.DateTime(d)

    assert repr(t) == "<DateTime '20070102T03:04:05' at %x>" % id(t)


def test_decode():
    d = " 20070908T07:11:13  "
    t1 = xmlrpc2.client.DateTime()

    t1.decode(d)

    tref = xmlrpc2.client.DateTime(datetime.datetime(2007, 9, 8, 7, 11, 13))

    assert t1 == tref

    t2 = xmlrpc2.client._datetime(d)

    assert t2 == tref


def test_comparison():
    now = datetime.datetime.now()
    then = now + datetime.timedelta(seconds=4)

    dtime = xmlrpc2.client.DateTime(now.timetuple())

    # datetime vs. DateTime
    assert dtime == now
    assert now == dtime
    assert then >= dtime
    assert dtime < then

    # str vs. DateTime
    dstr = now.strftime("%Y%m%dT%H:%M:%S")
    dtime_then = xmlrpc2.client.DateTime(then.timetuple())

    assert dtime == dstr
    assert dstr == dtime
    assert dtime_then >= dstr
    assert dstr < dtime_then

    # some other types
    dbytes = dstr.encode("ascii")
    dtuple = now.timetuple()

    with pytest.raises(TypeError):
        dtime == 1970

    with pytest.raises(TypeError):
        dtime != dbytes

    with pytest.raises(TypeError):
        dtime == bytearray(dbytes)

    with pytest.raises(TypeError):
        dtime != dtuple

    with pytest.raises(TypeError):
        dtime < float(1970)

    with pytest.raises(TypeError):
        dtime > dbytes

    with pytest.raises(TypeError):
        dtime <= bytearray(dbytes)

    with pytest.raises(TypeError):
        dtime >= dtuple
