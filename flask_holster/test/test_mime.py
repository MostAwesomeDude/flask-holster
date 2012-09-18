from unittest import TestCase

from flask_holster.mime import MIME

class TestMIMEMatch(TestCase):

    def test_mime_match_exact(self):
        s = "text/html"
        expected = 1.0
        mime = MIME(s).match("text/html")
        self.assertAlmostEqual(mime, expected)

    def test_mime_match_medium_q(self):
        s = "text/plain;q=0.8"
        expected = 0.8
        mime = MIME(s).match("text/plain")
        self.assertAlmostEqual(mime, expected)

    def test_mime_match_wildcard(self):
        s = "text/*"
        expected = 1.0
        mime = MIME(s).match("text/plain")
        self.assertAlmostEqual(mime, expected)
