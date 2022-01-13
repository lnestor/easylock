import settings
from shared.ast_modify import create_ilist

def create_const_comparator(moddef, inputs, pattern):
    """Creates a comparator that compares a pattern to the inputs

    If the inputs match the pattern, the output of the comparator is 1.
    If they do not match, the output is 0. The invert flag switches
    this behavior.

    TODO:
        - Support multiple patterns. This would require keeping track of
          each input being XORed with 0/1 so we can reuse those gates
          instead of making multiple copies of the same gate
        - Support inversion flag

    Parameters:
        moddef: the module definition AST node
        inputs (list): a list with the input names (str) to compare to the pattern
        pattern (str): a string of 0s and 1s where each index corresponds to
                       to the same index in the inputs list

    Returns:
        the name of the output gate of the comparator

    """
    if len(inputs) != len(pattern):
        print("ERROR: comparator input length doesn't match desired pattern")
        exit(-1)

    xnor_outputs = [None] * len(inputs)

    for i, input_pair in enumerate(zip(inputs, pattern)):
        output_name = "const_comp_xor_%i_%i" % (settings.uid, i)
        instance_name = "CONST_COMP_XOR_%i_%i" % (settings.uid, i)
        xnor = create_ilist(moddef, "xnor", instance_name, output_name, input_pair)
        xnor_outputs[i] = output_name

    output_name = "const_comp_and_%i" % settings.uid
    create_ilist(moddef, "and", "CONST_COMP_AND_%i" % settings.uid, output_name, xnor_outputs)
    return output_name
