import time


from .base import FunctionalTest
from .page_shop import ShopPage


class ShopPageTest(FunctionalTest):

    def test_can_add_and_edit_products(self):
        faker = self.faker

        # Alpha gets connected as manager
        user_alpha_email = faker.email()
        self.create_autoconnected_session(user_alpha_email, as_manager=True)

        # He goes to the products edition page
        self.not_implemented()

        # He adds a product to the shop in an existing category

        # He gets a message saying that the product has been created

        # He then modifies this products

        # He gets a message saying that the product has been modified

        # He has his friend bravo to look at the shop page, unconnected, and to confirm that the new
        # product is there with the good data

    def test_can_command_products(self):
        # # We should add some products automatically
        self.populate_db(products_count=10)

        # Alpha goes to the shop page
        shop = ShopPage(self).show()

        # Alpha sees that there are some products he could buy
        all_products = self.browser.find_elements_by_css_selector('#id_products_container .one_product h4')
        self.assertEqual(
            len(all_products), 10, 'Did not find the right number of products on the page')

        # He adds some of them to the cart

        # He sees that those items are listed in his cart

        # He clicks the validation button

        # He sees that the system asks him to connect or to create an account

        # He connects with his (fake) account, and can proceed to the checkout

        # He selects his destination (Yaoundé), and gets a confirmation for his command

        time.sleep(5)
        self.fail('This is where we are!')
