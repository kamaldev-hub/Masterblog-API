# Blog Post Management System

## Description
This project is a full-stack web application for managing blog posts. It features a Flask backend API and a JavaScript frontend, allowing users to create, read, delete, and search blog posts.

## Features
- Create new blog posts with title, content, author, and date
- View all blog posts
- Delete existing blog posts
- Search posts by content
- Responsive design for various screen sizes

## Technologies Used
- Backend:
  - Python 3.x
  - Flask
  - SQLite
- Frontend:
  - HTML5
  - CSS3
  - JavaScript (ES6+)

## Setup and Installation

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Backend Setup
1. Clone the repository:
git clone https://github.com/kamaldev-hub/Masterblog-API


2. Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate


3. Install required packages:
pip install -r requirements.txt


4. Run the Flask application:
python app.py

   
The backend server will start running on `http://localhost:5002`.

### Frontend Setup
1. Navigate to the frontend directory:
cd frontend


2. Run the frontend application:
python frontend_app.py


The frontend server will start running on `http://localhost:5001`.

## Usage
1. Open a web browser and go to `http://localhost:5001`.
2. Enter the backend API URL (`http://localhost:5002`) in the provided input field and click "Load Posts".
3. Use the interface to add new posts, view existing posts, delete posts, and search for posts.

## API Endpoints

- `GET /posts`: Retrieve all posts
- `POST /posts`: Create a new post
- `DELETE /posts/<post_id>`: Delete a specific post
- `GET /posts/search/<query>`: Search for posts containing the query string