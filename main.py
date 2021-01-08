'''
# File: main.py
# Project: tp2
# File Created: Monday, 4th January 2021 9:26:30 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Friday, 8th January 2021 2:57:28 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2021 MIT, Institue de neurosciences de la Timone
'''

from argparse import ArgumentParser
from src import writer

def parse_cli():
    """
    CLI command line

    Returns:
        [parser]: [CLI CMD]
    """
    parser = ArgumentParser(description='Hide message in png file .')
    parser.add_argument('-w', help = 'write a message in picture', action = "store_true")
    parser.add_argument('-i', help = 'input file')
    parser.add_argument('-f', help = 'file with text ')
    parser.add_argument('-t', help = 'msg to write')

    return parser.parse_args()

def main():
    """
    usage: main.py [-h] [-w] [-i I] [-f F] [-t T]

    Hide message in png file .

    optional arguments:
    -h, --help  show this help message and exit
    -w          write a message in picture
    -i I        input file
    -f F        file with text
    -t T        msg to write

    Example : 
        >>>>
    """
    args = parse_cli()
    if args.w :
        if args.t :
            writer.writeFunction(args.t,args.i)
        elif args.f :
            filename = open(args.f)
            text = filename.read()
            writer.writeFunction(text,args.i)
        else :
            text = input("Write your text to hide here : ")
            writer.writeFunction(text,args.i)
    else :
        messageDecrypt = writer.readFunction()
        print("Le message décrypter est : ", messageDecrypt)
    
if __name__ == '__main__':
    main()
