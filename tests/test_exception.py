from src import logger
from src.exception import CustomException
import unittest,sys
import os,re

def find_string_in_bracket(text):
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, text)
    return matches

class TestException(unittest.TestCase):
    def test_custom_exception(self):
        try :
            1/0
        except Exception as err :
            try : 
                raise CustomException(err, sys)
            except :
                with open(logger.LOG_PATH, "r") as f:
                    data = f.read()
                    self.assertEqual(str(err), find_string_in_bracket(data)[-1])
            


if __name__ == '__main__':
    unittest.main()