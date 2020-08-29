import os
import unittest

from tests.utils import test_write, test_read
from tradssat import ExpFile
from cassavapy import set_experiment

rsrcs = os.path.join(os.path.split(__file__)[0], 'mock')
input_classes = [ExpFile]


# Inputs must be read and written
class TestInputs(unittest.TestCase):

    def test_cassavapy(self):
        set_experiment("tests/mock/test")
        set_experiment("tests/mock/test2", "d60.csv")

        os.system('copy C:\DSSAT47\Cassava\TEST1980.CSX C:\\Users\\flsco\Desktop\projetos\CassavaPy\\tests\mock\TEST1980.CSX')
        os.system('copy C:\DSSAT47\Cassava\TEST1981.CSX C:\\Users\\flsco\Desktop\projetos\CassavaPy\\tests\mock\TEST1981.CSX')
        os.system('copy C:\DSSAT47\Cassava\TEST1982.CSX C:\\Users\\flsco\Desktop\projetos\CassavaPy\\tests\mock\TEST1982.CSX')
        os.system('copy C:\DSSAT47\Cassava\TEST1983.CSX C:\\Users\\flsco\Desktop\projetos\CassavaPy\\tests\mock\TEST1983.CSX')
        
    def test_read(self):
        for inp_class in input_classes:
            with self.subTest(inp_class.__name__):
                test_read(inp_class, folder=rsrcs, testcase=self)

        os.remove("tests/mock/TEST1980.CSX")
        os.remove("tests/mock/TEST1981.CSX")
        os.remove("tests/mock/TEST1982.CSX")
        os.remove("tests/mock/TEST1983.CSX")

if __name__ == "__main__":
    unittest.main()