class CantSetCartQuantityOnUnsavedProduct(Exception):
    pass


class AddedMoreToCartThanAvailable(Exception):
    pass


class NoAutoConnectionWithExistingUser(Exception):
    pass


class NoAutoConnectionOnProductionServer(Exception):
    pass


class AutoConnectionUnknownError(Exception):
    pass
