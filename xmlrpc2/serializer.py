from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import collections
import base64
import datetime

from lxml import etree


__all__ = ["Serializer"]


class Serializer(object):

    def serialize(self, data):
        if len(data) != 1:
            raise ValueError("Cannot serialize a multi item or empty dictionary")

        if "methodCall" in data:
            xml = etree.Element("methodCall")

            methodName = etree.Element("methodName")
            methodName.text = data["methodCall"]["methodName"]

            xml.append(methodName)

            data = data["methodCall"]
        else:
            raise ValueError("xmlrpc packet not able to be serialized")

        if "params" in data:
            params = etree.Element("params")

            for item in data["params"]:
                param = etree.Element("param")
                param.append(self.to_xml(item))
                params.append(param)

            xml.append(params)

        return etree.tostring(xml)

    def to_xml(self, data):
        value = etree.Element("value")

        if isinstance(data, str):
            item = etree.Element("string")
            item.text = data
        elif isinstance(data, bool):
            item = etree.Element("boolean")
            item.text = str(1 if data else 0)
        elif isinstance(data, int):
            item = etree.Element("int")
            item.text = str(data)
        elif isinstance(data, float):
            item = etree.Element("double")
            item.text = str(data)
        elif isinstance(data, datetime.datetime):
            item = etree.Element("dateTime.iso8601")
            item.text = data.isoformat()
        elif isinstance(data, bytes):
            item = etree.Element("base64")
            item.text = base64.b64encode(data)
        elif isinstance(data, collections.Mapping):
            item = etree.Element("struct")

            for k, v in data.items():
                member = etree.Element("member")

                name = etree.Element("name")
                name.text = k

                member.append(name)
                member.append(self.to_xml(v))

                item.append(member)
        elif isinstance(data, collections.Iterable):
            item = etree.Element("array")
            array_data = etree.Element("data")

            for x in data:
                array_data.append(self.to_xml(x))

            item.append(array_data)
        else:
            raise ValueError("Unable to serialize {cls} objects, unknown type".format(cls=data.__class__.__name__))

        value.append(item)

        return value

    def from_xml(self, data):
        if not data.tag == "value":
            raise ValueError("Cannot deserialize a non value")

        # Values without a type are considered strings
        if data.text:
            return data.text

        # XMLRPC packets always have a single item inside of a value
        value = data[0]

        if value.tag == "string":
            return value.text
        elif value.tag == "boolean":
            return bool(int(value.text))
        elif value.tag in ("int", "i4"):
            return int(value.text)
        elif value.tag == "double":
            return float(value.text)
        elif value.tag == "dateTime.iso8601":
            return datetime.datetime.strptime(value.text, "%Y-%m-%dT%H:%M:%S")  # @@@ Optionally use dateutil?
        elif value.tag == "base64":
            return base64.b64decode(value.text.encode("utf-8"))
        elif value.tag == "struct":
            mapping = {}

            for member in value.iterchildren():
                key, value = None, None
                for i in member.iterchildren():
                    if i.tag == "name":
                        key = i.text
                    elif i.tag == "value":
                        value = self.from_xml(i)
                    else:
                        raise ValueError("Unknown struct members")
                mapping[key] = value

            return mapping
        elif value.tag == "array":
            array_data = value.find("data")
            return [self.from_xml(x) for x in array_data.iterchildren()]
        else:
            ValueError("Unable to deserialize {type}, unknown type".format(type=value.tag))
