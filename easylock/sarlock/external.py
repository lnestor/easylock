import copy

from . import sarlock

def args_from_config(config, common_args):
    args = copy.deepcopy(common_args)
    args["key_bits"] = config["number-bits"]
    args["correct_key"] = "0" * int(args["key_bits"])

    return args

def run(ast, args):
    return sarlock.run(ast, args)
