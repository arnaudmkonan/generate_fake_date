import csv
import json
from faker import Faker
from xml.etree import ElementTree as ET


def generate_data(data_format, num_records):
    """
    Generates dummy data based on the provided format and number of records.

    Args:
        data_format (str): A string representing the desired data structure (e.g., "name,age,profession").
        num_records (int): The number of records to generate.

    Returns:
        list: A list of dictionaries containing generated data.
    """

    fake = Faker()
    data = []

    if isintance(data_format, dict):
        fields = data_format.keys()
    elif isintance(data_format, list):
        fields = data_format.split(",")

    # Use a whitelist approach for secure method calls
    allowed_methods = ["name", "address", "email",  "ssn", "city", "state", "country", "date_of_birth", "job", "text" ]  # Example whitelist

    # Generate data for each record
    for _ in range(num_records):
        record = {}
        fake = Faker()  # Create a Faker instance
        for field in fields:
            if field in allowed_methods:
                # Use attribute access on the Faker instance
                record[field] = getattr(fake, field)()
            else:
                raise ValueError(f"Field '{field}' not allowed for security reasons.")
        data.append(record)

    return data


def save_data(data, output_format, filename):
    """
    Saves the generated data to a file in the specified format.

    Args:
        data (list): A list of dictionaries containing generated data.
        output_format (str): The desired output format (CSV, XML, JSON).
        filename (str): The name of the output file.
    """

    if output_format == "csv":
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    elif output_format == "xml":
        root = ET.Element("data")
        for record in data:
            item = ET.SubElement(root, "record")
            for key, value in record.items():
                ET.SubElement(item, key).text = value
        tree = ET.ElementTree(root)
        tree.write(filename)
    elif output_format == "json":
        with open(filename, "w") as jsonfile:
            json.dump(data, jsonfile, indent=4)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


# Example usage
data_format = "name,age,email"
num_records = 10
output_format = "json"
filename = "output.json"

generated_data = generate_data(data_format, num_records)
save_data(generated_data, output_format, filename)

print(f"Generated {num_records} records and saved to {filename} as {output_format}")
