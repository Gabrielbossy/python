"""
Job Applicant Tracking System
------------------------------------
A simple console-based program to track applicants through multiple
interview stages, demonstrating nested dictionaries and all().
"""

INTERVIEW_STAGES = ["phone_screen", "technical", "final"]
PASSING_SCORE = 70


def add_applicant(applicants):
    """Register a new applicant with all interview stages unscored."""
    name = input("Enter applicant's name: ").strip()

    scores = {stage: None for stage in INTERVIEW_STAGES}
    applicants.append({"name": name, "scores": scores})
    print(f'"{name}" added to the tracking system.\n')


def find_applicant(applicants, name):
    """Helper function to find an applicant by name (case-insensitive)."""
    for applicant in applicants:
        if applicant["name"].lower() == name.lower():
            return applicant
    return None


def record_interview_score(applicants):
    """Record a score for one interview stage of a specific applicant."""
    name = input("Enter the applicant's name: ").strip()
    applicant = find_applicant(applicants, name)

    if applicant is None:
        print(f'No applicant named "{name}" was found.\n')
        return

    print(f"Interview stages: {', '.join(INTERVIEW_STAGES)}")
    stage = input("Enter the stage to record a score for: ").strip().lower()

    if stage not in INTERVIEW_STAGES:
        print(f'"{stage}" is not a valid stage.\n')
        return

    try:
        score = float(input(f"Enter score for {stage} (0-100): "))
        if score < 0 or score > 100:
            print("Score must be between 0 and 100.\n")
            return
    except ValueError:
        print("Invalid score.\n")
        return

    applicant["scores"][stage] = score
    print(f"Recorded {stage} score of {score} for {applicant['name']}.\n")


def all_stages_complete(applicant):
    """Return True if every interview stage has a recorded score."""
    # all() returns True only if EVERY item in the sequence is truthy.
    # "score is not None" checks each stage's score individually -
    # if even one stage is still None, all() returns False.
    return all(score is not None for score in applicant["scores"].values())


def average_score(applicant):
    """Helper function to calculate an applicant's average score."""
    scores = applicant["scores"].values()
    return sum(scores) / len(scores)


def get_qualified_applicants(applicants, passing_score):
    """Return applicants who finished all stages and meet the passing average."""
    qualified = []
    for applicant in applicants:
        if all_stages_complete(applicant) and average_score(applicant) >= passing_score:
            qualified.append(applicant)
    return qualified


def display_ranked_applicants(applicants):
    """Display applicants who finished all stages, ranked by average score."""
    completed = [a for a in applicants if all_stages_complete(a)]
    ranked = sorted(completed, key=average_score, reverse=True)

    print("\n--- Ranked Applicants ---")
    if not ranked:
        print("No applicants have completed all interview stages yet.")
    else:
        for rank, applicant in enumerate(ranked, start=1):
            print(f"{rank}. {applicant['name']} - Average: {average_score(applicant):.1f}")
    print("--------------------------\n")


def display_applicants(applicants):
    """Display all applicants and their current scores."""
    print("\n--- Applicants ---")
    if not applicants:
        print("No applicants added yet.")
    else:
        for applicant in applicants:
            scores_display = ", ".join(
                f"{stage}: {applicant['scores'][stage] if applicant['scores'][stage] is not None else 'N/A'}"
                for stage in INTERVIEW_STAGES
            )
            print(f"{applicant['name']} - {scores_display}")
    print("------------------\n")


def display_qualified(applicants):
    """Display applicants who qualify with the standard passing score."""
    qualified = get_qualified_applicants(applicants, PASSING_SCORE)

    print(f"\n--- Qualified Applicants (passing average: {PASSING_SCORE}) ---")
    if not qualified:
        print("No applicants currently qualify.")
    else:
        for applicant in qualified:
            print(f"{applicant['name']} - Average: {average_score(applicant):.1f}")
    print("---------------------------------------------------\n")


def display_summary(applicants):
    """Display the final summary before exiting."""
    total_applicants = len(applicants)
    completed_count = sum(1 for a in applicants if all_stages_complete(a))
    qualified = get_qualified_applicants(applicants, PASSING_SCORE)

    print("\n=== Hiring Summary ===")
    print(f"Total number of applicants: {total_applicants}")
    print(f"Completed all interview stages: {completed_count}")
    print(f"Qualify with passing average of {PASSING_SCORE}: {len(qualified)}")

    completed = [a for a in applicants if all_stages_complete(a)]
    if completed:
        top_applicant = max(completed, key=average_score)
        print(f"Top-ranked applicant: {top_applicant['name']} ({average_score(top_applicant):.1f})")
    else:
        print("Top-ranked applicant: N/A (no one has completed all stages)")
    print("=======================\n")


def main():
    applicants = []

    while True:
        try:
            num_applicants = int(input("Enter the number of applicants: "))
            if num_applicants <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_applicants):
        add_applicant(applicants)

    while True:
        print("Applicant Tracking Menu")
        print("1. View All Applicants")
        print("2. Record an Interview Score")
        print("3. View Qualified Applicants")
        print("4. View Ranked Applicants (by average score)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_applicants(applicants)
        elif choice == "2":
            record_interview_score(applicants)
        elif choice == "3":
            display_qualified(applicants)
        elif choice == "4":
            display_ranked_applicants(applicants)
        elif choice == "5":
            display_summary(applicants)
            print("Thank you for using the Job Applicant Tracking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()