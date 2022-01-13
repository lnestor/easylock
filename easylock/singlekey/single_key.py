import settings
from shared.ast_search import get_moddef, get_ilist_from_output
from shared.ast_modify import create_ilist, rename_ilist_output, add_wire
from shared.keys import create_keys

def add_key_gate(moddef, new_key, output_net_name):
    instance_name = "FLIP_IT_%i" % settings.uid
    changed_name = "signal_from_circuit_%i" % settings.uid

    create_ilist(moddef, "xor", instance_name, output_net_name, [new_key, changed_name], add_output_wire=False)

    ilist = get_ilist_from_output(moddef, output_net_name)
    rename_ilist_output(ilist, changed_name)
    add_wire(moddef, changed_name)

def run(ast, args):
    moddef = get_moddef(ast)
    new_key = create_keys(moddef, args["start_input_index"], 1)[0]
    add_key_gate(moddef, new_key, args["insertion_net_name"])

    run_data = {}
    run_data["locked_gate_output_net"] = args["insertion_net_name"]
    run_data["last_input_index"] = args["start_input_index"] - 1
    return run_data
