# ══════════════════════════════════════════════════════════════
#  WEEK 3  |  DAY 4  |  API REQUESTS
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand REST API concepts and make a GET request using the requests library
#  2. Read the response: status code, JSON body, and handle HTTP errors
#  3. Pass query parameters and headers to customize API requests
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python requests library GET API tutorial"
#  Search: "Python REST API requests params headers"
# ══════════════════════════════════════════════════════════════

# Install requests if needed:  pip install requests

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS A REST API, THE requests LIBRARY, GET REQUEST
# ══════════════════════════════════════════════════════════════
# A REST API is a web service that responds to HTTP requests with data,
# usually in JSON format.
#
# REQUEST METHOD | PURPOSE
#   GET          | Retrieve data (read-only, most common for data work)
#   POST         | Send new data to create a resource
#   PUT          | Update an existing resource
#   DELETE       | Delete a resource
#
# The requests library makes HTTP easy:
#   import requests
#   response = requests.get("https://api.example.com/endpoint")
#
# PUBLIC FREE APIs used in this lesson:
#   https://jsonplaceholder.typicode.com  -- fake REST API for testing
#   https://api.coindesk.com/v1/bpi/currentprice.json -- Bitcoin price index

# EXAMPLE ──────────────────────────────────────────────────────
try:
    import requests

    # --- Basic GET request ---
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)

    print("Status code:", response.status_code)       # 200 means OK
    print("Content type:", response.headers.get("Content-Type"))

    # Parse the JSON body into a Python dict
    post = response.json()
    print("Post ID:", post["id"])                     # 1
    print("Title:", post["title"])
    print("Body preview:", post["body"][:60])

    # --- Fetching a list ---
    url_list = "https://jsonplaceholder.typicode.com/posts"
    response_list = requests.get(url_list)
    posts = response_list.json()
    print(f"\nTotal posts returned: {len(posts)}")    # 100
    print("First post title:", posts[0]["title"])

    # --- Bitcoin price API (real financial data) ---
    btc_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    btc_response = requests.get(btc_url, timeout=5)
    if btc_response.status_code == 200:
        btc_data = btc_response.json()
        usd_rate = btc_data["bpi"]["USD"]["rate"]
        print(f"\nBitcoin price (USD): {usd_rate}")

except ImportError:
    print("requests not installed. Run: pip install requests")
    print("The examples below will show the patterns without running live.")
except Exception as e:
    print(f"Network request failed: {e}")
    print("Check your internet connection or the API endpoint.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Using the JSONPlaceholder API, fetch the list of users:
#   URL: https://jsonplaceholder.typicode.com/users
#
# For each user, print:
#   "<name> | <email> | <company name>"
# where company name comes from user["company"]["name"]
#
# Then print the total count of users.
#
# Expected output (first 3 of 10):
#   Leanne Graham | Sincere@april.biz | Romaguera-Crona
#   Ervin Howell | Shanna@melissa.tv | Deckow-Crist
#   Clementine Bauch | Nathan@yesenia.net | Romaguera-Jacobson
#   ...
#   Total users: 10




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — READING THE RESPONSE: status_code, .json(), ERROR HANDLING
# ══════════════════════════════════════════════════════════════
# Every HTTP response has a status code:
#   2xx  Success  (200 OK, 201 Created, 204 No Content)
#   4xx  Client error  (400 Bad Request, 401 Unauthorized, 404 Not Found)
#   5xx  Server error  (500 Internal Server Error, 503 Unavailable)
#
# response.raise_for_status() is the easiest way to check for errors —
# it raises an HTTPError if the status code is 4xx or 5xx.
#
# Always set a timeout to avoid your script hanging indefinitely.
# requests.get(url, timeout=10) will raise Timeout if the server is slow.

# EXAMPLE ──────────────────────────────────────────────────────
def safe_get(url, timeout=10):
    """
    Perform a GET request with error handling.
    Returns (dict/list, None) on success or (None, error_message) on failure.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()    # raises HTTPError for 4xx/5xx
        return response.json(), None
    except requests.exceptions.Timeout:
        return None, f"Request timed out after {timeout}s: {url}"
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP error {e.response.status_code}: {url}"
    except requests.exceptions.ConnectionError:
        return None, f"Could not connect: {url}"
    except requests.exceptions.JSONDecodeError:
        return None, "Response was not valid JSON"

try:
    # Good request
    data, error = safe_get("https://jsonplaceholder.typicode.com/posts/5")
    if error:
        print("Error:", error)
    else:
        print("Post 5 title:", data["title"])

    # Bad request — post 99999 does not exist (will get 404)
    data, error = safe_get("https://jsonplaceholder.typicode.com/posts/99999")
    if error:
        print("Error:", error)       # HTTP error 404
    else:
        print("Got data:", data)

    # Inspect the raw response before parsing
    resp = requests.get("https://jsonplaceholder.typicode.com/todos/1", timeout=5)
    print("\nRaw response text:", resp.text)
    print("Status:", resp.status_code)
    print("Headers keys:", list(resp.headers.keys())[:4])

except Exception as e:
    print(f"Skipping live example: {e}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Write a function called fetch_all_posts_by_user(user_id) that:
#   1. Calls safe_get with:
#      https://jsonplaceholder.typicode.com/posts?userId=<user_id>
#   2. If there is an error, prints the error message and returns []
#   3. If successful, prints "Found <n> posts for user <user_id>"
#      and returns the list of post dicts
#
# Call it twice:
#   fetch_all_posts_by_user(3)   -- should find 10 posts
#   fetch_all_posts_by_user(999) -- user 999 does not exist (returns empty list)
#
# Then print the titles of the first 3 posts returned for user 3.
#
# Expected output:
#   Found 10 posts for user 3
#   Found 0 posts for user 999
#   Post titles for user 3:
#     1. omnis laborum odio
#     2. unde repellendus nobis
#     3. doloribus ad provident suscipit at




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — PASSING PARAMETERS AND HEADERS TO A REQUEST
# ══════════════════════════════════════════════════════════════
# Most APIs accept query parameters to filter or paginate results.
#
# params={}   -- adds query string parameters to the URL
#               requests builds the URL automatically:
#               ?userId=1&_limit=5
#
# headers={}  -- adds HTTP headers such as authentication tokens,
#               content type, or API keys
#
# Common headers:
#   "Authorization": "Bearer YOUR_TOKEN_HERE"
#   "Accept": "application/json"
#   "X-API-Key": "YOUR_KEY"

# EXAMPLE ──────────────────────────────────────────────────────
try:
    # --- Using params to filter results ---
    url = "https://jsonplaceholder.typicode.com/posts"

    params = {
        "userId": 2,      # only posts from user 2
        "_limit": 3,      # only first 3 results (JSONPlaceholder extension)
    }

    response = requests.get(url, params=params, timeout=10)
    print("\nURL with params:", response.url)
    # https://jsonplaceholder.typicode.com/posts?userId=2&_limit=3

    posts = response.json()
    print(f"Posts returned: {len(posts)}")
    for p in posts:
        print(f"  [{p['id']}] {p['title'][:50]}")

    # --- Using headers to pass authentication ---
    # This example shows the PATTERN for authenticated APIs.
    # The Authorization header is shown but the token is fake.
    # Real tokens come from your API provider.
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer YOUR_TOKEN_HERE",   # replace with real token
        "X-Request-Source": "python-etl-pipeline",
    }

    # JSONPlaceholder ignores headers but accepts them without error
    response_auth = requests.get(
        "https://jsonplaceholder.typicode.com/users/1",
        headers=headers,
        timeout=10,
    )
    print("\nAuthenticated request status:", response_auth.status_code)
    user = response_auth.json()
    print("User:", user["name"], "|", user["email"])

    # --- Building a reusable API client ---
    def make_api_client(base_url, api_key=None):
        """Return a configured session with base headers."""
        session = requests.Session()
        session.headers.update({"Accept": "application/json"})
        if api_key:
            session.headers.update({"X-API-Key": api_key})
        session.base_url = base_url
        return session

    client = make_api_client("https://jsonplaceholder.typicode.com")
    r = client.get("https://jsonplaceholder.typicode.com/todos/1", timeout=5)
    print("\nTodo via session:", r.json()["title"])

except Exception as e:
    print(f"Skipping live example: {e}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# The JSONPlaceholder API has 100 posts total.
# Write a function called collect_posts(user_ids) that:
#   1. Accepts a list of user_ids (integers)
#   2. For each user_id, fetches posts using params={"userId": user_id}
#   3. Collects all posts into one flat list
#   4. Returns the combined list
#
# Call it with user_ids=[1, 2, 3] and print:
#   - Total posts collected
#   - The unique user IDs present in the results (use a set)
#
# Expected output:
#   Total posts collected: 30
#   User IDs in results: {1, 2, 3}


