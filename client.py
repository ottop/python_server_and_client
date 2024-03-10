import socket

def send_request(command, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(("127.0.0.1", 12345))

        request = f"{command}:{data}" #Set request to the format defined on the server
        client_socket.send(request.encode("utf-8"))

        response = client_socket.recv(4096).decode("utf-8")
        print(response)

while True:
    print("Choose an option:")
    print("1. Add a note")
    print("2. Get notes for a topic")
    print("3. Query Wikipedia for a topic")
    option = input("Option: ")

    if option == "1":
        topic = input("Enter topic: ")
        while topic == "": #Prevent adding empty values
            topic = input ("Topic needs a name. Enter topic: ")
        note_name = input("Enter note name: ")
        note_text = input("Enter note text: ")
        timestamp = input("Enter timestamp: ")

        send_request("ADD", f"{topic},{note_name},{note_text},{timestamp}")

    elif option == "2":
        topic = input("Enter topic to retrieve: ")
        send_request("GET", topic)

    elif option == "3":
        search_term = input("Enter search term for Wikipedia: ")
        send_request("WIKI", search_term)

    else:
        print("Invalid option. Try again.")