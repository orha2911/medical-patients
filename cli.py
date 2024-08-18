import argparse
from data_processing import get_diabetes_statistics, load, get_client_avg_sample, get_client_samples

# Initialize the parser
parser = argparse.ArgumentParser(description="Medical Data Analysis CLI")

# Add arguments
parser.add_argument("command", choices=['get_diabetes_statistics', 'load', 'get_client_avg_sample', 'get_client_samples'], help="The operation to perform")
parser.add_argument("--client_id", type=int, help="client id", default=None)
parser.add_argument("--field_name", type=str, help="field name", default=None)

# Parse the arguments
args = parser.parse_args()

# Perform the operation
if args.command == "load":
    result = load()
elif args.command == "get_diabetes_statistics":
    result = get_diabetes_statistics()
elif args.command == "get_client_avg_sample":
    result = get_client_avg_sample(args.client_id, args.field_name)
elif args.command == "get_client_samples":
    result = get_client_samples(args.client_id, args.field_name)

# Print the result
print(f"Result: {result}")
