import redis
import csv
import json

# Define constants
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CSV_FILE_PATH = 'diabetes_db.csv'

def load():
    #Load data from a CSV file into Redis, grouping by patient_id.
    try:
        # Create a Redis connection
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        # Open CSV file
        with open(CSV_FILE_PATH, mode='r') as file:
            reader = csv.DictReader(file)

            # Group data by patient_id
            data = {}
            for row in reader:
                patient_id = row.get('patient_id')
                if patient_id not in data:
                    data[patient_id] = []
                data[patient_id].append(row)
    
    except Exception as e:
        print(f"An unexpected error occurred while processing the CSV file: {e}")
        return "Failed to load data"
    
    try:
        # Save to Redis
        for patient_id, records in data.items():
            try:
                # Convert records to JSON string
                records_json = {i: json.dumps(record) for i, record in enumerate(records)}
                r.hmset(f'patient:{patient_id}', records_json)
            except Exception as e:
                return f"An unexpected error occurred while saving data for patient_id {patient_id}: {e}"
        
        return "Data loaded successfully"
    
    except Exception as e:
        print(f"An unexpected error occurred while saving data to Redis: {e}")
        return "Failed to save data"

def convert_record_to_dict(record: str):
    try:
        # Replace single quotes with double quotes to make it valid JSON
        record_json = record.replace("'", '"')
        
        # Convert the JSON string to a Python dictionary
        record_dict = json.loads(record_json)
        return record_dict
    except Exception as e:
        print(f"An unexpected error occurred in convert_record_to_dict: {e}")
        return {}

def get_patient_records(patient_id: int):
    try:
        # Create a Redis connection with decode_responses=True
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        
        # Fetch patient data from Redis
        patient_data = r.hgetall(f'patient:{patient_id}')
        
        # Convert the byte data to a dictionary
        patient_records = [convert_record_to_dict(record) for record in patient_data.values()]
        
        return patient_records
    except Exception as e:
        print(f"An unexpected error occurred in get_patient_records: {e}")
        # Return an empty list or handle this error as needed
        return []


def get_diabetes_statistics():
    try:
        # Create a Redis connection with decode_responses=True
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        
        # Get all patient keys
        keys = r.keys('patient:*')
        patients_num = len(keys)

        if patients_num == 0:
            # To avoid division by zero
            return 0.0

        diabetes_count = 0
        
        # Iterate over all patient keys retrieved from Redis
        for key in keys:
            patient_data = r.hgetall(key)
            # Iterate over all records for the current patient
            for record in patient_data.values():
                record_dict = convert_record_to_dict(record)
                if record_dict.get('has_diabetes') == '1':
                    # Increment the diabetes count and exit the loop for this patient
                    diabetes_count += 1
                    break
        
        # Calculate the diabetes probability 
        return diabetes_count / patients_num

    except Exception as e:
        print(f"An unexpected error occurred in get_diabetes_statistics: {e}")
        return 0.0  # Return 0.0 as a default value in case of unexpected error
    
def get_client_samples(client_id: int, field_name: str = None):
    try:
        # Fetch patient records
        patient_records = get_patient_records(client_id)
        
        if not patient_records:
            print("No patient records found.")
            return []  # Return an empty list if no records found

        if field_name:
            # Check if the field exists in any of the records
            field_exists = any(field_name in record for record in patient_records)
            
            if not field_exists:
                print(f"No such field: '{field_name}' found in records for client ID: {client_id}")
                return []  # Return an empty list if the field does not exist
            
            # If field_name is provided, return all values for that field
            field_values = [record.get(field_name) for record in patient_records]
            return field_values
        else:
            # If no field_name is provided, return all fields for each sample
            return patient_records
    
    except Exception as e:
        print(f"An unexpected error occurred in get_client_samples: {e}")
        return []
    
def get_client_avg_sample(client_id: int, field_name: str):
    try:
        if not field_name:
            return "Field name cannot be None."
    
        # Retrieve field values using get_client_samples
        field_values = get_client_samples(client_id, field_name)

        # Convert values to float and filter out None values
        field_values = [float(value) for value in field_values if value is not None]


        if not field_values:
            print(f"No valid values found for field: {field_name} and client ID: {client_id}")
            return float('nan')  # Return NaN if no valid field values found
                
        # Calculate the average
        avg_value = sum(field_values) / len(field_values)
        return avg_value

    except Exception as e:
        return f"An unexpected error occurred in get_client_avg_sample: {e}"