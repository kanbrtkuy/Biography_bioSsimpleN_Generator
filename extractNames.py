import json
import random

# Define paths
source_path = './sourceData'
output_path = './data'

def load_names(filename):
    """Load name list from file"""
    with open(f'{source_path}/{filename}', 'r') as file:
        return json.load(file)

def random_select(names_list, count):
    """Randomly select specified number of unique names"""
    if len(names_list) < count:
        print(f"Warning: Source data only has {len(names_list)} names, less than requested {count}")
        count = len(names_list)
    
    unique_names = list(set(names_list))
    return random.sample(unique_names, count)

def generate_names_file():
    """Generate names.json file"""
    try:
        # Load source data
        first_names = load_names('firstNames.json')
        middle_names = load_names('middleNames.json')
        last_names = load_names('lastNames.json')

        # Randomly select names
        selected_first_names = random_select(first_names, 400)
        selected_middle_names = random_select(middle_names, 400)
        selected_last_names = random_select(last_names, 1000)

        # Create output data structure
        output_data = {
            "first_names": selected_first_names,
            "middle_names": selected_middle_names,
            "last_names": selected_last_names
        }

        # Write to output file
        with open(f'{output_path}/names.json', 'w') as file:
            json.dump(output_data, file, indent=4)

        print("Successfully generated names.json")
        print(f"Selected {len(selected_first_names)} first names")
        print(f"Selected {len(selected_middle_names)} middle names")
        print(f"Selected {len(selected_last_names)} last names")

    except FileNotFoundError as e:
        print(f"Error: Source file not found - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: JSON format error - {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

def generate_universities_file():
    """Generate universities.json file"""
    try:
        # Read source JSON file
        with open(f'{source_path}/universitySource.json', 'r') as file:
            universities_data = json.load(file)

        # Extract all university names
        university_names = [university['name'] for university in universities_data]

        # Randomly select universities
        sample_size = min(300, len(university_names))
        selected_universities = random.sample(university_names, sample_size)

        # Create output data structure
        output_data = {
            "universities": selected_universities
        }

        # Write to output file
        with open(f'{output_path}/universities.json', 'w') as file:
            json.dump(output_data, file, indent=4)

        print("Successfully generated universities.json")
        print(f"Selected {sample_size} universities")

    except FileNotFoundError as e:
        print(f"Error: Source file not found - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: JSON format error - {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Generate both files
    generate_names_file()
    print("-" * 50)
    generate_universities_file()