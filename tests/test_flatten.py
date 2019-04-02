import unittest
import os
from looptools import Timer
from pdfconduit import Info, Flatten
from tests import *


class TestFlatten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    @Timer.decorator
    def test_flatten(self):
        """Create a 'flattened' pdf file without layers."""
        flat = Flatten(self.pdf_path, suffix='flat_2x').save()

        # Assert pdf file exists
        self.assertTrue(os.path.exists(flat))

        # Assert there are the same number of pages in the 'original' and 'flattened' pdf
        self.assertEqual(Info(self.pdf_path).pages, Info(flat).pages)

        # Confirm that PDF page sizes have not increased
        self.assertTrue(abs(Info(self.pdf_path).size[0] / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.pdf_path).size[1] / Info(flat).size[1]) <= 1)
        return flat


if __name__ == '__main__':
    unittest.main()
