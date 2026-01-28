from typing import Any


def parse_config(filepath: str) -> dict[str, Any]:

    config: dict[str, Any] = {}
    with open(filepath, "r") as f:

        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                raise ValueError(f"Line {line_num}: Missing '=' separator")
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key in ['WIDTH', 'HEIGHT', 'SEED']:
                try:
                    config[key] = int(value)
                except ValueError:
                    raise ValueError(f"Line {line_num}: {key} must be an "
                                     F"integer, got '{value}'")
            elif key in ['ENTRY', 'EXIT']:
                try:
                    x_str, y_str = value.split(',')
                    config[key] = (int(x_str.strip()), int(y_str.strip()))
                except ValueError:
                    raise ValueError(
                        f"Line {line_num}: {key} must be in "
                        F"format 'x,y', got '{value}'"
                    )
            elif key in ['OUTPUT_FILE', 'ALGORITHM', 'DISPLAY_MODE']:
                config[key] = value
            elif key == 'PERFECT':
                config[key] = value.lower() in ['true', '1', 'yes']
            else:
                print(f"Warning: Unknown key '{key}' on line {line_num}")
                config[key] = value

    return config


def validate_config(config: dict[str, Any]) -> None:

    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                     'OUTPUT_FILE', 'PERFECT']

    missing = []
    for key in required_keys:
        if key not in config:
            missing.append(key)

    if missing:
        raise ValueError(f"Missing required keys: {', '.join(missing)}")
    if config['WIDTH'] <= 0:
        raise ValueError(f"WIDTH must be greater than 0, "
                         f"got {config['WIDTH']}")

    if config['HEIGHT'] <= 0:
        raise ValueError(f"HEIGHT must be greater than 0"
                         f", got {config['HEIGHT']}")

    entry_x, entry_y = config['ENTRY']

    if not (0 <= entry_x < config['WIDTH']):
        raise ValueError(f"ENTRY x={entry_x} out of bounds (must "
                         f"be 0-{config['WIDTH']-1})")

    if not (0 <= entry_y < config['HEIGHT']):
        raise ValueError(f"ENTRY y={entry_y} out of bounds "
                         f"(must be 0-{config['HEIGHT']-1})")

    exit_x, exit_y = config['EXIT']

    if not (0 <= exit_x < config['WIDTH']):
        raise ValueError(f"EXIT x={exit_x} out of bounds "
                         f"(must be 0-{config['WIDTH']-1})")

    if not (0 <= exit_y < config['HEIGHT']):
        raise ValueError(f"EXIT y={exit_y} out of bounds "
                         f"(must be 0-{config['HEIGHT']-1})")

    if config['ENTRY'] == config['EXIT']:
        raise ValueError("ENTRY and EXIT cannot be at the same position")

    if 'ALGORITHM' not in config:
        config['ALGORITHM'] = "recursive_backtracker"
    else:
        valid_algos = ["prim's", "recursive_backtracker"]
        if config['ALGORITHM'].lower() not in valid_algos:
            raise ValueError(f"Unknown ALGORITHM: {config['ALGORITHM']}")

    if 'DISPLAY_MODE' not in config:
        config['DISPLAY_MODE'] = 'ascii'
