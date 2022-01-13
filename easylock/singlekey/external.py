import copy

from . import single_key

def args_from_config(config, common_args):
    args = copy.deepcopy(common_args)
    return args

def run(ast, args):
    return single_key.run(ast, args)
