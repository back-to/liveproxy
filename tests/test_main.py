import unittest

from liveproxy.main import check_streamlink_version


class TestMain(unittest.TestCase):
    def test_check_streamlink_version(self):
        wrong_version_is_false = [
            '0.12.1+53.g7ff1ce8',
            '0.12.1+60.g7ff1ce8',
            '0.13.0',
        ]
        for _s_verion in wrong_version_is_false:
            self.assertFalse(check_streamlink_version(_s_verion))

        wrong_version_is_true = [
            '0.11.0',
            '0.12.1',
            '0.12.1+11.g7ff1ce8',
        ]
        for _s_verion in wrong_version_is_true:
            self.assertTrue(check_streamlink_version(_s_verion))
