import os
import json
import sys
from datetime import datetime
from types import ModuleType
from dotenv import load_dotenv

# Patch js2py import issue with Python 3.13+
# Create mock modules to prevent the js2py import error
mock_js2py = ModuleType('js2py')
mock_js2py.eval_js = lambda code: ""
mock_js2py.EvalJs = lambda: None
sys.modules['js2py'] = mock_js2py

# Also mock the submodules that might be imported
for submod in ['js2py.base', 'js2py.utils', 'js2py.utils.injector']:
    sys.modules[submod] = ModuleType(submod)

from twikit import Client

load_dotenv()

# Twitter credentials from environment
USERNAME = os.getenv("TWITTER_USERNAME")
EMAIL = os.getenv("TWITTER_EMAIL")
PASSWORD = os.getenv("TWITTER_PASSWORD")

COOKIES_FILE = "cookies.json"

# Global client instance
_client: Client | None = None


async def get_client() -> Client:
    """Get or create an authenticated Twitter client."""
    global _client
    
    if _client is not None:
        return _client
    
    _client = Client('en-US')
    
    # Try to load existing cookies first
    if os.path.exists(COOKIES_FILE):
        _client.load_cookies(COOKIES_FILE)
    else:
        # Login with credentials
        if not USERNAME or not PASSWORD:
            raise ValueError(
                "Twitter credentials not set. Please set TWITTER_USERNAME, "
                "TWITTER_EMAIL, and TWITTER_PASSWORD environment variables."
            )
        # Disable ui_metrics to avoid js2py compatibility issues with Python 3.13
        await _client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD,
            enable_ui_metrics=False
        )
        _client.save_cookies(COOKIES_FILE)
    
    return _client


async def search_top_liked_posts(search_term: str, max_results: int = 10) -> list[dict]:
    """
    Search for posts containing the search term and return top liked posts.
    
    Args:
        search_term: The term to search for in tweets
        max_results: Maximum number of results to return (default 10)
    
    Returns:
        List of tweet dictionaries sorted by like count
    """
    client = await get_client()
    
    # Search for tweets - fetch more to sort by likes
    tweets_result = await client.search_tweet(search_term, 'Top', count=20)
    
    tweets = []
    for tweet in tweets_result:
        tweet_data = {
            "id": tweet.id,
            "text": tweet.text,
            "author_username": tweet.user.screen_name if tweet.user else "unknown",
            "author_name": tweet.user.name if tweet.user else "Unknown",
            "created_at": tweet.created_at if tweet.created_at else None,
            "like_count": tweet.favorite_count or 0,
            "retweet_count": tweet.retweet_count or 0,
            "reply_count": tweet.reply_count or 0,
            "quote_count": tweet.quote_count or 0,
            "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}" if tweet.user else f"https://twitter.com/i/status/{tweet.id}"
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
