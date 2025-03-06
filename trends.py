import requests
from bs4 import BeautifulSoup
import random
import time

# List of User-Agents to reduce bot detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
]

def scrape_amazon_trending(category_slug, domain="amazon.com.be"):
    """Scrapes the top 3 trending products from a user-specified Amazon Belgium category."""
    
    bestsellers_url = f"https://www.{domain}/gp/bestsellers/{category_slug}/"
    
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        response = requests.get(bestsellers_url, headers=headers, allow_redirects=True, timeout=10)
        response.raise_for_status()  # Raise error if response is not 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return []
    
    if "Robot Check" in response.text or response.status_code != 200:
        print("🚨 Amazon has blocked the request. Try using proxies or the API.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Updated selector for bestseller items
    items = soup.select(".p13n-sc-uncoverable-faceout, .zg-item, .a-section.a-spacing-none.p13n-asin")
    print(f"✅ Found {len(items)} trending products in {category_slug}.")

    products = []
    for item in items[:3]:  # Get the top 3 products
        rank_element = item.select_one(".zg-badge-text")
        
        # 🔥 Updated title selector to extract book titles correctly
        title_element = item.select_one("a.a-link-normal span")

        if title_element:
            title = title_element.get_text(strip=True)
        else:
            title = "❌ Unknown Title"
            print(f"❓ Debug: Could not find title for one item.\n{item.prettify()}\n")

        rank = int(rank_element.text.strip("#")) if rank_element else len(products) + 1

        products.append({"rank": rank, "title": title})

        # Add a short delay to avoid being blocked
        time.sleep(random.uniform(1, 3))

    return products

if __name__ == "__main__":
    domain = "amazon.com.be"

    # Step 1: Ask User to Enter Category
    category_slug = input("🔹 Enter product category (e.g., electronics, books, fashion): ").strip().lower().replace(" ", "-")

    print(f"\n🔍 Fetching top 3 trending products in **{category_slug}**...\n")

    # Step 2: Scrape the Trending Products
    trending_products = scrape_amazon_trending(category_slug, domain)

    # Step 3: Display Results
    if not trending_products:
        print("⚠️ No products found—check the category or try again later.")
    else:
        for product in trending_products:
            print(f"🏆 Rank #{product['rank']}: {product['title']}")
