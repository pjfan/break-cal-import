# break-event-to-cal

## Overview
The `break-event-to-cal` project is a FastAPI application that allows users to input a web link for a breaking event. The application retrieves event details from the HTML of the provided link and generates a CSV file that can be imported into Google Calendar.

## Project Structure
```
break-event-to-cal
├── app
│   ├── main.py
│   ├── api
│   │   └── endpoints.py
│   ├── services
│   │   └── event_parser.py
│   ├── utils
│   │   └── csv_generator.py
│   └── models
│       └── event.py
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd break-event-to-cal
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

3. Use the endpoint to submit a web link for a breaking event. The application will parse the event details and generate a CSV file for Google Calendar import.

## Dependencies
- FastAPI
- requests
- pandas
- beautifulsoup4
- httpx
- uvicorn

## Future development
- Test code
- Edit what's going into the CSV vs. editing the JSON
- Option to generate ical instead of csv
- Bulk event upload from csv
- Expand sites that you can import events from (ig?)
- Direct google account integration (skip csv generation)

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.