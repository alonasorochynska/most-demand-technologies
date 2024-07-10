import scrapy


class WorkUaJobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["work.ua"]
    start_urls = ["https://www.work.ua/en/jobs-python+developer/"]

    def parse(self, response):
        jobs = response.xpath("//div[@class='mb-lg mt-lg sm:mt-xl']")

        for job in jobs:
            link = response.urljoin(job.xpath(".//h2/a/@href").get())

            yield response.follow(link, self.parse_job_details, meta={"link": link})

        next_page = response.xpath(
            "//a[contains(@class, 'ga-pagination-default') and contains(@href, '?page=')]/@href"
        ).get()

        if next_page:

            yield response.follow(next_page, self.parse)

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
