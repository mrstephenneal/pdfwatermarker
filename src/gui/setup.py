import re
from setuptools import setup, find_packages

long_description = """
GUI wrapper for pdf.
"""

# Retrieve version number
VERSIONFILE = "pdf/conduit/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

setup(
    install_requires=[
        'PyPDF3>=0.0.6',
        'pdfrw',
        'PyMuPDF',
        'Pillow',
        'PySimpleGUI>=2.9.0',
        'reportlab',
        'looptools',
        'pdfconduit',
    ],
    name='pdfconduit-gui',
    version=verstr,
    packages=find_packages(),
    namespace_packages=['pdf'],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfconduit',
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='GUI wrapper for pdfconduit.',
    long_description=long_description,
)

