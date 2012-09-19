from unittest import TestCase

from flask_holster.mime import Accept, MIME

class TestMIMEPlain(TestCase):

    def test_mime_plain(self):
        s = "text/xml"
        mime = MIME.from_string(s)
        self.assertEqual(mime.plain(), s)

class TestMIMEMatch(TestCase):

    def test_mime_match_exact(self):
        mime1 = MIME("text", "html", 1.0)
        mime2 = MIME("text", "html", 1.0)
        result = mime1.match(mime2)
        self.assertAlmostEqual(result.params["q"], 1.0)
        self.assertEqual(result.plain(), "text/html")

    def test_mime_match_medium_q(self):
        mime1 = MIME("text", "html", 0.8)
        mime2 = MIME("text", "html", 1.0)
        result = mime1.match(mime2)
        self.assertAlmostEqual(result.params["q"], 0.8)
        self.assertEqual(result.plain(), "text/html")

    def test_mime_match_wildcard(self):
        mime1 = MIME("text", "*", 1.0)
        mime2 = MIME("text", "html", 1.0)
        result = mime1.match(mime2)
        self.assertAlmostEqual(result.params["q"], 1.0)
        self.assertEqual(result.plain(), "text/html")

class TestAcceptBest(TestCase):

    fx_accept_general = ("text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8")

    def test_accept_plaintext_fx(self):
        """
        Firefox will accept text/plain if necessary.
        """

        accept1 = Accept(self.fx_accept_general)
        accept2 = Accept("text/plain")

        result = accept1.best(accept2).plain()
        expected = "text/plain"
        self.assertEqual(result, expected)

    def test_accept_html_fx(self):
        """
        Firefox accepts text/html.
        """

        accept1 = Accept(self.fx_accept_general)
        accept2 = Accept("text/html")

        result = accept1.best(accept2).plain()
        expected = "text/html"
        self.assertEqual(result, expected)

    def test_accept_html_fx_multiple(self):
        """
        Firefox prefers text/html over text/plain.
        """

        accept1 = Accept(self.fx_accept_general)
        accept2 = Accept("text/html,text/plain")

        result = accept1.best(accept2).plain()
        expected = "text/html"
        self.assertEqual(result, expected)
