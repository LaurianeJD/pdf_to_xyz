from pathlib import Path
import re


def correct_common_seperator(s: str)->str:
    """
    Correct common misread separators in OCR output
    Adjust the pattern and replacement as needed
    """
    # Pattern to match misread 'M001's
    pattern = r"([M¥\\\/][0OQ][0OQ][1Il!\|])"
    # Replace matches with 'M001'
    s = re.sub(pattern, "M001", s)
    s = s.replace("¥O001", "M001")
    return s


def process_ocr_results(ocr_result: str)->tuple:
    """
    Note: The indicies are hardcoded and may need to be adjusted based on the OCR output
    Args:
        ocr_result (str): raw ocr string

    Returns:
        tuple: header, main_text, footer
    """

    lst_results = ocr_result.split("\n")  # get raw ocr string and split by newline
    lst_results = [" ".join(str.split()) for str in lst_results]  # remove extra spaces
    ocr_text_postprocessed = "\n".join(lst_results)
    ocr_text_corrected = correct_common_seperator(ocr_text_postprocessed)
    lines = ocr_text_corrected.split("\n")
    
    
    header = lines[:6]  # get header
    footer = lines[-6:]  # get footer
    ocr_main_text = lines[6:-7]

    unwanted_chars = "«°=¥()[]#?~©"
    translation_table = str.maketrans("", "", unwanted_chars)
    NEG_SIGN = r"[-−–—]"

    ocr_main_text_processed = []
    for line in ocr_main_text:
        line = line.translate(translation_table).strip()
        line = re.sub(NEG_SIGN + r"\s*", "-", line).strip()
        line = re.sub(r"\s+", " ", line)
        ocr_main_text_processed.append(line)

    return header, ocr_main_text_processed, footer

def get_molecule_data_from_ocr(ocr_main_text_processed:list, debug=False)->tuple:
    """_summary_
    The function extracts the molecule data from the OCR output but it is
    hardcoded for the specific format of the OCR output.
    The function should be adjusted based on the OCR output format.
    Args:
        ocr_main_text_processed (list): list of strings
        debug (bool, optional):  Defaults to False.

    Returns:
        _type_: _description_
    """
    molecule1 = []
    molecule2 = []

    for line in ocr_main_text_processed:
        # Split at the first occurrence of 'M001'
        parts = line.split('M001')
        mol1_part = parts[0].strip()
        mol2_part = parts[1].strip()
        # mol2_part = ' '.join(parts[1].strip().split(' ')[4:])
        molecule1.append(mol1_part)
        molecule2.append(mol2_part)
        # else:
        #     # 'M001' not found, skip or handle accordingly
        #     print('M001 not found, skip or handle accordingly')
        #     continue
        
    molecule1 = [' '.join(line.split()[2:-1]) for line in molecule1]

    molecule1_altered = []
    for line in molecule1:
        if '-3.008463%0' in line:
            line = re.sub(r'-3.008463%0', '-3.008463360', line)
        molecule1_altered.append(line)

    molecule2_altered = []
    for idx, line in enumerate(molecule2):
        line = line.split(' ')
        len_line = len(line)
        match len_line:
            case 12:
                line = ' '.join(line[-6:-1])
            case 11:
                if idx == 61:
                    line = ' '.join(line[-6:-1])
                else:
                    line = ' '.join(line[-5:-1])
            case 10:
                line = ' '.join(line[-5:-1])
            case 9:
                if idx == 2:
                    line = ' '.join(line[-4:])
                else:
                    line = ' '.join(line[-5:-1])
            
        molecule2_altered.append(line)

    molecule2_altered_fixed_errors = []
    for line in molecule2_altered:
        if '97994288' in line:
            line = re.sub(r'97994288', '979942885', line)
        elif '48135742' in line:
            line = re.sub(r'48135742', '481357425', line)
        elif '-3.23071635' in line:
            line = re.sub(r'-3.23071635', '-3.230716365', line)
        elif '2.721697' in line:
            line = re.sub(r'2.721697', '2.7221697', line)
        molecule2_altered_fixed_errors.append(line)
    
    if debug:
        print('--'*50)
        print('DEBUG MODE')
        print('--'*50)
        print('Inspecting molecule1')
        for line in molecule1_altered:
            print(line)
        print('--'*50)
        print('Inspecting molecule2')
        for line in molecule2_altered_fixed_errors:
            print(line)
        
    
    return molecule1_altered, molecule2_altered_fixed_errors

def normalize_number(s: str)->str:
    """_summary_
    The function normalizes the number string by removing unwanted characters
    and ensuring the number has up to 9 decimal places.
    Change the function as needed to handle specific cases.
    
    TODO: Make the function more robust to handle more cases and more general.
    Args:
        s (str): _description_

    Returns:
        str: _description_
    """
    s = s.replace(' ', '')
    # Replace misread negative signs and special characters with standard '-'
    MISREAD_NEG_SIGNS = r'[-−–—=©]+'
    s = re.sub(r'^(' + MISREAD_NEG_SIGNS + r'\s*)+', '-', s)
    # Remove any non-digit characters except decimal point and negative sign
    s = re.sub(r'[^0-9\.\-]', '', s)
    # Handle multiple decimal points by keeping only the first one
    parts = s.split('.')
    if len(parts) > 2:
        s = parts[0] + '.' + ''.join(parts[1:])
    # If no decimal point and s is digits only (excluding negative sign), insert decimal after first digit
    if '.' not in s:
        if s.startswith('-'):
            if s[1:].isdigit():
                s = s[:2] + '.' + s[2:]
        else:
            if s.isdigit():
                s = s[0] + '.' + s[1:]
    # Ensure up to 9 decimal places
    if '.' in s:
        before_dp, after_dp = s.split('.')
        after_dp = after_dp[:9]  # Truncate to 9 digits after decimal
        s = before_dp + '.' + after_dp
    return s

def parse_number(s: str)->tuple:
    """
    The function parses the number string to a float number.
    """
    s_normalized = normalize_number(s)
    try:
        number = float(s_normalized)
        return number, s_normalized
    except ValueError:
        return None, None

def correct_element_symbol(s: str)->str:
    """
    Correct misread element symbols in OCR output
    """
    s = s.strip()
    s = s.capitalize()
    
    # Correct specific misreadings
    s = re.sub(r'Car|C.ar', 'C', s)
    s = re.sub(r'Nar|N.ar', 'N', s)
    s = re.sub(r'Hes|Has', 'H', s)
    s = re.sub(r'Qo|Qo|0\d+|0.|0|Oar', 'O', s)
    s = re.sub(r'C\d+', 'C', s)
    s = re.sub(r'N\d+', 'N', s)     
    s = re.sub(r'F\d+', 'F', s)
    s = re.sub(r'S\d+', 'S', s)    
    s = re.sub(r'O\d+', 'O', s)     
    
    # Remove remaining digits, hyphens, periods
    s = re.sub(r'\d', '', s)
    s = re.sub(r'-', '', s)
    s = re.sub(r'\.', '', s)
    s = s.strip()
    s = re.sub(r' ', '*', s)
    return s

def process_line(line:str)->tuple:
    """
    The function processes a line of OCR output to extract the element symbol and x, y, z coordinates.
    The function should be adjusted based on the OCR output format.
    """
    tokens = line.split()
    element = correct_element_symbol(tokens[-1])
    tokens_without_element = tokens[:-1]
    numbers = []
    i = 0
    while i < len(tokens_without_element):
        token = tokens_without_element[i]
        # Clean the token by removing unwanted characters
        token_clean = re.sub(r'[^0-9\.\-]', '', token)
        # count the total number of digits in the token
        total_digits = len(token_clean.replace('.', '').replace('-', ''))

        # Continue combining tokens until total_digits >= 10 or no more tokens
        while total_digits < 10 and i + 1 < len(tokens_without_element):
            i += 1
            next_token = tokens_without_element[i]
            next_token_clean = re.sub(r'[^0-9]', '', next_token)
            if next_token_clean:
                token_clean += next_token_clean
                total_digits = len(token_clean.replace('.', '').replace('-', ''))
            else:
                break  # Next token is not numeric, stop combining

        # Normalize and parse the token
        number, number_str = parse_number(token_clean)
        if number is not None:
            numbers.append((number, number_str))
        i += 1

    # Ensure we have at least three numbers for x, y, z
    if len(numbers) == 3:
        x, x_str = numbers[0]
        y, y_str = numbers[1]
        z, z_str = numbers[2]
        data_tuple = (element, x, y, z, x_str, y_str, z_str)
        return data_tuple
    else:
        print(f"Could not extract x, y, z from line: {line}")
        

def get_xyz_coord(molecule_data:tuple, debug=False)->list:
    """
    The function extracts the xyz coordinates from the molecule data.
    x, y, z  coordinates are float numbers.
    x_str, y_str, z_str are the original string representations of the numbers,
    ensuring the same number of digits are used.
    """
    xyz_coord = []
    for line in molecule_data:
        data = process_line(line)
        element, x, y, z, x_str, y_str, z_str = data
        xyz_coord.append((element, x_str, y_str, z_str))
    if debug:
        print('DEBUG MODE')
        for data in xyz_coord:
            print(data)
            element, x_str, y_str, z_str = data
            print(f"{element} {x_str} {y_str} {z_str}")
    return xyz_coord

        

def write_xyz_file(xyz_coord:list, filename:Path):
    """
    Write the xyz coordinates to a file.
    """
    with open(filename, "w") as file:
        file.write(str(len(xyz_coord)) + "\n\n")
        file.writelines("\t".join(i) + "\n" for i in xyz_coord)


def main():
    project_dir = Path(__file__).resolve().parents[0]
    with open(Path(project_dir, "examples/ocr_results/ocr_result_img_xyz.txt"), "r") as file:
        ocr_result = file.read()


    header, ocr_main_text_processed, footer = process_ocr_results(ocr_result)
    molecule1_data, molecule2_data = get_molecule_data_from_ocr(ocr_main_text_processed, debug=False) 

    molecule1_xyz_coord = get_xyz_coord(molecule1_data, debug=False)
    molecule2_xyz_coord = get_xyz_coord(molecule2_data, debug=False)
    
    write_xyz_file(molecule1_xyz_coord, Path(project_dir, "examples/created_xyz/example_ocr/molecule1_ocr.xyz"))
    write_xyz_file(molecule2_xyz_coord, Path(project_dir, "examples/created_xyz/example_ocr/molecule2_ocr.xyz"))

if __name__ == "__main__":
    main()
    
