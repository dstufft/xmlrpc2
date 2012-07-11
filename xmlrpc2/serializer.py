import datetime

from collections import Iterable, Mapping

from lxml import etree
from lxml.builder import E

from .constants import MAXINT, MININT

from .compat import basestring, long, str


class Serializer(object):

    def __init__(self, encoding=None, allow_none=None, *args, **kwargs):
        super(Serializer, self).__init__(*args, **kwargs)

        self.encoding = encoding
        self.allow_none = allow_none

    def dumps(self, method, arguments):
        methodCall = E.methodCall(
                E.methodName(method),
                E.params(*[E.param(E.value(self.dump_arg(arg))) for arg in arguments]),
            )

        serialized = etree.tostring(methodCall)

        print serialized

        return serialized

    def dump_arg(self, obj):
        if obj is None:
            if not self.allow_none:
                raise TypeError("Cannot serialize None (Did you mean to allow_none=True?)")
            return E.nil()

        elif isinstance(obj, (int, long)):
            if obj > MAXINT or obj < MININT:
                raise OverflowError("int exceeds XML-RPC limits")
            return E.int(str(obj))

        elif isinstance(obj, bool):
            return E.boolean(str(1 if obj else 0))

        elif isinstance(obj, float):
            return E.double(str(float))

        elif isinstance(obj, basestring):
            return E.string(obj)

        elif isinstance(obj, datetime.datetime):
            node = etree.Element("dateTime.iso8601")
            node.text = obj.isoformat()
            return node

        elif isinstance(obj, Mapping):
            i = id(obj)

            if i in self.memo:
                raise TypeError("Cannot serialize recursive dictionaries")

            self.memo[i] = None

            members = []

            for k, v in obj.items():
                if not isinstance(k, basestring):
                    raise TypeError("dictionary keys must be strings")

                members.append(
                    E.member(
                        E.name(k),
                        E.value(self.dump_arg(v)),
                    )
                )

            del self.memo[i]

            return E.struct(*members)

        elif isinstance(obj, Iterable):
            i = id(obj)

            if i in self.memo:
                raise TypeError("Cannot serialize recursive sequences")

            self.memo[i] = None
            members = [self.dump_arg(i) for i in obj]
            del self.memo[i]

            return E.array(E.data(*members))

        else:
            raise TypeError("Cannot serialize object of type %s" % type(obj))
