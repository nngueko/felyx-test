import unittest
from app import DataManipulation


class ServicesTest(unittest.TestCase):

    def testRetrieveData(self):
        db = DataManipulation()
        res = db.retrieved_data()
        self.assertEqual(res, 1)


if __name__ == '__main__':
    unittest.main()
