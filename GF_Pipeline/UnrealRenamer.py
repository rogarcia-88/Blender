import re

name = name_var
index = index_var

resolved_find_pattern = eval( "f'"+find_pattern+"'") if allow_wildcards else find_pattern
resolved_replace_pattern = eval( "f'"+replace_pattern+"'") if allow_wildcards else replace_pattern

flags = 0 if case_sensitive else re.IGNORECASE

if from_right:
    output = re.sub (
        pattern=resolved_find_pattern[::-1],
        repl=resolved_replace_pattern[::-1],
        string=source_string[::-1],
        count=count,
        flags=flags,
)[::-1]

    
else:
    
    output = re.sub (
        pattern=resolved_find_pattern,
        repl=resolved_replace_pattern,
        string=source_string,
        count=count,
        flags=flags,
)


