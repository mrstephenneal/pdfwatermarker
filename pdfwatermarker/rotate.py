# Rotate a pdf file
import os
from tempfile import NamedTemporaryFile
from pdfwatermarker.thirdparty.PyPDF2 import PdfFileReader, PdfFileWriter
from pdfwatermarker.utils import add_suffix
from pdfrw import PdfReader, PdfWriter


def rotate(file_name, rotate, suffix='rotated', method='pypdf2', tempdir=None):
    """Rotate PDF by increments of 90 degrees."""
    # Set output file name
    if tempdir:
        outfn = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False)
    elif suffix:
        outfn = os.path.join(os.path.dirname(file_name), add_suffix(file_name, suffix))
    else:
        outfn = NamedTemporaryFile(suffix='.pdf')

    def pypdf2():
        pdf_in = open(file_name, 'rb')
        pdf_reader = PdfFileReader(pdf_in)
        pdf_writer = PdfFileWriter()
        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)
            page.rotateClockwise(rotate)
            pdf_writer.addPage(page)
        pdf_out = open(outfn.name, 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()
        return outfn.name

    def pdfrw():
        trailer = PdfReader(file_name)
        pages = trailer.pages

        ranges = [[1, len(pages)]]

        for onerange in ranges:
            onerange = (onerange + onerange[-1:])[:2]
            for pagenum in range(onerange[0] - 1, onerange[1]):
                pages[pagenum].Rotate = (int(pages[pagenum].inheritable.Rotate or
                                             0) + rotate) % 360

        outdata = PdfWriter(outfn)
        outdata.trailer = trailer
        outdata.write()
        return outfn.name

    if method is 'pypdf2':
        return pypdf2()
    else:
        return pdfrw()
