import subprocess

replications = 30
labels_of_already_done_experiments = ["accuracy-0-N0-standard-cache-mode-mix",
                                      "accuracy-0-N2-standard-cache-mode-mix",
                                      "accuracy-20-N0-standard-mix",
                                      "accuracy-20-N1-standard-mix",
                                      "accuracy-20-N2-standard-mix",
                                      "accuracy-40-N0-standard-mix",
                                      "accuracy-40-N1-standard-mix",]
# Define list of parameters to vary
accuracy_list = [0, 0.2, 0.4]  # 3
cache_not_found_list = [True, False]  # 2
neighbor_edge_nodes_list = [0, 1, 2]  # 3
cache_mode_list = ["standard", "cooperative"]  # 2
user_distributions = [  # 4
    {"id": 0.33, "type": 0.33, "location": 0.33},
    {"id": 1, "type": 0, "location": 0},
    {"id": 0, "type": 1, "location": 0},
    {"id": 0, "type": 0, "location": 1}]
# Execute experiments for each combination of parameters
for accuracy in accuracy_list:
    for cache_not_found in cache_not_found_list:
        for neighbor_edge_nodes in neighbor_edge_nodes_list:
            for cache_mode in cache_mode_list:
                for user_distribution in user_distributions:
                    label = f"accuracy-{accuracy*100}-N{neighbor_edge_nodes}-{cache_mode}-"
                    if (cache_not_found):
                        label += "cache-mode-"
                    elif (user_distribution['id'] == 1):
                        label += "id"
                    elif (user_distribution['location'] == 1):
                        label += "location"
                    elif (user_distribution['type'] == 1):
                        label += "type"
                    else:
                        label += "mix"
                    if(not label in labels_of_already_done_experiments):
                        # Define command to run simulation with current parameter settings
                        command = f"python3 simulator.py --label \"{label}\" --accuracy {accuracy} --cache-not-found-resource {cache_not_found} --neighbor-edge-nodes {neighbor_edge_nodes} --cache-mode \"{cache_mode}\" --replications {replications} --user-distribution-id {user_distribution['id']} --user-distribution-type {user_distribution['type']} --user-distribution-location {user_distribution['location']}"
                        # Print current parameter settings
                        print(command)
                        # Execute command and print output
                        subprocess.run(command, shell=True, check=True)