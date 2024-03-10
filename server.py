import socket
import threading
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests

def handle_client(client_socket):
    #Infinite loop to receive, process and respond to requests
    while True:
        request = client_socket.recv(4096).decode("utf-8")

        if not request:
            break

        response = process_request(request)
        client_socket.send(response.encode("utf-8"))

    client_socket.close()

def process_request(request):

    # If the xml file exists, but is incorrectly formatted, copy existing xml to a backup file and empty the existing xml
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        with open("backup_db.xml", "w") as backup_xml_file:
            backup_xml_file.write(xml_data)
        root = ET.fromstring("<data></data>")

    # Split the request into command and data
    command, data = request.split(":", 1)

    if command == "ADD":

        #Check that the request is correctly formatted and split the items into variables
        try:
            topic, note_name, note_text, timestamp = data.split(",")

        except ValueError:
            return "Invalid request: The data should be a string of the syntax: topic, note_name, note_text, timestamp"

        except:
            return "Invalid request: Unknown"

        try:
            # Check if the topic exists and create it otherwise
            topic_element = root.find(f".//topic[@name='{topic}']")
            if topic_element is None:
                topic_element = ET.SubElement(root, "topic", {"name": topic})

        except SyntaxError:
            return "Invalid request: The data needs to be a string"

        except:
            return "Invalid request: Unknown"

        # Create a new note
        note_element = ET.SubElement(topic_element, "note", {"name": note_name})
        text_element = ET.SubElement(note_element, "text")
        text_element.text = note_text
        timestamp_element = ET.SubElement(note_element, "timestamp")
        timestamp_element.text = timestamp

        update_xml(root)

        return f"Note added successfully:\n{xml_data}"

    elif command == "GET":
        topic = data.strip()

        try:
            # Find the topic from the xml
            topic_element = root.find(f".//topic[@name='{topic}']")
        
        except SyntaxError:
            return "Invalid request: The data needs to be a string"
        
        except:
            return "Invalid request: Unknown"

        if topic_element is not None:
            # Get the content of the topic
            topic_content = format_xml(topic_element)
            return f"Content for topic '{topic}':\n{topic_content}"

        else:
            return f"Topic '{topic}' not found."

    elif command == "WIKI":
        # Query Wikipedia
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={data}&limit=1&format=json"
        response = requests.get(search_url)
        result = response.json()

        try:
            if result[1]:
                # Append the Wikipedia link to the existing topic
                try:
                    topic_element = root.find(f".//topic[@name='{data}']")

                except SyntaxError:
                    return "Invalid request: The data needs to be a string"
        
                except:
                    return "Invalid request: Unknown"

                if topic_element is not None:
                    link_element = ET.SubElement(topic_element, "link")
                    link_element.text = result[3][0]

                    update_xml(root)

                    return f"Wikipedia information added to topic '{data}':\n{xml_data}"

                #Add the topic with a link if it doesn't exist
                else:
                    topic_element = ET.SubElement(root, "topic", {"name": data})
                    link_element = ET.SubElement(topic_element, "link")
                    link_element.text = result[3][0]

                    update_xml(root)

                    return f"New topic '{data}' added with a wikipedia link."

            else:
                return f"No Wikipedia information found for '{data}'."

        except KeyError:
            return "No wikipedia information for an empty topic"
    else:
        return "Invalid command"

def format_xml(element):
    rough_string = ET.tostring(element, "utf-8")
    reparsed = minidom.parseString(rough_string)
    lines = [line for line in reparsed.toprettyxml(indent="    ").split("\n") if line.strip()]
    return "\n".join(lines)

def update_xml(rootvar):
    global xml_data
    
    # Update the xml data
    xml_data = format_xml(rootvar)

    # Save the xml to the xml file
    with open("db.xml", "w") as xml_file:
        xml_file.write(xml_data)

# Main server logic
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen(5)
print("Server listening on port 12345")

# Read xml data from the file or create an empty xml file if it doesn"t exist
try:
    with open("db.xml", "r") as xml_file:
        xml_data = xml_file.read()

except FileNotFoundError:
    xml_data = "<data></data>"

while True:
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()