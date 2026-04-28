import logging
import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://restcountries.com/v3.1/name/{country}"


def get_country_info(country: str) -> str:
    try:
        url = BASE_URL.format(country=country)
        response = httpx.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()[0]

        name = data["name"]["common"]
        capital = data.get("capital", ["N/A"])[0]
        population = data.get("population", "N/A")
        area = data.get("area", "N/A")
        region = data.get("region", "N/A")
        currencies = ", ".join(v["name"] for v in data.get("currencies", {}).values())
        languages = ", ".join(data.get("languages", {}).values())

        return (
            f"Country: {name}\n"
            f"Capital: {capital}\n"
            f"Population: {population:,}\n"
            f"Area: {area:,.0f} km²\n"
            f"Region: {region}\n"
            f"Currency: {currencies}\n"
            f"Language(s): {languages}"
        )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.warning(f"Country not found: '{country}'")
            return f"No information found for '{country}'."
        logger.error(f"HTTP error fetching '{country}': {e.response.status_code}")
        return "The countries API returned an error. Please try again."

    except httpx.TimeoutException:
        logger.error(f"Timeout while fetching country '{country}'")
        return "The request timed out. Please try again."

    except httpx.RequestError as e:
        logger.error(f"Connection error while fetching '{country}': {e}")
        return "Could not connect to the countries API."