import requests
import pandas as pd
import time

def get_steam_reviews(app_id, num_reviews=30000, sleep_time=1):
    """
    Fetches Steam reviews for a given app_id.
    
    :param app_id: The Steam App ID for the game.
    :param num_reviews: The number of reviews to fetch (up to 100,000 per request).
    :param sleep_time: Sleep time between requests to prevent rate limiting.
    :return: A DataFrame containing the reviews.
    """
    url = "https://store.steampowered.com/appreviews/"
    params = {
        'json': 1,
        'filter': 'most_helpful',
        'language': 'english',
        'purchase_type': 'all',
        'num_per_page': 100,  # Fetch 100 reviews per page
    }
    
    all_reviews = []
    start_offset = 0
    
    while start_offset < num_reviews:
        params['start_offset'] = start_offset
        response = requests.get(f"{url}{app_id}", params=params)
        data = response.json()
        
        if 'reviews' not in data:
            break
        
        reviews = data['reviews']
        
        if not reviews:
            break
        
        for review in reviews:
            review_data = {
                'author': review['author']['steamid'],
                'recommendationid': review['recommendationid'],
                'review': review['review'],
                'timestamp_created': review['timestamp_created'],
                'timestamp_updated': review['timestamp_updated'],
                'voted_up': review['voted_up'],
                'votes_up': review['votes_up'],
                'votes_funny': review['votes_funny'],
                'weighted_vote_score': review['weighted_vote_score'],
                'comment_count': review['comment_count'],
                'steam_purchase': review['steam_purchase'],
                'received_for_free': review['received_for_free'],
                'written_during_early_access': review['written_during_early_access'],
            }
            all_reviews.append(review_data)
        
        start_offset += len(reviews)
        time.sleep(sleep_time)
        
        # Break the loop if no more reviews
        if len(reviews) < params['num_per_page']:
            break

    df_reviews = pd.DataFrame(all_reviews)
    return df_reviews

def save_to_excel(df, file_name):
    """
    Saves DataFrame to an Excel file.
    
    :param df: DataFrame containing reviews.
    :param file_name: Name of the Excel file to save.
    """
    df.to_excel(file_name, index=False)
    print(f"Reviews saved to {file_name}")

def main():
    # Replace this with the Steam App ID for the game you want to get reviews for
    app_id = '1123450'  # Example: Dota 2 App ID
    num_reviews = 1000  # Adjust the number of reviews to fetch

    print("Fetching reviews...")
    df_reviews = get_steam_reviews(app_id, num_reviews)
    
    # Save reviews to Excel
    file_name = f"steam_reviews_{app_id}.xlsx"
    save_to_excel(df_reviews, file_name)

if __name__ == '__main__':
    main()
