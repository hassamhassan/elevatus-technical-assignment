import csv
import datetime
from typing import List, Dict, Any

from schemas.candidates_schema import SearchParametersSchema


async def add_data_filters(candidate_filter: SearchParametersSchema) -> Dict[str, Any]:
    """
    Generate filters based on the provided candidate_filter.

    Args:
        candidate_filter: SearchParametersSchema - The filter criteria for candidates.

    Returns:
        Dict[str, Any]: A dictionary containing filters to be applied in data retrieval.
    """
    filters = {}

    for field in candidate_filter.model_fields:
        value = getattr(candidate_filter, field)
        if value:
            filters[field] = value

    return filters


def add_data_to_csv(candidates: List[Dict[str, Any]]) -> None:
    """
    Write candidate data to a CSV file.

    Args:
        candidates: List[Dict[str, Any]] - List of dictionaries representing candidate data.
    """
    candidate_data = [candidate for candidate in candidates]

    with open(f"{datetime.datetime.now()}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=candidate_data[0].keys())
        writer.writeheader()
        writer.writerows(candidate_data)
