import unittest
import os
import shutil
import time
from pdfconduit import Info, Flatten
from tests import *


class TestFlatten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(pdfs_dir, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'flatten')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        # Log destination
        cls.file_path = 'flatten_progress.csv'
        cls.csv = os.path.join(os.path.dirname(__file__), 'log', cls.file_path)
        cls.log = []

        cls.fname = pdf_path

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        write_log(cls.csv, cls.log)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[1:]), t))

        # Determine test result
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure

        # demo:   report short info immediately (not important)
        if not ok:
            typ, text = ('ERROR', error) if error else ('FAIL', failure)
        else:
            typ = 'PASS'

        # Log dump
        rows, file_path = dump_log(test_case=self.id().split('.'), time=t, result=typ)
        self.log.append(rows)
        self.file_path = file_path

        # Move each file into results folder
        for i in self.files:
            source = i
            target = os.path.join(self.dst, str(os.path.basename(i)))
            try:
                shutil.move(source, target)
                self.files.remove(i)
            except FileNotFoundError:
                pass

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    def test_flatten_gui(self):
        flat = Flatten(self.fname, scale=1.0, suffix='flat_gui', progress_bar='gui').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] / Info(flat).size[1]) <= 1)

    def test_flatten_tqdm(self):
        flat = Flatten(self.fname, scale=1.0, suffix='flat_tqdm', progress_bar='tqdm').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] / Info(flat).size[1]) <= 1)


if __name__ == '__main__':
    unittest.main()
