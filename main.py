import pandas as pd


# function to read a CSV file
def read_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"error reading {file_path}: {e}")
        return None


# function to check consistency of input data
def check_consistency(allocation, request, available):
    if allocation.shape != request.shape:
        return "inconsistent number of processes or resources in Allocation and Request files."
    if available.shape[0] != 1 or available.shape[1] != allocation.shape[1]:
        return "inconsistent format of Available data or mismatch with Allocation/Request files."
    return "consistent"


# function to detect a deadlock
def detect_deadlock(allocation, request, available):
    num_processes = allocation.shape[0]
    num_resources = allocation.shape[1]
    alloc_matrix = allocation.values
    req_matrix = request.values
    avail_vector = available.values[0]
    finish = [False] * num_processes

    while True:
        made_progress = False
        for i in range(num_processes):
            if not finish[i] and all(req_matrix[i, j] <= avail_vector[j] for j in range(num_resources)):
                for j in range(num_resources):
                    avail_vector[j] += alloc_matrix[i, j]
                finish[i] = True
                made_progress = True

        if all(finish):
            return False, []

        if not made_progress:
            deadlocked_processes = [allocation.index[i] for i in range(num_processes) if not finish[i]]
            return True, deadlocked_processes


# function to resolve a deadlock
def resolve_deadlock(allocation, request, available):
    num_resources = available.shape[1]
    avail_vector = available.values[0].copy()
    deadlock_resolved = False
    updated_available = available.copy()

    while not deadlock_resolved:
        for i in range(num_resources):
            avail_vector[i] += 1
            updated_available.iloc[0, i] = avail_vector[i]

            deadlock, _ = detect_deadlock(allocation, request, pd.DataFrame([avail_vector]))
            if not deadlock:
                print(f"deadlock resolved by increasing Resource {available.columns[i]} to {avail_vector[i]}")
                deadlock_resolved = True
                break

        if deadlock_resolved:
            break

    return updated_available, allocation, request


# function to suggest process execution order
def suggest_process_execution_order(allocation, request, available):
    num_processes = allocation.shape[0]
    num_resources = allocation.shape[1]
    alloc_matrix = allocation.values
    req_matrix = request.values
    avail_vector = available.values[0]
    finish = [False] * num_processes
    execution_order = []

    while not all(finish):
        made_progress = False
        for i in range(num_processes):
            if not finish[i] and all(req_matrix[i, j] <= avail_vector[j] for j in range(num_resources)):
                for j in range(num_resources):
                    avail_vector[j] += alloc_matrix[i, j]
                finish[i] = True
                made_progress = True
                execution_order.append(allocation.index[i])

        if not made_progress:
            print("no safe sequence found. There might be a deadlock.")
            return []

    return execution_order


# function to create a non-deadlock scenario
def create_non_deadlock_scenario(allocation, request, available):
    for resource_increase in range(1, 6):  # trying different increments
        for request_decrease in range(0, 3):  # trying different decrements
            modified_available = available + resource_increase
            modified_request = request - request_decrease
            modified_request[modified_request < 0] = 0

            if not detect_deadlock(allocation, modified_request, modified_available)[0]:
                print(
                    f"non-deadlock scenario achieved by increasing available resources by {resource_increase} "
                    f"and decreasing requests by {request_decrease}")
                return modified_available, modified_request

    print("failed to create a non-deadlock scenario.")
    return available, request


# main function
def main():
    allocation = read_csv("Allocation.csv")
    request = read_csv("Request.csv")
    available = read_csv("Available.csv")

    if allocation is not None and request is not None and available is not None:
        consistency_check = check_consistency(allocation, request, available)
        if consistency_check == "consistent":
            while True:
                deadlock, deadlocked_processes = detect_deadlock(allocation, request, available)
                if deadlock:
                    print("deadlock detected. Deadlocked Processes:", deadlocked_processes)
                    updated_available, updated_allocation, updated_request = resolve_deadlock(allocation, request,
                                                                                              available)
                    print("updated Available Resources:\n", updated_available)
                    available = updated_available
                else:
                    print("no deadlock detected.")
                    execution_order = suggest_process_execution_order(allocation, request, available)
                    if execution_order:
                        print("suggested execution order to avoid deadlock:", execution_order)
                    else:
                        modified_available, modified_request = create_non_deadlock_scenario(allocation, request,
                                                                                            available)
                        print("modified Available Resources:\n", modified_available)
                        print("modified Request Matrix:\n", modified_request)
                    break
        else:
            print(consistency_check)


# run the main function
if __name__ == '__main__':
    main()
