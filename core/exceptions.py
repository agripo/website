class CantSetCartQuantityOnUnsavedProduct(Exception):

    def __str__(self):
        return "Adding to cart on an unsaved object"


class AddedMoreToCartThanAvailable(Exception):

    def __str__(self):
        return "We may not add more to cart than available"


class NoAutoConnectionWithExistingUser(Exception):
    """ We may only autoconnect new users """

    def __str__(self):
        return "We may not autoconnect existing users"


class NoAutoConnectionOnProductionServer(Exception):
    """ We may only autoconnect on dev or staging servers """

    def __str__(self):
        return "Autoconnect is disabled on production server"


class AutoConnectionUnknownError(Exception):
    """ Unknown error during autoconnection """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
