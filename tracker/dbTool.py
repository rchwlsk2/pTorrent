import sys, signal, socket


##
# Tool to be able to see what is in the Tracker's database
#
# @author Paul Rachwalski
# @date Apr 21, 2015
##

def exit_handler(signum, frame):
    print("\nConnection stopped!")
    sock.close()
    sys.exit(0)

# Validate command line args
if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " <tracker ip> <tracker port>")
    sys.exit(0)

tracker_ip = sys.argv[1]
tracker_port = int(sys.argv[2])

# Initialize interrupt exit handler
signal.signal(signal.SIGINT, exit_handler)

# Connect to tracker
print("Connecting to " + tracker_ip + ":" + str(tracker_port))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.connect((tracker_ip, tracker_port))
except socket.error as sockerr:
    print("Could not connect to tracker at " + tracker_ip + ":" + tracker_port + " --- " + sockerr.strerror)
    sys.exit(0)

sock.recv(1024)
print("Connected!")
print("Type queries to send to tracker below")
print("----------")

# User query loop
inp = input("> ")
while inp:
    valid = inp.startswith("add ") or inp.startswith("rem ") \
            or inp.startswith("get ")

    if valid:
        sock.sendall(inp.encode())
        data = sock.recv(8096).decode()
        print(data)

    else:
        print("Invalid input")

    inp = input("> ")

# Exit gracefully
sock.close()
sys.exit(0)