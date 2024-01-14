import bs4
import logging
import re
import os
import jinja2

class ParsingFailedEception(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CompetitionParser:

    def __init__(self):
        self._l = logging.getLogger(__name__)

        self._partner = ''
        self._partnerin = ''
        self._date = ''
        self._title = ''
        self._number = ''
        self._group = ''
        self._class = ''
        self._section = ''
        self._ort = ''
        self._verein = ''
        self._telefon = ''

        self._reName = re.compile('Neue Meldung für (.*) / (.*)!')
        self._reDate = re.compile('([0-9]+)\.([0-9]+)\.([0-9]+)')
        self._reNumber = re.compile('Turnier: ([0-9]+)')
        self._rePhone = re.compile('Telefon: ([0-9 /]+)')
        self._rePlace = re.compile('Ort: (.*), (.*)')
        self._reCompetition = re.compile('(.*) ([A-ES]) ((?:Std)|(?:Lat)|(?:Kombi))')

        self._reCleaningString = re.compile('[^a-z0-9-]')
        self._reDashes = re.compile('-+')
    
    def parseMail(self, body: str):
        parser = bs4.BeautifulSoup(body, 'html.parser')
        self._getNames(parser.h2)
        self._parseTable(parser.table)

    def _getNames(self, h2):
        matcher = self._reName.match(h2.string)
        if matcher is None:
            self._l.error('Parsing of header "%s" failed.', h2)
            raise ParsingFailedEception('Header could not be successfully parsed')
        self._partner = matcher.group(1)
        self._partnerin = matcher.group(2)
    
    def _parseTable(self, table):
        def parseDate(date):
            match = self._reDate.fullmatch(date)
            if match is None:
                raise ParsingFailedEception('Cannot parse date %s in mail' % date)
            self._date = f'{match.group(3)}-{match.group(2)}-{match.group(1)}'
        
        def parseNumber(content):
            match = self._reNumber.fullmatch(content)
            if match is None:
                raise ParsingFailedEception(f'Cannot parse the turnier number in field {content}')
            self._number = match.group(1)

        def parseCompetition(competition):
            match = self._reCompetition.fullmatch(competition)
            if match is None:
                raise ParsingFailedEception(f'Cannot parse the competition line {competition}')
            self._group = match.group(1)
            self._class = match.group(2)
            self._section = match.group(3)
        
        def parsePlace(place):
            match = self._rePlace.fullmatch(place)
            if match is None:
                raise ParsingFailedEception(f'Cannot parse the place entry {place}')
            self._verein = match.group(1)
            self._ort = match.group(2)
        
        def parsePhone(phone):
            match = self._rePhone.fullmatch(phone)
            if match is None:
                raise ParsingFailedEception(f'Cannot parse the phone line {phone}')
            self._telefon = match.group(1)
        
        tds = table('td')
        parseDate(tds[0].string.strip())
        self._title = tds[1].string.strip()
        parseNumber(tds[2].string.strip())
        parseCompetition(tds[3].string.strip())
        parsePlace(tds[4].string.strip())
        parsePhone(tds[5].string.strip())

    def _cleanName(self, name: str) -> str:
        cleanedName = name.lower()
        cleanedName = re.sub('ä', 'ae', cleanedName)
        cleanedName = re.sub('ö', 'oe', cleanedName)
        cleanedName = re.sub('ü', 'ue', cleanedName)
        cleanedName = re.sub('ß', 'ss', cleanedName)
        cleanedName = re.sub(self._reCleaningString, '-', cleanedName)
        cleanedName = re.sub(self._reDashes, '-', cleanedName)
        return cleanedName.lower()

    def getFilename(self, prefix: str) -> str:
        namePartner = self._cleanName(self._partner)
        namePartnerin = self._cleanName(self._partnerin)
        competition = f'{self._group} {self._class} {self._section}'
        competitionName = self._cleanName(competition)

        return os.path.join(
            prefix,
            self._date[0:4],
            f'{self._date}-{self._ort.lower()}-{namePartner}-{namePartnerin}-{competitionName}.md'
        )   
    
    def getContent(self) -> str:
        with open(os.path.join(os.path.dirname(__file__), 'contenttemplate.md.tmpl')) as fp:
            tpl = fp.read()
        j2 = jinja2.Template(tpl)
        vars = {
            'date': self._date,
            'partner': self._partner,
            'partnerin': self._partnerin,
            'verein': self._verein,
            'ort': self._ort,
            'telefon': self._telefon,
            'group': self._group,
            'class': self._class,
            'section': self._section,
            'title': self._title,
            'number': self._number,
        }
        return j2.render(**vars)
