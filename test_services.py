"""Integration checks for the locally running public demo services (real requests)."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
NODE=ROOT/'server/database/app.js'
SENTIMENT=ROOT/'server/microservices/app.py'

class ServicesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dealer=subprocess.Popen(['node',str(NODE)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                                    env={**os.environ,'DEALER_PORT':'13030'})
        cls.sentiment=subprocess.Popen([sys.executable,str(SENTIMENT)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                                    env={**os.environ,'SENTIMENT_PORT':'15050'})
        for _ in range(40):
            try:
                if cls.get('http://127.0.0.1:13030/health')['status']=='ok' and cls.get('http://127.0.0.1:15050/health')['status']=='ok':
                    return
            except Exception:time.sleep(.1)
        raise RuntimeError('One or more API servers failed to start')
    @classmethod
    def tearDownClass(cls):
        for p in (cls.dealer,cls.sentiment):
            p.terminate()
            try:p.wait(timeout=3)
            except subprocess.TimeoutExpired:p.kill()
    @staticmethod
    def get(url):
        with urlopen(url,timeout=2) as r:return json.load(r)
    def test_all_50_dealers(self):
        response=self.get('http://127.0.0.1:13030/fetchDealers')
        self.assertEqual(len(response),50)
        self.assertTrue(all({'id','city','state','address','zip','lat','long','short_name','full_name'}<=set(d) for d in response))
    def test_dealer_by_id_and_state(self):
        self.assertEqual(self.get('http://127.0.0.1:13030/fetchDealer/1')[0]['id'],1)
        kansas=self.get('http://127.0.0.1:13030/fetchDealers/Kansas')
        self.assertTrue(kansas)
        self.assertTrue(all(x['state']=='Kansas' for x in kansas))
    def test_reviews(self):
        reviews=self.get('http://127.0.0.1:13030/fetchReviews/dealer/1')
        self.assertTrue(reviews)
        self.assertEqual(reviews[0]['dealership'],1)
    def test_sentiment(self):
        result=self.get('http://127.0.0.1:15050/analyze/Fantastic%20services')
        self.assertEqual(result['sentiment'],'positive')
    def test_missing_path(self):
        from urllib.error import HTTPError
        with self.assertRaises(HTTPError) as ctx:self.get('http://127.0.0.1:13030/missing')
        self.assertEqual(ctx.exception.code,404)

if __name__=='__main__':unittest.main()
