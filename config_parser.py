import sys
import os
from typing import Any, Dict, Set, Tuple


def _convert_value(key: str, value: str, line_num: int) -> Any:
    """
    Convert a raw config value to the expected type for the given key.

    Args:
        key: Config key (uppercase).
        value: Raw string value.
        line_num: Line number (for error messages).

    Returns:
        Converted value (int, tuple, bool, or str).

    Raises:
        ValueError: If the value format/type is invalid for the key.
    """
    if key in {'WIDTH', 'HEIGHT', 'SEED'}:
        if not value.isdigit():
            raise ValueError(
                f"Line {line_num}: {key} must be a non-negative integer."
            )
        return int(value)

    elif key in {'ENTRY', 'EXIT'}:
        try:
            parts = value.split(',')
            if len(parts) != 2:
                raise ValueError
            return (int(parts[0]), int(parts[1]))
        except ValueError:
            raise ValueError(
                f"Line {line_num}: {key} must be 'x,y' integers."
            )

    elif key == 'PERFECT':
        lower_value = value.lower()
        if lower_value in {'true', '1', 'yes'}:
            return True
        elif lower_value in {'false', '0', 'no'}:
            return False
        else:
            raise ValueError(
                f"Line {line_num}: PERFECT must be boolean."
            )

    return value


def _parse_line(
    line: str,
    line_num: int,
    allowed: Set[str],
    config: Dict[str, Any]
) -> None:
    """
    Parse one config line and store the converted value into config.

    Args:
        line: Stripped non-empty, non-comment line.
        line_num: Line number (for error messages).
        allowed: Allowed keys (uppercase).
        config: Output dictionary to fill.

    Raises:
        ValueError: If syntax is invalid, key is unknown/duplicate,
        or value invalid.
    """
    if '=' not in line:
        raise ValueError(
            f"Line {line_num}: Missing '='. Expected KEY=VALUE"
        )

    raw_key, raw_value = [part.strip() for part in line.split('=', 1)]
    key = raw_key.upper()

    if not raw_key or not raw_value:
        raise ValueError(f"Line {line_num}: Empty key or value.")
    if key not in allowed:
        raise ValueError(f"Line {line_num}: Unknown key '{key}'.")
    if key in config:
        raise ValueError(f"Line {line_num}: Duplicate key '{key}'.")

    config[key] = _convert_value(key, raw_value, line_num)


def parse_config(filepath: str) -> Dict[str, Any]:
    """
    Parse a config file into a dictionary.

    Args:
        filepath: Path to the config file.

    Returns:
        Parsed config dictionary.

    Side Effects:
        Prints an error to stderr and exits with code 1 on failure.
    """
    config: Dict[str, Any] = {}
    allowed_keys: Set[str] = {
        'WIDTH', 'HEIGHT', 'SEED', 'ENTRY', 'EXIT',
        'OUTPUT_FILE', 'PERFECT', 'ALGORITHM'
    }

    try:
        with open(filepath, "r") as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('#'):
                    continue
                _parse_line(clean_line, line_num, allowed_keys, config)

    except (FileNotFoundError, PermissionError) as e:
        print(f"File Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Config Error: {e}", file=sys.stderr)
        sys.exit(1)

    return config


def _validate_bounds(width: int, height: int) -> None:
    """
    Validate WIDTH/HEIGHT bounds.

    Args:
        width: Maze width.
        height: Maze height.

    Raises:
        ValueError: If width/height are outside allowed ranges.
    """
    if width < 9 or width > 100:
        raise ValueError(
            f"WIDTH must be between 9 and 100 inclusive "
            f"(9 ≤ WIDTH ≤ 100), got {width}"
        )
    if height < 7 or height > 100:
        raise ValueError(
            f"HEIGHT must be between 7 and 100 inclusive "
            f"(7 ≤ HEIGHT ≤ 100), got {height}"
        )


def _validate_entry_exit(
    entry: Tuple[int, int],
    exit_pos: Tuple[int, int],
    width: int,
    height: int
) -> None:
    """
    Validate ENTRY/EXIT coordinates and ensure they are distinct.

    Args:
        entry: Entry coordinates (x, y).
        exit_pos: Exit coordinates (x, y).
        width: Maze width.
        height: Maze height.

    Raises:
        ValueError: If out of bounds or entry equals exit.
    """
    for name, (x, y) in [('ENTRY', entry), ('EXIT', exit_pos)]:
        if x < 0 or y < 0 or x >= width or y >= height:
            raise ValueError(
                f"{name} ({x},{y}) is outside bounds "
                f"(0-{width-1}, 0-{height-1})"
            )

    if entry == exit_pos:
        raise ValueError("ENTRY and EXIT cannot be the same position.")


def _validate_output_file(output_file: str, config_path: str) -> None:
    """
    Validate OUTPUT_FILE path safety.

    Args:
        output_file: Output path from config.
        config_path: Config file path (prevent overwrite).

    Raises:
        ValueError: If path is unsafe or overwrites config.
    """
    if '..' in output_file or os.path.isabs(output_file):
        raise ValueError(
            f"OUTPUT_FILE must be relative and safe: '{output_file}'"
        )

    if os.path.abspath(output_file) == os.path.abspath(config_path):
        raise ValueError(
            "OUTPUT_FILE cannot be the same as the config file."
        )


def validate_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Validate required keys and normalize optional settings.

    Args:
        config: Parsed config dictionary (may be updated in-place).
        config_path: Path to config file (prevent overwrite).

    Side Effects:
        Prints an error to stderr and exits with code 1 on validation failure.
    """
    try:
        required_keys = {
            'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'
        }

        missing_keys = required_keys - config.keys()
        if missing_keys:
            raise ValueError(f"Missing keys: {', '.join(missing_keys)}")

        _validate_bounds(config['WIDTH'], config['HEIGHT'])

        _validate_entry_exit(
            config['ENTRY'],
            config['EXIT'],
            config['WIDTH'],
            config['HEIGHT']
        )

        _validate_output_file(config['OUTPUT_FILE'], config_path)

        algo = config.setdefault('ALGORITHM', 'prims').lower()
        if algo not in {'prims', 'recursive_backtracker'}:
            raise ValueError(f"Unknown ALGORITHM: '{algo}'")
        config['ALGORITHM'] = algo

    except ValueError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        sys.exit(1)
