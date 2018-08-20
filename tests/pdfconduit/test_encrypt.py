import unittest
import os
import shutil
from pdfconduit import Encrypt, Info
from tests import pdf, directory


class TestEncrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = []

    @classmethod
    def tearDownClass(cls):
        # Destination directory
        dst = os.path.join(directory, 'results')

        # Create destination if it does not exist
        if not os.path.isdir(dst):
            os.mkdir(dst)

        # Move each file into results folder
        for i in cls.files:
            source = os.path.join(directory, str(os.path.basename(i)))
            target = os.path.join(dst, str(os.path.basename(i)))
            shutil.move(source, target)

        # Move /P value files into results/P
        if not os.path.isdir(os.path.join(dst, 'P')):
            os.mkdir(os.path.join(dst, 'P'))
        for f in os.listdir(dst):
            if f.startswith('-'):
                source = os.path.join(dst, f)
                target = os.path.join(dst, 'P', f)
                shutil.move(source, target)

    def setUp(self):
        self.owner_pw = 'foo'
        self.user_pw = 'baz'

    def test_encrypt(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, suffix='secured')
        self.files.append(str(p))
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)
        self.assertEqual(security['/P'], -1852)

    def test_encrypt_128bit(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, bit128=True, suffix='secured_128bit')
        self.files.append(str(p))
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)

    def test_encrypt_40bit(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, bit128=False, suffix='secured_40bit')
        self.files.append(str(p))

        self.assertTrue(Info(p.output, self.user_pw).encrypted)

    def test_encrypt_commenting(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, allow_commenting=True, suffix='secured_commenting')
        self.files.append(str(p))
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/P'], -1500)

    def test_encrypt_pflag(self):
        _range = [-(x + 50) for x in range(0, 1852)[::100]]
        for i in _range:
            p = Encrypt(pdf, self.user_pw, self.owner_pw, output=os.path.join(directory, str(i) + '.pdf'),
                        overwrite_permission=i)
            self.files.append(str(p))
            security = Info(p.output, self.user_pw).security

            self.assertTrue(Info(p.output, self.user_pw).encrypted)
            self.assertEqual(security['/Length'], 128)
            self.assertEqual(security['/P'], i)


if __name__ == '__main__':
    unittest.main()
