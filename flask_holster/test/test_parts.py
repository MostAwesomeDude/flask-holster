from unittest import TestCase

from flask_holster.parts import extend

class TestExtend(TestCase):

    def test_extend_standard(self):
        i = "/standard"
        o = "/standard.<ext>"
        self.assertEqual(extend(i), o)

    def test_extend_params(self):
        i = "/<params>"
        o = "/<params>.<ext>"
        self.assertEqual(extend(i), o)

    def test_extend_root(self):
        i = "/"
        o = "/.<ext>"
        self.assertEqual(extend(i), o)

    def test_extend_directory(self):
        i = "/dir/"
        o = "/dir.<ext>/"
        self.assertEqual(extend(i), o)
