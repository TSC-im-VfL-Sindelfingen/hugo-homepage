from . import cli
from . import mail
from . import headerExtractor
from . import mailParser
from . import competitionParser
from . import mboxReader

import logging
import debugpy
import os

def main():
    args = cli.getArgs()

    logging.basicConfig()
    logger = logging.getLogger(__name__)

    verbosityMap = {
        0: logging.WARNING,
        1: logging.INFO,
    }
    rootLogger = logging.getLogger()
    rootLogger.setLevel(verbosityMap.get(args.verbose, logging.DEBUG))

    if args.debug:
        debugpy.listen(5678)
        debugpy.wait_for_client()

    mp = mailParser.MailParser()
    cp = competitionParser.CompetitionParser()

    if args.read_mbox is not None:
        if args.output_folder is None:
            logger.error('Cannot use batch mode without explicit output folder.')
            exit(1)
        
        reader = mboxReader.MBocReader()
        mails = reader.parseMBoxFile(args.read_mbox[0])
        for mail in mails:
            body = mp.parseMail(mail)
            cp.parseMail(body)
            filename = cp.getFilename(args.output_folder[0])
            logger.info('Using file %s to generate the output.', filename)
            folder = os.path.dirname(filename)
            os.makedirs(folder, exist_ok=True)
            with open(filename, 'w') as fp:
                fp.write(cp.getContent())
    else:
        raise Exception('Not yet implemented')

