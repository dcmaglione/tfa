import scrapy
from scrapy.crawler import CrawlerProcess


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia-spider"
    custom_settings = {
        'BOT_NAME': 'wikipediabot',
        # Temporarily set to suppress warning
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    }

    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']

    def parse(self, response):
        TFA_SELECTOR = response.css('#mp-tfa p')

        # Get title, link, text from the selector
        TITLE_SELECTOR = TFA_SELECTOR.css('b a::attr(title)').extract_first()
        URL_SELECTOR = TFA_SELECTOR.css('b a::attr(href)').extract_first()
        TEXT_SELECTOR = TFA_SELECTOR.css('::text').extract()

        # Clean up the link and text
        URL_CLEAN = 'https://en.wikipedia.org' + URL_SELECTOR
        # Join the text, replace newline, replace unicode, remove (Full article...)
        TEXT_CLEAN = ''.join(TEXT_SELECTOR).replace(
            '\n', '').replace(u'\xa0', u' ').split(
            ' (Full article')[0]

        yield {
            'title': TITLE_SELECTOR,
            'url': URL_CLEAN,
            'text': TEXT_CLEAN,
        }


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WikipediaSpider)
    process.start()
