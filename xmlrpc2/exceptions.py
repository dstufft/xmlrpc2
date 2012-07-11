##
# Base class for all kinds of client-side errors.


class Error(Exception):
    """Base class for client errors."""
    def __str__(self):
        return repr(self)

##
# Indicates an HTTP-level protocol error.  This is raised by the HTTP
# transport layer, if the server returns an error code other than 200
# (OK).
#
# @param url The target URL.
# @param errcode The HTTP error code.
# @param errmsg The HTTP error message.
# @param headers The HTTP header dictionary.


class ProtocolError(Error):
    """Indicates an HTTP protocol error."""
    def __init__(self, url, errcode, errmsg, headers):
        Error.__init__(self)
        self.url = url
        self.errcode = errcode
        self.errmsg = errmsg
        self.headers = headers

    def __repr__(self):
        return (
            "<ProtocolError for %s: %s %s>" %
            (self.url, self.errcode, self.errmsg)
            )

##
# Indicates a broken XML-RPC response package.  This exception is
# raised by the unmarshalling layer, if the XML-RPC response is
# malformed.


class ResponseError(Error):
    """Indicates a broken response package."""
    pass

##
# Indicates an XML-RPC fault response package.  This exception is
# raised by the unmarshalling layer, if the XML-RPC response contains
# a fault string.  This exception can also be used as a class, to
# generate a fault XML-RPC message.
#
# @param faultCode The XML-RPC fault code.
# @param faultString The XML-RPC fault string.


class Fault(Error):
    """Indicates an XML-RPC fault package."""
    def __init__(self, faultCode, faultString, **extra):
        Error.__init__(self)
        self.faultCode = faultCode
        self.faultString = faultString

    def __repr__(self):
        return "<Fault %s: %r>" % (self.faultCode, self.faultString)
