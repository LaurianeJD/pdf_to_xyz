import re
import os
from rdkit import Chem

def extract_coords(text:str):
    """Extract coordinates in text string and save all molecules in list of lists"""

    # Regex for: element coord-x coord-y coord-z
    # element needs to be only one letter
    # coord consider scientific notation and negative numberss
    pattern = re.compile(r'((([A-Z][a-z]?[0-9]*)|([0-9]{1,2}))\ *((\-?[0-9]\.[0-9]*\ *[eE]\ *\-?[0-9]*)|(\-?[0-9]\.[0-9]*))\ *((\-?[0-9]\.[0-9]*\ *[eE]\ *\-?[0-9]*)|(\-?[0-9]\.[0-9]*))\ *((\-?[0-9]\.[0-9]*\ *[eE]\ *\-?[0-9]*)|(\-?[0-9]\.[0-9]*)))')

    all_mols = []
    mol = []

    # Read text
    lines = text.split('\n')
    for line in lines:
        find = re.findall(pattern, line)
        # If coordinates line, add it to molecule
        if find:
            coord=[item[0] for item in find]
            for c in coord:
                # If atomic number, convert it in element letter
                if c[0].isdigit():
                    atomic_number_pattern = re.compile(r'([0-9]{1,2})')
                    find_atomic_number = re.search(atomic_number_pattern, c)
                    atomic_number = find_atomic_number.groups()[0]
                    letter = Chem.GetPeriodicTable().GetElementSymbol(int(atomic_number))
                    c = c.replace(atomic_number, letter, 1)
                mol.append(c)
        # If not anymore, save the molecule
        else:
            if mol:
                all_mols.append(mol)
            mol = []
    # Saved the last molecules if not already saved
    if mol:
        all_mols.append(mol)
    
    return all_mols

def write_xyz(list_mols:list, path_dir:str="./xyz_dir"):
    """Write list of coordinates into separate xyz files"""
    
    # Ensure the output directory exists
    os.makedirs(path_dir, exist_ok=True)

    # Iterate through each molecule in the list
    for idx, mol in enumerate(list_mols):
        # Create file and write data
        file_path = os.path.join(path_dir, f"molecule_{idx}.xyz")
        with open(file_path, 'w') as file:
            # Write the number of atoms
            file.write(f"{len(mol)}\n")
            # Write each coord to the file + empty line first
            for line in mol:
                file.write("\n" + line)

def save_xyz(text:str, path_dir:str="./xyz_dir"):
    list_mols = extract_coords(text)
    write_xyz(list_mols, path_dir)
    
