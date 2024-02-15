import os

#========================================================================
# LOCAL PARAMETERS
#========================================================================

MODULE_NAME_LIMIT = 10
FAILED_RETRIVALS = 0
REMOVED_MODULES = 0
INPUT_SET = 'dataset.txt'

#========================================================================
# Goes through the INPUT_SET .txt and seperates all the provided 
# verilog code into its own .txt named after the module name of the code
# block. The scipts prints the number of failed retriavals in the terminal.
#========================================================================

if not os.path.exists("verilog"):
    os.mkdir("verilog")

with open(INPUT_SET, "r") as f:
    contents = f.read()
    
modules = contents.split("endmodule")

for module in modules:
    module_index = module.find("module")
    open_paren_index = module.find("(", module_index)
    name = module[module_index + len("module"):open_paren_index]
    name = name.replace("#", "")
    name = name.replace("/", "")
    name = name.replace (" ", "")

    if(len(name) < MODULE_NAME_LIMIT):
        try:
            with open(f"verilog/{name}.v", "w") as f:
                end_index = module.find('endmodule')
                f.write(module[:end_index]+ "\n" + 'endmodule')
        except:
            end_index = module.find('endmodule')
            FAILED_RETRIVALS+=1
            print("Error rewriting module number: "+ str(FAILED_RETRIVALS))
    else:
        end_index = module.find('endmodule')
        REMOVED_MODULES += 1 

print('Number of failed retrivals = ' + str(FAILED_RETRIVALS))
print('Number of modules removed because module name was too long = '+ str(REMOVED_MODULES))
