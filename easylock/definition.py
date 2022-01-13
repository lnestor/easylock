import importlib

class Definition:
    def __init__(self, data):
        self._name = data["name"]
        self._key = data["key"]
        self._module_name = data["module"]
        self._module = importlib.import_module(self._module_name)

        self._check_module()

    def get_args(self, config, common_args):
        return self._module.args_from_config(config, common_args)

    def run(self, ast, args):
        return self._module.run(ast, args)

    def _check_module(self):
        has_args = hasattr(self._module, "args_from_config")
        has_run = hasattr(self._module, "run")

        if not has_args and not has_run:
            print("ERROR: module %s does not implement args_from_config or run" % self._module_name)
            exit(-1)
        elif not has_args:
            print("ERROR: module %s does not implement args_from_config" % self._module_name)
            exit(-1)
        elif not has_run:
            print("ERROR: module %s does not implement run" % self._module_name)
            exit(-1)


