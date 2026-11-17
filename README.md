# GMaps Leads

Collects business listings from Google Local Services for a business type and area, and turns them into a lead list a sales team can work from.

This is the scraper behind the GMaps Leads case study on [falcontreras.com](https://falcontreras.com).

## What it collects

Each listing becomes a typed `Card` record (Pydantic) with:

- company name, address and service area
- rating and review count
- phone number and website
- years in business and listed services

## How it works

- `main.py` opens the Local Services results for a search with SeleniumBase and pages through them 20 at a time.
- It opens each listing, waits for the details panel and reads the fields. If a listing does not load, it retries up to three times before moving on.
- Results can be exported to CSV, Excel, JSON, HTML or a SQL table.
- `app.py` is a Streamlit dashboard. Enter a business type and an area, run the search, check the results (counts with phone and website, average rating), then download CSV, Excel or JSON.

## Run it

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/). A Chrome browser window opens while a search runs.

```bash
uv sync
uv run streamlit run app.py     # dashboard
uv run python main.py           # command-line example: writes Toronto.csv
```

## Notes

- The scraper reads the page's markup, so it needs updating when Google changes the Local Services layout.
- Collect and use the data in line with Google's terms and the privacy rules that apply to you.
