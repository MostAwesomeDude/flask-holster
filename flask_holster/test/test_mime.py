from unittest import TestCase

from flask_holster.mime import MIME

class TestMIMEMatch(TestCase):

    def test_mime_match_exact(self):
        s = "text/html"
        expected = 1.0
        mime = MIME(s).match("text/html")
        self.assertEqual(mime, expected)
