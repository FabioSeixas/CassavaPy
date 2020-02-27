import classes
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.filex = classes.FileX("cruz", "CRUZ9101", "irf")

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


if __name__ == "__main__":
    unittest.main()
