"""Utils functions for the CIE10 mapping project."""

import pandas as pd


def clean_cie10_code(code):
    """Normalize a CIE10 code to a standardized format.

    - Adds '.0' to codes that start with 'F' and contain only digits afterward (e.g., 'F3' becomes 'F3.0').
    - Removes a trailing '0' after the decimal in codes like 'F3.10' to make them 'F3.1'.
    - Leaves codes unchanged if they don't match either pattern.

    Parameters:
        code (str): A CIE10 code as a string.

    Returns:
        str: The normalized CIE10 code.
    """
    # If key starts with 'F' and the rest are digits and no dot, change key to have '.0'
    if code.startswith("F") and code[1:].isdigit() and "." not in code:
        return f"{code}.0"
    # If key matches pattern F<digits>.<digits>0 (e.g., F3.10), convert to F<digits>.<digits> (e.g., F3.1)
    elif (
        code.startswith("F")
        and "." in code
        and code.endswith("0")
        and not code.endswith(".0")
    ):
        return code[:-1]
    else:
        return code


def read_cie10_file(file_path):
    """Read a CSV file containing CIE10 variable-label mappings and returns a complete mapping dictionary.

    The function processes the CSV to exclude entries with label "<none>", constructs a dictionary
    mapping CIE10 codes to their descriptions, adds additional predefined mappings, and normalizes
    CIE10 codes by appending '.0' to those that start with 'F' and are followed by digits without a period.

    Parameters:
        file_path (str): The path to the CSV file containing CIE10 variables and their labels.
                         Expected columns are "Variable" and "Label".

    Returns:
        dict: A dictionary mapping CIE10 codes (as strings) to their corresponding descriptions.
    """
    vars_df = pd.read_csv(file_path)

    vars_df = vars_df[vars_df["Label"] != "<none>"]
    cie10_map = dict(zip(vars_df["Variable"], vars_df["Label"]))

    # Add the CIE10 values that are not in the vars_df
    CIE10_values_not_in_vars = {
        "F32": "Episodio depresivo",
        "F33": "Trastorno depresivo mayor, recurrente",
        "F4": "Trastorno de ansiedad, disociativo, relacionado con estrés y otros trastornos mentales somatomorfos no psicóticos",
        "F40": "Trastornos de ansiedad fóbica",
        "F50": "Trastornos de la conducta alimentaria",
        "COGNITIV": "Dimensión cognitiva",
        "FAM_APO": "Problemas y conflictos familiares",
        "LAB_MOB": "Problemas y conflictos laborales",
        "No_DX": "No diagnóstico",
        "PAREJ": "Problemas y conflictos de pareja",
        "altas_capacidades": "Altas capacidades intelectuales",
    }
    cie10_map.update(CIE10_values_not_in_vars)

    # Clean the cie10 codes
    cie10_map = {clean_cie10_code(key): value for key, value in cie10_map.items()}

    return cie10_map
