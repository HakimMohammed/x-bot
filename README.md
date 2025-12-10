# X (Twitter) Top Posts API

A FastAPI application that searches for the most liked posts on X (Twitter) containing a search term using [twikit](https://github.com/d60/twikit).

## Features

-   Search for posts containing any search term
-   Returns the top 10 most liked posts
-   Saves all search results to a JSON file
-   Exposes a REST API endpoint that returns the most liked post URL
-   Uses twikit library for Twitter scraping (no official API key required)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Twitter Credentials

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Twitter account credentials:

```
TWITTER_USERNAME=your_username
TWITTER_EMAIL=your_email@example.com
TWITTER_PASSWORD=your_password
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

This application uses [twikit](https://github.com/d60/twikit) to interact with Twitter. Some notes:

-   Requires a Twitter account (username, email, password)
-   Cookies are saved to `cookies.json` after first login to avoid repeated logins
-   Be mindful of Twitter's rate limits
-   For account safety, consider using a secondary account
