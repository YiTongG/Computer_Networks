import socket

dns_records = {}

def handle_registration(data, addr):
    lines = data.split("\n")
    if lines[0] == "TYPE=A":
        hostname = lines[1].split("=")[1]
        ip = lines[2].split("=")[1]
        dns_records[hostname] = ip
        # Store to a file or persistent storage as needed

def handle_query(data, addr, sock):
    lines = data.split("\n")
    if lines[0] == "TYPE=A":
        hostname = lines[1].split("=")[1]
        if hostname in dns_records:
            ip = dns_records[hostname]
            response = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
            sock.sendto(response.encode(), addr)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("0.0.0.0", 53533))
        while True:
            data, addr = sock.recvfrom(1024)
            data = data.decode()
            if "VALUE" in data:
                handle_registration(data, addr)
            else:
                handle_query(data, addr, sock)

if __name__ == "__main__":
    main()
