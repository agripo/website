import re

from .base import FunctionalTest
from django.core.urlresolvers import reverse
from .page_shop import ShopPage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class ShopPageTest(FunctionalTest):

    def add_products_to_cart(self, number=1, quantity=1, product_id=None):
        if product_id:
            number = 1
            all_products = [self.browser.find_element_by_id('product_{}'.format(product_id))]
        else:
            all_products = self.browser.find_elements_by_css_selector('.one_product_category .one_product')

        count = 0
        for i in range(0, len(all_products)):
            try:
                prod = all_products[i].find_element_by_css_selector("input[type='number']")
            except NoSuchElementException:
                pass
            else:
                prod.clear()
                prod.send_keys(quantity)
                all_products[i].find_element_by_css_selector("input[type='submit']").click()
                searched = ".add_to_cart_confirm_message"
                WebDriverWait(all_products[i], timeout=10).until(
                    lambda b: b.find_element_by_css_selector(searched),
                    'Could not find element with css selector "{}".'.format(searched)
                )

                count += 1
                if count == number:
                    return prod

    def test_can_add_edit_command_products(self):
        faker = self.faker
        user_alpha_email = faker.email()  # We want a different email each time (for staging)

        # The shop already contains some products
        self.populate_db(categories_count=2, products_count=2)

        # Alpha gets connected as manager after having gone to the shop page
        shop = ShopPage(self).show()

        self.create_autoconnected_session(user_alpha_email, as_manager=True, as_farmer=True)

        # He goes to the products edition page
        self.show_admin_page("core", 'product', 'add')

        # He adds a product to the shop in an existing category
        the_product_name = faker.sentence()
        self.browser.find_element_by_id(shop.id_field_name).send_keys(the_product_name)
        select = Select(self.browser.find_element_by_id(shop.id_field_category))
        select.select_by_index(2)
        self.browser.find_element_by_id(shop.id_field_price).send_keys('100')
        message = self.admin_save('/admin/core/product/')
        new_product_id = re.compile("[^0-9]+([0-9]+)[^0-9]+").match(message).group(1)

        # He then adds some stock for this product
        self.show_admin_page("core", 'stock', 'add')
        select = Select(self.browser.find_element_by_id('id_product'))
        select.select_by_value(new_product_id)
        select = Select(self.browser.find_element_by_id('id_farmer'))
        select.select_by_index(1)
        self.browser.find_element_by_id('id_stock').send_keys('10')
        self.admin_save('/admin/core/stock/')

        # He confirms the shop page contains the new product
        page = shop.show()
        products = self.browser.find_elements_by_css_selector('.product_name')
        found = False
        for product in products:
            found = found or the_product_name.startswith(product.text, 0, -3)

        self.assertTrue(
            found, "New product not found on shop page (searched '{}')".format(the_product_name))

        # He sees his cart is empty
        self.browser.find_element_by_id("cart_is_empty")  # should not raise

        # He adds two products to his cart
        self.add_products_to_cart(2)

        # He sees that those items are listed in his cart
        self.assert_is_hidden("cart_is_empty")
        cart_products = self.browser.find_elements_by_css_selector('#cart_contents li')
        self.assertEqual(len(cart_products), 2)

        # He deletes a product from his cart
        self.add_products_to_cart(1, quantity=0)
        self.assert_is_hidden("cart_is_empty")

        # He sees there still is one
        cart_products = self.browser.find_elements_by_css_selector('#cart_contents li')
        self.assertEqual(len(cart_products), 1)

        # He deletes the other product from his cart, which gives him back an empty cart
        self.add_products_to_cart(2, quantity=0)
        self.browser.find_element_by_id("cart_is_empty")  # should not raise

        # He adds again two products
        self.add_products_to_cart(2, 2)  # two products with quantity = 2
        self.add_products_to_cart(1, 1)  # the first's quantity is changed to 1

        # He adds the entire quantity of the new product
        self.add_products_to_cart(quantity=10, product_id=new_product_id)

        # He clicks the validation button
        self.click_link(reverse('checkout'))

        # He selects his destination (Yaoundé), and gets a confirmation for his command
        self.select_option_by_index('id_delivery', 2, True)
        self.dev_point(10)

        # He notices that the cart is empty, and the button to checkout is not there anymore

        # He goes to the delivery admin page and sees the summary of his command

        # He writes the delivery as done from the deliveries list

        # He goes to the delivery's detail form, and confirms it has been set as done

        # He sees in thedeliveries list that there are deliveries without commands (no links)
        # and ons with commands (with a link)

        # He follows a link, and sees there are instructions, list of products, and commands

    def test_farmer_admin(self):
        # # Some products are added to the shop
        self.populate_db(categories_count=2, products_count=2)
        self.dev_point()

        # Alpha, an administrator, goes to the administration page of a product and notes the stock

        # Bravo, a farmer, goes to the shop page

        # Alpha and bravo see the exact same page, except for the connection box, and
        # a stock management box shown only to Bravo

        # Bravo follows his stock management link

        # He sees a page listing all the products, and showing his stocks for each of them.

        # He updates his stock for the product viewed by alpha and saves

        # Alpha refreshes the page, and confirms that the new calculated stock has been majored
        # by the same amount
