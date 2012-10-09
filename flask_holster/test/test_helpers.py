from unittest import TestCase

from flask_holster.helpers import lift

class TestLift(TestCase):

    def test_lift_basic(self):
        def lifted(x):
            return x + 1

        def source():
            return 1

        l = lift(lifted)(source)

        self.assertEqual(l(), 2)
