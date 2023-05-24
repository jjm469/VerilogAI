import openai
import os

#========================================================================
# LOCAL PARAMETERS
#========================================================================

MAX_TOKENS = 2000
API_KEY = ""
TEMPERATURE = 0
FOLDER = "finetune_verilog(davinci)"
# OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MODEL = "text-davinci-003"
PROMPT = "I have supplied you with a block of Verilog code. Give an in-depth explanation of what the code does. At the end of your explanation, be sure to write the following "'module MODULE_NAME(INPUTS/OUTPUTS)'". Change "'MODULE_NAME'", "'INPUTS/OUTPUTS'" with the repective module name, inputs, and outputs for the supplied verilog code. Also, do not rewrite the supplied code in the description or give your own implementation of the supplied verilog code."
SAMPLE_RESPONSE = "This Verilog code defines a 4:1 multiplexer module named multiplexer, which has six input ports including 4 single-bit data inputs, a, b, c, and d, and 2 single-bit select inputs, s0 and s1, and a single-bit output port, out, which represents the selected input. The assign statement inside the module assigns the selected input value to the out output based on the s0 and s1 input values. If s1 is 1, then the value of out is either c or d, depending on the value of s0, and if s1 is 0, then the value of out is either a or b, again depending on the value of s0. Finally, the out output is declared as a reg type. multiplexer(a, b, c, d, s0, s1, out);input a, b, c, d; input s0, s1; output out; reg out;"

#========================================================================
# split_string is a function shortens long strings to have a max of 80
# characters per line. Does not split words.
#========================================================================

def split_string(string):
    if len(string) <= 80:
        return string
    else:
        split_idx = string[:80].rfind(' ')
        if split_idx == -1:
            split_idx = 80
        return string[:split_idx] + '\n' + split_string(string[split_idx+1:])

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

        if (OPENAI_MODEL == "text-davinci-003"):
            response = openai.Completion.create(
                engine= OPENAI_MODEL,
                prompt= PROMPT + str(content),
                max_tokens=MAX_TOKENS,
                temperature = TEMPERATURE
                )
            NEW_PROMPT = '/* PROMPT: Generate Verilog code fitting the provided description' + "\n" + split_string(response.choices[0].text) + "\n" + "*/"
            print(response.choices[0].text)

        else:
            message = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are describing code to help with AI finetuning prompt generation. You do no write your own implementation"},
                    {"role": "user", "content": PROMPT + str(content)},
                    # {"role": "assistant", "content": SAMPLE_RESPONSE},
                ]
            )
            response = message['choices'][0]['message']['content']
            NEW_PROMPT = '/* PROMPT: Generate Verilog code fitting the provided description' + "\n" + split_string(response) + "\n" + "*/"
            print(response)

        file.seek(0, 0)
        file.write( NEW_PROMPT + "\n" + "\n" + "// CODE: " + "\n" + content)



# TODOS
# - Add Try-Except for token sizes. There is a way to get the #tokens used relative to the cap.
