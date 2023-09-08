def format_diff(diff, depth=0, indent=4):
    result = ""
    prefix = " " * depth * indent
    opening_bracket = "{"
    closing_bracket = "}"

    for node in diff:
        key = node['key']
        status = node['status']

        if status == 'nested':
            children = format_diff(node['children'], depth + 1, indent)
            result += f"{prefix}  {key}: {opening_bracket}\n{children}\n{prefix}  {closing_bracket},\n"
        else:
            value = node.get("value", "")
            if isinstance(value, str):
                value = f'{value}'
            if status == 'unchanged':
                result += f"{prefix}  {key}: {value},\n"
            elif status == 'changed':
                old_value = node.get("old_value", "")
                new_value = node.get("new_value", "")
                if isinstance(old_value, str):
                    old_value = f'"{old_value}"'
                if isinstance(new_value, str):
                    new_value = f'"{new_value}"'
                result += f"{prefix}- {key}: {old_value}\n{prefix}+ {key}: {new_value},\n"
            elif status == 'removed':
                result += f"{prefix}- {key}: {value},\n"
            elif status == 'added':
                result += f"{prefix}+ {key}: {value},\n"

    result = result.rstrip(',\n')  # Remove trailing comma and newline
    return result


































































































