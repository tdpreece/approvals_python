import unittest

import six


if six.PY2:
    print('Runnging Python2')
else:
    print('Not running Python2')


class Test(unittest.TestCase):
    def test(self):
        pass
