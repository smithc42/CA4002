# Scrapy settings for eidw project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'eidw'

SPIDER_MODULES = ['eidw.spiders']
NEWSPIDER_MODULE = 'eidw.spiders'
ITEM_PIPELINES = ['eidw.pipelines.DatabasePipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'eidw (+http://www.yourdomain.com)'
