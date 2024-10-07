from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    
    # Validate parameters
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Missing parameters", 400

    # Query Authoritative Server (AS) to resolve hostname
    ip = query_authoritative_server(hostname, as_ip, as_port)
    if not ip:
        return "DNS lookup failed", 404

    # Query Fibonacci Server (FS)
    url = f"http://{ip}:{fs_port}/fibonacci?number={number}"
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return "Fibonacci Server error", 500

def query_authoritative_server(hostname, as_ip, as_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        message = f"TYPE=A\nNAME={hostname}"
        sock.sendto(message.encode(), (as_ip, int(as_port)))
        response, _ = sock.recvfrom(1024)
        # Parse response
        lines = response.decode().split("\n")
        if lines[0] == "TYPE=A":
            return lines[2].split("=")[1]  # IP address
    return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
