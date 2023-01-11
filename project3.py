# project3.py
#
# ICS 33 Fall 2022
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

import grin



def main() -> None:
    lines = []
    line = input()

    while line.strip() != '.':
        lines.append(line)
        line = input()

    end_program = False
    command_list = []

    try:
        command_list = list(grin.parse(lines))
    except Exception as e:
        print(e)
        end_program = True

    if end_program != True:
        grin.execute_command(command_list)


if __name__ == '__main__':
    main()
