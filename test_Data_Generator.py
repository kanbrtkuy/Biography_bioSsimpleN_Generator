import json
import random
from datetime import datetime, timedelta
from tqdm import tqdm
import os
import argparse

class BioSsimpleGenerator:
    def __init__(self, data_dir="data", output_dir="output"):
        """
        Initialize the generator and load all necessary data
        :param data_dir: Directory containing JSON files
        :param output_dir: Directory for output files
        """
        self.data_dir = data_dir
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load all necessary data
        self.names = self._load_json("names.json")
        self.universities = self._load_json("universities.json")["universities"]
        self.majors = self._load_json("majors.json")["majors"]
        self.cities = self._load_json("cities.json")["cities"]
        self.employers = self._load_json("employers.json")["employers"]
        
        # Validate data sizes
        self._validate_data_sizes()
        
        # Define pronouns
        self.pronouns = [
            {"subject": "He", "possessive": "his"},
            {"subject": "She", "possessive": "her"}
        ]

        # Define generation space sizes
        self.N0 = 400 * 400 * 1000  # Total possible name combinations
        self.date_combinations = 12 * 28 * 200  # Total possible date combinations

        # Define months for date generation
        self.months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

    def _validate_data_sizes(self):
        """Validate that all data sizes meet the requirements"""
        assert len(self.names["first_names"]) == 400, "First names should be 400"
        assert len(self.names["middle_names"]) == 400, "Middle names should be 400"
        assert len(self.names["last_names"]) == 1000, "Last names should be 1000"
        assert len(self.universities) == 300, "Universities should be 300"
        assert len(self.majors) == 100, "Majors should be 100"
        assert len(self.cities) == 200, "Cities should be 200"
        assert len(self.employers) == 263, "Employers should be 263"

    def _load_json(self, filename):
        """Load and return data from a JSON file"""
        try:
            with open(os.path.join(self.data_dir, filename), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            raise

    def _generate_date(self):
        """
        Generate a random date following the format 'Month Day, Year'
        Constraints: 12 months × 28 days × 200 years
        """
        # Randomly select a month name
        month = random.choice([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        
        # Generate day (1-28)
        day = random.randint(1, 28)
        
        # Generate year (1825-2024)
        year = 1825 + random.randint(0, 199)
        
        # Return formatted date string
        return f"{month} {day}, {year}"

    def _generate_name(self):
        """
        Generate a random name following the 400×400×1000 constraint
        Returns a full name (first middle last)
        """
        first = random.choice(self.names["first_names"])
        middle = random.choice(self.names["middle_names"])
        last = random.choice(self.names["last_names"])
        return f"{first} {middle} {last}"

    def validate_generation_size(self, n):
        """
        Validate that the requested generation size doesn't exceed possible combinations
        :param n: Number of biographies to generate
        """
        if n > self.N0:
            raise ValueError(f"Requested size {n} exceeds maximum possible combinations {self.N0}")

    def generate_biography(self):
        """
        Generate a single biography following the template
        Returns a formatted biography string
        """
        name = self._generate_name()
        birth_date = self._generate_date()
        birth_city = random.choice(self.cities)
        university = random.choice(self.universities)
        major = random.choice(self.majors)
        employer = random.choice(list(self.employers.keys()))
        work_city = self.employers[employer]  # Work city is determined by employer
        pronouns = random.choice(self.pronouns)

        biography = (
            f"{name} was born on {birth_date}. "
            f"{pronouns['subject']} spent {pronouns['possessive']} early years in {birth_city}. "
            f"{pronouns['subject']} received mentorship and guidance from faculty members at {university}. "
            f"{pronouns['subject']} completed {pronouns['possessive']} education with a focus on {major}. "
            f"{pronouns['subject']} had a professional role at {employer}. "
            f"{pronouns['subject']} was employed in {work_city}."
        )
        
        return biography

    def generate_dataset(self, n, batch_size=10000):
        """
        Generate the complete dataset
        :param n: Number of biographies to generate
        :param batch_size: Number of biographies to write at once
        :return: Path to the generated file
        """
        # Validate generation size
        self.validate_generation_size(n)
        
        output_file = os.path.join(self.output_dir, f"bioSsimple_{n}.txt")
        print(f"Generating {n} biographies...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for i in tqdm(range(n), desc="Generating biographies"):
                biography = self.generate_biography()
                f.write(biography + '\n')
                
                if (i + 1) % batch_size == 0:
                    f.flush()
        
        print(f"Dataset generation completed. Saved to {output_file}")
        return output_file

def main():
    """
    Main function to handle command line arguments and run the generator
    """
    parser = argparse.ArgumentParser(description='Generate bioSsimple dataset')
    parser.add_argument('--size', type=int, choices=[500, 20000, 50000, 100000, 200000, 500000, 1000000],
                      required=True, help='Size of the dataset to generate')
    parser.add_argument('--data_dir', type=str, default='data',
                      help='Directory containing input JSON files')
    parser.add_argument('--output_dir', type=str, default='output',
                      help='Directory for output files')
    parser.add_argument('--seed', type=int, default=42,
                      help='Random seed for reproducibility')
    parser.add_argument('--batch_size', type=int, default=10000,
                      help='Batch size for writing to file')
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(args.seed)
    
    try:
        # Initialize generator
        generator = BioSsimpleGenerator(data_dir=args.data_dir, output_dir=args.output_dir)
        
        # Generate dataset
        output_file = generator.generate_dataset(args.size, args.batch_size)
        print(f"Successfully generated dataset at: {output_file}")
        
    except Exception as e:
        print(f"Error generating dataset: {e}")
        raise

if __name__ == "__main__":
    main()