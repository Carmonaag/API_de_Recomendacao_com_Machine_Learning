import logging
import numpy as np
from app.schemas.model import EvaluationMetrics
from app.data.sample_data import get_sample_interactions
from app.ml.utils.metrics import calculate_rmse, calculate_mae, precision_recall_at_k
from joblib import load

logger = logging.getLogger(__name__)

def evaluate_model(model_path: str, test_data: str) -> EvaluationMetrics | None:
    """
    Evaluates a trained model.
    """
    logger.info(f"Evaluating model from '{model_path}' using data from '{test_data}'")

    try:
        # Load the model
        model, user_item_matrix, item_ids = load(model_path)

        # Load the test data
        interactions = get_sample_interactions()
        test_df = interactions.copy() # In a real scenario, this would be a separate test set

        # Make predictions
        predictions = []
        for index, row in test_df.iterrows():
            user_id = row['user_id']
            item_id = row['item_id']
            rating = row['rating']

            if user_id in user_item_matrix.index and item_id in item_ids:
                user_index = user_item_matrix.index.get_loc(user_id)
                item_index = item_ids.get_loc(item_id)

                user_latent_matrix = model.transform(user_item_matrix.iloc[user_index].values.reshape(1, -1))
                reconstructed_ratings = np.dot(user_latent_matrix, model.components_)
                predicted_rating = reconstructed_ratings[0, item_index]
                predictions.append((user_id, item_id, rating, predicted_rating, None))

        if not predictions:
            logger.warning("No predictions were made. Cannot evaluate the model.")
            return None

        # Calculate metrics
        true_ratings = [p[2] for p in predictions]
        predicted_ratings = [p[3] for p in predictions]

        rmse = calculate_rmse(true_ratings, predicted_ratings)
        mae = calculate_mae(true_ratings, predicted_ratings)
        precision, recall = precision_recall_at_k(predictions, k=5)
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        metrics = {
            "rmse": rmse,
            "mae": mae,
            "precision_at_5": precision,
            "recall_at_5": recall,
            "f1_score": f1_score
        }

        logger.info(f"Evaluation metrics: {metrics}")
        return EvaluationMetrics(**metrics)

    except FileNotFoundError:
        logger.error(f"Model file not found at: {model_path}")
        return None
    except Exception as e:
        logger.error(f"Error during evaluation: {e}")
        return None
