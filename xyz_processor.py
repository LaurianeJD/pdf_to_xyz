from openai import OpenAI

def xyz_processor(raw_string:str, api_key_path="./api_key.txt", role="isolate", model="gpt-4o-mini"):
    """
    Extracts and formats XYZ coordinates from a raw string using OpenAI API.

    This function processes a string that contains multiple chemical XYZ coordinate blocks,
    either isolating and formatting them into a clean template, or cleaning the block for inconsistencies.

    Args:
        raw_string (str): The raw string containing multiple XYZ coordinate blocks. Each XYZ block is composed 
            of an atom descriptor followed by three numerical coordinates, which can be in scientific notation.
        api_key_path (str, optional): The path to the file containing the OpenAI API key. Defaults to 
            "/home/jovyan/work/15-1-castor/code_snippets/api_key.txt".
        role (str, optional): The processing mode. Can be either "isolate" or "clean". 
            - "isolate": Extracts and formats the XYZ blocks into a consistent template.
            - "clean": Cleans the XYZ blocks by removing inconsistencies, such as formatting errors or unnecessary spaces.
            Defaults to "isolate".
        model (str, optional): the OpenAI model to use. Defaults to "gpt-4o-mini".

    Returns:
        openai.Message: The completion response from the OpenAI API, which contains the processed XYZ coordinates.

    Example:
        >>> xyz_extractor("H  0.000000  0.000000  0.000000\nO  0.000000  0.000000  1.207400\n")
        'H  0.000000  0.000000  0.000000\nO  0.000000  0.000000  1.207400\n'

    Raises:
        FileNotFoundError: If the API key file is not found at the specified path.
        openai.error.OpenAIError: If there is an issue with the OpenAI API request.

    """
    
    with open(api_key_path, "r") as f:
        api_key=f.read()
    client = OpenAI(api_key = api_key)
    isolate_message= "You are a helpful assistant. Your job is to take a string that is composed of multiple chemical XYZ coordinates block from XYZ files and to format them correctly."\
            "An XYZ block looks like this: <ATOM_DESCRIPTOR>\t<NUMBER>\t<NUMBER>\t<NUMBER>. The atom descriptor can be C, O, Na, I,... And the numbers can be either in scientific notation. The selected number should in any way not be an int, but rather a precise number"\
            "Note that an XYZ block will always follow this general principle but there may be more columns, that you should discard, and there may be some variation in the formating. The produced template should still remain the same."\
            "Your answer should look like this: <ATOM_DESCRIPTOR>\t<NUMBER>\t<NUMBER>\t<NUMBER>\n<ATOM_DESCRIPTOR>\t<NUMBER>\t<NUMBER>\t<NUMBER>\n<ATOM_DESCRIPTOR>\t<NUMBER>\t<NUMBER>\t<NUMBER>... ."\
            "strictly adhere to the answer template and pay attention that the columns are straight using the number of spaces."
            #"Do not use spaces between the elements, but use tabs"},
    clean_message="You are a helpful assistant. Your job is to take a string that is composed of multiple chemical XYZ coordinates blocks from XYZ files and to clean."\
            "An XYZ block looks like this: <ATOM_DESCRIPTOR>\t<NUMBER>\t<NUMBER>\t<NUMBER>. The atom descriptor can be C, O, Na, I,... And the numbers can be either in scientific notation. The selected number should in any way not be an int, but rather a precise number"\
            "Note that an XYZ block will always follow this general principle but there may be more columns, that you should discard, and there may be some variation in the formating."\
            "Your answer should be the same string back, but inconsistencies removed. Inconsistencies mainly consist of spaces in odd places, anything out of place that is the result of an OCR parsing error."\
            "Do not add any text as a response, only return the cleaned string"
    separate_message="You are a helpful assistant. Your job is to take a string that is composed of multiple chemical XYZ coordinates and isolate them, separating them by a line of stars: *******************. Remove everything that is not a XYZ coordinates block. At the beginning of each produced block, write a unique name that will be the file name"
    
    message={"isolate": isolate_message, "clean": clean_message, "separate": separate_message}
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": message[role] }, {"role": "user", "content": raw_string}]
        
    )
    
    return completion.choices[0].message.content

if __name__=="__main__":
    xyz_processor("dfsdgfdfndsfnwfewihfpiewnfpiregpirengregèregèregèorejgorejoijtp4jin wéoeif j'aime les jus d'orange1 Pd       -1.332314       0.071934   0.041918  ''\n P        -3.633249       0.002904       0.027078  '' Pd     1.33 2232             0.071  594      -0.041948   P          3.63318       0.002679      -0.027147  ' I         0.000301       2.441273        3.5e-05  I        -0.000418      -2.305068        3.1e -05 '", role="clean")
    with open("output.txt", "w") as f:
        f.write(completion.choices[0].message.content)