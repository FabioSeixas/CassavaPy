import classes
import unittest
from datetime import date
import numpy as np


class Test_basic_FileX_phf(unittest.TestCase):
    ''' 3 datas de plantio
        3 datas de colheita
        design "phf", sem irrigação'''

    def setUp(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", "phf")
        self.filex.p_from = date.fromisoformat('1992-12-30')

        self.filex.set_planting(n_plant=3,
                                p_from='1992-12-30',
                                p_by=25)

        self.filex.set_harvest(n_harvest=3,
                               h_from='1993-01-01',
                               h_by=60)

    def test_planting(self):
        expected = ["92365", "93024", "93049"]
        self.assertEqual(self.filex._planting, expected)

    def test_harvest(self):
        expected = ["93001", "93061", "93121"]
        self.assertEqual(self.filex._harvest, expected)

    def test_tratmatrix(self):
        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 0],
                    ["BA002", 2, 2, 0],
                    ["BA003", 3, 3, 0]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)


class Test_basic_FileX_NULL(unittest.TestCase):
    ''' 4 datas de plantio
        3 datas de colheita
        design: "NULL"
        sem irrigação. '''

    def setUp(self):

        self.filex = classes.FileX("cruz", "CRUZ9101")
        self.filex.p_from = date.fromisoformat('1992-12-30')

        self.filex.set_planting(n_plant=4,
                                p_from='1992-12-30',
                                p_by=25)

        self.filex.set_harvest(n_harvest=3,
                               h_from='1993-01-01',
                               h_by=60)

    def test_planting(self):
        expected = ["92365", "93024", "93049", "93074"]
        self.assertEqual(self.filex._planting, expected)

    def test_harvest(self):
        expected = ["93001", "93061", "93121"]
        self.assertEqual(self.filex._harvest, expected)

    def test_tratmatrix(self):
        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 0],
                    ["BA002", 1, 2, 0],
                    ["BA003", 1, 3, 0],
                    ["BA004", 2, 1, 0],
                    ["BA005", 2, 2, 0],
                    ["BA006", 2, 3, 0],
                    ["BA007", 3, 1, 0],
                    ["BA008", 3, 2, 0],
                    ["BA009", 3, 3, 0],
                    ["BA010", 4, 1, 0],
                    ["BA011", 4, 2, 0],
                    ["BA012", 4, 3, 0]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)


class Test_basic_FileX_phf_irf(unittest.TestCase):
    '''3 datas de plantio
       3 datas de colheita
       design: "phf" e "irf"

       '''

    def setUp(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", ["phf", "irf"])

        self.filex.p_from = date.fromisoformat('1992-12-30')

        self.filex.set_planting(n_plant=3,
                                p_from='1992-12-30',
                                p_by=25)

        self.filex.set_harvest(n_harvest=3,
                               h_from='1993-01-01',
                               h_by=60)

    def test_irrigation_one_lamina(self):
        self.filex.set_irrigation(n_irrig=5,
                                  from_irrig=0,
                                  by_irrig=60,
                                  laminas=15)  # Same water depth to all irrigation events

        expected = [[["92365", "15"],
                     ["93059", "15"],
                     ["93119", "15"],
                     ["93179", "15"],
                     ["93239", "15"]]]

        np.testing.assert_equal(self.filex._irrig, expected)

    def test_irrigation_more_laminas(self):

        self.filex.set_irrigation(n_irrig=5,
                                  from_irrig=0,
                                  by_irrig=60,
                                  laminas=[10, 20, 40, 50, 10])

        expected = [[["92365", "10"],
                     ["93059", "20"],
                     ["93119", "40"],
                     ["93179", "50"],
                     ["93239", "10"]]]

        np.testing.assert_equal(self.filex._irrig, expected)

    def test_irrigation_dont_match(self):
        '''n_irrig = 5
           len(laminas) = 4.
           '''
        with self.assertRaises(ValueError):

            self.filex.set_irrigation(n_irrig=5,
                                      from_irrig=0,
                                      by_irrig=60,
                                      laminas=[10, 20, 40, 50])

    def test_tratmatrix_with_no_regdict(self):
        self.filex.set_irrigation(n_irrig=5,
                                  from_irrig=0,
                                  by_irrig=60,
                                  laminas=[10, 20, 40, 50, 10],
                                  reg_dict="NULL")  # "NULL" is the Default

        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 1],
                    ["BA002", 2, 2, 1],
                    ["BA003", 3, 3, 1]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)

    def test_tratmatrix_with_regdict(self):
        self.filex.set_irrigation(n_irrig=5,
                                  from_irrig=0,
                                  by_irrig=60,
                                  laminas=[10, 20, 40, 50, 10],
                                  reg_dict=[1, 3])  # Apply the irrigation to treatments one and three

        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 1],
                    ["BA002", 2, 2, 0],
                    ["BA003", 3, 3, 1]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)

    def test_tratmatrix_with_regdict_out_of_range(self):
        self.filex.set_irrigation(n_irrig=5,
                                  from_irrig=0,
                                  by_irrig=60,
                                  laminas=[10, 20, 40, 50, 10],
                                  reg_dict=[1, 3, 5, 10, 15])

        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 1],
                    ["BA002", 2, 2, 0],
                    ["BA003", 3, 3, 1]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)

    def test_tratmatrix_with_regdict_out_of_range_2(self):
        self.filex.set_irrigation(n_irrig=5,
                                  from_irrig=0,
                                  by_irrig=60,
                                  laminas=[10, 20, 40, 50, 10],
                                  reg_dict=[5, 10, 15])

        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 0],
                    ["BA002", 2, 2, 0],
                    ["BA003", 3, 3, 0]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)

    def test_tratmatrix_with_regdict_dictionary_ERROR(self):
        self.filex.set_irrigation(n_irrig=5,
                                  from_irrig=0,
                                  by_irrig=60,
                                  laminas=[10, 20, 40, 50, 10],
                                  reg_dict={1: [1, 2, 3]})

        with self.assertRaises(TypeError):
            self.filex.set_tratmatrix("BA")


class Test_basic_FileX_phf_irnf(unittest.TestCase):
    '''3 datas de plantio
       3 datas de colheita
       design: "phf" e "irnf"

       '''

    def setUp(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", ["phf", "irnf"])

        self.filex.p_from = date.fromisoformat('1992-12-30')

        self.filex.set_planting(n_plant=3,
                                p_from='1992-12-30',
                                p_by=25)

        self.filex.set_harvest(n_harvest=3,
                               h_from='1993-01-01',
                               h_by=60)

        self.reg = [[0, 5, 10, 15, 20, 25, 30],
                    [0, 10, 20, 30, 40],
                    [10, 20, 30, 40, 50, 60]]

    def test_irrigation_one_lamina(self):
        self.filex.set_irrigation(reg=self.reg,
                                  laminas=[11, 22, 33],
                                  reg_dict={1: 3, 2: 1, 3: 2})

        expected = [[["92365", "11"], ["93004", "11"], ["93009", "11"], ["93014", "11"], ["93019", "11"], ["93024", "11"], ["93029", "11"]],
                    [["92365", "22"], ["93009", "22"], ["93019", "22"], ["93029", "22"], ["93039", "22"]],
                    [["93009", "33"], ["93019", "33"], ["93029", "33"], ["93039", "33"], ["93049", "33"], ["93059", "33"]]]

        np.testing.assert_equal(self.filex._irrig, expected)

    def test_irrigation_more_laminas(self):
        self.filex.set_irrigation(reg=self.reg,
                                  laminas=[[10, 11, 10, 11, 10, 11, 12],
                                           [5, 6, 7, 5, 6],
                                           [10, 12, 11, 10, 14, 13]],
                                  reg_dict={1: 3, 2: 1, 3: 2})

        expected = [[["92365", "10"], ["93004", "11"], ["93009", "10"], ["93014", "11"], ["93019", "10"], ["93024", "11"], ["93029", "12"]],
                    [["92365", "5"], ["93009", "6"], ["93019", "7"], ["93029", "5"], ["93039", "6"]],
                    [["93009", "10"], ["93019", "12"], ["93029", "11"], ["93039", "10"], ["93049", "14"], ["93059", "13"]]]

        np.testing.assert_equal(self.filex._irrig, expected)

    def test_irrigation_more_laminas_2(self):
        self.filex.set_irrigation(reg=self.reg,
                                  laminas=[10,
                                           [5],
                                           [10, 12, 11, 10, 14, 13]],
                                  reg_dict={1: 3, 2: 1, 3: 2})

        expected = [[["92365", "10"], ["93004", "10"], ["93009", "10"], ["93014", "10"], ["93019", "10"], ["93024", "10"], ["93029", "10"]],
                    [["92365", "5"], ["93009", "5"], ["93019", "5"], ["93029", "5"], ["93039", "5"]],
                    [["93009", "10"], ["93019", "12"], ["93029", "11"], ["93039", "10"], ["93049", "14"], ["93059", "13"]]]

        np.testing.assert_equal(self.filex._irrig, expected)

    def test_irrigation_more_laminas_dont_match(self):

        with self.assertRaises(ValueError):
            self.filex.set_irrigation(reg=self.reg,
                                      laminas=[[10, 11, 10, 11, 10, 11, 12],
                                               [5, 6, 7, 5, 6],
                                               [10, 12, 11, 10, 14, 13, 15]],  # One more than 'reg'
                                      reg_dict={1: 3, 2: 1, 3: 2})

    def test_irrigation_reg_dict_ERROR(self):

        with self.assertRaises(AssertionError):
            self.filex.set_irrigation(reg=self.reg,
                                      laminas=[[10, 11, 10, 11, 10, 11, 12],
                                               [5, 6, 7, 5, 6],
                                               [10, 12, 11, 10, 14, 13]],
                                      reg_dict={4: 3, 2: 1, 3: 2})

    def test_irrigation_tratmatrix(self):
        self.filex.set_irrigation(reg=self.reg,
                                  laminas=[[10, 11, 10, 11, 10, 11, 12],
                                           [5, 6, 7, 5, 6],
                                           [10, 12, 11, 10, 14, 13]],
                                  reg_dict={1: 3, 2: 1, 3: 2})

        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 2],
                    ["BA002", 2, 2, 3],
                    ["BA003", 3, 3, 1]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)

    def test_irrigation_tratmatrix_dict_missing_trat(self):
        self.filex.set_irrigation(reg=self.reg,
                                  laminas=[[10, 11, 10, 11, 10, 11, 12],
                                           [5, 6, 7, 5, 6],
                                           [10, 12, 11, 10, 14, 13]],
                                  reg_dict={1: 3, 2: 1})

        self.filex.set_tratmatrix("BA")

        expected = [["BA001", 1, 1, 2],
                    ["BA002", 2, 2, 0],
                    ["BA003", 3, 3, 1]]

        np.testing.assert_equal(self.filex._tratmatrix,
                                expected)


if __name__ == "__main__":
    unittest.main()
