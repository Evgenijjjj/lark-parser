import sys

from lark import Lark
from lark.tree import pydot__tree_to_png

try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except IndexError:
    print("Аргументы не заданы.")
    exit(0)

grammar = r"""
    start: (function_definition)*

    function_definition: "fun" FUN_NAME "(" parameters? ")" function_body
    function_call: FUN_NAME "(" function_call_params? ")"

    parameters: single_param ("," single_param)*
    single_param: PARAM_NAME
    function_call_params: atoms ("," atoms)*

    function_body: "{" (function_suit ";" | condition_statement)* "}"
    function_suit: return_statement | variable_statement | function_call

    variable_assignment_statement: PARAM_NAME "=" variable_value
    variable_statement: "var"? variable_assignment_statement
    variable_value: (atoms | atoms_expression_and_comp_op)
    return_statement: "return" (atoms | atoms_expression_and_comp_op)
    
    atoms: atom_op ((add_op | mul_op) atoms)?
    atom: function_call | NUMBER | PARAM_NAME
    atom_op: prefix_atom_op | pow_atom_op
    prefix_atom_op: ("--" | "++")? atom
    pow_atom_op: atom "**" atom
    
    atoms_expression_and_comp_op: atoms_and_or_expression | atoms_brackets_comp_op
    atoms_brackets: "(" atoms_and_or_expression ")" 
    atoms_brackets_comp_op: ((atoms_brackets ((AND | OR| comp_op) atoms_brackets)?))
    atoms_and_or_expression: ((atoms_expression ((AND | OR) atoms_expression)?) | ("(" atoms_and_or_expression ")"))
    atoms_expression: atoms ((comp_op) atoms)?
    if_statement: "if" "(" (atoms_expression_and_comp_op)* ")" function_body ["else" function_body]
    while_statement: "while" "(" atoms_expression_and_comp_op* ")" function_body
    condition_statement: if_statement | while_statement
    
    factor_op: "-"
    add_op: "+"|"-"
    mul_op: "*"|"/"
    MUL: "*"
    DIV: "/"
    ADD: "+"
    SUB: "-"
    LT: "<"
    LTE: "<="
    GT: ">"
    GTE: ">="
    NEQ: "/="
    EQ: "=="
    AND: "&&"
    OR: "||"
    comp_op: "<"|">"|"=="|">="|"<="|"/="

    NUMBER: /(0|[1-9][0-9]*)/

    FUN_NAME: /(?!(if|else|fun)\b)[a-z]\w*/
    PARAM_NAME: /(?!(if|else|var)\b)[a-z]\w*/

    %import common.WS
    %import common.NEWLINE
    
    %ignore WS
    %ignore NEWLINE
"""

p = Lark(grammar)


def make_png(parsed_tree, filename):
    pydot__tree_to_png(parsed_tree, filename)


if __name__ == '__main__':
    with open(input_file, "r") as file:
        try:
            code = file.read()
            print(code)
            tree = p.parse(code)
            make_png(tree, output_file)
        except Exception as e:
            print(f"Parse error! {e}")
