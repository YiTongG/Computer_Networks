from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        return "Missing parameters", 400

    # Register with Authoritative Server (AS)
    register_to_authoritative_server(hostname, ip, as_ip, as_port)
    return "Registered", 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    try:
        number = int(number)
    except ValueError:
        return "Invalid number", 400

    result = calculate_fibonacci(number)
    return jsonify({"fibonacci": result}), 200

def calculate_fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def register_to_authoritative_server(hostname, ip, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), (as_ip, int(as_port)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
