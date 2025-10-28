# Maintenance Service

This is a Flask backend application for managing maintenance services.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd maintenance-service
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. Set up environment variables in the `.env` file.

## Running the Application

To run the application, execute the following command:
```
python src/app.py
```

## Testing

To run the tests, use the following command:
```
pytest
```

## License

This project is licensed under the MIT License.



# maintenance-service/
# ├── app/
# │   ├── __init__.py
# │   ├── models/
# │   │   ├── __init__.py
# │   │   └── maintenance.py
# │   ├── routes/
# │   │   ├── __init__.py
# │   │   └── maintenance_routes.py
# │   ├── services/
# │   │   ├── __init__.py
# │   │   └── maintenance_service.py
# │   ├── schemas/
# │   │   ├── __init__.py
# │   │   └── maintenance_schema.py
# │   └── utils/
# │       ├── __init__.py
# │       └── validators.py
# ├── config.py
# ├── requirements.txt
# └── run.py