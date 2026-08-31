"""
Customer Support Ticket Queue System
----------------------------------------------
A simple console-based program to manage support tickets on a
first-come, first-served (FIFO queue) basis.
"""


def submit_ticket(queue, ticket_counter):
    """Create a new ticket and add it to the end of the queue.

    Returns the updated ticket_counter (the next available ticket ID).
    """
    customer = input("Enter customer name: ").strip()
    issue = input("Briefly describe the issue: ").strip()

    ticket = {"ticket_id": ticket_counter, "customer": customer, "issue": issue}

    # Adding to the END of the list -> this is what makes it a queue.
    queue.append(ticket)

    print(f"Ticket #{ticket_counter} submitted for {customer}. Added to the back of the queue.\n")
    return ticket_counter + 1


def resolve_next_ticket(queue, resolved_tickets):
    """Resolve the ticket at the FRONT of the queue (first in, first out)."""
    if not queue:
        print("The queue is empty. No tickets to resolve.\n")
        return

    # Removing from index 0 (the front) -> this is the FIFO rule.
    # A regular .pop() with no argument would remove from the END instead,
    # which would make this a stack (LIFO), not a queue.
    ticket = queue.pop(0)
    resolved_tickets.append(ticket)

    print(f"Resolved Ticket #{ticket['ticket_id']} for {ticket['customer']} "
          f"({ticket['issue']}).\n")


def average_wait_position(queue):
    """Calculate and return the average queue position of waiting tickets."""
    if not queue:
        return 0
    positions = range(1, len(queue) + 1)  # 1, 2, 3, ... for each ticket in order
    return sum(positions) / len(queue)


def view_queue(queue):
    """Display every ticket currently waiting, in order, with its position."""
    print("\n--- Current Queue ---")
    if not queue:
        print("The queue is empty.")
    else:
        for position, ticket in enumerate(queue, start=1):
            print(
                f"{position}. Ticket #{ticket['ticket_id']} - {ticket['customer']} "
                f"- {ticket['issue']}"
            )
        avg_position = average_wait_position(queue)
        print(f"\nAverage wait position: {avg_position:.1f}")
    print("----------------------\n")


def view_resolved(resolved_tickets):
    """Display all resolved tickets."""
    print("\n--- Resolved Tickets ---")
    if not resolved_tickets:
        print("No tickets have been resolved yet.")
    else:
        for ticket in resolved_tickets:
            print(f"Ticket #{ticket['ticket_id']} - {ticket['customer']} - {ticket['issue']}")
    print("------------------------\n")


def display_summary(queue, resolved_tickets):
    """Display the final summary before exiting."""
    total_submitted = len(queue) + len(resolved_tickets)
    resolved_count = len(resolved_tickets)
    waiting_count = len(queue)

    print("\n=== Support Desk Summary ===")
    print(f"Total tickets ever submitted: {total_submitted}")
    print(f"Tickets resolved: {resolved_count}")
    print(f"Tickets still waiting: {waiting_count}")

    if queue:
        first_waiting = queue[0]  # front of the queue
        print(
            f"First ticket still waiting: Ticket #{first_waiting['ticket_id']} "
            f"({first_waiting['customer']})"
        )
    else:
        print("First ticket still waiting: None (queue is empty)")
    print("=============================\n")


def main():
    queue = []
    resolved_tickets = []
    ticket_counter = 1  # next ticket ID to assign

    while True:
        print("Support Ticket Menu")
        print("1. Submit New Ticket")
        print("2. Resolve Next Ticket")
        print("3. View Queue")
        print("4. View Resolved Tickets")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            ticket_counter = submit_ticket(queue, ticket_counter)
        elif choice == "2":
            resolve_next_ticket(queue, resolved_tickets)
        elif choice == "3":
            view_queue(queue)
        elif choice == "4":
            view_resolved(resolved_tickets)
        elif choice == "5":
            display_summary(queue, resolved_tickets)
            print("Thank you for using the Support Ticket Queue System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()