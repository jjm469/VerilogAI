<<<<<<< HEAD
#========================================================================
# Package containing all scripts used in dataset generation scripts 
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

=======
#========================================================================
# Package containing all scripts used in dataset generation scripts 
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

>>>>>>> 85397b349e72263acf5f4bdbe065b66df470343f
