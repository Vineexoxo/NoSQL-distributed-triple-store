# Distributed NoSQL Triple Store

This project aims to develop a distributed NoSQL triple store for managing and querying large-scale RDF (Resource Description Framework) datasets. The prototype utilizes a client-server architecture, where each server hosts a distinct NoSQL database management system (DBMS) such as MongoDB, MySQL, or Hive. These servers act as independent nodes capable of storing and managing triples (subject-predicate-object entities) within their respective databases.

## Features

1. **Distributed Architecture**: The system comprises multiple servers, each hosting a different NoSQL DBMS, enabling scalability and fault tolerance.
2. **State-based Object Management**: Triples are managed as state-based objects, enabling efficient tracking of changes and timestamps.
3. **Merge Operations and Conflict Resolution**: Merge operations and conflict resolution logic ensure data consistency across distributed servers, resolving conflicts based on timestamps and updating triple values accordingly.
4. **Client Interface**: The client interface allows users to perform operations such as querying, updating, merging, and fetching logs for auditing purposes.

## Technologies Used

- **Programming Language**: Python
- **Libraries**: PyMongo (for MongoDB integration), MySQL.connector (for MySQL integration), PyHive (for Hive integration)

## Getting Started

1. Clone the repository
2. Install the required dependencies
3. Configure the database connections by updating the appropriate settings in the `config.py` file.
4. Run the application

## Usage

The client interface provides the following commands:

- `query`: Query triples based on specified subject, predicate, or object criteria.
- `update`: Update or insert triple values in the distributed store.
- `merge`: Initiate a merge operation between servers to synchronize data and resolve conflicts.
- `fetch_logs`: Retrieve logs for auditing purposes.

Follow the prompts in the terminal-based interface to interact with the system and perform the desired operations.

## Testing

The project includes a comprehensive test suite to ensure the correctness and reliability of the system. To run the tests, execute the following command:
