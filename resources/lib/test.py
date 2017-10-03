import os
import sys
import re
import unittest

filename = os.path.dirname( os.path.realpath(__file__) )
sys.path.append( os.path.join ( filename, '..', '..', '..','script.module.stream.resolver','lib') )
sys.path.append( os.path.join ( filename, '..', '..', '..','script.module.demjson','lib') )
sys.path.append( os.path.join ( filename , '..','..', '..','script.module.stream.resolver','lib','contentprovider') )
sys.path.append( os.path.join ( filename , '..','..', '..','script.module.stream.resolver','lib','server') )
import provider
import util
import joj

class TestJoj(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.provider = joj.JojContentProvider()

    def test_listing_base(self):
        for base_url in joj.BASE_URL.values():
            url = base_url + '/archiv-filter'
            res = self.provider.list_base(url)
            self.assertTrue(len(res) > 0, 'no shows from "%s" url!'% url)
            print "'%s' - listed %d shows" %(url, len(res))

    def _test_list_series(self, url):
        res = self.provider.list_show(url, list_series=True)
        self.assertTrue(len(res) > 0, 'no series from "%s" url!'% url)
        print "'%s' - listed %d series" %(url, len(res))
        serie_pattern = re.compile(r'^\d+')
        for i in res:
            serie_match = serie_pattern.search(i['title'])
            self.assertIsNotNone(serie_match, '"%r" looks to be not a serie item!'%i)

    def _test_list_episodes(self, url):
        res = self.provider.list_show(url, list_episodes=True)
        self.assertTrue(len(res) > 0, 'no episodes from "%s" url!'% url)
        print "'%s' - listed %d episodes" %(url, len(res))

    def test_list_series(self):
        urls = ['http://www.joj.sk/15-min-kuchar/archiv/2016-04-10-15-minut-kuchar-premiera',
                'http://plus.joj.sk/ako-som-prezil/epizody/2015-06-20-ako-som-prezil']
        for url in urls:
            self._test_list_series(url)

    def test_list_episodes_no_episodes_table(self):
        urls = ['http://www.joj.sk/15-min-kuchar/archiv/2016-04-10-15-minut-kuchar-premiera']
        for url in urls:
            self._test_list_episodes(url)

    def test_list_episodes_with_episodes_table_season_episode(self):
        urls = ['http://plus.joj.sk/ako-som-prezil/epizody/2015-06-20-ako-som-prezil',
                'http://divokekone.joj.sk/archiv/2016-01-08-divoke-kone-ii-finale-serialu-premiera']
        for url in urls:
            self._test_list_episodes(url)


    def test_list_episodes_with_episodes_table_date(self):
        urls = ['http://velkenoviny.joj.sk/archiv/2016-07-01-noviny-tv-joj']
        for url in urls:
            self._test_list_episodes(url)

    def test_vod_resolving(self):
        urls = ['https://www.joj.sk/inkognito/archiv/2017-09-28-inkognito']
        for url in urls:
            res = self.provider.resolve({'url':url})
            print "'%s' - resolved %d videos" %(url, len(res))

if __name__ == "__main__":
    unittest.main()
