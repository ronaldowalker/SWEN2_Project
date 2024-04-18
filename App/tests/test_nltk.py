import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
from App.controllers import (
    analyze_sentiment,
    analyze_text
)

class NLTKUnitTests(unittest.TestCase):

    def test_analyze_text(self):
        processed_text = analyze_text("This is amazing")
        assert processed_text is not None

    def test_analyze_sentiment(self):
        scores = analyze_sentiment("This is amazing")
        assert scores is not None
        if scores is not None:
            self.assertDictEqual(scores, {
                'neg': 0.0,
                'neu': 0.0,
                'pos': 1.0,
                'compound': 0.5859
            })