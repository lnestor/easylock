import pyverilog.vparser.ast as vast

from shared.ast_search import find_last_wire

def create_ilist(moddef, module, name, output, inputs, add_output_wire=True):
    items = list(moddef.items)

    out_port = vast.PortArg(None, vast.Identifier(output))
    in_ports = [vast.PortArg(None, vast.Identifier(name)) for name in inputs]

    portlist = (out_port, *in_ports)
    parameterlist = ()
    instance = vast.Instance(module, name, portlist, parameterlist)
    ilist = vast.InstanceList(module, (), (instance,))

    if add_output_wire:
        # This adds new key input nodes to the AST, could also append to a
        # node if there's only 1. But this way seems more general and better
        last_wire_index = find_last_wire(moddef)
        items.insert(last_wire_index - 1, vast.Decl([vast.Wire(output)]))

    items.append(ilist)
    moddef.items = tuple(items)

    return output

def rename_ilist_output(ilist, new):
    ilist.children()[0].children()[0].children()[0].name = new

def add_wire(moddef, name):
    items = list(moddef.items)
    last_wire_index = find_last_wire(moddef)
    items.insert(last_wire_index - 1, vast.Decl([vast.Wire(name)]))
    moddef.items = tuple(items)
