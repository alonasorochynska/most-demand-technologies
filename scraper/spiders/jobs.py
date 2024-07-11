import scrapy


class WorkUaJobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["work.ua"]
    start_urls = ["https://www.work.ua/en/jobs-python/"]
    total_pages = 0

    def parse(self, response):
        job_blocks = response.xpath("//div[contains(@class, 'job-link')]")

        for job_block in job_blocks:
            link = job_block.xpath(".//h2/a/@href").get()
            if link:
                link = response.urljoin(link)
                yield response.follow(link, self.parse_job_details, meta={"link": link})

        if not self.total_pages:
            page_info = response.xpath("//span[@class='text-default']/@title").get()
            if page_info:
                self.total_pages = int(page_info.split("of ")[-1].strip())
                self.logger.info(f"Total pages: {self.total_pages}")

                for page_number in range(2, self.total_pages + 1):
                    next_page_url = response.urljoin(f"?page={page_number}")
                    yield response.follow(next_page_url, self.parse)

    def parse_job_details(self, response):
        link = response.meta["link"]
        title = response.xpath("//h1/text()").get(default="").strip()
        skills = response.xpath("//span[@class='ellipsis']/text()").getall()
        job_description = response.xpath("//div[@id='job-description']//text()").getall()
        job_description = " ".join(job_description).replace("\r\n", "").strip()
        salary = response.xpath(
            "//span[@title='Salary']/following-sibling::span[@class='strong-500']/text()"
        ).get(default="").replace("\u2009", "").replace("\u202f", "").strip()
        company = response.xpath(
            "//span[@title='Company Information']/following-sibling::a/span[@class='strong-500']/text()"
        ).get(default="").strip()

        yield {
            "title": title,
            "skills": skills,
            "salary": salary,
            "company": company,
            "job_description": job_description,
            "link": link,
        }
