import csv
csv.field_size_limit(100000000)

#========================================================================
# LOCAL PARAMETERS
#========================================================================

NOT_SORTED_MODULES = open('not-sorted.txt', 'x')   # File to hold unsorted module
SORTED_MODULES = open('sorted.txt', 'x')           # File to hold sorted modules
NUM_FILES = 0                                      # number of modules currently copied
VALID_MODULE = False                               # flag to indicate if the current module is valid
DUP_MODULES = []                                   # list to track duplicate modules
REMOVED_DUPS = 0                                   # variable to track duplicates removed
REMOVED_SkyWater = 0                               # variable to track SkyWater Modules removed 
REMOVED_DEPENDENT = 0                              # variable to keep track of modules with external dependencies (I.e. they instanciate submodules)
SPACE_LIMIT=50                                     # Threshold for what is deemed a dependency vs independent instances of '.' and '()' 
VIOLATED_INDICES = []                              
INPUT_SET = 'Verilog_bigquery_GitHub.csv'

#========================================================================
# Goes through the INPUT_SET and removed duplicates, Skywater modules, 
# and modules with dependencies. Prints the number of files removed 
# to the terminal at the end. 
# Explanation of the dependent module removal process: 
# Consider the following line of Verilog code, 
# .submodule_input                    (module_input)
# The "." is at index 0
# The ")" is at index 49
# abs(index of . - index of )) = 49
# space_limit = 50 so this module is discarded
# Note, increasing the space limit increases the risk of deleting a 
# module that doesn't have dependencies. For example, if the doc spec has 
# a ".", "(", and ")" within 50 characters of each other, it will be marked 
# as dependent and removed. 
#========================================================================

with open(INPUT_SET, 'r', encoding='utf-8', errors='ignore') as file:
    reader = csv.reader(file)
    try:
        for row in reader:
            for i in row:
                try:
                    VALID_MODULE = True
                    CURR_MODULE = i
                    DEPENDENCY = False

                    # valid modules end with 'endmodule'
                    if CURR_MODULE.find('endmodule') != -1:

                        # If this module has already been extracted, set flag to false
                        if CURR_MODULE in DUP_MODULES:
                            VALID_MODULE = False
                            REMOVED_DUPS += 1

                        # If the module is from the SkyWater PDK, remove it
                        if (VALID_MODULE and CURR_MODULE.find('SkyWater')!=-1):
                            VALID_MODULE = False
                            REMOVED_SkyWater += 1 

                        # Used to detect submodules. 
                        if (VALID_MODULE):

                            dot_list = []
                            close_bracket_list = []

                            for i in range(len(CURR_MODULE)):
                                if CURR_MODULE[i] == ".":
                                    dot_list.append(i)
                                elif CURR_MODULE[i] == ")":
                                    close_bracket_list.append(i)

                            for i in dot_list:
                                for j in close_bracket_list:
                                    if(abs(i-j) < SPACE_LIMIT):
                                        if(CURR_MODULE[i:j+1].find('(')!=-1):
                                            VIOLATED_INDICES.append(CURR_MODULE[i:j+1])
                                            DEPENDENCY = True
                                            break

                            if(DEPENDENCY):
                                VALID_MODULE = False
                                REMOVED_DEPENDENT += 1

                            dot_list = []
                            close_bracket_list = []
                            VIOLATED_INDICES = []

                        # Will add module name to list if it is new
                        if (VALID_MODULE and CURR_MODULE.find('SkyWater')==-1):
                            NOT_SORTED_MODULES.write(CURR_MODULE + '\n')
                            DUP_MODULES.append(CURR_MODULE)
                            NUM_FILES += 1

                        CURR_MODULE = []
                except Exception as e:
                    print('Error processing row:','Error message:', str(e))

    except Exception as e:
        print('Error reading CSV file:', str(e))
    finally:
        print('Number of unique modules extracted:', NUM_FILES)
        print('Number of duplicate modules removed:', REMOVED_DUPS)
        print('Number of SkyWater modules removed:', REMOVED_SkyWater)
        print('Number of dependent modules removed:', REMOVED_DEPENDENT)
        print('Number of total modules removed:', REMOVED_SkyWater + REMOVED_DUPS + REMOVED_DEPENDENT)
        NOT_SORTED_MODULES.close()

Sort= sorted(DUP_MODULES, key=len)

for i in Sort:
    SORTED_MODULES.write(i + '\n')
SORTED_MODULES.close()
