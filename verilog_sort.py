import os
import utils
import shutil

# Script to extract valid verilog modules from Huggingface repo. Verilog 
# modules must comply with the following criteria:
# - Must not be from Skywater PDK
# - Must not contain instanciations of other modules 
# - Must not be a duplicate
# - Must contain an Always block
# - Must contain all legal characters (for parsing)
# Script outputs a log file that keeps track of removed modules as well as
# the reason they were removed. Removed files stored in REMOVED_DIR and 
# extracted, valid files stored in TARGET_DIR. 

#========================================================================
# LOCAL PARAMETERS
#========================================================================

NUM_FILES = 0                                      # number of modules currently copied
VALID_MODULE = False                               # flag to indicate if the current module is valid
DUP_MODULES = []                                   # list to track duplicate modules
REMOVED_DUPS = 0                                   # variable to track duplicates removed
REMOVED_SkyWater = 0                               # variable to track SkyWater Modules removed 
REMOVED_DEPENDENT = 0                              # variable to keep track of modules with external dependencies (I.e. they instanciate submodules)
REMOVED_MULTIPLE = 0               
ERROR = 0 
SOURCE_DIR = 'output_files'
# SOURCE_DIR = 'test'
TARGET_DIR = 'verilog'
REMOVED_DIR = 'removed'
INFRACTION_LIST = []

if(os.path.exists(TARGET_DIR)):
    shutil.rmtree(TARGET_DIR)
os.mkdir(TARGET_DIR)

if(os.path.exists(REMOVED_DIR)):
    shutil.rmtree(REMOVED_DIR)
os.mkdir(REMOVED_DIR)

count = 1

for root, dirs, files in os.walk(SOURCE_DIR, topdown=True):
    with open("file_check.txt", "w") as file:
        if(count == 1):
            file.write(str(files))
            file.write('*' + str(len(files)))
            count = 0
    for file in files:
        VALID_MODULE = True
        INFRACTION = "None"
        file_path = SOURCE_DIR + '/' + str(file)
        print(file_path)
        try:
            x = utils.parse(file_path)
            # if(x.find("InstanceList") != -1):
            if(x.find("InstanceList") != -1 or x.find("Always") == -1):
                VALID_MODULE = False
                shutil.copy(file_path, REMOVED_DIR)
                REMOVED_DEPENDENT += 1
                INFRACTION = "Dependent"
            elif(x.count("ModuleDef")>1 or x.count("ModuleDef") == 0):
                VALID_MODULE = False
                shutil.copy(file_path, REMOVED_DIR)
                REMOVED_MULTIPLE += 1
                INFRACTION = "Multiple"
        except:
            VALID_MODULE = False
            ERROR += 1
            INFRACTION = "Error"
            pass
    
        if(VALID_MODULE):
            try:
                with open(file_path, 'r') as verilog_file:
                    CURR_MODULE = verilog_file.read()

                    if CURR_MODULE in DUP_MODULES:
                        VALID_MODULE = False
                        REMOVED_DUPS += 1
                        INFRACTION = "Duplicate"

                    if (VALID_MODULE and (CURR_MODULE.find('SkyWater')!=-1 or CURR_MODULE.find('SKYWATER')!=-1 or CURR_MODULE.find('skywater')!=-1)):
                        VALID_MODULE = False
                        REMOVED_SkyWater += 1 
                        INFRACTION = "Skywater"

                    if (VALID_MODULE):
                        DUP_MODULES.append(CURR_MODULE)
                        NUM_FILES += 1
                        shutil.copy(file_path,TARGET_DIR)
                    else:
                        shutil.copy(file_path,REMOVED_DIR)
                    verilog_file.close()
            except Exception as e:
                print('Error processing row:','Error message:', str(e))

        if(VALID_MODULE is False):
            INFRACTION_LIST.append(file_path + "Infraction: " + INFRACTION)

    

if os.path.exists("log.txt"):
    os.remove("log.txt")

with open("log.txt", 'w') as log:
    for infraction in INFRACTION_LIST:
        log.write(infraction + '\n')
    log.close()
    
print('Number of unique modules extracted:', NUM_FILES)
print('Number of duplicate modules removed:', REMOVED_DUPS)
print('Number of SkyWater modules removed:', REMOVED_SkyWater)
print('Number of dependent modules removed:', REMOVED_DEPENDENT)
print('Number of files containing multiple module declarations removed:', REMOVED_MULTIPLE)
print('Number of files containing MISC errors: ', ERROR)
print('Number of total modules removed:', REMOVED_SkyWater + REMOVED_DUPS + REMOVED_DEPENDENT + REMOVED_MULTIPLE+ ERROR)


# Clean-up temp files

if os.path.exists("ast.txt"):
    os.remove("ast.txt")

if os.path.exists("parser.out"):
    os.remove("parser.out")

if os.path.exists("parsetab.py"):
    os.remove("parsetab.py")

if os.path.exists("file_check.txt"):
    os.remove("file_check.txt")







