# Biography Simple N Generator

## Project Overview
This project aims to implement the bioSsimple(N) dataset generation as described in Section 2 on page 6 of [Physics of Language Models: Part 3.3,
Knowledge Capacity Scaling Laws](https://arxiv.org/pdf/2404.05405). The bioSsimple(N) dataset is characterized by biographies generated with fixed random selection and ordering of sentence templates.

## Project Purpose
The main purpose is to generate a large-scale biographical dataset with controlled variability and consistent structure. Each biography follows a template-based approach where variables are filled from predefined sets of possible values.

## Data Space Definition

### Name Generation Space (N0 = 400 × 400 × 1000)
- 400 first names
- 400 middle names
- 1,000 last names

### Attribute Value Spaces
- Birth Dates: 12 months × 28 days × 200 years
- Birth Cities: 200 city names
- Universities: 300 universities
- Majors: 100 academic majors
- Employers: 263 company names
- Work Cities: Determined by employer headquarters location
- Pronouns: he/she (2 options)

## Example Biography Template
```text
[FirstName] [MiddleName] [LastName] was born on [Month] [Day], [Year] in [BirthCity]. 
[Pronoun] received guidance from faculty at [University] where [pronoun] studied [Major]. 
[Pronoun] worked at [Employer] in [WorkCity].
```

## Project Structure

```bash
Biography_bioSsimpleN_Generator/
├── data/                    # Core data files
│   ├── names.json          # Combined name data
│   ├── universities.json   # University information
│   ├── majors.json        # Academic majors
│   ├── cities.json        # City information
│   └── employers.json     # Employer information
├── sourceData/             # Source data and processing scripts
│   ├── firstNames.json    # First names dataset
│   ├── lastNames.json     # Last names dataset
│   ├── middleNames.json   # Middle names dataset
│   └── universitySource.json  # University source data
├── output/                 # Generated biography files
├── dataGenerator.py   # Main generation script
├── extractNames.py    # First/middle/last/school name extraction utility
├── checkDuplicate.py  # Duplication checker
└── README.md              # Project documentation
```

## Data Sources

### Name Data
The source name data in `sourceData/firstNames.json`, `sourceData/middleNames.json`, and `sourceData/lastNames.json` are obtained from:
- Source: [random-name GitHub repository](https://github.com/dominictarr/random-name/tree/master)

### University Data
The university information in `sourceData/universitySource.json` is sourced from:
- Source: [Universities API Documentation](https://documenter.getpostman.com/view/35240/SVmyRxAn)

### Other Data
The following files contain ChatGPT-generated random, unique entries:
- `majors.json`: 100 unique academic majors
- `cities.json`: 200 unique city names
- `employers.json`: 263 unique company names

Note: Due to the large number of employer entries (263), `checkDuplicate.py` is used to verify and ensure no duplicate company names exist in the generated data.

## Data Extraction Process

`extractNames.py` generates both `data/names.json` and `data/universities.json` by randomly sampling from source files:

### Source Files
- `sourceData/firstNames.json`
- `sourceData/middleNames.json`  
- `sourceData/lastNames.json`
- `sourceData/universitySource.json`

### Generated Files
`extractNames.py` randomly extracts:
- Name space (N0 = 400 × 400 × 1000):
  - 400 first names
  - 400 middle names 
  - 1000 last names
- 300 unique universities

The extracted data is saved to:
- `data/names.json`
- `data/universities.json`

## Data Generation Usage

### Basic Usage

Generate 50,000 biographies:

```bash
python generate_dataset.py --size 50000
```

### Advanced Usage
Generate with custom directories:
```bash
python generate_dataset.py --size 100000 --data_dir custom_data --output_dir custom_output
```

Set specific random seed:
```bash
python generate_dataset.py --size 200000 --seed 123
```

Modify batch size:
```bash
python generate_dataset.py --size 500000 --batch_size 20000
```

### Parameters
```bash
--size: Number of biographies to generate (required)
--data_dir: Input JSON files directory (default: 'data')
--output_dir: Output files directory (default: 'output')
--seed: Random seed for reproducibility (default: 42)
--batch_size: Batch size for file writing (default: 10000)
```

Output Format
```bash
Filename: bioSsimple_[size].txt
One biography per line
UTF-8 encoding
Each biography follows a fixed 6-sentence template
Dates formatted as "Month Day, Year"
```

