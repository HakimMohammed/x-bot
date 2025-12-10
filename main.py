from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from twitter_client import search_top_liked_posts, save_search_results

app = FastAPI(
    title="X (Twitter) Top Posts API",
    description="Search for the most liked posts containing a search term on X (Twitter)",
    version="1.0.0"
)


class SearchResponse(BaseModel):
    search_term: str
    most_liked_post_url: str
    like_count: int
    saved_file: str


class ErrorResponse(BaseModel):
    detail: str


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "X (Twitter) Top Posts API",
        "endpoints": {
            "/search": "Search for the most liked post containing a term",
            "/docs": "API documentation"
        }
    }


@app.get(
    "/search",
    response_model=SearchResponse,
    responses={
        404: {"model": ErrorResponse, "description": "No posts found"},
        500: {"model": ErrorResponse, "description": "Twitter API error"}
    }
)
async def search(
    q: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="The search term to find posts for"
    )
):
    """
    Search for posts containing the search term and return the most liked post.
    
    - **q**: The search term to look for in posts
    
    Returns the URL to the most liked post found. All top 10 posts are saved to a JSON file.
    """
    try:
        # Search for top liked posts
        tweets = await search_top_liked_posts(q, max_results=10)
        
        if not tweets:
            raise HTTPException(
                status_code=404,
                detail=f"No posts found for search term: '{q}'"
            )
        
        # Save all results to JSON file
        saved_file = save_search_results(q, tweets)
        
        # Get the most liked post (first in sorted list)
        most_liked = tweets[0]
        
        return SearchResponse(
            search_term=q,
            most_liked_post_url=most_liked["url"],
            like_count=most_liked["like_count"],
            saved_file=saved_file
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching Twitter: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
