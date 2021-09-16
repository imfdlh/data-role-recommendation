import scrapy
from data_engineer.items import DataEngineerItem


class ReviewspiderSpider(scrapy.Spider):
    
    name = 'reviewspiderMultiple'
    start_urls = ['https://id.indeed.com/lowongan-kerja?q=%2F+title%3A(data+engineer)&l=Indonesia&limit=50&lang=en']

    for i in range(50, 101, 50):
        start_urls.append('https://id.indeed.com/lowongan-kerja?q=%2F+title%3A(data+engineer)&l=Indonesia&limit=50&lang=en&start=' + str(i))
    
    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "resultWithShelf")]/@href'):
            url = 'https://id.indeed.com' + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = DataEngineerItem()
        
        item['job_title'] = response.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader-title")]/text()').extract()[0]
        item['company'] = response.xpath('//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]/descendant-or-self::*/text()').extract()[0]
        item['location'] = response.xpath('//div[@class="jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating"]/following-sibling::div[1]/text()').extract()[0]
        item['job_description'] = response.xpath('//div[@id="jobDescriptionText"]/descendant-or-self::*/text()').extract()[0:]
        item['available_since'] = response.xpath('//div[contains(@class, "jobsearch-JobMetadataFooter")]/div[text()[contains(., "ago")]]/text()').extract()[0]

        yield item