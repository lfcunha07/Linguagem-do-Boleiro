# Linguagem do Boleiro
## Aproveitando o ritmo de copa, apresentamos a mais nova linguagem de programação, a linguagem do boleiro. Para os "juvenas", segue um [link](https://www.torcedores.com/noticias/2016/06/19-expressoes-que-so-quem-e-muito-boleiro-entende) com os as gírias e seus respectivos significados para refência.
---
## EBNF
```C#
PROGRAM = DECLARATION;
DECLARATION = "regulamento", IDENTIFIER, "(", DEFINITION, ")", (λ, "->", TYPE), BLOCK;
STATEMENT = ( λ | ASSIGMENT | FUNCTION | PRINT | DEFINITION , ";") | ( RETURN | WHILE | IF | BLOCK) | ";";

ASSIGNMENT = IDENTIFIER, "=", REL_EXPRESSION;
FUNCTION = IDENTIFIER, "(", (REL_EXPRESSION | IDENTIFIER), [{",", (REL_EXPRESSION | IDENTIFIER)}], ")";
PRINT = "explana", "(", REL_EXPRESSION, ")";
DEFINITION = "jogador", IDENTIFIER, [{",", IDENTIFIER}], ":", TYPE;
RETURN = "recua", REL_EXPRESSION;
WHILE = "enquanto", "(", REL_EXPRESSION, ")", STATEMENT;
IF = "resenha", "(", REL_EXPRESSION, ")", STATEMENT, "ramelou";
BLOCK = "{", { STATEMENT }, "}";

REL_EXPRESSION = EXPRESSION, { ( "<" | ">" | "==" ), EXPRESSION};
EXPRESSION = TERM, { ("+" | "-" | "ou"), TERM };
TERM = FACTOR, { ("*" | "/" | "e" ), FACTOR };
FACTOR = (("+" | "-" | "nao" ), FACTOR) | NUMBER | STRING | "(", REL_EXPRESSION, ")" | IDENTIFIER | IDENTIFIER, "(", (REL_EXPRESSION | IDENTIFIER), [{",", (REL_EXPRESSION | IDENTIFIER)}], ")" | READ;
READ = "faz_teu_nome", "(", ")";
IDENTIFIER = LETTER, { LETTER | "_" | DIGIT};

TYPE = ("numero" | "nome");
NUMBER = DIGIT, { DIGIT };
STRING = ("" | ", LETTER, ");

LETTER = ( a | ... | z | A | ... | Z );
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0);
```
---
## Exemplo
```C#
# Método de tes com todos os comandos

regulamento soma(x: i32, y: i32) -> i32{
    recua x + y;
}

regulamento Main(){
// v2.3 testing
jogador x_1: i32;
x_1 = 2;
x_1 = soma(1, x_1);

x_1 = faz_teu_nome();
resenha ((x_1 > 1) && !(x_1 < 1)) {
    x_1 = 3;
}
ramelou {
    {
    x_1 = (-20+30)*4*3/40;;;;; // teste de comentario
    }
}
explana(x_1);
x_1 = faz_teu_nome();
resenha ((x_1 > 1) && !(x_1 < 1))
    x_1 = 3;
ramelou
    x_1 = (-20+30)*12/40;;;;;

explana(x_1);
enquanto ((x_1 > 1) || (x_1 == 1)) {x_1 = x_1 - 1;explana(x_1);}}
```