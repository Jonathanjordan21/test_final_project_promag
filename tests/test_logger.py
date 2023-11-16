from src.logger import logging
import unittest

class TestLogger(unittest.TestCase):
    def test_logging_info(self):
        logging.info("[TEST]")


if __name__ == '__main__':
    unittest.main()