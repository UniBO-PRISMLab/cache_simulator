def read_file_and_print(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            raw_lines = line.strip()
            # Split the string by underscores
            parts = raw_lines.split('_')
            print(parts)
            # Join the desired parts using the join() method
            result = parts[0]
            lines.append(result)
    return lines

# Provide the filename you want to read
filename = 'files.out'

# Call the function to read the file and get the list of lines
lines_list = read_file_and_print(filename)

# Print the list
for line in lines_list:
    print(line)