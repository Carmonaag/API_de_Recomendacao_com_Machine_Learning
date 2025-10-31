import pytest
import pandas as pd

@pytest.fixture(scope="session")
def sample_data():
    """Gera dados de exemplo para os testes."""
    interactions_df = pd.DataFrame({
        "user_id": ["user1", "user1", "user2", "user3", "user3", "user3"],
        "item_id": ["item1", "item2", "item2", "item1", "item3", "item4"],
        "rating": [5, 4, 3, 5, 2, 1],
    })

    item_data_df = pd.DataFrame({
        "item_id": ["item1", "item2", "item3", "item4", "item5"],
        "category": ["cat1", "cat2", "cat1", "cat3", "cat2"],
        "description": ["desc1", "desc2", "desc3", "desc4", "desc5"],
    })
    
    user_data_df = pd.DataFrame({
        "user_id": ["user1", "user2", "user3"],
        "age": [25, 30, 35],
    })

    return {
        "interactions": interactions_df,
        "items": item_data_df,
        "users": user_data_df
    }
