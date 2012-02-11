from twisted.trial.unittest import TestCase
from twisted.test import proto_helpers
from twisted.internet.protocol import ClientFactory

from .. import spdy

example_frames = "\x80\x02\x00\x01\x01\x00\x018\x00\x00\x00\x01\x00\x00\x00\x00\x00\x008\xea\xdf\xa2Q\xb2b\xe0f`\x83\xa4\x17\x06{\xb8\x0bu0,\xd6\xae@\x17\xcd\xcd\xb1.\xb45\xd0\xb3\xd4\xd1\xd2\xd7\x02\xb3,\x18\xf8Ps,\x83\x9cg\xb0?\xd4=:`\x07\x81\xd5\x99\xeb@\xd4\x1b3\xf0\xa3\xe5i\x06A\x90\x8bu\xa0N\xd6)NI\xce\x80\xab\x81%\x03\x06\xbe\xd4<\xdd\xd0`\x9d\xd4<\xa8\xa5\xbc(\x89\x8d\x81\x13\x1a$\xb6\x06\x0c,\xa0\xdc\xcf \x95\x9b\x9a\x92\x99\x98\x04LvyUz\xb9\x89\xc5\xd9\x99z\xf9E\xe9V\x96\x06\x06\x06\x0cl\xb9\xc0\x12(?\x85\x81\xd9\xdd5\x84\x81\xad\x18hNn*\x03kFI\t@\x05\xc5\x0c\xcc\xa0\xd0a\xd4g\xe0Bdi\x862\xdf\xfc\xaa\xcc\x9c\x9cD}S=\x03\x05\r\xdf\xc4\xe4\xcc\xbc\x92\xfc\xe2\x0ck\x05O`*\xcbQ\x00\n(\xf8\x07+D(\x18\x1a\xc4\x9b\xc5[h*8\x02\x03,5<5\xc9;\xb3D\xdf\xd4\xd8T\xcf\xd0PA\xc3\xdb#\xc4\xd7GG!'3;U\xc1=59;_S\xc19\x03XT\xa5\xea\x1b\x9a\xeb\x01\xc3\xd3\xccX\xcf\xc4L!81-\xb1(\x13\xaa\x89\x81\x1d\x1aa\x0c\x1c\xb0x\x04\x00\x00\x00\xff\xff"

class SpdyProtocolTest(TestCase):
    def setUp(self):
        self.factory = ClientFactory()
        self.factory.protocol = spdy.SpdyProtocol
        self.proto = self.factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def tearDown(self):
        return self.tr.loseConnection()
    
    def send(self, data):
        self.proto.dataReceived(data)    

    def testExampleFrames(self):
        self.send(example_frames)
        #self.assertTrue(False)
        # FIXME: ASSERT SOMETHING
        
                