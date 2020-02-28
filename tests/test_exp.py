import classes
import unittest
from datetime import date
import numpy as np

# DEPOS: Adicionar testes de 'raiseError'!


class Test(unittest.TestCase):

    def setUp(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", "irf")
        self.filex.p_from = date.fromisoformat('1992-12-30')

    def test_planting(self):
        self.n_plant = 3
        self.p_from = '1992-12-30'
        self.p_by = 25

        self.filex.set_planting(self.n_plant,
                                self.p_from, self.p_by)

        self.assertEqual(self.filex._planting, ["92365", "93024", "93049"])

    def test_harvest(self):
        self.n_harvest = 3
        self.h_from = '1993-01-01'
        self.h_by = 60

        self.filex.set_harvest(self.n_harvest,
                               self.h_from, self.h_by)

        self.assertEqual(self.filex._harvest, ["93001", "93061", "93121"])

    def test_irrigation_irf(self):

        n_irrig = 5
        from_irrig = 0
        by_irrig = 60

        laminas = [10, 20, 40, 50, 10]

        self.filex.set_irrigation(n_irrig=n_irrig, from_irrig=from_irrig, by_irrig=by_irrig, laminas=laminas)

        np.testing.assert_equal(self.filex._irrig, [["92365", "10"], ["93059", "20"], ["93119", "40"], ["93179", "50"], ["93239", "10"]])

        n_irrig = 5
        from_irrig = 0
        by_irrig = 60

        laminas = 10

        self.filex.set_irrigation(n_irrig=n_irrig, from_irrig=from_irrig, by_irrig=by_irrig, laminas=laminas)

        np.testing.assert_equal(self.filex._irrig, [["92365", "10"], ["93059", "10"], ["93119", "10"], ["93179", "10"], ["93239", "10"]])

    def test_irrigation_irnf(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", "irnf")
        self.filex.p_from = date.fromisoformat('1992-12-30')

        reg = [[0, 4, 6, 10, 11],
               [3, 5, 7, 9],
               [1, 5, 21]]

        laminas = [5,
                   [10, 20, 30, 40],
                   7]

        self.filex.set_irrigation(reg=reg, laminas=laminas)

        np.testing.assert_equal(self.filex._irrig,
                                [[["92365", "5"],
                                  ["93003", "5"],
                                  ["93005", "5"],
                                  ["93009", "5"],
                                  ["93010", "5"]],
                                 [["93002", "10"],
                                  ["93004", "20"],
                                  ["93006", "30"],
                                  ["93008", "40"]],
                                 [["92366", "7"],
                                  ["93004", "7"],
                                  ["93020", "7"]]])

    def test_plantharvest_fix(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", 'phf')

        # Planting
        self.n_plant = 3
        self.p_from = '1992-12-30'
        self.p_by = 25

        self.filex.set_planting(self.n_plant,
                                self.p_from, self.p_by)

        # Harvest
        self.n_harvest = 3
        self.h_from = '1993-01-01'
        self.h_by = 60

        self.filex.set_harvest(self.n_harvest,
                               self.h_from, self.h_by)

        # Test
        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 0],
                                 ["BA002", 2, 2, 0],
                                 ["BA003", 3, 3, 0]])

    def test_plantharvest_notfix(self):
        self.filex = classes.FileX("cruz", "CRUZ9101")

        # Planting
        self.n_plant = 3
        self.p_from = '1992-12-30'
        self.p_by = 25

        self.filex.set_planting(self.n_plant,
                                self.p_from, self.p_by)

        # Harvest
        self.n_harvest = 3
        self.h_from = '1993-01-01'
        self.h_by = 60

        self.filex.set_harvest(self.n_harvest,
                               self.h_from, self.h_by)

        # Test
        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 0],
                                 ["BA002", 1, 2, 0],
                                 ["BA003", 1, 3, 0],
                                 ["BA004", 2, 1, 0],
                                 ["BA005", 2, 2, 0],
                                 ["BA006", 2, 3, 0],
                                 ["BA007", 3, 1, 0],
                                 ["BA008", 3, 2, 0],
                                 ["BA009", 3, 3, 0]])

    def test_set_tratmatrix(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", "irf")
        self.filex.p_from = date.fromisoformat('1992-12-30')

        # Planting
        self.n_plant = 2
        self.p_from = '1992-12-30'
        self.p_by = 25

        self.filex.set_planting(self.n_plant,
                                self.p_from, self.p_by)

        # Harvest
        self.n_harvest = 3
        self.h_from = '1993-01-01'
        self.h_by = 60

        self.filex.set_harvest(self.n_harvest,
                               self.h_from, self.h_by)

        # Irrigation
        n_irrig = 5
        from_irrig = 0
        by_irrig = 60

        laminas = [10, 20, 40, 50, 10]

        self.filex.set_irrigation(n_irrig=n_irrig, from_irrig=from_irrig, by_irrig=by_irrig, laminas=laminas)

        # Test 1
        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 1],
                                 ["BA002", 1, 2, 1],
                                 ["BA003", 1, 3, 1],
                                 ["BA004", 2, 1, 1],
                                 ["BA005", 2, 2, 1],
                                 ["BA006", 2, 3, 1]])

        # Teste 1.1
        self.filex.set_irrigation(n_irrig=n_irrig, from_irrig=from_irrig, by_irrig=by_irrig, laminas=laminas, reg_dict=[1, 6])

        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 1],
                                 ["BA002", 1, 2, 0],
                                 ["BA003", 1, 3, 0],
                                 ["BA004", 2, 1, 0],
                                 ["BA005", 2, 2, 0],
                                 ["BA006", 2, 3, 1]])

        # Test 2
        self.filex = classes.FileX("cruz", "CRUZ9101", ["phf", "irf"])
        self.filex.p_from = date.fromisoformat('1992-12-30')

        self.n_plant = 3

        self.filex.set_planting(self.n_plant,
                                self.p_from, self.p_by)

        self.filex.set_harvest(self.n_harvest,
                               self.h_from, self.h_by)

        self.filex.set_irrigation(n_irrig=n_irrig, from_irrig=from_irrig, by_irrig=by_irrig, laminas=laminas)

        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 1],
                                 ["BA002", 2, 2, 1],
                                 ["BA003", 3, 3, 1]])

        # Test 3
        self.filex.set_irrigation(n_irrig=n_irrig, from_irrig=from_irrig, by_irrig=by_irrig, laminas=laminas, reg_dict=[1, 3])

        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 1],
                                 ["BA002", 2, 2, 0],
                                 ["BA003", 3, 3, 1]])

        # Teste 4
        self.filex.set_irrigation(n_irrig=n_irrig, from_irrig=from_irrig, by_irrig=by_irrig, laminas=laminas, reg_dict=[])

        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 0],
                                 ["BA002", 2, 2, 0],
                                 ["BA003", 3, 3, 0]])

    def test_error(self):

        self.assertRaises(AttributeError, classes.FileX, "cruz", "CRUZ9101", ["phf", "irf", "irnf"])

    def test_set_tratmatrix_irnf(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", "irnf")
        self.filex.p_from = date.fromisoformat('1992-12-30')

        # Planting
        self.n_plant = 2
        self.p_from = '1992-12-30'
        self.p_by = 25

        self.filex.set_planting(self.n_plant,
                                self.p_from, self.p_by)

        # Harvest
        self.n_harvest = 3
        self.h_from = '1993-01-01'
        self.h_by = 60

        self.filex.set_harvest(self.n_harvest,
                               self.h_from, self.h_by)

        laminas = [10, 20, 40]

        reg = [[0, 4, 6, 10, 21, 50, 100, 500],
               [3, 5, 7, 5],
               [1, 5, 20]]

        self.filex.set_irrigation(reg=reg, laminas=laminas, reg_dict={1: 3, 2: 1, 3: [6, 4]})

        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 2],
                                 ["BA002", 1, 2, 0],
                                 ["BA003", 1, 3, 1],
                                 ["BA004", 2, 1, 3],
                                 ["BA005", 2, 2, 0],
                                 ["BA006", 2, 3, 3]])

    def test_tratmatrix_rainfed(self):
        self.filex = classes.FileX("cruz", "CRUZ9101")
        self.filex.p_from = date.fromisoformat('1992-12-30')

        # Planting
        self.n_plant = 2
        self.p_from = '1992-12-30'
        self.p_by = 25

        self.filex.set_planting(self.n_plant,
                                self.p_from, self.p_by)

        # Harvest
        self.n_harvest = 2
        self.h_from = '1993-01-01'
        self.h_by = 60

        self.filex.set_harvest(self.n_harvest,
                               self.h_from, self.h_by)

        self.filex.set_tratmatrix("BA")

        np.testing.assert_equal(self.filex._tratmatrix,
                                [["BA001", 1, 1, 0],
                                 ["BA002", 1, 2, 0],
                                 ["BA003", 2, 1, 0],
                                 ["BA004", 2, 2, 0]])


if __name__ == "__main__":
    unittest.main()
