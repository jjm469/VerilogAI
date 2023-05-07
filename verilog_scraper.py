import os
from github import Github

#========================================================================
# LOCAL PARAMETERS
#========================================================================

g = Github("")                                             # Create a PyGithub object with Github API token
query = "language:verilog"                                 # Define the search query
results = g.search_repositories(query)                     # Search for repositories matching the query
MAX_FILES_PER_TEXT_FILE = 1000                             # Define the maximum number of files per text file
FILE_COUNT = 0                                             # Initialize the file count and text file index
TEXT_FILE_INDEX = 1

#========================================================================
# Uses the GitHub API to collect Verilog code from public repos
#========================================================================

if not os.path.exists("text_files"):
    os.mkdir("text_files")

for repo in results:
    repo_clone = g.get_repo(repo.full_name)                             # Loop through the files in the repository                
    for content_file in repo_clone.get_contents(""):                    # Check if the file is a Verilog file
        if content_file.name.endswith(".v"):
            try:
                file_content = content_file.decoded_content.decode('utf-8')
                with open(f"text_files/text_file_{TEXT_FILE_INDEX}.txt", "a", encoding="utf-8") as f:
                    f.write(file_content)
                FILE_COUNT += 1
                if FILE_COUNT >= MAX_FILES_PER_TEXT_FILE:
                    FILE_COUNT = 0
                    TEXT_FILE_INDEX += 1
            except:
                try: 
                    file_content = content_file.decoded_content.decode('base64')
                    with open(f"text_files/text_file_{TEXT_FILE_INDEX}.txt", "ab") as f:
                        f.write(file_content)
                    FILE_COUNT += 1
                    if FILE_COUNT >= MAX_FILES_PER_TEXT_FILE:
                        FILE_COUNT = 0
                        TEXT_FILE_INDEX += 1
                except:
                    print("failed")                                     # Print when neither utf-8 or base64 encoding works
                

