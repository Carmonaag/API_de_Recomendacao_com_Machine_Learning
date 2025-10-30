# Recommendation ML API

This is a Recommendation System API built with FastAPI. It provides item recommendations to users based on different strategies: Collaborative Filtering, Content-Based Filtering, and a Hybrid approach.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up the environment variables:**
    Create a `.env` file in the `app` directory and add the following variables:
    ```
    DATABASE_URL=postgresql://user:password@localhost:5432/recommendations
    REDIS_URL=redis://localhost:6379/0
    ```

4.  **Run the application:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

## API Endpoints

-   `GET /docs`: API documentation.
-   `GET /health`: Health check.
-   `POST /api/v1/recommendations/user/{user_id}`: Get recommendations for a user.
-   `POST /api/v1/models/train`: Trigger model training.
-   `GET /api/v1/models/{model_id}/evaluate`: Get model evaluation metrics.
-   `POST /api/v1/users/`: Create a user.
-   `GET /api/v1/users/`: Get all users.
-   `POST /api/v1/items/`: Create an item.
-   `GET /api/v1/items/`: Get all items.
