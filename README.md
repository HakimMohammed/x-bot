# X (Twitter) Top Posts API

A FastAPI application that searches for the most liked posts on X (Twitter) containing a search term.

## Features

-   Search for posts containing any search term
-   Returns the top 10 most liked posts
-   Saves all search results to a JSON file
-   Exposes a REST API endpoint that returns the most liked post URL

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Twitter API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a project and app if you haven't already
3. Get your API Key and API Secret from the "Keys and tokens" section
4. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

5. Edit `.env` and add your API credentials:

```
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
```

### 3. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /search

Search for the most liked post containing a term.

**Query Parameters:**

-   `q` (required): The search term

**Example Request:**

```bash
curl "http://localhost:8000/search?q=python"
```

**Example Response:**

```json
{
    "search_term": "python",
    "most_liked_post_url": "https://twitter.com/username/status/1234567890",
    "like_count": 1500,
    "saved_file": "searches/python_20241210_120000.json"
}
```

### GET /docs

Interactive API documentation (Swagger UI)

### GET /redoc

Alternative API documentation (ReDoc)

## Saved Search Results

Each search saves the top 10 results to a JSON file in the `searches/` directory with the following structure:

```json
{
    "search_term": "python",
    "search_timestamp": "2024-12-10T12:00:00.000000",
    "total_results": 10,
    "tweets": [
        {
            "id": "1234567890",
            "text": "Tweet content...",
            "author_id": "987654321",
            "author_username": "username",
            "author_name": "Display Name",
            "created_at": "2024-12-10T10:00:00+00:00",
            "like_count": 1500,
            "retweet_count": 200,
            "reply_count": 50,
            "quote_count": 10,
            "url": "https://twitter.com/username/status/1234567890"
        }
    ]
}
```

## Note

The Twitter API v2 has rate limits. The free tier allows:

-   10 requests per 15 minutes for tweet search
-   Maximum 100 tweets per request

For higher limits, consider upgrading to a paid tier.
