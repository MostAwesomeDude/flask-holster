from unittest import TestCase

from werkzeug.datastructures import MIMEAccept

from flask_holster.mime import preferring


class TestPreferring(TestCase):

    def test_preferring_ahead(self):
        t = "text/plain"
        a = MIMEAccept([("text/plain", 1), ("text/xml", 1)])
        a = preferring(t, a)
        self.assertEqual(a.best, t)

    def test_preferring_behind(self):
        t = "text/plain"
        a = MIMEAccept([("text/xml", 1), ("text/plain", 1)])
        a = preferring(t, a)
        self.assertEqual(a.best, t)

    def test_preferring_quality(self):
        t = "text/plain"
        a = MIMEAccept([("text/plain", 0.9), ("text/xml", 1)])
        a = preferring(t, a)
        self.assertEqual(a.best, t)

    def test_preferring_quality_behind(self):
        t = "text/plain"
        a = MIMEAccept([("text/xml", 1), ("text/plain", 0.9)])
        a = preferring(t, a)
        self.assertEqual(a.best, t)

    def test_preferring_new(self):
        t = "text/plain"
        a = MIMEAccept([("text/xml", 1), ("image/png", 0.9)])
        a = preferring(t, a)
        self.assertEqual(a.best, t)
