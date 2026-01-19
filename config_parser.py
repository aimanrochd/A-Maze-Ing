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
                    raise ValueError(
                        f"Line {line_num}: {key} must be an integer, got '{value}'"
                    ) 
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


if __name__ == "__main__":
    
    try:
        result = parse_config('config.txt')
        
        print("Parsing successful!")
        print()
        
        print("Parsed configuration:")
        for key, val in result.items():
            print(f"  {key}: {val} ({type(val).__name__})")
    
    except FileNotFoundError as e:
        print(f"File Error: {e}")
    
    except ValueError as e:
        print(f"Parsing Error: {e}")
    
    except Exception as e:
        print(f"Unexpected Error: {e}")