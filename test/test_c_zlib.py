from twisted.trial.unittest import TestCase

from .. import c_zlib

class CZlibTest(TestCase):
    def testRoundTrip(self):
        dictionary = 'foobar'
        compressed = c_zlib.compress('foobar', level=9, dictionary=dictionary)
        decompressed = c_zlib.decompress(compressed, dictionary=dictionary)
        self.assertEqual('foobar', decompressed)
