import logging


def parse(rawfile_path=None, gsfile_path=None):
    logging.info("Parsing file: {}".format(rawfile_path))
    pairs = []
    with open(rawfile_path) as raw_file:
        raw_lines = raw_file.readlines()
        with open(gsfile_path) as gs_file:
            gs_lines = gs_file.readlines()
            for raw_line, gs_line in zip(raw_lines, gs_lines):
                if gs_line.replace("\n", "").isdigit():
                    gs = float(gs_line.replace("\n", ""))
                    split = raw_line.split("\t")
                    pairs.append((split[0], split[1], gs))
    return pairs
