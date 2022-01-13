import random

import settings
import interference
from shared.ast_search import get_output_names

def get_common_args(ast, config, run_data):
    args = {}
    args["insertion_net_name"] = get_insertion_net(ast, config, run_data)
    args["start_input_index"] = get_primary_input_start(config, run_data)
    args["input_index_direction"] = get_primary_input_dir(config)

    settings.uid = config["index"]

    return args

def get_insertion_net(ast, config, run_data):
    if "integration-node" not in config and "interference" not in config:
        print("ERROR: integration node or interference not present in pass %s" % config["name"])
        exit(-1)

    if "integration-node" in config:
        return get_integration_node(ast, config, run_data)
    else:
        return get_interference_node(ast, config, run_data)

def get_integration_node(ast, config, run_data):
    if config["integration-node"]["type"] == "output":
        output_names = get_output_names(ast.children()[0].children()[0])
        return random.choice(output_names)
    elif config["integration-node"]["type"] == "random":
        raise NotImplementedError
    elif config["integration-node"]["type"] == "previous":
        index = config["index"]
        return run_data[index - 1]["locked_gate_output_net"]
    elif config["integration-node"]["type"] == "net":
        return config["integration-node"]["name"]
    else:
        raise NotImplementedError

def get_interference_node(ast, config, run_data):
    type_ = config["interference"]["type"]
    pass_ = config["interference"]["pass"]

    if type_ == "direct":
        gates = interference.direct(ast, run_data[pass_]["locked_gate_output_net"])
    elif type_ == "indirect":
        gates = interference.indirect(ast, run_data[pass_]["locked_gate_output_net"])
    elif type_ == "none":
        gates = interference.none(ast, run_data[pass_]["locked_gate_output_net"])
    else:
        print("ERROR: interference type %s not supported" % type_)

    if len(gates) == 0:
        print("ERROR: no suitable locations for pass %i" % config["index"])
        exit(-1)

    # Distance should throw an error if used with "none" interference
    if "distance" not in config["interference"]:
        return random.choice(list(gates.keys()))
    else:
        dist = config["interference"]["distance"]
        valid_gates = [g for g in gates if gates[g] == dist]

        if len(valid_gates) == 0:
            print("ERROR: no gates within %i hops for interference type %s" % (dist, type_))
            exit(-1)
        return random.choice(valid_gates)


def get_primary_input_start(config, run_data):
    if "primary-input-start" not in config:
        return 0
    elif config["primary-input-start"] == "continuous":
        index = config["index"]
        return run_data[index - 1]["last_input_index"] + 1
    else:
        return int(config["primary-input-start"])

def get_primary_input_dir(config):
    if "primary-input-start" not in config:
        return 1
    elif config["primary-input-start"] == "continuous":
        return 1
    else:
        return 1
