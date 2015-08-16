import time


from .base import FunctionalTest
from .page_shop import ShopPage



class ShopPageTest(FunctionalTest):

    def test_can_command_products(self):
        # # We should add some products automatically
        # Alpha gets connected as manager
        shop = ShopPage(self).show()

        # Alpha sees that there are some products he could buy

        # He adds some of them to the cart

        # He sees that those items are listed in his cart

        # He clicks the validation button

        # He sees that the system asks him to connect or to create an account

        # He connects with his (fake) account, and can proceed to the checkout

        # He selects his destination (Yaoundé), and gets a confirmation for his command

        time.sleep(5)
        self.fail('This is where we are!')
