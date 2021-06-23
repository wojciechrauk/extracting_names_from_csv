def all_whitespace_to_space(name: str) -> str:
    return ' '.join(name.split())

def convert_to_initials_form(name: str) -> str:
    name_parts = name.split()
    return ' '.join([name_part[0] for name_part in name_parts[:-1]] + [name_parts[-1]])

def convert_to_initial_name_and_surname(name: str) -> str:
    name_parts = name.split()
    if len(name_parts) > 1:
        return f'{name_parts[0][0]} {name_parts[-1]}'
    return name

def delete_dots(name: str) -> str:
    return name.replace('. ', ' ').replace('.', ' ')

def delete_hyphen(name: str) -> str:
    character = '-'
    name_parts = name.rsplit(' ', 1)
    if len(name_parts) < 2:
        return name
    name_parts[0] = name_parts[0].replace(character, ' ')
    return name_parts[0] + ' ' + name_parts[1]
