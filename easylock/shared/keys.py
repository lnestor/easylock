import pyverilog.vparser.ast as vast

import settings
from shared.ast_search import find_last_input

def create_keys(moddef, start, count):
    keys = [create_key(moddef, number) for number in range(start, start + count)]
    return keys

def create_key(moddef, number):
    portlist = moddef.children()[1]
    ports = list(portlist.ports)
    items = list(moddef.items)

    key_name = "keyIn_%i_%i" % (settings.uid, number)
    port = vast.Port(key_name, None, None, None)
    ports.append(port)

    last_input_index = find_last_input(moddef)
    # moddef.items != moddef.children(), all indices are 2 off
    items.insert(last_input_index - 1, vast.Decl([vast.Input(key_name)]))

    portlist.ports = tuple(ports)
    moddef.items = tuple(items)

    return key_name
