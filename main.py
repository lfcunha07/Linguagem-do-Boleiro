import sys
from utils import ExpressionParser
from tokens import *

def main():

    st = SimbolTable()

    with open(sys.argv[1], "r") as file:
        ExpressionParser.run(file.read()).evaluate(st)
if __name__ == "__main__":
    main()