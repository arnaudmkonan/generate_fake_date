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

    # Split the data format string into fields
    fields = data_format.split(",")

    # Generate data for each record
    for _ in range(num_records):
        record = {}
        for field in fields:
            # Use Faker methods based on field type (e.g., name, address)
            if field == "name":
                record[field] = fake.name()
            elif field == "address":
                record[field] = fake.address()
            # Add more cases for other data types as needed
            else:
                raise ValueError(f"Unsupported field type: {field}")
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
