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

    def test_lift_name(self):
        """
        ``lift()`` correctly preserves names of things it has wrapped.
        """

        def named(none):
            pass

        def dummy(none):
            pass

        l = lift(dummy)(named)

        self.assertEqual(l.__name__, "named")

    def test_lift_name_inner(self):
        """
        ``lift()`` correctly preserves names of things it has wrapped, even on
        the inner level.
        """

        def named(none):
            pass

        l = lift(named)

        self.assertEqual(l.__name__, "named")
