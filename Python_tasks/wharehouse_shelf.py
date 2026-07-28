class PalletConflictError(Exception):
    pass

# Helper Function
def parse_weight(weight_string):
    try:
        if weight_string.endswith("kg"):
            return int(weight_string.replace("kg", ""))

        elif weight_string.endswith("ton"):
            return int(weight_string.replace("ton", "")) * 1000

        else:
            raise ValueError("Invalid weight format")

    except (ValueError, TypeError):
        raise
    
# Main Function
def process_shelf_assignments(request_batch, active_zones):

    successful_placements = 0

    pallet_zones = {}

    failed_requests = {
        "invalid_schema": [],
        "parsing_error": [],
        "pallet_conflict": []
    }

    # Priority order
    priority_order = {
        "critical": 1,
        "standard": 2,
        "backlog": 3
    }
