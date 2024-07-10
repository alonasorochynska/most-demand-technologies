import scrapy


class WorkuaJobsSpider(scrapy.Spider):
    name = "workua_jobs"
    allowed_domains = ["work.ua"]
    start_urls = ["https://www.work.ua/en/jobs-python+developer/"]

    def parse(self, response):
        jobs = response.css("div.job-link")

        for job in jobs:
            title = job.css("h2 > a::text").get(default="").strip()
            link = response.urljoin(job.css("h2 > a::attr(href)").get())

            yield response.follow(
                link, self.parse_job_details, meta={"title": title, "link": link}
            )

        next_page = response.css(
            'a.ga-pagination-default[href*="?page="]::attr(href)'
        ).get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_job_details(self, response):
        title = response.meta["title"]
        link = response.meta["link"]
        skills = response.css("span.ellipsis::text").getall()
        job_description = response.xpath(
            '//div[@id="job-description"]//text()'
        ).getall()
        job_description = " ".join(job_description).replace("\r\n", "").strip()
        salary = (
            response.css('span[title="Salary"] + span.strong-500::text')
            .get(default="")
            .replace("\u2009", "")
            .replace("\u202f", "")
            .strip()
        )
        company = (
            response.css('span[title="Company Information"] + a span.strong-500::text')
            .get(default="")
            .strip()
        )

        yield {
            "title": title,
            "link": link,
            "skills": skills,
            "salary": salary,
            "company": company,
            "job_description": job_description,
        }
