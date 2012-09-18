from unittest import TestCase

from flask_holster.mime import Accept, MIME

class TestMIMEPlain(TestCase):

    def test_mime_plain(self):
        s = "text/xml"
        mime = MIME(s)
        self.assertEqual(mime.plain(), s)

class TestMIMEMatch(TestCase):

    def test_mime_match_exact(self):
        s = "text/html"
        expected = s, 1.0
        mime = MIME(s).match("text/html")
        self.assertAlmostEqual(mime, expected)

    def test_mime_match_medium_q(self):
        s = "text/plain;q=0.8"
        expected = "text/plain", 0.8
        mime = MIME(s).match("text/plain")
        self.assertAlmostEqual(mime, expected)

    def test_mime_match_wildcard(self):
        s = "text/*"
        expected = "text/plain", 1.0
        mime = MIME(s).match("text/plain")
        self.assertAlmostEqual(mime, expected)

class TestAcceptBest(TestCase):

    def test_accept_plaintext_fx(self):
        """
        Firefox will accept text/plain if necessary.
        """

        accepted = ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                "*/*;q=0.8")
        expected = "text/plain"
        t = Accept(accepted).best("text/plain")
        self.assertEqual(t, expected)

    def test_accept_html_fx(self):
        """
        Firefox prefers text/html.
        """

        accepted = ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                "*/*;q=0.8")
        expected = "text/html"
        t = Accept(accepted).best("text/html")
        self.assertEqual(t, expected)
