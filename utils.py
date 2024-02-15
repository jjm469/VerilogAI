from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser

try:
    from StringIO import StringIO
except:
    from io import StringIO

import pyverilog
from pyverilog.vparser.parser import parse
from pyverilog.vparser.parser import VerilogCodeParser


#========================================================================
# Package containing helper functions used in dataset generation scripts 
#========================================================================

"""
split_string is a function shortens long strings to have a max of 80 
characters per line. Does not split words.
"""
def split_string(string):
    if len(string) <= 80:
        return string
    else:
        split_idx = string[:80].rfind(' ')
        if split_idx == -1:
            split_idx = 80
        return string[:split_idx] + '\n' + split_string(string[split_idx+1:])

"""
generate abstract syntax tree for determining dependencies
"""

def parse(file):
    INFO = "Verilog code parser"
    VERSION = pyverilog.__version__
    USAGE = "Usage: python example_parser.py file ..."

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    optparser = OptionParser()
    optparser.add_option("-v", "--version", action="store_true", dest="showversion",
                         default=False, help="Show the version")
    optparser.add_option("-I", "--include", dest="include", action="append",
                         default=[], help="Include path")
    optparser.add_option("-D", dest="define", action="append",
                         default=[], help="Macro Definition")
    (options, args) = optparser.parse_args()

    filelist = [file]
    if options.showversion:
        showVersion()

    for f in filelist:
        if not os.path.exists(f):
            raise IOError("file not found: " + f)

    if len(filelist) == 0:
         showVersion()

    parser = VerilogCodeParser(filelist,
                               preprocess_include=options.include,
                               preprocess_define=options.define)
    
    ast = parser.parse()
    directives = parser.get_directives()

    output = StringIO()
    ast.show(buf=output)

    for lineno, directive in directives:
        output.write('Line %d : %s' % (lineno, directive))
    
    rslt = output.getvalue()

    print(rslt)

    with open("ast.txt", "w") as file:
        file.write(rslt)
    
    return rslt