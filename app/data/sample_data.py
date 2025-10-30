import pandas as pd

def get_sample_interactions():
    data = {
        'user_id': [1, 1, 2, 2, 3, 3, 3, 4, 4, 5],
        'item_id': ['A', 'B', 'B', 'C', 'A', 'C', 'D', 'B', 'D', 'A'],
        'rating': [5, 4, 3, 5, 4, 5, 2, 4, 3, 5]
    }
    return pd.DataFrame(data)

def get_sample_items():
    data = {
        'item_id': ['A', 'B', 'C', 'D'],
        'category': ['electronics', 'books', 'books', 'electronics'],
        'description': [
            'A great pair of wireless headphones',
            'A classic novel about adventure',
            'A deep dive into machine learning',
            'A powerful and slim laptop'
        ]
    }
    return pd.DataFrame(data)
