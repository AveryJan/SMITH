"""Lightweight sentiment endpoint with required /analyze/<text> interface.
For production-grade VADER sentiment, replace this keyword-based demo with the
IBM starter's NLTK SentimentIntensityAnalyzer implementation.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

POSITIVE = {'fantastic','excellent','great','amazing','good','friendly','helpful','love','wonderful'}
NEGATIVE = {'terrible','awful','bad','horrible','poor','worst','rude','disappointing'}

def analyze(text):
    words = set(''.join(c.lower() if c.isalpha() else ' ' for c in text).split())
    score = len(words & POSITIVE) - len(words & NEGATIVE)
    return 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/health':
            response={'status':'ok'}
        elif self.path.startswith('/analyze/'):
            text=unquote(self.path[len('/analyze/'):]).split('?')[0]
            response={'text':text,'sentiment':analyze(text)}
        else:
            self.send_error(404)
            return
        blob=json.dumps(response).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

if __name__ == '__main__':
    port=int(os.environ.get('SENTIMENT_PORT','5050'))
    print('Sentiment service listening on',port,flush=True)
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
