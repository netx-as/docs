import os
import re
import glob

NETC_ACTUAL_DIR = "netc-actual"
DOCS_DIR = "docs"
OUTPUT_FILE = os.path.join(DOCS_DIR, "cli", "command-reference.md")

command_tree = {}

PLACEHOLDERS = {
    '%IF': '<interface>',
    '%IFS': '<interfaces>',
    '%IP': '<ip-address>',
    '%IP4': '<ipv4-address>',
    '%IP4PORT': '<ipv4:port>',
    '%NET4': '<ipv4/mask>',
    '%NET4DHCP': '<ipv4/mask|dhcp>',
    '%IP6': '<ipv6-address>',
    '%IP6PORT': '<ipv6.port>',
    '%NET6': '<ipv6/mask>',
    '%NET': '<ip-prefix>',
    '%PORTRANGE': '<port-range>',
    '%MAC': '<mac-address>',
    '%STR': '<string>',
    '%COL': '<collection>',
    '%HOST': '<host>',
    '%CRYPT': '<crypt>',
    '%NUM': '<number>',
    '%NUMH': '<number-with-unit>',
    '%NUMS': '<numbers>',
    '%NUMCS': '<numbers-comma>',
    '%SEC': '<seconds>',
    '%HHMM': '<hh:mm>',
    '%HEX': '<hex>',
    '%HEXMASK': '<hex/mask>',
    '%LOGAMOUNT': '<log-amount>',
    '%QDISC': '<qdisc>',
    '%EMAIL': '<email>',
}

def format_key(key):
    return PLACEHOLDERS.get(key, key)

def add_to_tree(path, description, ops=None):
    parts = path.split('/')
    current = command_tree
    for part in parts:
        if part not in current:
            current[part] = {'_children': {}, '_desc': None, '_ops': set()}
        if part == parts[-1]:
            if description:
                current[part]['_desc'] = description
            if ops:
                current[part]['_ops'].update(ops)
        current = current[part]['_children']

def parse_yaml_files():
    files = glob.glob(os.path.join(NETC_ACTUAL_DIR, "netc.d", "*.yml"))
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
            docs = content.split('---')
            for doc in docs:
                if not doc.strip():
                    continue
                
                lines = doc.strip().split('\n')
                node = None
                descr = None
                ops = set()
                
                in_options = False
                current_opt_type = None
                current_opt_name = None
                parsed_options = {}

                for line in lines:
                    stripped = line.strip()
                    if not stripped:
                        continue
                        
                    indent = len(line) - len(line.lstrip())
                    
                    if stripped.startswith('OPTIONS:'):
                        in_options = True
                        continue
                    
                    if in_options:
                        if indent == 0:
                            in_options = False
                        else:
                            if indent == 4:
                                key = stripped.split(':')[0].strip()
                                if key in ['SET', 'GET', 'SHOW', 'UNSET']:
                                    current_opt_type = key
                                else:
                                    current_opt_type = None
                                current_opt_name = None
                            elif indent == 8:
                                if current_opt_type:
                                    current_opt_name = stripped.split(':')[0].strip()
                                    if current_opt_name not in parsed_options:
                                        parsed_options[current_opt_name] = {'desc': None, 'value': None, 'ops': set()}
                                    
                                    op_category = 'Config' if current_opt_type in ['SET', 'GET', 'UNSET'] else 'Info'
                                    if current_opt_type == 'SHOW':
                                        op_category = 'Info'
                                    
                                    parsed_options[current_opt_name]['ops'].add(op_category)
                            elif indent == 12:
                                if current_opt_name:
                                    if stripped.startswith('VALUE:'):
                                        val = stripped.split(':', 1)[1].strip().strip("'")
                                        parsed_options[current_opt_name]['value'] = val
                                    elif stripped.startswith('DESCR:'):
                                        val = stripped.split(':', 1)[1].strip().strip("'")
                                        parsed_options[current_opt_name]['desc'] = val
                            continue

                    if stripped.startswith('NODE:'):
                        node = stripped.split(':', 1)[1].strip().strip("'")
                    elif stripped.startswith('DESCR:'):
                        descr = stripped.split(':', 1)[1].strip().strip("'")
                    
                    if re.match(r'^\s*SET:', stripped):
                        ops.add('Config')
                    if re.match(r'^\s*SHOW:', stripped):
                        ops.add('Info')
                    if re.match(r'^\s*GET:', stripped):
                        ops.add('Config')

                if node:
                    add_to_tree(node, descr, ops)
                    for opt_name, opt_data in parsed_options.items():
                        opt_node = f"{node}/{opt_name}"
                        if opt_data['value']:
                            add_to_tree(opt_node, None, opt_data['ops'])
                            val_node = f"{opt_node}/{opt_data['value']}"
                            add_to_tree(val_node, opt_data['desc'], opt_data['ops'])
                        else:
                            add_to_tree(opt_node, opt_data['desc'], opt_data['ops'])

def parse_config_pm():
    config_path = os.path.join(NETC_ACTUAL_DIR, "lib", "NetC", "Config.pm")
    if not os.path.exists(config_path):
        print(f"Config.pm not found at {config_path}")
        return

    with open(config_path, 'r') as f:
        lines = f.readlines()

    stack = [] # List of (level, key)
    level = 0
    in_root = False
    
    key_regex = re.compile(r"'([^']+)'\s*=>\s*\{")
    descr_regex = re.compile(r"DESCR\s*=>\s*'((?:[^'\\]|\\.)*)'")
    
    set_regex = re.compile(r"\bSET\s*=>")
    unset_regex = re.compile(r"\bUNSET\s*=>")
    show_regex = re.compile(r"\bSHOW\s*=>")
    get_regex = re.compile(r"\bGET\s*=>")
    
    current_ops = set()
    current_descr = None
    
    for line in lines:
        line_content = line.split('#')[0]
        
        if '$NETC_ROOT = {' in line_content:
            in_root = True
            level = 0
            level += line_content.count('{') - line_content.count('}')
            continue
        
        if not in_root:
            continue
            
        if line_content.strip() == '};':
            in_root = False
            break

        open_braces = line_content.count('{')
        close_braces = line_content.count('}')
        
        match = descr_regex.search(line_content)
        if match:
            current_descr = match.group(1).replace("\\'", "'")
            
        if set_regex.search(line_content):
            current_ops.add('Config')
        # if unset_regex.search(line_content):
        #     current_ops.add('UNSET')
        if show_regex.search(line_content):
            current_ops.add('Info')
        if get_regex.search(line_content):
            current_ops.add('Config')

        match = key_regex.search(line_content)
        if match:
            key = match.group(1)
            if key != 'CHILD':
                stack.append((level + 1, key))
                
        if stack:
            path = "/".join([k for l, k in stack])
            if current_descr or current_ops:
                add_to_tree(path, current_descr, current_ops)
                current_descr = None
                current_ops = set()

        level += open_braces
        level -= close_braces
        
        while stack and stack[-1][0] > level:
            stack.pop()


def print_tree(node, level=0, file_handle=None):
    indent = "  " * level
    for key, value in sorted(node.items()):
        if key.startswith('_'):
            continue
            
        # Start with current node info
        full_display_str = f"**{format_key(key)}**"
        current_desc = value.get('_desc', '')
        current_ops = value.get('_ops', set()).copy()
        current_children = value.get('_children', {})
        
        # Check if we can merge children
        while len(current_children) == 1:
            child_key = list(current_children.keys())[0]
            child_value = current_children[child_key]
            
            # Append child key, bolded
            full_display_str += f" **{format_key(child_key)}**"
            
            # Update ops
            current_ops.update(child_value.get('_ops', set()))
            
            # Update desc (child overrides parent if present)
            if child_value.get('_desc'):
                current_desc = child_value.get('_desc')
            
            # Move to next level
            current_children = child_value.get('_children', {})
        
        ops_str = ""
        if current_ops:
            ops_list = sorted(list(current_ops))
            ops_str = f" `[{', '.join(ops_list)}]`"
        
        if current_desc:
            file_handle.write(f"{indent}- {full_display_str}{ops_str}: {current_desc}\n")
        else:
            file_handle.write(f"{indent}- {full_display_str}{ops_str}\n")
            
        if current_children:
            print_tree(current_children, level + 1, file_handle)

def main():
    parse_yaml_files()
    parse_config_pm()
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write("# Netc Command Reference\n\n")
        f.write("This document is auto-generated from the source code.\n\n")
        f.write("Operations: `[Config]` = Configuration command, `[Info]` = Information/Status command (using show command)\n\n")
        print_tree(command_tree, file_handle=f)
    
    print(f"Documentation generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
