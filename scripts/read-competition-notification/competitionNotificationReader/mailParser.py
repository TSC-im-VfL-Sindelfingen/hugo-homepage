import competitionNotificationReader as cnr
import logging
import re

class MailParser:
    def __init__(self):
        self._l = logging.getLogger(__name__)
    
    def parseMail(self, rawMail: cnr.mail.Mail):
        # Look for the correct Mail encoding
        contentType, boundary = self._getContentType(rawMail)
        subMails = self._splitMultipartBody(rawMail.body, boundary)

        def isCorrectContentType(mail):
            for header in mail.headers:
                if header[0].lower() != 'content-type':
                    continue
                return header[1].startswith('text/html')
            return False
        subMails = list(filter(isCorrectContentType, subMails))
        
        def isCorrectContentEncoding(mail):
            for header in mail.headers:
                if header[0].lower() != 'content-transfer-encoding':
                    continue
                return header[1] == 'quoted-printable'
            return False
        subMails = list(filter(isCorrectContentEncoding, subMails))
        
        if len(subMails) != 1:
            raise Exception('Not implemented')

        body = self._mapQuotedrintable(subMails[0].body)
        return body
        
    
    def _getContentType(self, rawMail: cnr.mail.Mail) -> str:
        ctHeaders = list(filter(lambda x: x[0].lower() == 'content-type', rawMail.headers))
        if len(ctHeaders) != 1:
            self._l.error('No unique content type of the mail was found.')
            exit(1)
        
        ct = ctHeaders[0][1]
        if not ct.startswith('multipart/alternative'):
            raise Exception('Not yet implemented')
        
        parser = re.compile('.*boundary="([^"]+)"')
        matcher = parser.match(ct)
        if matcher is None:
            self._l.error('Cannot extract boundary from mail header.')
            exit(1)
        
        boundary = matcher.group(1)

        return 'multipart/alternative', boundary
    
    def _splitMultipartBody(self, bodyLines: list[str], boundary: str):
        parts = []
        subBody = []
        for line in bodyLines:
            if line.startswith(f'--{boundary}'):
                if len(subBody) > 0:
                    parts.append(subBody)
                    subBody = []
            else:
                subBody.append(line)
        return list(map(lambda x: cnr.headerExtractor.splitHeaders(x), parts))
    
    def _mapQuotedrintable(self, lines: list[str]):
        def mergeLines():
            # Drop terminating newlines
            ret = [l for l in lines]
            r = list(range(len(ret)))
            r.reverse()
            for i in r:
                currentLine = ret[i]
                if currentLine.endswith('='):
                    currentLine = currentLine[:-1] + ret.pop(i+1)
                    ret[i] = currentLine

            return ret
        
        mergedLines = mergeLines()

        def mapUnicodeChars():
            ret = []
            for line in mergedLines:
                i = 0
                chars = []
                while i < len(line):
                    if line[i] != '=':
                        chars.extend(list(line[i].encode()))
                    else:
                        hexChars = line[i+1:i+3]
                        value = int(hexChars, 16)
                        # print(f'{hexChars} -> {value}')
                        chars.append(value)
                        i += 2
                    i += 1
                ret.append(chars)
            
            return ret
        
        mappedLines = mapUnicodeChars()

        def decodeLine(l):
            bytes = [x.to_bytes(1, 'big') for x in l]
            decodedLine = b''.join(bytes).decode()
            return decodedLine
        decodedLines = list(map(decodeLine, mappedLines))

        return ''.join(decodedLines)

