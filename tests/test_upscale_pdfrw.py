import unittest
import os
import shutil
import time
from pdfconduit import Info, upscale
from tests import *


class TestUpscalePdfrw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'scale')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        # Log destination
        cls.file_path = 'upscale_pdfrw.csv'
        cls.csv = os.path.join(os.path.dirname(__file__), 'log', cls.file_path)
        cls.log = []

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        write_log(cls.csv, cls.log)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[2:]), t))

        # Log dump
        rows, file_path = dump_log(test_case=self.id().split('.'), time=t)
        self.log.append(rows)
        self.file_path = file_path

        # Move each file into results folder
        for i in self.files:
            source = i
            target = os.path.join(self.dst, str(os.path.basename(i)))
            shutil.move(source, target)
            self.files.remove(i)

    def test_upscale_pdfrw(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_20x_pdfrw(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_2.0_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_15x_pdfrw(self):
        s = 1.5
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_1.5_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_30x_pdfrw(self):
        s = 3.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_3.0_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))


if __name__ == '__main__':
    unittest.main()
