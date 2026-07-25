# Custom Exception
class VlanConflictError(Exception):
    pass


# Helper Function
def parse_bandwidth(bw_string):
    try:
        if bw_string.endswith("Mbps"):
            return int(bw_string.replace("Mbps", ""))

        elif bw_string.endswith("Gbps"):
            return int(bw_string.replace("Gbps", "")) * 1000

        else:
            raise ValueError("Invalid bandwidth format")

    except (ValueError, TypeError):
        raise


# Main Function
def process_network_configs(task_batch, active_servers):

    successful_updates = 0

    server_vlans = {}

    failed_tasks = {
        "invalid_schema": [],
        "parsing_error": [],
        "vlan_conflict": []
    }

    # Environment order
    environment_order = {
        "production": 1,
        "staging": 2,
        "development": 3
    }

    # Sort tasks
    task_batch.sort(key=lambda task: environment_order[task["env"]])

    # Process tasks
    for task in task_batch:

        try:
            task_id = task["task_id"]
            server_ip = task["server_ip"]
            vlan_id = task["vlan_id"]
            bandwidth = parse_bandwidth(task["bandwidth"])

            # Ignore inactive servers
            if server_ip not in active_servers:
                continue

            # Check VLAN conflict
            if server_ip in server_vlans and server_vlans[server_ip] != vlan_id:
                raise VlanConflictError

            # Assign VLAN
            server_vlans[server_ip] = vlan_id
            successful_updates += 1

        except KeyError:
            failed_tasks["invalid_schema"].append(
                task.get("task_id", "Unknown")
            )

        except (ValueError, TypeError):
            failed_tasks["parsing_error"].append(
                task.get("task_id", "Unknown")
            )

        except VlanConflictError:
            failed_tasks["vlan_conflict"].append(
                task.get("task_id", "Unknown")
            )

    summary = {
        "successful_updates": successful_updates,
        "server_vlans": server_vlans,
        "failed_tasks": failed_tasks
    }

    return summary


# Sample Data
active_servers = {
    "10.0.0.5",
    "10.0.0.6",
    "10.0.0.7",
    "10.0.0.8",
    "10.0.1.10"
}

task_batch = [
    {"task_id": "T01", "server_ip": "10.0.0.5", "vlan_id": 40, "bandwidth": "500Mbps", "env": "staging"},
    {"task_id": "T02", "server_ip": "10.0.1.99", "vlan_id": 20, "bandwidth": "100Mbps", "env": "production"},
    {"task_id": "T03", "server_ip": "10.0.0.6", "vlan_id": 10, "bandwidth": "1Gbps", "env": "production"},
    {"task_id": "T04", "server_ip": "10.0.0.7", "vlan_id": 40, "env": "development"},
    {"task_id": "T05", "server_ip": "10.0.0.8", "vlan_id": 30, "bandwidth": "Max", "env": "staging"},
    {"task_id": "T06", "server_ip": "10.0.0.6", "vlan_id": 50, "bandwidth": "200Mbps", "env": "production"}
]

# Run the program
result = process_network_configs(task_batch, active_servers)

print("Final Summary")
print(result)