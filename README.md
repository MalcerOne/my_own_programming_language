# PickleRick Programming Language
Programming Language created by my own, based in the TV series Rick and Morty. Compiler made with Python in the class of Logica da Computação (Computer Logic), at Insper


# EBNF
BLOCK = "{", { STATEMENT }, "}" ;<br />
STATEMENT = ( λ | ASSIGNMENT | WHILE | IF | PRINT ), ";" | BLOCK ;<br />
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION, ";" ;<br />
WHILE = "squanch","(", RelEXPRESSION, ")"| BLOCK ;<br />
IF = "if","(", RelEXPRESSION, ")"| BLOCK ,  ( λ |  ( "else" |BLOCK));<br />
PRINT = "show_me_what_you_got", "(", RelEXPRESSION, ")";<br />
RelEXPRESSION = EXPRESSION, { ("==" | "mortyer_than" | "rickier_than"), EXPRESSION } ;<br />
EXPRESSION = TERM, { ("+" | "-" | "or"), TERM } ;<br />
TERM = FACTOR, { ("*" | "/" | "and"), FACTOR } ;<br />
FACTOR = (("+" | "-" | "not"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;<br />
IDENTIFIER = "meeseeks", LETTER, { LETTER | DIGIT | "_" } ;<br />
NUMBER = DIGIT, { DIGIT } ;<br />
LETTER = ( a | ... | z | A | ... | Z ) ;<br />
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;<br />
