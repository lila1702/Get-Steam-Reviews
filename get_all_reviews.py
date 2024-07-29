import requests
import pandas as pd
import time

def get_reviews(game_id, params={"json":1}):
    url = "https://store.steampowered.com/appreviews/"
    response = requests.get(url=url+game_id, params=params)
    headers = {"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"}
    return response.json()

def get_steam_reviews(game_id, n=30000):
    reviews = []
    cursor = "*"
    params = {
        "json" : 1,
        "filter" : "all",
        "language" : "english",
        "day_range" : 9223372036854775807,
        "review_type" : "all",
        "purchase_type" : all,
    }
    
    while (n > 0):
        params["cursor"] = cursor.encode()
        params["num_per_page"] = min(100, n)
        n -= 100
        
        response = get_reviews(game_id, params)
        cursor = response["cursor"]
        reviews += response["reviews"]
        
        if (len(response["reviews"]) < 100): break
        
    return reviews

def save_to_excel(list_reviews, file_name):
    reviews_df = pd.DataFrame(list_reviews)
    reviews_df.to_excel(file_name, index=False)
    print(f"Reviews saved to {file_name}")

if (__name__ == "__main__"):
    games = {
        "chicory" : "1123450",
        "tlou pt 1" : "1888930"
    }
    for x in games:
        game_id = games[x]
        # game_id = "1123450"
    
        print("Fetching reviews...")
        
        reviews = get_steam_reviews(game_id)
        
        file_name = f"steam_reviews_{game_id}.xlsx"
        save_to_excel(reviews, file_name)