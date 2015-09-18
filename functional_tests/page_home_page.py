class HomePage(object):
    id_login = "id_login_persona"
    id_logout = "id_logout"
    id_page = 'id_home_page'
    id_page_uses_cookies = "id_uses_cookies"
    id_admin_homepage_content = "id_homepage_content"
    id_admin_news_count = "id_news_count"

    def __init__(self, test):
        self.test = test

    def show(self):
        self.test.browser.get(self.test.server_url)
        self.test.wait_for(self._is_home_page)
        return self

    def _is_home_page(self):
        return self.test.browser.find_element_by_id(self.id_page)

    def check_connection_status(self, status):
        if status:
            self.get_logout_button()
        else:
            self.get_login_button()

        return self

    def get_login_button(self):
        return self.test.browser.find_element_by_id(self.id_login)

    def get_logout_button(self):
        return self.test.browser.find_element_by_id(self.id_logout)
