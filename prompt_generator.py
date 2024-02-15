import openai
import os
from utils import *

# Uses openai API to open a verilog file, extract the code, and generate
# a description of the provided code. It then takes the generated
# description and appends it to the top of the file.

#========================================================================
# LOCAL PARAMETERS
#========================================================================

MAX_TOKENS = 2000
API_KEY = input("Enter your OpenAI API key: ")
TEMPERATURE = 0
FOLDER = input("Enter a folder containing the Verilog files to be used: ")
PROMPT = "I have supplied you with a block of Verilog code. Give an explanation of the expected behavior as well as any important design details. At the end of your explanation, be sure to provide the module name, the port list, as well as any parameters. Also, do not rewrite the supplied code in the description or give your own implementation of the supplied verilog code. It is extremely important you do not give an implementation of the described code or rewrite the provided code. The end result should have a description of the code as well as the module name, port list, and parameters."
# SAMPLE_RESPONSE = "This Verilog code defines module named [MODULE NAME], which has [X NUMBER OF INPUT PORTS] including 4 single-bit data inputs, a, b, c, and d, and 2 single-bit select inputs, s0 and s1, and a single-bit output port, out, which represents the selected input. The assign statement inside the module assigns the selected input value to the out output based on the s0 and s1 input values. If s1 is 1, then the value of out is either c or d, depending on the value of s0, and if s1 is 0, then the value of out is either a or b, again depending on the value of s0. Finally, the out output is declared as a reg type. multiplexer(a, b, c, d, s0, s1, out);input a, b, c, d; input s0, s1; output out; reg out;"

print("========================================================================")
print("OpenAI Models")
print("1 - gpt-3.5-turbo")
print("2 - text-davinci-003")
print("========================================================================")

model_choice = input("Select an OpenAI model (input the corresponding number for the desired model): ")
if model_choice == "1":
    OPENAI_MODEL = "gpt-3.5-turbo"
elif model_choice == "2":
    OPENAI_MODEL = "text-davinci-003"
else:
    print("Invalid model choice. Using default model 'gpt-3.5-turbo'.")
    OPENAI_MODEL = "gpt-3.5-turbo"

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
            # print(response)

        file.seek(0, 0)
        file.write( NEW_PROMPT + "\n" + "\n" + "// CODE: " + "\n" + content)
