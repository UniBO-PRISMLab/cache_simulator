import json
from datetime import datetime, timedelta
import argparse


def generate_timestamps(file_name, num_lines):
    with open(f"{file_name}.json", 'w', newline='') as file:
        timestamp = datetime.now()
        
        for _ in range(num_lines):
            timestamp_iso = timestamp.isoformat(sep='T', timespec='seconds')
            line_to_write = json.dumps({'timestamp': timestamp_iso})
            file.write(f"{line_to_write}\n")
            timestamp += timedelta(minutes=2)
            



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate timestamps and save to a JSON file.')
    parser.add_argument('--filename', type=str, default='timestamps', help='Name of the JSON file')
    parser.add_argument('--lines', type=int, default=10, help='Number of lines')
    args = parser.parse_args()
    generate_timestamps(args.filename, args.lines)
    print(f"{args.lines} lines with timestamps have been written to {args.filename}.json")
