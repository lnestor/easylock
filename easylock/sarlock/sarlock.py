import settings
from shared.ast_modify import create_ilist, rename_ilist_output, add_wire
from shared.ast_search import get_input_names, get_ilist_from_output
from shared.comparator.signal_comparator import create_signal_comparator
from shared.comparator.constant_comparator import create_const_comparator
from shared.keys import create_keys

def create_comparator(moddef, key_inputs, primary_inputs, args):
    start_idx = args["start_input_index"]
    offset = len(key_inputs) * args["input_index_direction"]
    chosen_primary_inputs = primary_inputs[start_idx:start_idx + offset]

    comparator = create_signal_comparator(moddef, key_inputs, chosen_primary_inputs)
    return comparator

def add_mask(moddef, comparator, key_inputs, args):
    correct_key = args["correct_key"]
    mask_comparator = create_const_comparator(moddef, key_inputs, correct_key, inverted=True)

    instance_name = "MASK_AND_%i" % settings.uid
    output_name = "mask_and_%i" % settings.uid
    create_ilist(moddef, "and", instance_name, output_name, [comparator, mask_comparator])
    return output_name

def insert_locking(moddef, locking_output, output_net_name):
    instance_name = "FLIP_IT_%i" % settings.uid
    changed_name = "signal_from_circuit_%i" % settings.uid
    create_ilist(moddef, "xor", instance_name, output_net_name, [locking_output, changed_name], add_output_wire=False)

    ilist = get_ilist_from_output(moddef, output_net_name)
    rename_ilist_output(ilist, changed_name)
    add_wire(moddef, changed_name)

def run(ast, args):
    moddef = ast.children()[0].children()[0]
    primary_inputs = get_input_names(moddef)
    new_keys = create_keys(moddef, args["start_input_index"], args["key_bits"])

    comparator = create_comparator(moddef, new_keys, primary_inputs, args)
    mask = add_mask(moddef, comparator, new_keys, args)
    insert_locking(moddef, mask, args["insertion_net_name"])

    run_data = {}
    run_data["locked_gate_output_net"] = args["insertion_net_name"]
    run_data["last_input_index"] = args["start_input_index"] + args["key_bits"] - 1
    return run_data
