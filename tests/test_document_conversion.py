import pytest
import sys
import pathlib
from src.utils import getDocxText, getDocText, getOdtText, getPdfText

THIS_DIR = pathlib.Path(__file__).parent
test_data_dir = THIS_DIR.joinpath("test_data")

def test_getDocxText():
    file = THIS_DIR.joinpath(test_data_dir,"hello_world.docx")
    assert getDocxText(file).strip() == "Hello World!"

def test_getDocText():
    file = THIS_DIR.joinpath(test_data_dir,"hello_world.doc")
    assert getDocText(file).strip() == "Hello World!"

def test_getOdtText():
    file = THIS_DIR.joinpath(test_data_dir,"hello_world.odt")
    assert getOdtText(file).strip() == "Hello World!"

def test_getPdfText():
    file = THIS_DIR.joinpath(test_data_dir,"hello_world.pdf")
    assert getPdfText(file).strip() == "Hello World!"