"""Sanity

Usage:
  sanity.py -h | --help
  sanity.py --version
  sanity.py sanity (--i <input>) (--o <output>) (--f <function>)

Options:
  -h --help     Show this screen.
  --version     Show version.
  --i            Sanity Input Bucket
  --o            Sanity Output Bucket
  --f            Function Name

"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='sanity 1.0')
    #print(arguments)
    #print(arguments.get('<input>'))
    #print(arguments.get('<output>'))
    #print(arguments.get('<function>'))
    input_bucket = arguments.get('<input>')
    output_bucket = arguments.get('<output>')
    function_name = arguments.get('<function>')