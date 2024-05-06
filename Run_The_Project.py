import psycopg2
from server_interface import TripleStore
from postgres_triple_store import \
    MySQLTripleStore  # Assuming your PostgresTripleStore class is defined in a separate module
import subprocess
from datetime import datetime
from server_interface import TripleStore
from MongDB_store import MongoDBTripleStore

import mysql.connector

def start_mongodb_server():
    # Start MongoDB server using subprocess
    print("Starting MongoDB server...")
    subprocess.Popen(["mongod"])  # Adjust the command as per your MongoDB installation

def main():
    # Initialize PostgresTripleStore with your database credentials
    mongodb_triple_store = MongoDBTripleStore(dbname="triples", host="localhost", port=27017)

    # Example usage of query method
    mongodb_triple_store.load_tsv_file(r"C:\Users\shahi\OneDrive\Documents\data.txt")
    results = mongodb_triple_store.query("hi", "hey")
    print("Query Results:", results)

    # Example usage of update method
    mongodb_triple_store.update("hi", "hey", "new_object_value")
    print("Update Successful")

    dbname = "triples"
    user = "root"
    password = "Shishir@123"
    host = "localhost"  # Replace "your_host" with your actual host
    port = 3306  # Assuming your port is 8000, change it if it's different


    triple_store = MySQLTripleStore(dbname, user, password, host, port)

    # Example usage of query method
    # triple_store.load_tsv_file(r"C:\Users\shahi\OneDrive\Documents\data.txt")


    # Example usage of update method
    triple_store.update("hi", "hey", "new_object_value1")
    print("Update Successful")
    results = triple_store.query("hi", "hey")
    print("Query Results:", results)
    results1=triple_store.fetch_logs(mongodb_triple_store.server_type)
    triple_store.merge(mongodb_triple_store)
    # Example usage of merge method
    # Implement merge logic in your merge method in PostgresTripleStore class
    # triple_store.merge(server_id)


if __name__ == "__main__":
    main()
