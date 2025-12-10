import os
import json
import tweepy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


def get_twitter_client() -> tweepy.Client:
    """Create and return a Twitter API v2 client."""
    if not BEARER_TOKEN:
        raise ValueError("TWITTER_BEARER_TOKEN environment variable is not set")
    return tweepy.Client(bearer_token=BEARER_TOKEN)


def search_top_liked_posts(search_term: str, max_results: int = 10) -> list[dict]:
    """
    Search for posts containing the search term and return top liked posts.
    
    Args:
        search_term: The term to search for in tweets
        max_results: Maximum number of results to return (default 10)
    
    Returns:
        List of tweet dictionaries sorted by like count
    """
    client = get_twitter_client()
    
    # Search for recent tweets containing the search term
    # We fetch more than needed to sort by likes and get top 10
    response = client.search_recent_tweets(
        query=f"{search_term} -is:retweet lang:en",
        max_results=100,  # Fetch more to find most liked
        tweet_fields=["public_metrics", "created_at", "author_id"],
        expansions=["author_id"],
        user_fields=["username", "name"]
    )
    
    if not response.data:
        return []
    
    # Create a mapping of author_id to user info
    users = {}
    if response.includes and "users" in response.includes:
        for user in response.includes["users"]:
            users[user.id] = {
                "username": user.username,
                "name": user.name
            }
    
    # Process tweets and extract relevant info
    tweets = []
    for tweet in response.data:
        metrics = tweet.public_metrics
        author_info = users.get(tweet.author_id, {"username": "unknown", "name": "Unknown"})
        
        tweet_data = {
            "id": str(tweet.id),
            "text": tweet.text,
            "author_id": str(tweet.author_id),
            "author_username": author_info["username"],
            "author_name": author_info["name"],
            "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
            "like_count": metrics["like_count"],
            "retweet_count": metrics["retweet_count"],
            "reply_count": metrics["reply_count"],
            "quote_count": metrics["quote_count"],
            "url": f"https://twitter.com/{author_info['username']}/status/{tweet.id}"
        }
        tweets.append(tweet_data)
    
    # Sort by like count (descending) and take top results
    tweets.sort(key=lambda x: x["like_count"], reverse=True)
    top_tweets = tweets[:max_results]
    
    return top_tweets


def save_search_results(search_term: str, tweets: list[dict]) -> str:
    """
    Save search results to a JSON file.
    
    Args:
        search_term: The search term used
        tweets: List of tweet data to save
    
    Returns:
        Path to the saved file
    """
    # Create searches directory if it doesn't exist
    os.makedirs("searches", exist_ok=True)
    
    # Create a safe filename from the search term
    safe_term = "".join(c if c.isalnum() else "_" for c in search_term)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"searches/{safe_term}_{timestamp}.json"
    
    # Prepare data to save
    data = {
        "search_term": search_term,
        "search_timestamp": datetime.now().isoformat(),
        "total_results": len(tweets),
        "tweets": tweets
    }
    
    # Save to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filename
