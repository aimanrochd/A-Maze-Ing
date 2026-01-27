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
                    raise ValueError(f"Line {line_num}: {key} must be an integer, got '{value}'") 
            elif key in ['ENTRY', 'EXIT']:
                try:
                    x_str, y_str = value.split(',')
                    config[key] = (int(x_str.strip()), int(y_str.strip()))
                except ValueError:
                    raise ValueError(
                        f"Line {line_num}: {key} must be in format 'x,y', got '{value}'"
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

    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']

    missing = []
    for key in required_keys:
        if key not in config:
            missing.append(key)

    if missing:
        raise ValueError(f"Missing required keys: {', '.join(missing)}")
    if config['WIDTH'] <= 0:
        raise ValueError(f"WIDTH must be greater than 0, got {config['WIDTH']}")
    
    if config['HEIGHT'] <= 0:
        raise ValueError(f"HEIGHT must be greater than 0, got {config['HEIGHT']}")
    
    entry_x, entry_y = config['ENTRY']

    if not (0 <= entry_x < config['WIDTH']):
        raise ValueError(f"ENTRY x={entry_x} out of bounds (must be 0-{config['WIDTH']-1})")
    
    if not (0 <= entry_y < config['HEIGHT']):
        raise ValueError(f"ENTRY y={entry_y} out of bounds (must be 0-{config['HEIGHT']-1})")
    
    exit_x, exit_y = config['EXIT']
    
    if not (0 <= exit_x < config['WIDTH']):
        raise ValueError(f"EXIT x={exit_x} out of bounds (must be 0-{config['WIDTH']-1})")
    
    if not (0 <= exit_y < config['HEIGHT']):
        raise ValueError(f"EXIT y={exit_y} out of bounds (must be 0-{config['HEIGHT']-1})")
    
    if config['ENTRY'] == config['EXIT']:
        raise ValueError("ENTRY and EXIT cannot be at the same position")
    
    if 'ALGORITHM' not in config:
        config['ALGORITHM'] = "prim's"
    
    if 'DISPLAY_MODE' not in config:
        config['DISPLAY_MODE'] = 'ascii'


if __name__ == "__main__":
    """Test parsing AND validation."""
    
    try:
        # Step 1: Parse the file
        result = parse_config('config.txt')
        print("[OK] Parsing successful!")
        
        # Step 2: Validate the parsed config
        validate_config(result)
        print("[OK] Validation successful!")
        
        # Step 3: Display final config
        print("\n-> Final configuration:")
        for key, val in result.items():
            print(f"  {key}: {val} ({type(val).__name__})")
    
    except FileNotFoundError as e:
        print(f"[KO] File Error: {e}")
    
    except ValueError as e:
        print(f"[KO] Error: {e}")
    
    except Exception as e:
        print(f"[KO] Unexpected Error: {e}")