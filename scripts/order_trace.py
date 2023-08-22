import json

# Read the JSON file and parse its content
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [json.loads(line.strip()) for line in lines]

# Write a list of dictionaries as JSON lines to a file
def write_json_lines(file_path, data):
    with open(file_path, 'w') as file:
        for item in data:
            json.dump(item, file)
            file.write('\n')

# Sort JSON lines by the "timegenerated" field
def sort_json_lines_by_time(json_lines):
    return sorted(json_lines, key=lambda x: x['timegenerated'])

# Input and output file paths
input_file = '../data/most_stable_cs_host.json'  # Replace with your input file path
output_file = '../data/most_stable_cs_host_ordered.json'  # Replace with your desired output file path

# Read JSON lines from the input file
json_lines = read_json_file(input_file)

# Sort JSON lines by "timegenerated"
sorted_json_lines = sort_json_lines_by_time(json_lines)

# Write sorted JSON lines to the output file
write_json_lines(output_file, sorted_json_lines)

print(f"Ordered JSON lines written to {output_file}")
