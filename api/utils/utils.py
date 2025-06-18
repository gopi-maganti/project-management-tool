from typing import Dict

def stringify_errors(errors: Dict) -> Dict:
    """
    Converts DRF error details into plain string format for clean logging.

    Args:
        errors (dict): Serializer or form errors.

    Returns:
        dict: Flattened stringified error dictionary.
    """
    return {
        k: [str(item) for item in v] if isinstance(v, list) else str(v)
        for k, v in errors.items()
    }

def pretty_print_errors(errors: Dict) -> str:
    """
    Converts error details into a pretty-printed string format.

    Args:
        errors (dict): Serializer or form errors.

    Returns:
        str: Pretty-printed string of errors.
    """
    return "\n".join(
        f"{key}: {', '.join(value) if isinstance(value, list) else value}"
        for key, value in stringify_errors(errors).items()
    )