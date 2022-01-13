from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

def print_ast(ast, filename):
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(ast)

    if filename:
        with open(filename, "w") as f:
            f.write(rslt)
    else:
        print(rslt)

