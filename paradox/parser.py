import logging
import json
import os


def parse(mapping="corpus/mapping.json", mode='train'):
    mapping = json.loads(open(mapping).read())[mode]
    pairs = []
    for k, v in mapping.iteritems():
        pairs.extend(_parse(rawfile_path=k, gsfile_path=v))
    return pairs


def _parse(rawfile_path=None, gsfile_path=None):
    pairs = []
    with open(os.path.join("corpus", rawfile_path)) as raw_file:
        logging.info("Parsing raw file: {}".format(rawfile_path))
        raw_lines = raw_file.readlines()
        with open(os.path.join("corpus", gsfile_path)) as gs_file:
            logging.info("Parsing gs file: {}".format(gsfile_path))
            gs_lines = gs_file.readlines()
            for raw_line, gs_line in zip(raw_lines, gs_lines):
                if gs_line.replace("\n", "").isdigit():
                    gs = float(gs_line.replace("\n", ""))
                    split = raw_line.split("\t")
                    pairs.append((split[0].replace("\n", "") +
                                  '<<STOP>>' +
                                  split[1].replace("\n", ""), gs))
    return pairs
