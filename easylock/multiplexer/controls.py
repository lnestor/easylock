import settings
from shared.ast_modify import create_ilist

def create_mux_controls(moddef, primary_inputs, new_keys, args):
    if args["control_type"] == "normal":
        return normal_type(moddef, primary_inputs, new_keys, args)
    else:
        print("ERROR: mux control type %s not supported" % control_type)
        exit(-1)

def normal_type(moddef, primary_inputs, new_keys, args):
    controls = [None] * len(new_keys)

    for i in range(len(new_keys)):
        instance_name = "MUX_CONTROL_XOR_%i_%i" % (settings.uid, i)
        output_name = "mux_control_xor_%i_%i" % (settings.uid, i)
        input_index = args["start_input_index"] + i * args["input_index_direction"]
        inputs = [new_keys[i], primary_inputs[input_index]]
        create_ilist(moddef, "xor", instance_name, output_name, inputs)

        controls[i] = output_name

    return controls
