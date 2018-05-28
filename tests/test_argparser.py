import unittest

from liveproxy.argparser import ip_address


class TestArgparser(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            '127.0.0.1',
            '0.0.0.0',
        ]
        for ip in should_match:
            self.assertTrue(ip_address(ip))

        should_not_match = [
            'abc',
            '123abc',
        ]
        for ip in should_not_match:
            with self.assertRaises(ValueError):
                ip_address(ip)
