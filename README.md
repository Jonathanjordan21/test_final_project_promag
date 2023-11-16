# final_project_promag
Final Project Data Academy Team Promag

# Unit Test
Change {test_name} to the python test file name. <br><br>

run multiple test cases in the folder
```bash
python -m unittest -v tests/{test_name}.py
```

run a single test case function 
```bash
python -m unittest -v tests.{test_name}.{TestClassName}.{test_method_name}
```

<br>
Add several logs in the python file using logger
```python
from src.logger import logging

logging.info("{custom info}")
```

For Errors / Exceptions, use CustomException class in exception
```python
from src.exception import CustomException

try :
    1/0 # some error / bug in program
except Exception as err :
    raise CustomException(err, sys) # CustomException will automatically store the error information inside logs folder
```

The logs will be stored in logs folder. The logs folder is not pushed to github as it contains sensitive information

