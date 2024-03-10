# Python server and client

## Description
This is an university project in which I used Python to program a server and a client. Fundamentally the server handles topics in an xml mock database. The topics can include notes as well as Wikipedia links. 

The database mock is created upon the creation of the first topic. It is persistent and continues to get used upon subsequent uses of the program. 

## What it does
A request is sent from the client to the server in the format `command:data` where the command defines what the server should do and the data is the data that gets used.

The server has a few commands:
- ADD: Adds a new note into the xml database. If the topic exists, the note is added to the topic. If the topic does not exist, the topic is created.
- GET: Return the content of a specific topic in the xml database.
- WIKI: Uses the OpenSearch API to find a link to the topic in Wikipedia. If the topic exists in the xml database, the link gets added to it. If the topic does not exist, the topic is created.

A database created by this server could end up looking something like the following:

db.xml
```
<?xml version="1.0" ?>
<data>
    <topic name="helsinki">
        <link>https://en.wikipedia.org/wiki/Helsinki</link>
    </topic>
    <topic name="example">
        <note name="a">
            <text>a</text>
            <timestamp>08.03.2024</timestamp>
        </note>
        <link>https://en.wikipedia.org/wiki/Example</link>
    </topic>
    <topic name="a">
        <note name="note 2">
            <text>text of note 2</text>
            <timestamp>09.03.2024</timestamp>
        </note>
        <note name="note 3">
            <text>3 text</text>
            <timestamp>10.03.2024</timestamp>
        </note>
    </topic>
</data>
```

## Failure management

### XML:
- The xml file doesn't exist: It gets created with an empty `<data></data>` structure to accommodate the data format.
- The xml file exists, but has incorrect formatting: The xml file gets backed up to backup_db.xml and db.xml is reset to an empty `<data></data>` structure.

### Commands
- An invalid command: Returns a message that the command is invalid.

### ADD requests
- The data has the wrong number of items: An error message is returned.
- The data is of a type that causes problems (list, etc): An error message is returned.
- Unknown error handling exists, too. 

### GET requests
- The data doesn't exist,: Returns a message stating that the topic is not found.
- The data is of a type that causes problems (list, etc): An error message is returned.
- Unknown error handling exists, too. 

### WIKI requests
- The topic is empty: An error message is returned. 
- The topic isn't found through the OpenSearch API: Returns a message stating that the topic couldn't be found in Wikipedia.
- The data is of a type that causes problems (list, etc): An error message is returned.
- Unknown error handling exists, too

### Client limitations
- Client uses input prompts: User inputs are limited to intended functionality.
- Topic name does not allow empty inputs: All topics have a name, preventing unexpected behaviour in case of extended functionality. 