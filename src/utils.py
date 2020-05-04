import pathlib
import os

import docx
import win32com.client
from odf.opendocument import load as odf_load
from odf import text as odf_text
from odf import teletype as odf_teletype
from tika import parser


def getDocxText(path):
    '''extract text from .docx files'''
    doc = docx.Document(path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getDocText(path):
    '''extract text from .doc files'''
    word = win32com.client.Dispatch("Word.Application")
    word.visible = False
    wb = word.Documents.Open(path.absolute().as_uri())
    doc = word.ActiveDocument

    return doc.Range().Text

def getOdtText(path):
    '''extract text from .odt files'''
    textdoc = odf_load(path)
    allparas = textdoc.getElementsByType(odf_text.P)
    
    return '\n'.join([ odf_teletype.extractText(p) for p in allparas ])

def getPdfText(path):
    '''extract text from .pdf files'''

    file_data = parser.from_file(path.__str__())

    return file_data['content']
