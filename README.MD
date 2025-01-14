# AI Task Management Agent

This project demonstrates how AI agents can integrate with task management tools to automate workflows seamlessly. The application uses Cohere's LLM to process user inputs, interact with Asana, and perform actions like creating tasks with due dates—all through a conversational interface.

---

## Sample Screenshot

![Application Screenshot](sampleUI.jpeg)

---

## Features

- AI-powered task management
- Integration with Asana for demonstration
- Conversational interface
- Backend built with FastAPI
- Frontend built with Vite + React

---

## Tech Stack

- **Backend**: FastAPI, Python  
- **Frontend**: Vite + React  
- **Large Language Model**: Cohere  
- **Task Management Tool**: Asana  

---

## Prerequisites

- Python 3.8 or higher  
- Node.js and npm  
- An Asana account (for task management)  
- API keys for Cohere and Asana  

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mekazstan/task-create-agent.git
cd task-create-agent
```

### 2. Set Up the Backend

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
    ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
        pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Copy `.env.example` to `.env`
    ```bash
        cp ../.env.example ../.env
    ```
    - Fill in your Cohere API key, Asana API key, and other configurations.

5. Run the backend server:
    ```bash
        uvicorn main:app --reload
    ```
    The backend server will start on http://127.0.0.1:8000.

### . Set Up the Frontend
1. Navigate to the frontend folder:
    ```bash
        cd ../frontend
    ```

2. Install dependencies:
    ```bash
        npm install
    ```
3. Start the frontend development server:
    ```bash
        npm run dev
    ```
    The frontend will start on http://127.0.0.1:5173

### Usage
1. Open the frontend in your browser.
2. Interact with the AI assistant by providing task-related inputs.
3. The backend will process your requests and interact with Asana to manage tasks.

### Contributing
Contributions are welcome! If you'd like to improve this project, feel free to:

1. Fork the repository.
2. Make your changes.
3. Submit a pull request with a detailed description of your modifications.

### License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute this project under the terms of the license.

### Author
Chukwuemeka Stanley
For more projects, vist my ![GitHub Repo](https://github.com/Mekazstan)