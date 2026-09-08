import asyncio
import json
import sys
import urllib.error
import urllib.request

WEB = sys.platform == "emscripten"

if WEB:
    import platform

# wrangler dev uses 8787, astro uses 4321
BASE_URL = f'http://localhost:{8000}'

# Sends a score to the database
def post_score(game, username, score):
    body = json.dumps({"username": username, "score": score})
    url = f"{BASE_URL}/api/scores/{game}"
    try:
        if WEB:
            platform.window.fetch(
                url,
                platform.window.eval(f"""({{
                    method: "POST",
                    headers: {{"Content-Type": "application/json"}},
                    body: {json.dumps(body)}
                }})"""),
            )
        else:
            req = urllib.request.Request(
                url,
                data=body.encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req)
    except Exception as e:
        print(f"{game}: Failed to post score: {e}")

def _fetch_sync(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read())

# Fetch the top 5 high scores
async def fetch_scores(game):
    url = f"{BASE_URL}/api/scores/{game}"
    try:
        if WEB:
<<<<<<< HEAD:pygame-utils/scores_api.py
            resp = await platform.window.fetch(url)
            data = await resp.json()
            data = data.to_py()
=======
            async with platform.fopen(url, "r") as f:
                data = json.loads(f.read())
>>>>>>> 75ac5a881190bf443997ddeef3fa26cb21576d3c:pygame-utils/scores-api.py
        else:
            data = await asyncio.to_thread(_fetch_sync, url)
    except Exception as e:
        print(f"{game}: Failed to fetch high scores: {e}")
        return []
<<<<<<< HEAD:pygame-utils/scores_api.py
    return data
=======
    return data
>>>>>>> 75ac5a881190bf443997ddeef3fa26cb21576d3c:pygame-utils/scores-api.py
