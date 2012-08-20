from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import base64
import datetime

from lxml import etree


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

        print(etree.tostring(xml))

    def to_xml(self, data):
        value = etree.Element("value")

        if isinstance(data, int):
            item = etree.Element("int")
            item.text = data
        elif isinstance(data, bool):
            item = etree.Element("boolean")
            item.text = 1 if data else 0
        elif isinstance(data, str):
            item = etree.Element("string")
            item.text = data
        elif isinstance(data, float):
            item = etree.Element("double")
            item.text = data
        elif isinstance(data, datetime.datetime):
            item = etree.Element("dateTime.iso8601")
            item.text = data.isoformat()
        elif isinstance(data, bytes):
            item = etree.Element("base64")
            item.text = base64.b64encode(data)
        else:
            raise ValueError("Unable to serialize {cls} objects, unknown type".format(cls=data.__class__.__name__))

        value.append(item)

        return value
