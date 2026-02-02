# import random
from mazgen.algorithms import generate_backtracking_maze
import sys
from mazgen.hex_writer import write_hex_output, cell_to_hex 
from config_parser import parse_config, validate_config
from mazgen.algorithms import generate_backtracking_maze
from typing import List
from mazgen.cell import Cell

if __name__ == "__main__":
    try:
        config = parse_config(sys.argv[1])
        validate_config(config)
        
        maze = generate_backtracking_maze(
            width=config['WIDTH'], 
            height=config['HEIGHT'], 
            seed=config.get('SEED')
        )
        
        print("Maze generated successfully!")
        write_hex_output(
    maze_grid=maze,
    entry=config['ENTRY'],
    exit=config['EXIT'],
    solution_path="NONE",
    output_file=config['OUTPUT_FILE']
)

    except ValueError as e:
        print(f"Config Error: {e}")