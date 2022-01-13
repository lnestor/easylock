from shared.ast_search import try_get_ilist_from_output, get_ilist_inputs, get_input_names, get_ilists_from_input, get_ilist_output

def dfs(moddef, net_name):
    visited = {}
    _dfs_internal(moddef, net_name, visited, 0)
    return visited

def _dfs_internal(moddef, net_name, visited, hops):
    ilist = try_get_ilist_from_output(moddef, net_name)

    if ilist is None:
        return

    visited[net_name] = hops
    inputs = get_ilist_inputs(ilist)

    if len(inputs) == 0:
        return

    for i in inputs:
        if i in visited and visited[i] < hops + 1:
            continue
        else:
            _dfs_internal(moddef, i, visited, hops + 1)

def dfs_forward(moddef, net_name):
    visited = {}
    _dfs_forw_internal(moddef, net_name, visited, 0)
    return visited

def _dfs_forw_internal(moddef, net_name, visited, hops):
    ilists = get_ilists_from_input(moddef, net_name)
    ilist_outputs = [get_ilist_output(i) for i in ilists]

    if len(ilist_outputs) == 0:
        return

    for output in ilist_outputs:
        if output in visited and visited[output] < hops:
            continue
        else:
            visited[output] = hops
            _dfs_forw_internal(moddef, output, visited, hops + 1)
