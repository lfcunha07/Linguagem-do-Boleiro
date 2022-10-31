# Linguagem do Boleiro
## Aproveitando o ritmo de copa, apresentamos a mais nova linguagem de programação, a linguagem do boleiro. Para os "juvenas", segue um [link](https://www.torcedores.com/noticias/2016/06/19-expressoes-que-so-quem-e-muito-boleiro-entende) com os as gírias e seus respectivos significados para refência.
---
## EBNF
```C#
BLOCK = "{", { STATEMENT }, "}"; x 
STATEMENT = ( λ | ASSIGMENT | PRINT | DECLARATION| WHILE | IF | BLOCK | DEFINITION | FUNCTION), ";"; x
ASSIGNMENT = IDENTIFIER, "=", REL_EXPRESSION;
DEFINITION = "regulamento", IDENTIFIER, "(", DECLARATION, ")", STATEMENT;
FUNCTION = IDENTIFIER, "(", (REL_EXPRESSION | IDENTIFIER), [{",", (REL_EXPRESSION | IDENTIFIER)}], ")";
PRINT = "explana", "(", REL_EXPRESSION, ")";
WHILE = "enquanto", "(", REL_EXPRESSION, ")", STATEMENT;
IF = "resenha", "(", REL_EXPRESSION, ")", STATEMENT, "ramelou";
REL_EXPRESSION = EXPRESSION, { ( "<" | ">" | "==" ), EXPRESSION};
EXPRESSION = TERM, { ("+" | "-" | "ou"), TERM };
TERM = FACTOR, { ("*" | "/" | "e" ), FACTOR };
FACTOR = (("+" | "-" | "nao" ), FACTOR) | NUMBER | STRING | "(", REL_EXPRESSION, ")" | IDENTIFIER;
DECLARATION = TYPE, IDENTIFIER, [{IDENTIFIER, ","}];
IDENTIFIER = LETTER, { LETTER | "_" | DIGIT};
NUMBER = DIGIT, { DIGIT };
TYPE = ("numero" | "nome");
LETTER = ( a | ... | z | A | ... | Z );
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0);
```
---
## Exemplo
```C#
# Cria método par identificar se número 10 é par ou ímpar e printa seu resultado

regulamento par_ou_impar(i):
    resenha (i%2==0):
        recua "par"
    ramelou:
        recua "ímpar"

explana(par_ou_impar(10))
```