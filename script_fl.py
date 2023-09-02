import random
import subprocess


def distribute_number(total, size):
    users = [0 for _ in range(size)]
    for i in range(total):
        rand = int(min(size-1, max(0, random.gauss(size/2, size/4))))
        users[rand] += 1

    return users

    # Number of repetitions
num_edge = 12  # Change this to the desired number of repetitions
num_users = 100

users_per_edge = distribute_number(num_users, num_edge)
# Command to execute

print(users_per_edge)
edge_index = 0
# Execute the command multiple times
for users in (users_per_edge):
    command = ['python', 'simulator.py', '--users', f'{users}', '--rep', f'{edge_index+13}']
    edge_index += 1
    print(command)
    subprocess.run(command)
