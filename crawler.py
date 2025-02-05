import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_venues_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_venues():
    """
    Main function to crawl venue data from the website.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "venue_crawl_session"

    # Initialize state variables
    page_number = 1
    all_venues = []
    seen_names = set()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # Fetch and process data from the current page
            venues, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                print("No more venues found. Ending crawl.")
                break  # Stop crawling when "No Results Found" message appears

            if not venues:
                print(f"No venues extracted from page {page_number}.")
                break  # Stop if no venues are extracted

            # Add the venues from this page to the total list
            all_venues.extend(venues)
            page_number += 1  # Move to the next page

            # Pause between requests to be polite and avoid rate limits
            await asyncio.sleep(2)  # Adjust sleep time as needed

    # Save the collected venues to a CSV file
    if all_venues:
        save_venues_to_csv(all_venues, "complete_venues.csv")
        print(f"Saved {len(all_venues)} venues to 'complete_venues.csv'.")
    else:
        print("No venues were found during the crawl.")

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


async def main():
    """
    Entry point of the script.
    """
    await crawl_venues()


if __name__ == "__main__":
    asyncio.run(main())
