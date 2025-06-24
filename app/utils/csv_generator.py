import pandas as pd
import tempfile

def generate_csv(event_details: dict) -> str:
    """
    Generates a temporary CSV file suitable for calendar import from an event_details dictionary.
    Returns the temp file path.
    """
    # Prepare the description with event_link as the first line
    event_link = event_details.get("event_link", "")
    description = event_details.get("description", "")

    # Format brackets as "Name (Format)"
    brackets = event_details.get("brackets", [])
    if brackets:
        bracket_lines = [f"{b['name']} ({b['format']})" for b in brackets if b.get('name') and b.get('format')]
        brackets_text = "\n".join(bracket_lines)
        if description:
            full_description = f"{event_link}\n{description}\n{brackets_text}" if event_link else f"{description}\n{brackets_text}"
        else:
            full_description = f"{event_link}\n{brackets_text}" if event_link else brackets_text
    else:
        full_description = f"{event_link}\n{description}" if event_link else description

    row = {
        "Subject": event_details.get("title", ""),
        "Start Date": event_details.get("start_date", ""),
        "Start Time": event_details.get("start_time", ""),
        "End Date": event_details.get("end_date", ""),
        "End Time": event_details.get("end_time", ""),
        "All Day Event": "False",
        "Description": full_description,
        "Location": event_details.get("location", ""),
        "Private": "False"
    }

    df = pd.DataFrame([row])
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="", encoding="utf-8")
    # Use quoting=1 to ensure all fields with commas are quoted (csv.QUOTE_ALL)
    df.to_csv(tmp.name, index=False, quoting=1)
    tmp.close()
    return tmp.name
