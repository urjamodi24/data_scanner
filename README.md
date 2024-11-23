Here's how to structure your `README.md` file for your project, which includes a diagram and instructions to set up and run the project locally.

### Example of `README.md`

```markdown
# Sensitive Data Detection Tool

This project is a sensitive data detection tool that scans uploaded files for Personally Identifiable Information (PII) and Payment Card Information (PCI). The application extracts sensitive information like PAN, SSN, and Credit Card numbers from text files and stores it in a database.

## System Overview

The system consists of a backend application built using **Flask**, **SQLAlchemy**, and **SQLite**. The application allows users to upload files, scans them for sensitive data, and stores the extracted information in a database.

### Key Features:
- **File Upload**: Users can upload text files containing sensitive information.
- **Sensitive Data Extraction**: The system scans the files for PAN, SSN, and Credit Card numbers.
- **Database**: All files and the extracted sensitive data are stored in a SQLite database.
- **API Endpoints**: 
    - `/upload`: Endpoint to upload files.
    - `/files`: Endpoint to list all uploaded files with sensitive data.

## Database Design

The application uses an **SQLite** database with two primary tables:

### `File` Table:
| Field         | Type      | Description                             |
|---------------|-----------|-----------------------------------------|
| id            | Integer   | Primary Key                             |
| name          | String    | Name of the uploaded file               |
| upload_date   | DateTime  | Timestamp when the file was uploaded   |

### `SensitiveData` Table:
| Field         | Type      | Description                             |
|---------------|-----------|-----------------------------------------|
| id            | Integer   | Primary Key                             |
| type          | String    | Type of sensitive data (e.g., PAN, SSN) |
| content       | String    | Extracted sensitive data content        |
| classification| String    | Classification of the sensitive data    |
| file_id       | Integer   | Foreign Key (references `File.id`)      |

## System Diagram

```plaintext
  +-----------------+        +-----------------+        +------------------+
  |    Frontend    | -----> |  Flask Backend  | -----> |     Database     |
  |   (HTML/CSS)   |        |   (Python API)  |        |  (SQLite - File  |
  |                |        |                 |        |  and Sensitive   |
  +-----------------+        +-----------------+        |   Data tables)   |
                                             +--------> +------------------+
                                             |
                                             v
                                  +-------------------------+
                                  |  Sensitive Data Scanning |
                                  +-------------------------+
```

The **Frontend** (HTML/CSS) communicates with the **Flask Backend** via HTTP requests. The **Flask Backend** processes these requests and interacts with the **SQLite Database** to store the uploaded files and their extracted sensitive data.

## Installation Instructions

Follow these steps to set up and run the project locally:

### Prerequisites:
- Python 3.7 or higher
- `pip` (Python package manager)
- Git (for version control)

### Step 1: Clone the Repository

Clone the repository to your local machine.

```bash
git clone https://github.com/urjamodi24/data_scanner.git
cd data_scanner
```

### Step 2: Set up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies for your project.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, you can create one by running:

```bash
pip freeze > requirements.txt
```

### Step 4: Set up the Database

Before running the app, you'll need to set up the database. Flask-SQLAlchemy will create the necessary tables for you.

```bash
# Start the Flask shell and create the database
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### Step 5: Run the Application

Now that everything is set up, you can run the application locally.

```bash
python app.py
```

By default, the app will run on `http://127.0.0.1:5000/`.

### Step 6: Accessing the API

- To upload a file, use the `/upload` endpoint.
- To list all uploaded files and their sensitive data, use the `/files` endpoint.

## Endpoints

### `POST /upload`

Uploads a file and extracts sensitive data. The request should include a file in the form-data.

**Request:**
```bash
POST http://127.0.0.1:5000/upload
Content-Type: multipart/form-data
Body: file=<your file>
```

**Response:**
```json
{
  "message": "File 'example.txt' uploaded and processed successfully",
  "file_id": 1,
  "sensitive_data": [
    {
      "type": "SSN",
      "content": "123-45-6789",
      "classification": "PII"
    }
  ]
}
```

### `GET /files`

Fetches a list of all uploaded files along with their extracted sensitive data.

**Request:**
```bash
GET http://127.0.0.1:5000/files
```

**Response:**
```json
[
  {
    "file_id": 1,
    "file_name": "example.txt",
    "upload_date": "2024-11-23T12:34:56",
    "sensitive_data": [
      {
        "type": "SSN",
        "content": "123-45-6789",
        "classification": "PII"
      }
    ]
  }
]





