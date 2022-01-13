import copy

from . import multiplexer

def args_from_config(config, common_args):
    args = copy.deepcopy(common_args)
    args["number_to_add"] = config["number-to-add"]
    args["control_type"] = config["control-type"]

    return args

def run(ast, args):
    multiplexer.run(ast, args)
