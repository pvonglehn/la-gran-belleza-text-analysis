import pathlib
import os
import re
import csv
import logging
from utils import getDocxText, getDocText, getOdtText, getPdfText

ROOT_DIR = pathlib.Path(__file__).parent.parent


# Set directories and create them if necessary
plain_text_dir = pathlib.Path().joinpath(ROOT_DIR,"data","plaintext")
raw_doc_path = pathlib.Path().joinpath(ROOT_DIR,"data","raw")
structured_data_dir = pathlib.Path().joinpath(ROOT_DIR,"data","structured")
logging_dir = pathlib.Path().joinpath(ROOT_DIR,"logs")

for dir_ in plain_text_dir, raw_doc_path, structured_data_dir, logging_dir:
    try:
        os.mkdir(dir_)
    except FileExistsError:
        pass

# Set up logging
logging_file = pathlib.Path().joinpath(logging_dir,'convert_to_raw_text.log')
logging.basicConfig(filename=logging_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('convert_to_raw_logger')


suffix2function = { ".docx":getDocxText, ".doc":getDocText, ".odt":getOdtText,  '.pdf':getPdfText}

# ignore temporary word files starting with ~$
files = [ file for file in os.listdir(raw_doc_path) if not file.startswith("~$")]
paths = [ raw_doc_path.joinpath(file) for file in files]
# Sort paths in order of suffix 
paths = sorted(paths,key=lambda x: getattr(x,"suffix"))

# Dictionary numbers to titles
num2title = dict()

failed_conversions_log = logging_dir.joinpath("failed_conversions.log")
failed_converstions = list()

with open(failed_conversions_log,"w") as failed_f:

    # Main loop to convert to plain texts
    for path in paths:
        suffix = path.suffix
        try:
            text = suffix2function[suffix](path)
        except Exception as e:
            logging.error(f'failed to convert {path}', exc_info=True)
            failed_f.write(path.__str__() + "\n")
            failed_converstions.append(path)
            continue

        stem = path.stem
        number = re.match("\d+",stem).group()
        num2title[number] = stem

        new_path = plain_text_dir.joinpath(number).with_suffix(".txt")
        with open(new_path,"w",encoding="UTF-8") as wf:
            wf.write(text)

num2title_path = pathlib.Path().joinpath(structured_data_dir,"num2title.tsv")
with open(num2title_path,'w') as csvfile:
    w = csv.writer(csvfile,delimiter='\t')
    num2title = sorted(num2title.items(),key=lambda x: int(x[0]))
    w.writerows(num2title)

n_failed = len(failed_converstions)
if n_failed > 0:
    logging.warning(f"{n_failed} files failed to convert. See {failed_conversions_log} for details")