# scraper.py
import requests
from typing import List

# Replace with your own Google Maps API key
GOOGLE_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
PLACES_ENDPOINT = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def scrape_businesses_without_websites(category: str = "all", location: str = "South Africa") -> List[dict]:
    query = f"{category} businesses in {location}" if category != "all" else f"businesses in {location}"
    
    params = {
        "query": query,
        "key": GOOGLE_API_KEY,
    }

    results = []
    response = requests.get(PLACES_ENDPOINT, params=params)
    data = response.json()

    if data.get("status") != "OK":
        return {"error": "Failed to fetch data", "details": data.get("error_message")}

    for place in data.get("results", []):
        website = place.get("website")
        name = place.get("name")
        photos = place.get("photos", [])
        address = place.get("formatted_address", "")
        business_status = place.get("business_status", "UNKNOWN")

        if not website:
            result = {
                "name": name,
                "address": address,
                "photo_ref": photos[0]["photo_reference"] if photos else None,
                "status": business_status,
                "place_id": place.get("place_id"),
                "location": place.get("geometry", {}).get("location", {}),
                "has_website": False
            }
            results.append(result)

    return {"count": len(results), "businesses": results}
