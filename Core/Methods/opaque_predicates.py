import random

def insert_opaque_predicates(code):
    """
    Insert opaque predicates into the code to make it harder to analyze.
    """
    lines = code.split('\n')
    obfuscated_lines = []
    current_indent = 0
    in_multiline_comment = False
    inside_function = False

    for line in lines:
        stripped_line = line.strip()
        
        # Check for multiline comments
        if stripped_line.startswith('"""') or stripped_line.startswith("'''"):
            in_multiline_comment = not in_multiline_comment

        # Skip empty lines, comments, and lines within multiline comments
        if not stripped_line or stripped_line.startswith("#") or in_multiline_comment:
            obfuscated_lines.append(line)
            continue

        # Update current indentation level
        current_indent = len(line) - len(line.lstrip())

        # Detect if inside a function definition
        if stripped_line.endswith(":") and "def " in stripped_line:
            inside_function = True

        # Add the current line
        obfuscated_lines.append(line)

        # Only add opaque predicates after lines ending with ":"
        if stripped_line.endswith(":") and not stripped_line.startswith("class") and inside_function:
            predicate = generate_opaque_predicate(current_indent + 4)  # Increase indent for block contents
            obfuscated_lines.append(predicate)
        elif not stripped_line.endswith(":") and inside_function:
            inside_function = False

    return '\n'.join(obfuscated_lines)

def generate_opaque_predicate(indentation_level):
    """
    Generate an opaque predicate with correct indentation.
    """
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = a + b
    indentation = ' ' * indentation_level
    predicate = f'{indentation}if {a} + {b} != {c}:\n{indentation}    pass  # Opaque Predicate'
    return predicate