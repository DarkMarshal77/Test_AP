INT_SIZE = 4
LONG_SIZE = 8
BOOL_SIZE = 1
CHAR_SIZE = 1
REAL_SIZE = 4
STRING_MAX_SIZE = 512

Null = "\00"

types = ["SIGNED_INT", "ESCAPED_STRING", "SIGNED_FLOAT", "CHAR", "BOOL", "LONG"]

type_convert = {"SIGNED_INT": "i" + str(INT_SIZE * 8),
                "LONG": "i" + str(LONG_SIZE * 8),
                "SIGNED_FLOAT": "double",
                "CHAR": "i8",
                "BOOL": "i1",
                "ESCAPED_STRING": "i8*",
                "VOID": "void",
                }

size_map = {"SIGNED_INT": INT_SIZE,
            "LONG": LONG_SIZE,
            "SIGNED_FLOAT": REAL_SIZE,
            "CHAR": CHAR_SIZE,
            "BOOL": BOOL_SIZE,
            "ESCAPED_STRING": STRING_MAX_SIZE * CHAR_SIZE,
            "VOID": 0
            }

var_sign = ['@', '%']

INIT_ST = {"array": {},
           "assign": {},
           "boolean": {},
           "break": {},
           "begin": {},
           "char": {},
           "continue": {},
           "do": {},
           "else": {},
           "end": {},
           "function": {},
           "procedure": {},
           "if": {},
           "integer": {},
           "long": {},
           "of": {},
           "real": {},
           "return": {},
           "string": {},
           "while": {},
           "var": {},
           "write": {"out_type": 'SIGNED_INT'},
           "read": {"out_type": 'SIGNED_INT'},
           "strlen": {"out_type": 'SIGNED_INT'},
           "false": {"type": "BOOL", "size": BOOL_SIZE},
           "true": {"type": "BOOL", "size": BOOL_SIZE},
           }

temp_value = {"SIGNED_INT": "0",
              "LONG": "0",
              "SIGNED_FLOAT": "0.0",
              "CHAR": "0",
              "BOOL": "false",
              "ESCAPED_STRING": 'getelementptr inbounds ([1 x i8], [1 x i8]* @.str_func_def_ret, i32 0, i32 0)',
              "VOID": "",
              }

unary_op = ["-", "~"]

COMP_SIGN_TO_FLAG = {"SIGNED_INT": {
        "==": "eq",
        "<>": "ne",
        ">=": "sge",
        "<=": "sle",
        ">": "sgt",
        "<": "slt",
        "op": "icmp",
    },
    "LONG": {
        "==": "eq",
        "<>": "ne",
        ">=": "sge",
        "<=": "sle",
        ">": "sgt",
        "<": "slt",
        "op": "icmp",
    },
    "SIGNED_FLOAT": {
        "==": "oeq",
        "<>": "one",
        ">=": "oge",
        "<=": "ole",
        ">": "ogt",
        "<": "olt",
        "op": "fcmp",
    },
}

OP_NAME_TO_SIGN = {"add": "+",
                   "sub": "-",
                   "mul": "*",
                   "div": "/",
                   "rem": "%",
                   "bitwise_and": "&",
                   "bitwise_or": "|",
                   "bitwise_xor": "^",
                   "boolean_and": "and",
                   "boolean_or": "or",
                   "==": "==",
                   "<>": "<>",
                   ">=": ">=",
                   "<=": "<=",
                   ">": ">",
                   "<": "<",
                   }

bitwise_op = ["|", "^", "&"]
boolean_op = ["and", "or"]
compare_op = [">", "<", ">=", "<=", "==", "<>"]
calc_op = ["+", "*", "/", "%", "-"]


def result_type(operation, type1, type2):
    combined_types = (type1, type2)
    if combined_types == ("SIGNED_INT", "SIGNED_INT") and OP_NAME_TO_SIGN[operation] in calc_op + bitwise_op + compare_op:
        return "SIGNED_INT"
    if combined_types == ("SIGNED_INT", "SIGNED_INT") and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"

    if combined_types in [("SIGNED_INT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_INT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_INT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_INT", "BOOL"), ("BOOL", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("SIGNED_INT", "BOOL"), ("BOOL", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_INT", "BOOL"), ("BOOL", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_INT", "CHAR"), ("CHAR", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("SIGNED_INT", "CHAR"), ("CHAR", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_INT", "CHAR"), ("CHAR", "SIGNED_INT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_FLOAT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_FLOAT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_FLOAT", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_FLOAT", "BOOL"), ("BOOL", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_FLOAT", "BOOL"), ("BOOL", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_FLOAT", "BOOL"), ("BOOL", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("SIGNED_FLOAT", "CHAR"), ("CHAR", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("SIGNED_FLOAT", "CHAR"), ("CHAR", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("SIGNED_FLOAT", "CHAR"), ("CHAR", "SIGNED_FLOAT")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("BOOL", "BOOL"), ("BOOL", "BOOL")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("BOOL", "BOOL"), ("BOOL", "BOOL")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("BOOL", "BOOL"), ("BOOL", "BOOL")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("BOOL", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("BOOL", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("BOOL", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("CHAR", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_INT"
    if combined_types in [("CHAR", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("CHAR", "CHAR"), ("CHAR", "BOOL")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types == ("LONG", "LONG") and OP_NAME_TO_SIGN[operation] in calc_op + bitwise_op + compare_op:
        return "LONG"
    if combined_types == ("LONG", "LONG") and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"

    if combined_types in [("LONG", "SIGNED_INT"), ("SIGNED_INT", "LONG")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "LONG"
    if combined_types in [("LONG", "SIGNED_INT"), ("SIGNED_INT", "LONG")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("LONG", "SIGNED_INT"), ("SIGNED_INT", "LONG")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("LONG", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "LONG")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "SIGNED_FLOAT"
    if combined_types in [("LONG", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "LONG")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("LONG", "SIGNED_FLOAT"), ("SIGNED_FLOAT", "LONG")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("LONG", "BOOL"), ("BOOL", "LONG")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "LONG"
    if combined_types in [("LONG", "BOOL"), ("BOOL", "LONG")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("LONG", "BOOL"), ("BOOL", "LONG")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"

    if combined_types in [("LONG", "CHAR"), ("CHAR", "LONG")] and OP_NAME_TO_SIGN[operation] in calc_op + compare_op:
        return "LONG"
    if combined_types in [("LONG", "CHAR"), ("CHAR", "LONG")] and OP_NAME_TO_SIGN[operation] in boolean_op:
        return "BOOL"
    if combined_types in [("LONG", "CHAR"), ("CHAR", "LONG")] and OP_NAME_TO_SIGN[operation] in bitwise_op:
        return "SIGNED_INT"
