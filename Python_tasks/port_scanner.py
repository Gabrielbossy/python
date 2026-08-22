import socket


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0  # 0 means the connection succeeded (port is open)


def scan_range(ip, start_port, end_port):
    print(f"Scanning {ip} from port {start_port} to {end_port}...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            print(f"Port {port} is OPEN")
            open_ports.append(port)
    print("Scan complete.")
    if not open_ports:
        print("No open ports found in this range.")
    return open_ports


def main():
    ip = input("Enter IP to scan (use 127.0.0.1 for your own machine): ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))
    scan_range(ip, start_port, end_port)


if __name__ == "__main__":
    main()