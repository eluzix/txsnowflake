import unittest, sys
sys.path.append('../txsnowflake')
from txsnowflake import SnowflakeServiceHandler

__author__ = 'uzix'

class SnowflakeTest(unittest.TestCase):

    def test_100_basic(self):
        handler = SnowflakeServiceHandler(0, 0)
        ret1 = handler.get_id('me')
        ret2 = handler.get_id('me')

        self.assertGreater(ret1, 0)
        self.assertGreater(ret2, 0)
        self.assertGreater(ret2, ret1)

    def test_101_multiple(self):
        handler1 = SnowflakeServiceHandler(0, 0)
        handler2 = SnowflakeServiceHandler(1, 0)
        ret1 = handler1.get_id('me')
        ret2 = handler2.get_id('me')

        self.assertGreater(ret1, 0)
        self.assertGreater(ret2, 0)
        self.assertNotEqual(ret2, ret1)


    def test_102_long_run(self):
        handler = SnowflakeServiceHandler(0, 0)
        ret = set()
        total_runs = 20000

        for i in xrange(total_runs):
            ret.add(handler.get_id('me'))

        self.assertFalse(None in ret)
        self.assertEquals(len(ret), total_runs)

if __name__ == '__main__':
    unittest.main()
