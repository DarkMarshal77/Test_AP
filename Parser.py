from lark import Lark
from CodeGen import CodeGen

grammar = """
start: func_def start
     | proc_def start
     | var_dcl start
     |

var_dcl: simple_var 
       | array_var
       
simple_var: type id 
          | type id assignment
          
array_var: "array" type id 
         | "array" type id assignment
         
assignment: ":=" expr 
       
func_def: "function" id "(" args ")" ":" type block

proc_def: "procedure" id "(" args ")" block

args: var_dcl args_prime
    | 
args_prime: "," var_dcl args_prime
          | 

block: "begin" stl "end"

stl: st ";" stl
   | 

st: expr
  | "(" id id_plus ")" assignment
  | id assignment
  | var_dcl
  | loop 
  | "return" id
  | conditional

id_plus: "," id id_plus 
       | "," id
// ___________________________________________ expression handling here
op: constant
  | function_call
  | id

// _______________________ or and
expr: expr_or "or" expr
    | expr_or
expr_or: e "and" expr_or
       | e
       
// _______________________ | ^ & 
e: e_or "|" e
 | e_or
e_or: e_xor "^" e_or
    | e_xor
e_xor: e_and "&" e_xor
     | e_and
     
// _______________________ >= > < <=
e_and: e_eq "==" e_and
     | e_eq "<>" e_and
     | e_eq
e_eq: e_lg ">" e_eq
    | e_lg ">=" e_eq
    | e_lg "<" e_eq
    | e_lg "<=" e_eq
    | e_lg

// _______________________ + - / * % - ~
e_lg: t "+" e_and
     | t "-" e_and
     | t
t: f "*" t
 | f "/" t
 | f "%" t
 | f
f: "-" p
 | "~" p
 | p
p: op
 | "(" e ")"

// ___________________________________________________________________
function_call: id "(" exprs ")"

exprs: expr exprs_prime
     | 
exprs_prime: "," expr exprs_prime
           | 
           
id: CNAME

constant: SIGNED_INT
        | "0x" SIGNED_INT
        | SIGNED_FLOAT
        | ESCAPED_STRING
        | "\'" CHAR "\'"

type: "integer"
    | "real"
    | "string"

loop: "while" "(" expr ")" "do" block

conditional: "if" "(" expr ")" "then" block ep

ep: "else" block
  | 
 
CHAR: /./

%import common.SIGNED_NUMBER
%import common.SIGNED_INT
%import common.SIGNED_FLOAT
%import common.ESCAPED_STRING
%import common.CNAME
%import common.WS
%ignore WS
"""

parser = Lark(grammar, parser="lalr", transformer=CodeGen(), debug=True)
# parser = Lark(grammar)
print(parser.parse("""
function main(integer a, string b) : integer
begin
if (9 + b(20)) then 
begin
a := 10;
end;
end
""").pretty())
