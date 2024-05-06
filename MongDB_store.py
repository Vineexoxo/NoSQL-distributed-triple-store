from datetime import datetime
import pymongo
from server_interface import TripleStore

class MongoDBTripleStore(TripleStore):
    def __init__(self, dbname, host, port):
        self.server_type="mongo"
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[dbname]
        self.triples_collection = self.db['triples']

    def query(self, subject, predicate):
        return list(self.triples_collection.find({"subject": subject, "predicate": predicate}))

    def update(self, subject, predicate, obj):
        current_timestamp = datetime.now()
        result = self.triples_collection.update_one(
            {"subject": subject, "predicate": predicate},
            {"$set": {"object": obj, "timestamp": current_timestamp}},
            upsert=True  # Insert if the document does not exist
        )
        print(result)
        # Log the update
        self.db['log'].insert_one({
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "timestamp": current_timestamp
        })
    def fetch_logs(self, server_id):
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_merge_timestamp = self.db['merge_log'].find_one({"server_id": server_id}, sort=[("timestamp", pymongo.DESCENDING)])

        triplets = []

        if last_merge_timestamp:
            last_merge_timestamp = last_merge_timestamp["timestamp"]

            # Fetch logs from the database
            logs = self.db['log'].find({"timestamp": {"$gt": last_merge_timestamp}})

            # Update merge log timestamp
            self.db['merge_log'].update_one({"server_id": server_id}, {"$set": {"timestamp": current_timestamp}})

            # Iterate over each log entry and create triplets
            for log in logs:
                triplet = (log["subject"], log["predicate"], log["object"], log["timestamp"])
                triplets.append(triplet)

        else:
            # If there are no previous merge timestamps, fetch all logs
            logs = self.db['log'].find()

            # Insert new entry in merge log
            self.db['merge_log'].insert_one({"server_id": server_id, "timestamp": current_timestamp})

            # Iterate over each log entry and create triplets
            for log in logs:
                triplet = (log["subject"], log["predicate"], log["object"], log["timestamp"])
                triplets.append(triplet)

        return triplets
    def merge(self, server_object):
        log_entries=server_object.fetch_log(self.server_type)
        for log_entry in log_entries:
            subject, predicate, obj, timestamp = log_entry

            # Check if the entry already exists in the main collection based on subject and predicate
            existing_entry = self.main_collection.find_one({"subject": subject, "predicate": predicate})

            if existing_entry:
                # Check if the existing entry's timestamp is older than the new log entry's timestamp
                if existing_entry["timestamp"] < timestamp:
                    # Entry exists and its timestamp is older, update it with the new object and timestamp
                    self.main_collection.update_one({"_id": existing_entry["_id"]},
                                                    {"$set": {"object": obj, "timestamp": timestamp}})
            else:
                # Entry does not exist, insert a new document
                self.main_collection.insert_one({"subject": subject, "predicate": predicate, "object": obj, "timestamp": timestamp})


    def load_tsv_file(self, file_path):
        current_timestamp = datetime.now()
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(' ')
                if len(data) == 3:
                    subject, predicate, obj = data
                    self.triples_collection.update_one(
                        {"subject": subject, "predicate": predicate},
                        {"$set": {"object": obj, "timestamp": current_timestamp}},
                        upsert=True
                    )
                else:
                    print(f"Ignore line: {line.strip()}. Not in the format 'subject predicate object'.")

