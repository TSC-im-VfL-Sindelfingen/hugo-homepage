import logging
import re
import io

import competitionNotificationReader as cnr

class MBocReader:

    def __init__(self):
        self._l = logging.getLogger(__name__)
    
    def parseMBoxFile(self, filename: str) -> list[cnr.mail.Mail]:
        self._l.debug('Reading MBox file "%s"', filename)

        mails = []
        with open(filename) as fp:
            return self._parseMails(fp)
    
    def _isNewMailLine(self, line: str):
        return line.startswith('From ')
    
    def _fixSingleLine(self, line: str) -> str:
        regex = re.compile('^>+From ')
        matcher = regex.match(line)

        if matcher is None:
            return line

        return line[1:]
    
    def _parseMails(self, fp: io.FileIO) -> list[cnr.mail.Mail]:
        lines = []
        mails = []
        while True:
            line = fp.readline()
            if line == '':
                if len(lines) > 0:
                    mails.append(self._parseSingleMail(lines))
                return mails
            
            if self._isNewMailLine(line):
                if len(lines) > 0:
                    mails.append(self._parseSingleMail(lines))
                lines = []
            else:
                lines.append(self._fixSingleLine(line[0:-1]))
    
    def _parseSingleMail(self, lines: list[str]) -> cnr.mail.Mail:
        return cnr.headerExtractor.splitHeaders(lines)
