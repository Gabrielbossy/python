"""
Marathon Race Results System
----------------------------------
A simple console-based program to record finish times and rank runners,
demonstrating sorting with sorted() and a key function.
"""


def add_runner(runners):
    """Register a new runner with an auto-generated bib number."""
    name = input("Enter runner's name: ").strip()
    bib = 101 + len(runners)

    runners.append({"name": name, "bib": bib, "finish_time": None})
    print(f'"{name}" registered with bib number {bib}.\n')


def find_runner_by_bib(runners, bib):
    """Helper function to find a runner by bib number."""
    for runner in runners:
        if runner["bib"] == bib:
            return runner
    return None


def record_finish_time(runners):
    """Record a runner's finish time in minutes."""
    try:
        bib = int(input("Enter bib number: "))
    except ValueError:
        print("Invalid bib number.\n")
        return

    runner = find_runner_by_bib(runners, bib)

    if runner is None:
        print(f"No runner found with bib number {bib}.\n")
        return

    try:
        finish_time = float(input("Enter finish time (minutes): "))
        if finish_time <= 0:
            print("Finish time must be a positive number.\n")
            return
    except ValueError:
        print("Invalid finish time.\n")
        return

    runner["finish_time"] = finish_time
    print(f"Recorded finish time for {runner['name']}: {finish_time} minutes.\n")


def get_ranked_results(runners):
    """Return finished runners sorted by finish time, fastest first."""
    finished_runners = [r for r in runners if r["finish_time"] is not None]

    # sorted() builds a NEW sorted list rather than changing the original.
    # key=lambda r: r["finish_time"] tells sorted() to compare runners
    # by their finish_time value, not by the dictionary itself
    # (dictionaries can't be compared directly with < or >).
    ranked = sorted(finished_runners, key=lambda r: r["finish_time"])
    return ranked


def display_results(runners):
    """Display all finished runners in ranked order."""
    ranked = get_ranked_results(runners)

    print("\n--- Ranked Results ---")
    if not ranked:
        print("No runners have finished yet.")
    else:
        for rank, runner in enumerate(ranked, start=1):
            print(
                f"{rank}. {runner['name']} (Bib {runner['bib']}) - "
                f"{runner['finish_time']} min"
            )
    print("-----------------------\n")


def get_podium(runners):
    """Return the top 3 finishers (or fewer, if fewer have finished)."""
    ranked = get_ranked_results(runners)
    # List slicing: [:3] takes the first 3 items of the list.
    # If there are fewer than 3, it safely returns however many exist,
    # without raising an error.
    return ranked[:3]


def display_podium(runners):
    """Display the top 3 finishers with medal-style labels."""
    podium = get_podium(runners)
    medals = ["🥇", "🥈", "🥉"]

    print("\n--- Podium (Top 3) ---")
    if not podium:
        print("No runners have finished yet.")
    else:
        for i, runner in enumerate(podium):
            print(f"{medals[i]} {runner['name']} - {runner['finish_time']} min")
    print("-----------------------\n")


def display_all_runners(runners):
    """Display every registered runner and their status."""
    print("\n--- Runners ---")
    if not runners:
        print("No runners registered yet.")
    else:
        for runner in runners:
            status = f"{runner['finish_time']} min" if runner["finish_time"] is not None else "Not finished"
            print(f"{runner['name']} (Bib {runner['bib']}) - {status}")
    print("---------------\n")


def display_summary(runners):
    """Display the final summary before exiting."""
    total_runners = len(runners)
    finished_count = sum(1 for r in runners if r["finish_time"] is not None)
    not_finished_count = total_runners - finished_count

    print("\n=== Race Summary ===")
    print(f"Total runners registered: {total_runners}")
    print(f"Runners finished: {finished_count}")
    print(f"Runners not finished: {not_finished_count}")

    ranked = get_ranked_results(runners)
    if ranked:
        winner = ranked[0]
        print(f"Winner: {winner['name']} ({winner['finish_time']} min)")
    else:
        print("Winner: N/A (no one has finished yet)")
    print("=====================\n")


def main():
    runners = []

    while True:
        try:
            num_runners = int(input("Enter the number of runners: "))
            if num_runners <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_runners):
        add_runner(runners)

    while True:
        print("Marathon Menu")
        print("1. View All Runners")
        print("2. Record a Finish Time")
        print("3. View Ranked Results")
        print("4. View Podium (Top 3)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_all_runners(runners)
        elif choice == "2":
            record_finish_time(runners)
        elif choice == "3":
            display_results(runners)
        elif choice == "4":
            display_podium(runners)
        elif choice == "5":
            display_summary(runners)
            print("Thank you for using the Marathon Race Results System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()