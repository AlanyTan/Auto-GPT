""" Fix invalid escape sequences in JSON strings. """
import json
import re
from autogpt.config import Config
from autogpt.json_fixes.utilities import extract_char_position

CFG = Config()

def fix_unescaped_quotation_marks (json_to_load: str):
    regex = r'([^{}\]\[,: "\n]+[ ]*)\"([ ]*[^{}\]\[,: "]+)\"'
    json_to_load = (re.sub(regex,r"\1\"\2\"",txt))
    return json_to_load

def fix_invalid_escape(json_to_load: str, error_message: str) -> str:
    """Fix invalid escape sequences in JSON strings.

    Args:
        json_to_load (str): The JSON string.
        error_message (str): The error message from the JSONDecodeError
          exception.

    Returns:
        str: The JSON string with invalid escape sequences fixed.
    """

    while error_message.startswith("Invalid \\escape"):
        bad_escape_location = extract_char_position(error_message)
        json_to_load = (
            json_to_load[:bad_escape_location] + json_to_load[bad_escape_location + 1 :]
        )
        try:
            json.loads(json_to_load)
            return json_to_load
        except json.JSONDecodeError as e:
            if CFG.debug_mode:
                print("json loads error - fix invalid escape", e)
            error_message = str(e)
    return json_to_load
