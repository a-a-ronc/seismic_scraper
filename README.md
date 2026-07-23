# seismic_scraper

Extracts pertinent data from **seismic calculation packages** sent by seismic engineering companies, turning PDF submittals into structured data for compliance workflows and quote preparation.

Seismic calc packages arrive as dense PDFs; the numbers that matter (anchorage, base plates, forces, applicable code sections) are buried across pages. This scraper pulls them into structured output so nobody reads 40 pages to find 6 values.

## How it works

1. **Input** — seismic calculation PDFs from engineering partners
2. **Parsing** — locates and extracts the relevant calculation values
3. **Output** — structured data feeding downstream compliance and quoting tools (see [BOM-Scraper](https://github.com/a-a-ronc/BOM-Scraper))

## Stack

Python · PDF/document extraction

## Usage

Run instructions coming — reach out if you want a walkthrough.
