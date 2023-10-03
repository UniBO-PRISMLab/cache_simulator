import random
import subprocess
import pandas as pd


def distribute_number(total, size):
    users = [0 for _ in range(size)]
    for i in range(total):
        rand = int(min(size-1, max(0, random.gauss(size/2, size/4))))
        users[rand] += 1

    return users

    # Number of repetitions
num_edge = 1  # Change this to the desired number of repetitions
num_users = 100
replications = 50 # Number of experiments to run
cache_expiration_time =  100
                        #3600000
filename = 'scripts/resultsIvan.csv'
label = 'local'
df = pd.read_csv(filename)

for index, row in df.iterrows():
    n_edge = row['N_EDGE']
    rounds = row['ROUNDS']
    average_diff = row['Average of diff']
    std_diff = row['Standard Deviation of diff']
    avg_hit_rate = float(row['Average Percentage of hit rate'])/100
    #users_per_edge = distribute_number(num_users, num_edge)

    # Set the label based on conditions
    if rounds == 1:
        label = 'local'
    elif rounds < 1:
        label = 'global'
    else:
        label = f'fl_{int(rounds)}'
    label = 'baseline'
    if (n_edge < 0):
        n_edge = 1

    divided_num_users = int(num_users / int(n_edge))
    print(divided_num_users)
    # Execute the command multiple times
    command = [
        'python', 'simulator.py', '--users', f'{divided_num_users}', '--pre-req-time-avg', f'{average_diff}',
        '--pre-req-time-std', f'{std_diff}', '--replications', f'{replications}', '--label', f'{label}_{int(n_edge)}_final',
        '--edge-nodes', f'{num_edge}', '--cache-expiration-time', f'{cache_expiration_time}', '--accuracy', f'{0}']
    print(command)
    subprocess.run(command)
