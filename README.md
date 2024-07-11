## Most Demand Technologies Analysis

This repository contains a Python scraper for extracting job offers from [work.ua](https://www.work.ua/) related to "Python" positions.

<hr>

### Data Scraping

The scraper is implemented using Scrapy and is located in `scraper/spiders/jobs.py`.

### Analytics and Cleaning

After scraping the data, you can perform analytics and cleaning using the Jupyter notebook located at
`analytics/main.ipynb`. The notebook uses Pandas, Matplotlib, and Seaborn for data analysis and visualization.

* The notebook reads the scraped CSV data and translates it to English using `deep_translator.GoogleTranslator` and
  `asyncio`.

* Skills and job positions are normalized to create plots for top skills, top positions, and a heatmap correlating them.

### Usage

1. Clone the repository:

```shell
git clone https://github.com/alonasorochynska/most-demand-technologies.git
```

2. Create and activate virtual environment:

```shell
# for Windows
python -m venv venv
venv\Scripts\activate
# for macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```shell
pip install -r requirements.txt
```

4. Run the scraper script:

```shell
scrapy crawl jobs -o data/scraped-jobs.csv
```

5. Open and run the `main.ipynb` Jupyter notebook file to perform analytics and generate visualizations.

### Example Data

You can find an example of the scraped CSV file and logs in the `data` folder.

<hr>

Feel free to adjust the README.md as per your specific project details or additional information you'd like to include.
This template provides a basic structure to document the functionality and usage of your repository for others to
understand and use effectively.
