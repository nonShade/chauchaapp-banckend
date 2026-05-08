import feedparser
import httpx


async def fetch_feed(client, url: str):
    resp = await client.get(url, timeout=10)
    resp.raise_for_status()
    return feedparser.parse(resp.text)
