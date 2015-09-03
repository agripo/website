import time


from .base import FunctionalTest
from .page_shop import ShopPage
from selenium.webdriver.support.select import Select


class ShopPageTest(FunctionalTest):

    def test_can_add_and_edit_products(self):
        faker = self.faker
        faker.seed(1000)
        # The shop already contains some products
        self.populate_db(categories_count=2)

        # Alpha gets connected as manager after having gone to the shop page
        shop = ShopPage(self).show()
        user_alpha_email = faker.email()
        self.create_autoconnected_session(user_alpha_email, as_manager=True)

        # He goes to the products edition page
        self.show_admin_page("core", 'product', 'add')  # Base admin page

        # He adds a product to the shop in an existing category
        the_product_name = faker.sentence()
        self.browser.find_element_by_id(shop.id_field_name).send_keys(the_product_name)
        select = Select(self.browser.find_element_by_id(shop.id_field_category))
        select.select_by_index(2)
        self.browser.find_element_by_id(shop.id_field_price).send_keys('100')

        # He saves
        self.admin_save('/admin/core/product/')

        # He confirms the shop page contains the new product
        shop.show()
        products = self.browser.find_elements_by_css_selector('.product_name')
        found = False
        for product in products:
            found = found or the_product_name.startswith(product.text, 0, -3)

        self.assertTrue(
            found, "New product not found on shop page (searched '{}')".format(the_product_name))

    def test_can_command_products(self):
        # # We should add some products automatically
        self.populate_db(categories_count=1, products_count=10)

        # Alpha goes to the shop page
        shop = ShopPage(self).show()

        # Alpha sees that there are some (at least 10) products he could buy
        all_products = self.browser.find_elements_by_css_selector('.one_product_category .one_product')
        self.assertLess(
            9, len(all_products), 'Did not find enough products on the page (should be at least 10)')

        # He adds some of them to the cart

        # He sees that those items are listed in his cart

        # He clicks the validation button

        # He sees that the system asks him to connect or to create an account

        # He connects with his (fake) account, and can proceed to the checkout

        # He selects his destination (Yaoundé), and gets a confirmation for his command
        self.dev_point(5)
