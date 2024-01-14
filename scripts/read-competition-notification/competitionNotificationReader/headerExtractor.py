import competitionNotificationReader as  cnr
import logging

def splitHeaders(lines: list[str]) -> cnr.mail.Mail:
    l = logging.getLogger(__name__)

    l.debug('Separating headers of an email')
    
    def _getHeaders(lines: list[str]):
        headerLines = []
        for idx,l in enumerate(lines):
            if l == '':
                remainingLines = lines[idx+1:]
                for j,rl in enumerate(remainingLines):
                    if rl.strip() != '':
                        return headerLines, remainingLines[j:]
                return headerLines, []
            
            if l.startswith('\t') or l.startswith(' '):
                lastLine = headerLines.pop()
                newLine = f'{lastLine[1]} {l.strip()}'
                headerLines.append(tuple([lastLine[0], newLine]))
            else:
                parts = l.split(':', 1)
                headerLines.append(tuple([parts[0].strip(), parts[1].strip()]))
    
    headerLines, bodyLines = _getHeaders(lines)

    mail = cnr.mail.Mail(headerLines, bodyLines)
    return mail
