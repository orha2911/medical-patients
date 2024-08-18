# Medical Data Analysis CLI

## Overview

This script provides a CLI tool for analyzing and managing diabetes-related medical data using Redis. It enables data loading, statistical analysis, and data retrieval through simple CLI commands. This project, my first in Python, has been a valuable learning experience.
## Setup
### 1. **Clone the Repository**

Clone the repository to your local machine:

`git clone https://github.com/orha2911/medical-patients`

### 2. **Navigate to the Project Directory**

`cd medical-patients`

### 3. **Preparing to Run the Script**

Before running the script, ensure the following:

#### Windows:

Download and install the Redis Windows port from Redis on Windows GitHub.

#### Mac:

Install Homebrew (if not already installed):
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

Install Redis:
  ```bash
brew install redis
  ```

Start Redis:
  ```bash
brew services start redis
  ```

Install Python packages:
  ```bash
pip install redis
  ```

#### Configuration:
  If needed - update REDIS_HOST, REDIS_PORT, and CSV_FILE_PATH in the script according to your environment.

## Running the Script
To use the CLI, run the script with one of the commands listed below.

### Commands

- `load`: Load data into the system. **This must be run before any other command.**
- `get_diabetes_statistics`: Get overall statistics for diabetes data.
- `get_client_avg_sample`: Get the average value of a specific field for a given client.
- `get_client_samples`: Get all samples of a specific field for a given client.

### Command Arguments

- `--client_id`: The ID of the client for which you want to perform the operation. Required for `get_client_avg_sample` and `get_client_samples`.
- `--field_name`: The field name to query. Required for `get_client_avg_sample` and optional for `get_client_samples`.

### Example Commands
```bash
python cli.py load
  ```

```bash
python cli.py get_client_avg_sample --client_id 2 --field_name cholestoral
  ```

## Technologies

Several technologies were evaluated for managing data in this project:

### Pickle
- **Pros:**
  - Easy serialization of Python objects.
- **Cons:**
  - Inefficient for large-scale applications.
  - Not ideal for concurrent access.

### Python Cache
- **Pros:**
  - Suitable for temporary caching.
- **Cons:**
  - Limited to runtime memory.
  - Lacks long-term storage capabilities.

### Parquet
- **Pros:**
  - Efficient columnar storage for large datasets.
- **Cons:**
  - Complex management.
  - Not designed for real-time access.

### Redis
- **Pros:**
  - **Performance:** Fast in-memory data store.
  - **Scalability:** Handles large datasets and scales easily.
  - **Ease of Use:** Simple commands for data manipulation.
  - **Modern Tool:** Popular for real-time analytics and caching.
- **Cons:**
  - Requires managing an external service.

### Conclusion
Redis was chosen for its superior performance, ease of use, scalability, and modern features, making it ideal for the script’s requirements.
