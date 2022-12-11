# PickleRick Programming Language
Programming Language created by my own, based in the TV series Rick and Morty. Compiler made with Python in the class of Logica da Computação (Computer Logic), at Insper


# EBNF
PROGRAM = (λ | DECLARATION);<br />
DECLARATION = ("fn"), IDENTIFIER, "(", {IDENTIFIER, {","}, (":"), ("i32" | "String")}, ")", BLOCK;<br />
BLOCK = "{", { STATEMENT }, "}" ;<br />
STATEMENT = ({ASSIGNMENT | WHILE | IF | PRINT | VARDEC ), ";" | BLOCK ;<br />
VARDEC = "meeseeks", IDENTIFIER, {",", IDENTIFIER}, ":", ("i32" | "String");<br />
ASSIGNMENT = IDENTIFIER, "=", RelEXPRESSION, ";" ;<br />
WHILE = "squanch","(", RelEXPRESSION, ")"| STATEMENT ;<br />
IF = "if","(", RelEXPRESSION, ")"| STATEMENT ,  ( λ |  ( "else" | STATEMENT));<br />
PRINT = "show_me_what_you_got", "(", RelEXPRESSION, ")";<br />
RelEXPRESSION = EXPRESSION, { ("==" | "mortyer_than" | "rickier_than"), EXPRESSION } ;<br />
EXPRESSION = TERM, { ("+" | "-" | "||"), TERM } ;<br />
TERM = FACTOR, { ("*" | "/" | "&&"), FACTOR } ;<br />
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", RelEXPRESSION, ")" | IDENTIFIER | ("Read", "(", ")");<br />
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;<br />
NUMBER = DIGIT, { DIGIT } ;<br />
LETTER = ( a | ... | z | A | ... | Z ) ;<br />
STRING = '"', (LETTER | DIGIT), '"';
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;<br />
