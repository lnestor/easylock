import pyverilog.vparser.ast as vast

def get_wire_names(moddef):
    wire_nodes = get_decl_nodes(moddef, vast.Wire)
    return [n.name for n in wire_nodes]

def get_primary_input_names(moddef):
    input_names = get_input_names(moddef)
    return [name for name in input_names if "key" not in name]

def get_key_input_names(moddef):
    input_names = get_input_names(moddef)
    return [name for name in input_names if "key" in name]

def get_input_names(moddef):
    input_nodes = get_decl_nodes(moddef, vast.Input)
    return [n.name for n in input_nodes]

def get_output_names(moddef):
    output_nodes = get_decl_nodes(moddef, vast.Output)
    return [n.name for n in output_nodes]

def get_decl_nodes(moddef, cls):
    decls = [n for n in moddef.children() if len(n.children()) > 0 and isinstance(n.children()[0], cls)]
    nodes = [child for node in decls for child in node.children()]
    return nodes

def find_last_input(moddef):
    return find_last_decl(moddef, vast.Input)

def find_last_wire(moddef):
    return find_last_decl(moddef, vast.Wire)

def find_last_decl(moddef, cls):
    index = 0
    for idx in range(len(moddef.children())):
        if len(moddef.children()[idx].children()) > 0 and isinstance(moddef.children()[idx].children()[0], cls):
            index = idx

    return index

def try_get_ilist_from_output(moddef, output):
    ilists = get_ilists(moddef)
    ilists = list(filter(lambda x: get_ilist_output(x) == output, ilists))

    if len(ilists) == 0:
        return None
    else:
        return ilists[0]

def get_ilist_from_output(moddef, output):
    ilists = get_ilists(moddef)
    return list(filter(lambda x: get_ilist_output(x) == output, ilists))[0]

def get_ilists_from_input(moddef, input_):
    ilists = get_ilists(moddef)
    return list(filter(lambda x: input_ in get_ilist_inputs(x), ilists))

def get_ilists(moddef):
    return list(filter(lambda x: isinstance(x, vast.InstanceList), moddef.children()))

def get_ilist_output(ilist):
    return ilist.children()[0].children()[0].children()[0].name

def get_ilist_inputs(ilist):
    children = ilist.children()[0].children()[1:]
    return [c.children()[0].name for c in children]

def get_ilist_input(ilist, index):
    return ilist.children()[0].children()[index + 1].children()[0].name

def get_moddef(ast):
    return ast.children()[0].children()[0]
