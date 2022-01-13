import argparse
import importlib
from pyverilog.vparser.parser import parse
import os

from common_args import get_common_args
import definition
from shared.easy_yaml import read_yaml
from shared.ast_print import print_ast

DEFINITIONS_FILENAME = "definitions.yaml"

def get_definitions():
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, DEFINITIONS_FILENAME)
    data = read_yaml(path)
    return {d["key"]: definition.Definition(d) for d in data["locking-types"]}

def get_args():
    parser = argparse.ArgumentParser(description="Lock a circuit using several different locking circuits")
    parser.add_argument("circuit", help="The circuit to lock")
    parser.add_argument("--config", help="The config file containing information on how the lock the circuit", required=True)
    parser.add_argument("-o", "--output", help="The verilog file to output to. Otherwise it will print to the screen.")
    return parser.parse_args()

def get_config(args):
    config = read_yaml(args.config)
    return config

def setup():
    defs = get_definitions()
    args = get_args()
    config = get_config(args)

    return defs, args, config

def run_pass(ast, pass_, defs, run_data):
    type_ = pass_["locking-type"].lower()
    if type_ not in defs:
        print("ERROR: locking type %s not recognized" % type_)
        exit(-1)

    common_args = get_common_args(ast, pass_, run_data)
    args = defs[type_].get_args(pass_, common_args)
    return defs[type_].run(ast, args)

def main():
    defs, args, config = setup()

    ast, _ = parse([args.circuit], debug=False)
    run_data = []
    for idx, pass_ in enumerate(config["passes"]):
        pass_["index"] = idx
        data = run_pass(ast, pass_, defs, run_data)
        run_data.append(data)

    print_ast(ast, args.output)

if __name__ == "__main__":
    main()
