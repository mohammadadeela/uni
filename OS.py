import pandas as pd


def is_deadlocked_corrected(allocation, request, available):
    # getting the number of processes (n) and resources (m)
    n, m = allocation.shape
    finished = [False] * n  # keeping track of which processes are done

    # switching from dataframes to numpy arrays for easier handling
    alloc = allocation.iloc[:, 1:].to_numpy()
    req = request.iloc[:, 1:].to_numpy()
    avail = available.iloc[0].to_numpy()

    safe_sequence = []
    while True:
        did_allocate = False
        for i in range(n):
            # checking if a process can be completed
            if not finished[i] and all(req[i, j] <= avail[j] for j in range(m - 1)):
                # if yes, release its resources and mark it as finished
                avail += alloc[i, :]  # adding resources back
                finished[i] = True  # marking this process as done
                safe_sequence.append(allocation.iloc[i, 0])  # adding to the safe sequence
                did_allocate = True

        # if no process can be completed, exit the loop
        if not did_allocate:
            break

    # checking if there's a deadlock or not
    if all(finished):
        # if every process is finished, no deadlock
        return False, safe_sequence
    else:
        # if some processes are unfinished, deadlock
        deadlocked_processes = [allocation.iloc[i, 0] for i in range(n) if not finished[i]]
        return True, deadlocked_processes


# file paths for the input data
available_file = 'Available.csv'
allocation_file = 'Allocation.csv'
request_file = 'Request.csv'

# reading the data from the files
available_df = pd.read_csv(available_file)
allocation_df = pd.read_csv(allocation_file)
request_df = pd.read_csv(request_file)

# making sure the data dimensions line up
num_resources = available_df.shape[1]
num_processes_allocation = allocation_df.shape[0]
num_processes_request = request_df.shape[0]

# checking if dimensions are consistent, and notifying if not
if num_processes_allocation != num_processes_request:
    print("error: number of processes in allocation and request do not match.")
elif allocation_df.shape[1] != request_df.shape[1] or allocation_df.shape[1] != (num_resources + 1):
    print("error: mismatch in number of resources between files.")
else:
    # using the function to detect deadlock
    deadlocked, result = is_deadlocked_corrected(allocation_df, request_df, available_df)

    # printing the outcome
    if deadlocked:
        print("deadlocked. the following processes are in a deadlock:", result)
    else:
        print("no deadlock. safe sequence of process execution:", result)
