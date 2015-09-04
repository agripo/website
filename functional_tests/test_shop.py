import time


from .base import FunctionalTest
from django.core.urlresolvers import reverse
from .page_shop import ShopPage
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class ShopPageTest(FunctionalTest):

    def add_products_to_cart(self, number):
        all_products = self.browser.find_elements_by_css_selector('.one_product_category .one_product')
        count = 0
        for i in range(0, len(all_products)):
            try:
                prod = all_products[i].find_element_by_css_selector("input[type='number']")
            except NoSuchElementException:
                pass
            else:
                prod.clear()
                prod.send_keys('1')
                all_products[i].find_element_by_css_selector("input[type='submit']").click()
                searched = ".add_to_cart_confirm_message"
                WebDriverWait(all_products[i], timeout=10).until(
                    lambda b: b.find_element_by_css_selector(searched),
                    'Could not find element with id {}. Page text was:\n{}'.format(
                        searched, all_products[i].find_element_by_css_selector(searched)
                    )
                )

                count += 1
                if count == number:
                    break

    def test_can_add_edit_command_products(self):
        faker = self.faker
        user_alpha_email = faker.email()  # We want a different email each time (for staging)
        faker.seed(1000)

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
        self.admin_save('/admin/core/product/')

        # He then adds som stock for two products
        go_directly = False
        for i in range(2, 6):
            self.show_admin_page("core", 'stock', 'add', directly=go_directly)
            select = Select(self.browser.find_element_by_id('id_product'))
            select.select_by_index(i)
            select = Select(self.browser.find_element_by_id('id_farmer'))
            select.select_by_index(1)
            self.browser.find_element_by_id('id_stock').send_keys('100')
            self.admin_save('/admin/core/stock/')
            go_directly = True

        # He confirms the shop page contains the new product
        page = shop.show()
        products = self.browser.find_elements_by_css_selector('.product_name')
        found = False
        for product in products:
            found = found or the_product_name.startswith(product.text, 0, -3)

        self.assertTrue(
            found, "New product not found on shop page (searched '{}')".format(the_product_name))

        # He sees his cart is empty
        self.assertContains(page, "Votre panier est vide")

        # He adds two products to his cart
        self.add_products_to_cart(2)

        # He sees that those items are listed in his cart
        self.assertNotContains(page, "Votre panier est vide")
        cart_products = self.browser.find_elements_by_css_selector('ul.cart_contents li')
        self.assertEqual(len(cart_products), 2)

        # He deletes a product from his cart
        first = cart_products[0]
        first.find_element_by_tag_name("a").click()
        self.wait_for_element_with_id("product_removed_successfully")
        self.assertNotContains(page, "Votre panier est vide")

        # He sees there still is one
        all_products = self.browser.find_elements_by_css_selector('.one_product_category .one_product')
        self.assertEqual(len(all_products), 1)

        # He deletes the other product from his cart, which gives him an empty cart
        first = cart_products[1]
        first.find_element_by_tag_name("a").click()
        self.wait_for_element_with_id("product_removed_successfully")
        self.assertContains(page, "Votre panier est vide")

        # He adds again two products
        self.add_products_to_cart(2)

        # He clicks the validation button
        self.browser.find_element_by_id('id_checkout').click()
        self.wait_for_element_with_id("checkout_form")

        # He selects his destination (Yaoundé), and gets a confirmation for his command
        self.dev_point(5)
