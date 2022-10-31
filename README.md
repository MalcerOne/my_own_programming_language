# PickleRick Programming Language
Programming Language created by my own, with my compiler made in the class of Logica da Computação (Computer Logic), at Insper


# EBNF
BLOCK = "{", { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGNMENT | WHILE | IF | PRINT ), ";" | BLOCK ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION, ";" ;
WHILE = "squanch","(", RelEXPRESSION, ")"| BLOCK ;
IF = "if","(", RelEXPRESSION, ")"| BLOCK ,  ( λ |  ( "else" |BLOCK));
PRINT = "show_me_what_you_got", "(", RelEXPRESSION, ")";
RelEXPRESSION = EXPRESSION, { ("==" | "mortyer_than" | "rickier_than"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-" | "or"), TERM } ;
TERM = FACTOR, { ("*" | "/" | "and"), FACTOR } ;
FACTOR = (("+" | "-" | "not"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = "meeseeks", LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
