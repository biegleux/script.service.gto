#!/usr/bin/python

from .. tools import *


class Scraper():
    def __init__(self):

        # Properties

        self.enabled = True
        self.baseurl = 'https://www.csfd.cz/'
        self.lang = 'cs_CZ'
        self.rssurl = 'https://www.csfd.cz/televize/'
        self.friendlyname = 'TV tipy dne'
        self.shortname = 'CSFD.cz'
        self.icon = 'csfd.png'
        self.selector = '<div class="box-content box-content-striped-articles">'
        self.subselector = '<article class="article article-poster-78">'
        self.err404 = 'csfd_dummy.jpg'

    def reset(self):

        # Items

        self.channel = ''
        self.title = ''
        self.thumb = False
        self.detailURL = ''
        self.startdate = ''
        self.enddate = ''
        self.runtime = 0
        self.genre = ''
        self.plot = ''
        self.cast = ''
        self.rating = 0

    def scrapeRSS(self, content):

        self.reset()
        try:
            self.channel = re.compile('</strong> na <img alt="(.+?)" src', re.DOTALL).findall(content)[0]
            self.title = re.compile('class="film-title-name">(.+?)</a>', re.DOTALL).findall(content)[0]
            self.plot = re.compile('<p class="p-tvtips-2row p-tvtips-2row-long">(.+?)<span', re.DOTALL).findall(content)[0].strip()
        except IndexError:
            pass
        try:
            _s = re.compile('<strong>(.+?)</strong>', re.DOTALL).findall(content)[0].split(' - ')[0]
            _e = re.compile('<strong>(.+?)</strong>', re.DOTALL).findall(content)[0].split(' - ')[1]
            _ds = datetime.datetime.today()
            self.startdate = _ds.replace(hour=int(_s[0:2]), minute=int(_s[3:5]))
            self.enddate = _ds.replace(hour=int(_e[0:2]), minute=int(_e[3:5]))
            if self.enddate < self.startdate: self.enddate += datetime.timedelta(days=1)
        except IndexError:
            pass
        try:
            self.genre = re.compile('<span class="info">(.+?)</span>', re.DOTALL).findall(content)[1].split(', ')[1].strip()
            self.runtime = int((self.enddate - self.startdate).total_seconds())
        except (IndexError, ValueError):
            pass
        try:
            self.thumb = 'https:' + re.compile('srcset="(.+?)"', re.DOTALL).findall(content)[0].split(', ')[2].split()[0]
        except (IndexError, TypeError):
            self.thumb = os.path.join(ADDON_PATH, 'resources', 'lib', 'media', self.icon)
