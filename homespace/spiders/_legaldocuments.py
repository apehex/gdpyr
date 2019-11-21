# -*- coding: utf-8 -*-

"""
===============
Legal Documents
===============

Scrape and version the explicit commitments of companies.

Especially the commitments regarding personal privacy, put into
light by the European GDPR.
"""

from __future__ import division, print_function, absolute_import

import scrapy

from typical import checks

from homespace.items._legaldocument import LegalDocument, LegalDocumentLoader

#####################################################################
# SPIDER
#####################################################################

class LegalDocumentsSpider(scrapy.Spider):
    name = 'legal_documents'

    #################################################################
    # CRAWLING METHODS
    #################################################################

    def __init__(
            self,
            *args,
            **kwargs):
        """
        Initiate the scraping env.
        """
        super(LegalDocumentsSpider, self).__init__(*args, **kwargs)

        # enable specific pipelines
        self._pipelines = ['LegalDocumentPipeline']

        #############################################################
        # URLS
        #############################################################

        self.providers = {}

    def start_requests(
            self):
        """
        Queue all the legal document's urls.
        """
        # forge the search urls & queue the requests
        for __provider, __meta in self.providers.items():
            self.log('[{provider}] requesting cookies policy...'.format(
                provider=__provider))
            yield scrapy.Request(
                url=__meta['url'],
                callback=self.parse,
                meta={'provider': __provider, 'selector': __meta['selector']})

    def parse(
            self,
            response):
        """
        Process the downloaded html pages.
        """
        __provider = response.meta.get(
            'provider',
            'none')
        __selector = response.meta.get(
            'selector',
            '//body')

        self.log('[{provider}] parsing cookies policy...'.format(
            provider = __provider))

        __loader = LegalDocumentLoader(
            item=LegalDocument(),
            response=response)

        __loader.add_value('url', response.url)
        __loader.add_value('provider', __provider)
        __loader.add_xpath('text', __selector)

        return __loader.load_item()
