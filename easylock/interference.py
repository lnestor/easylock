from shared.ast_graph import dfs, dfs_forward
from shared.ast_search import get_moddef, get_ilist_from_output, get_ilist_input, get_output_names, get_wire_names

def direct(ast, net_name):
    moddef = get_moddef(ast)
    ilist = get_ilist_from_output(moddef, net_name)
    circuit_net_name = get_ilist_input(ilist, 1)

    # This only takes into account the gates BEFORE the gate of
    # interest. More work is needed to support if "direct" also
    # means after the gate of interest
    gates = dfs(moddef, circuit_net_name)
    return gates

def indirect(ast, output_net_name):
    moddef = get_moddef(ast)
    ilist = get_ilist_from_output(moddef, output_net_name)
    locking_input_net_name = get_ilist_input(ilist, 0)
    circuit_input_net_name = get_ilist_input(ilist, 1)

    gates_locking = dfs(moddef, locking_input_net_name)
    gates_behind = dfs(moddef, circuit_input_net_name)
    gates_ahead = dfs_forward(moddef, output_net_name)
    outputs = [g for g in gates_ahead if g in get_output_names(moddef)]

    gates_in_subcircuits = {}
    for output in outputs:
        gates = dfs(moddef, output)
        gates_in_subcircuits.update(gates)

    to_return = gates_in_subcircuits
    to_return = {k: v for k, v in to_return.items() if k not in gates_locking}
    to_return = {k: v for k, v in to_return.items() if k not in gates_behind}
    to_return = {k: v for k, v in to_return.items() if k not in gates_ahead}
    to_return = {k: v for k, v in to_return.items() if k != output_net_name}
    to_return = {k: v - gates_in_subcircuits[output_net_name] for k, v in to_return.items()}

    return to_return

def none(ast, output_net_name):
    moddef = get_moddef(ast)
    gates_ahead = dfs_forward(moddef, output_net_name)
    outputs = [g for g in gates_ahead if g in get_output_names(moddef)]

    gates_in_subcircuits = {}
    for output in outputs:
        gates = dfs(moddef, output)
        gates_in_subcircuits.update(gates)

    all_nets = get_wire_names(moddef)
    to_return = {n: 0 for n in all_nets if n not in gates_in_subcircuits.keys()}
    return to_return
