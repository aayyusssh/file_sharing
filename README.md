# File Sharing

The files uploaded by Operation User can be downloaded by client through secure encrypted URL. 

## Prerequisites

Make sure you have the following installed on your machine:

- Python (version 3)
- Pip (Python package installer)
- Virtualenv (optional but recommended)

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aayyusssh/file_sharing.git
   ```

## Navigate to the project directory:

   ```bash
   cd file_sharing
   ```

## Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

##Activate the virtual environment:

   ```bash
   # On Windows
   .\venv\Scripts\activate

   # On Linux/Mac
   source venv/bin/activate
   ```

## Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Apply database migrations:

   ```bash
   python manage.py migrate
   ```

## Create a superuser which will play the role of operation user:

   ```bash
   python manage.py createsuperuser
   ```
## Import the Postman Collection Provided in the Repository

## Run the development server:

   ```bash
   python manage.py runserver
   ```

The application will be accessible at http://localhost:8000/.
