from .base import FunctionalTest
from functional_tests.pages_webdoc import WebdocPages


class WebdocPagesTest(FunctionalTest):

    def test_display_all_pages(self):
        webdoc_pages = WebdocPages(self)

        # Alpha goes to evry page of the webdoc
        for page in webdoc_pages.all_pages:
            webdoc_pages.show(page)
