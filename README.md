# Text-to-Image Web Application

This repository contains a simple web application that generates an image from user-provided text using Python, FastAPI, and Pillow.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Backend:** Python, FastAPI
- **Image Processing:** Pillow (PIL)
- **Server:** Uvicorn

## Features

- Generate an image from input text using a REST API.
- Download or clear generated images.
- Responsive and user-friendly web interface.
- Static file serving for frontend assets.

## Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/asis-shukla/text-to-image.git
    cd text-to-image
    ```

2. **(Optional) Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    Or, if using [pyproject.toml](pyproject.toml):
    ```bash
    pip install .
    ```

4. **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

5. **Access the app:**
    - Open [http://localhost:8000](http://localhost:8000) in your browser.

## API Endpoints

- `GET /api/info` — Get project and server info.
- `POST /api/text-to-image` — Generate an image from text.  
  **Request:** `{ "text": "your text here" }`  
  **Response:** `{ "text": "...", "image_url": "/static/..." }`
- `POST /api/clear` — Delete a generated image by filename.

## Project Structure

```
main.py
static/
    index.html
    style.css
    main.js
pyproject.toml
README.md
```

## License

This project is provided free of charge, with no restrictions on usage. It is distributed without any warranty; the authors are not liable for any damages or issues arising from its use.