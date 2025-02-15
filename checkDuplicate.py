import json

# Define file path
file_path = './data/employers.json'

def check_company_duplicates():
    try:
        # Read JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Get all company names (keys from employers dictionary)
        company_names = list(data['employers'].keys())
        
        # Check for duplicate company names
        seen_companies = set()
        duplicate_companies = set()
        
        for company in company_names:
            if company in seen_companies:
                duplicate_companies.add(company)
            else:
                seen_companies.add(company)
        
        print("Check Results:")
        print("-" * 50)
        
        if not duplicate_companies:
            print("✓ No duplicate company names found")
            print(f"✓ Total number of companies: {len(company_names)}")
        else:
            print("! Found the following duplicate company names:")
            for company in duplicate_companies:
                print(f"  - {company}")
            print(f"! Number of duplicates found: {len(duplicate_companies)}")
        
        print("-" * 50)

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    check_company_duplicates()