import settings
from shared.ast_modify import create_ilist, rename_ilist_output
from shared.ast_search import get_primary_input_names, get_key_input_names, get_ilist_from_output, get_ilist_input
from shared.keys import create_keys

from .controls import create_mux_controls

def add_muxes(moddef, net_name, controls):
    # Note: this assumes the muxes are hooked up to a key gate where the
    # key bit is the first argument and the circuit signal is the second
    # this should be changed
    ilist = get_ilist_from_output(moddef, net_name)
    input1 = get_ilist_input(ilist, 1)
    input2 = "flipped_signal_%i" % settings.uid
    output = net_name
    rename_ilist_output(ilist, input2)

    for i in range(len(controls)):
        portnames = (input1, input2, output)
        mux_output = add_mux(moddef, portnames, controls[i], i)

        if i < len(controls) - 1:
            mux_ilist = get_ilist_from_output(moddef, mux_output)
            new_name = "mux_output_%i" % i
            rename_ilist_output(mux_ilist, new_name)
            input2 = new_name

def add_mux(moddef, portnames, control, index):
    input1, input2, output = portnames

    not_ = create_ilist(moddef, "not", "MUX_NOT_%i_%i" % (settings.uid, index), "mux_not_%i_%i" % (settings.uid, index), [control])
    and0_ = create_ilist(moddef, "and", "MUX_AND0_%i_%i" % (settings.uid, index), "mux_and0_%i_%i" % (settings.uid, index), [input1, not_])
    and1_ = create_ilist(moddef, "and", "MUX_AND1_%i_%i" % (settings.uid, index), "mux_and1_%i_%i" % (settings.uid, index), [input2, control])
    or_ = create_ilist(moddef, "or", "MUX_OR_%i_%i" % (settings.uid, index), output, [and0_, and1_], add_output_wire=False)

    return or_

def run(ast, args):
    moddef = ast.children()[0].children()[0]

    primary_inputs = get_primary_input_names(moddef)
    key_inputs = get_key_input_names(moddef)

    new_keys = create_keys(moddef, len(key_inputs), args["number_to_add"])
    controls = create_mux_controls(moddef, primary_inputs, new_keys, args)
    add_muxes(moddef, args["insertion_net_name"], controls)
