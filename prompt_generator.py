import openai
import os

#========================================================================
# LOCAL PARAMETERS
#========================================================================

MAX_TOKENS = 3000
API_KEY = 
TEMPERATURE = 0
FOLDER = "finetune_verilog"
PROMPT = "I have supplied you with a block of Verilog code. Please explain what the code does. At the end of your explanation, be sure to write the following "'module MODULE_NAME(INPUTS/OUTPUTS)'". Change "'MODULE_NAME'", "'INPUTS/OUTPUTS'" with the repective module name, inputs, and outputs for the supplied verilog code. Do not also put this at the beginning of the explanation."

#========================================================================
# split_string is a function shortens long strings to have a max of 80
# characters per line.
#========================================================================

def split_string(string):
    if len(string) <= 80:
        return string
    else:
        return string[:80] + '\n' + split_string(string[80:])


#========================================================================
# Uses openai API to open a verilog file, extract the code, and generate
# a description of the provided code. It then takes the generated
# description and appends it to the top of the file.
#========================================================================

openai.api_key = API_KEY
for filename in os.listdir(FOLDER):
    file_path = os.path.join(FOLDER, filename)

    with open(file_path, "r+") as file:
        content = file.read()
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt= PROMPT + str(content),
            max_tokens=MAX_TOKENS,
            temperature = TEMPERATURE
            )

        NEW_PROMPT = '/* PROMPT: Generate Verilog code fitting the provided description' + "\n" + split_string(response.choices[0].text) + "\n" + "*/"
        file.seek(0, 0)
        file.write( NEW_PROMPT + "\n" + "// CODE: " + "\n" + content)
        print(response.choices[0].text)
