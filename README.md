# PickleRick Programming Language
![Rick Image](https://github.com/MalcerOne/my_own_programming_language/blob/main/imgs/rickimage.png?raw=true)
Programming Language created by my own, based in the TV series Rick and Morty. Compiler made with Python in the class of Logica da Computação (Computer Logic), at Insper

# Testes
Para realizar os testes, temos as pastas ./tests com os arquivos .txt utilizados para testar se a linguagem esta funcionando e o compilador esta conseguindo compilar tal codigo. Para isso:
```terminal
python3 main.py /tests/teste1.txt
```
Se o output dessa execucao for igual ao ./outputs/output1.txt, esta tudo certo.

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

# Credito
Rafael Seicali Malcervelli<br />
7 semestre - Engenharia de Computacao - Insper
