# data_scanner

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
