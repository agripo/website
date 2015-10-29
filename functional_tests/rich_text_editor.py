class RichTextEditor(object):

    def __init__(self, test, field_id):
        self.test = test
        self.browser = test.browser
        self.field_id = field_id
        self.editor_frame = self.test.wait_for_element_with_selector(
            'iframe[title="Rich Text Editor, {}"]'.format(self.field_id))

    def _activate(self, frame=None):
        if not frame:
            frame = self.editor_frame
        self.browser.switch_to.frame(frame)

    def _deactivate(self):
        self.browser.switch_to.default_content()

    def _get_content_element(self):
        return self.browser.find_element_by_css_selector("body")

    def insert_content(self, content):
        self._activate()
        self.browser.find_element_by_css_selector("body").send_keys(content)
        self._deactivate()

    def empty_content(self):
        self._activate()
        self.browser.execute_script("document.getElementsByTagName('body')[0].innerHTML = '';")
        self._deactivate()
