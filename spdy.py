import struct

from twisted.web import iweb
from twisted.protocols import stateful
from zope.interface import implements

from spdy_headers import SpdyHeaders

# frame types
DATA_FRAME = 0x00
# Control frame, version number is 2.
CTL_FRM = 0x8002
CTL_SYN_STREAM = 0x01
CTL_SYN_REPLY = 0x02
CTL_RST_STREAM = 0x03
CTL_SETTINGS = 0x04
CTL_NOOP = 0x05
CTL_PING = 0x06
CTL_GOAWAY = 0x07

# flags
FLAG_NONE = 0x00
FLAG_FIN = 0x01
FLAG_UNIDIRECTIONAL = 0x02

STREAM_MASK = 0x7fffffff

class SpdyProtocol(stateful.StatefulProtocol):
    def __init__(self):
        self.streams = {}

    def getInitialState(self):
        return self.parseFrameHeader, 8
        
    def parseFrameHeader(self, header):
        # borrowed from nbhttp
        (d1, self._frameFlags, d2, d3) = struct.unpack("!IBBH", header[:8])
        if d1 >> 31 & 0x01: # control frame
            self._frameVersion = ( d1 >> 16 ) & 0x7fff # TODO: check version
            # FIXME: we use 0x00 internally to indicate data frame
            self._frameType = d1 & 0x0000ffff
            self._frameStreamId = None
        else: # data frame
            self._frameType = DATA_FRAME
            self._streamId = d1 & STREAM_MASK
        self._frameSize = (( d2 << 16 ) + d3)
        return self.parseFrameData, self._frameSize
        
    def parseFrameData(self, data):
        if self._frameType == CTL_SYN_STREAM:
            self.parseSynStreamFrame(data)
        return self.parseFrameHeader, 8
    
    def parseSynStreamFrame(self, data):
        streamId = struct.unpack("!I", data[:4])[0] & STREAM_MASK # FIXME: what if they lied about the frame len?
        tuplePos = 4 + 2
        if self._frameType == CTL_SYN_STREAM:
            associatedStreamId = struct.unpack("!I", data[4:8])[0]
            tuplePos += 4
        headers = SpdyHeaders(data=data[tuplePos:])
        request = SpdyRequest(streamId, headers)
        self.streams[streamId] = request
        self.streams[streamId].process()
        # FIXME: expose pri
        #self._input_start(stream_id, hdr_tuples)
    
    def sendReplyFrame(self, streamId, data):
        pass
    
    
class SpdyRequest:
    implements(iweb.IRequest)

    method = ''
    uri = ''
    path = None
    args = None
    requestHeaders = None
    responseHeaders = None
    
    def __init__(self, streamId, headers):
        self.streamId = streamId
        self.requestHeaders = headers

    def getHeader(key):
        pass

    def getCookie(key):
        pass

    def getAllHeaders():
        pass

    def getRequestHostname():
        pass

    def getHost():
        pass

    def getClientIP():
        pass

    def getClient():
        pass

    def getUser():
        pass

    def getPassword():
        pass

    def isSecure():
        pass

    def getSession(sessionInterface=None):
        pass
        
    def URLPath():
        pass

    def prePathURL():
        pass

    def rememberRootURL():
        pass

    def getRootURL():
        pass
        
    # Methods for outgoing response
    def finish():
        pass
        
    def write(data):
        pass
        
    def addCookie(k, v, expires=None, domain=None, path=None, max_age=None, comment=None, secure=None):
        pass

    def setResponseCode(code, message=None):
        pass
        
    def setHeader(k, v):
        pass

    def redirect(url):
        pass

    def setLastModified(when):
        pass

    def setETag(etag):
        pass

    def setHost(host, port, ssl=0):
        pass
