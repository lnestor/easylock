import settings
from shared.ast_modify import create_ilist

def create_signal_comparator(moddef, inputs1, inputs2):
    """Creates a comparator that compares two signals

    If the inputs match the pattern, the output of the comparator is 1.
    If they do not match, the output is 0.

    TODO:
        - Support inversion flag
        - Using settings.uid doesn't work when this is called twice with the
          same uid

    Parameters:
        moddef: the module definition AST node
        inputs1 (list): a list with the first input names (str) to compare
        inputs2 (list): a list with the second input names (str) to comapre
                        to the same index in the first inputs list

    Returns:
        the output gate of the comparator

    """
    if len(inputs1) != len(inputs2):
        print("ERROR: comparator inputs of different lengths")
        exit(-1)

    xnor_outputs = [None] * len(inputs1)

    for i, input_pair in enumerate(zip(inputs1, inputs2)):
        output_name = "sig_comp_%i_%i" % (settings.uid, i)
        instance_name = "SIG_COMP_XOR_%i_%i" % (settings.uid, i)
        xnor = create_ilist(moddef, "xnor", instance_name, output_name, input_pair)
        xnor_outputs[i] = output_name

    output_name = "sig_comp_and_%i" % settings.uid
    create_ilist(moddef, "and", "SIG_COMP_AND_%i" % settings.uid, output_name, xnor_outputs)
    return output_name
