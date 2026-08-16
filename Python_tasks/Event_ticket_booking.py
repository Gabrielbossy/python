"""
Event Ticket Booking System
--------------------------------
A simple console-based program to manage ticket sales for events.
"""


def add_event(events):
    """Add a new event with a ticket price and available tickets."""
    name = input("Enter event name: ").strip()

    try:
        price = float(input(f"Enter ticket price for {name}: "))
        if price < 0:
            print("Price cannot be negative.\n")
            return
    except ValueError:
        print("Invalid price. Please enter a number.\n")
        return

    try:
        tickets_available = int(input(f"Enter number of tickets available for {name}: "))
        if tickets_available < 0:
            print("Tickets available cannot be negative.\n")
            return
    except ValueError:
        print("Invalid number. Please enter a whole number.\n")
        return

    events.append({"name": name, "price": price, "tickets_available": tickets_available})
    print(f'Event "{name}" added with {tickets_available} ticket(s) at ${price:.2f} each.\n')


def find_event(events, name):
    """Helper function to find an event by name (case-insensitive)."""
    for event in events:
        if event["name"].lower() == name.lower():
            return event
    return None


def display_events(events):
    """Display all events and their remaining ticket availability."""
    print("\n--- Events ---")
    if not events:
        print("No events have been added yet.")
    else:
        for event in events:
            print(
                f"{event['name']} - ${event['price']:.2f}/ticket - "
                f"{event['tickets_available']} available"
            )
    print("--------------\n")


def calculate_revenue(sales):
    """Calculate and return the total revenue from all sales."""
    return sum(sale["price"] * sale["quantity"] for sale in sales)


def buy_ticket(events, sales):
    """Sell tickets for an event, if enough are available. Returns amount charged."""
    display_events(events)
    event_name = input("Enter the event name: ").strip()
    event = find_event(events, event_name)

    if event is None:
        print(f'Event "{event_name}" was not found.\n')
        return 0

    if event["tickets_available"] <= 0:
        print(f'Event "{event["name"]}" is sold out.\n')
        return 0

    customer_name = input("Enter customer name: ").strip()

    try:
        quantity = int(input("Enter number of tickets to buy: "))
        if quantity <= 0:
            print("Quantity must be a positive number.\n")
            return 0
    except ValueError:
        print("Invalid quantity.\n")
        return 0

    if quantity > event["tickets_available"]:
        print(f'Only {event["tickets_available"]} ticket(s) left for "{event["name"]}".\n')
        return 0

    event["tickets_available"] -= quantity
    amount = quantity * event["price"]

    sales.append({
        "event": event["name"],
        "customer": customer_name,
        "quantity": quantity,
        "price": event["price"],
    })

    print(f"{customer_name} bought {quantity} ticket(s) to {event['name']}.")
    print(f"Amount charged: ${amount:.2f}\n")
    return amount


def refund_ticket(events, sales):
    """Refund a customer's ticket purchase and return tickets to availability."""
    customer_name = input("Enter customer name: ").strip()
    event_name = input("Enter event name: ").strip()

    matching_sale = None
    for sale in sales:
        if (sale["customer"].lower() == customer_name.lower()
                and sale["event"].lower() == event_name.lower()):
            matching_sale = sale
            break

    if matching_sale is None:
        print(f'No matching sale found for {customer_name} - "{event_name}".\n')
        return

    event = find_event(events, matching_sale["event"])
    if event is not None:
        event["tickets_available"] += matching_sale["quantity"]

    sales.remove(matching_sale)
    print(f'Refunded {matching_sale["quantity"]} ticket(s) for {customer_name} - "{event_name}".\n')


def display_sales_report(sales):
    """Display every sale and the total revenue."""
    print("\n--- Sales Report ---")
    if not sales:
        print("No sales have been made yet.")
    else:
        for sale in sales:
            print(
                f"{sale['event']} - {sale['customer']} - "
                f"{sale['quantity']} ticket(s)"
            )
        total_revenue = calculate_revenue(sales)
        print(f"Total revenue: ${total_revenue:.2f}")
    print("---------------------\n")


def display_summary(events, sales):
    """Display the final summary before exiting."""
    total_events = len(events)
    total_tickets_sold = sum(sale["quantity"] for sale in sales)
    total_revenue = calculate_revenue(sales)

    print("\n=== Final Summary ===")
    print(f"Total number of events: {total_events}")
    print(f"Total tickets sold: {total_tickets_sold}")
    print(f"Total revenue generated: ${total_revenue:.2f}")

    if sales:
        sales_by_event = {}
        for sale in sales:
            sales_by_event[sale["event"]] = sales_by_event.get(sale["event"], 0) + sale["quantity"]
        best_event = max(sales_by_event, key=sales_by_event.get)
        print(f"Best-selling event: {best_event} ({sales_by_event[best_event]} tickets)")
    else:
        print("Best-selling event: N/A (no sales)")
    print("======================\n")


def main():
    events = []
    sales = []

    while True:
        try:
            num_events = int(input("Enter the number of events: "))
            if num_events <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for i in range(num_events):
        print(f"Event {i + 1}:")
        add_event(events)

    while True:
        print("Event Ticket Menu")
        print("1. View All Events")
        print("2. Buy Ticket")
        print("3. Refund Ticket")
        print("4. View Sales Report")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            display_events(events)
        elif choice == "2":
            buy_ticket(events, sales)
        elif choice == "3":
            refund_ticket(events, sales)
        elif choice == "4":
            display_sales_report(sales)
        elif choice == "5":
            display_summary(events, sales)
            print("Thank you for using the Event Ticket Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()