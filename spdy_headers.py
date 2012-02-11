import struct

from twisted.web import http_headers

from c_zlib import compress, decompress

dictionary = \
"optionsgetheadpostputdeletetraceacceptaccept-charsetaccept-encodingaccept-" \
"languageauthorizationexpectfromhostif-modified-sinceif-matchif-none-matchi" \
"f-rangeif-unmodifiedsincemax-forwardsproxy-authorizationrangerefererteuser" \
"-agent10010120020120220320420520630030130230330430530630740040140240340440" \
"5406407408409410411412413414415416417500501502503504505accept-rangesageeta" \
"glocationproxy-authenticatepublicretry-afterservervarywarningwww-authentic" \
"ateallowcontent-basecontent-encodingcache-controlconnectiondatetrailertran" \
"sfer-encodingupgradeviawarningcontent-languagecontent-lengthcontent-locati" \
"oncontent-md5content-rangecontent-typeetagexpireslast-modifiedset-cookieMo" \
"ndayTuesdayWednesdayThursdayFridaySaturdaySundayJanFebMarAprMayJunJulAugSe" \
"pOctNovDecchunkedtext/htmlimage/pngimage/jpgimage/gifapplication/xmlapplic" \
"ation/xhtmltext/plainpublicmax-agecharset=iso-8859-1utf-8gzipdeflateHTTP/1" \
".1statusversionurl\0"

class SpdyHeaders(http_headers.Headers):

    def __init__(self, data=None, rawHeaders=None):
        super(SpdyHeaders, self).__init__(rawHeaders=rawHeaders)
        if data:
            self._parseHeaders(data)

    def asBinary(self, compressed=True):
        hdr_tuples = []
        for name, values in self._rawHeaders.items():
            hdr_tuples.extend([(name, value,) for value in values])
        hdr_tuples.sort()
        fmt = ["!H"]
        args = [len(hdr_tuples)]
        for n, v in hdr_tuples:
            # TODO: check for overflowing n, v lengths
            fmt.append("H%dsH%ds" % (len(n), len(v)))
            args.extend([len(n), n, len(v), v])
        hdrs = struct.pack("".join(fmt), *args)
        if compressed:
            return compress(hdrs, dictionary=dictionary)
        return hdrs
        
    def _parseHeaders(self, data):
        "Given a control frame data block, return a list of (name, value) tuples."
        # TODO: separate null-delimited into separate instances
        data = decompress(data, dictionary=dictionary) # FIXME: catch errors
        cursor = 2
        (num_hdrs,) = struct.unpack("!h", data[:cursor]) # FIXME: catch errors
        hdrs = []
        while cursor < len(data):
            try:
                (name_len,) = struct.unpack("!h", data[cursor:cursor+2]) # FIXME: catch errors
                cursor += 2
                name = data[cursor:cursor+name_len] # FIXME: catch errors
                cursor += name_len
            except IndexError:
                raise
            except struct.error:
                raise
            try:
                (val_len,) = struct.unpack("!h", data[cursor:cursor+2]) # FIXME: catch errors
                cursor += 2
                value = data[cursor:cursor+val_len] # FIXME: catch errors
                cursor += val_len
            except IndexError:
                raise
            except struct.error:
                print len(data), cursor, data # FIXME
                raise
            self.addRawHeader(name, value)

__all__ = ['SpdyHeaders']
