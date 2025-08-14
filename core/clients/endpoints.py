from enum import Enum


class PetEndpoints(Enum):
    PET_ENDPOINT = '/pet'
    PET_BY_STATUS = '/pet/findByStatus'
    PET_BY_TAGS = '/pet/findByTags'

class StoreEndpoints(Enum):
    STORE_INVENTORY = '/store/inventory'
    STORE_ORDER = '/store/order'

class UserEndpoints(Enum):
    USER_ENDPOINT = '/user'
    USER_CREATE_WITH_LIST = '/user/createWithList'
    USER_LOGIN = '/user/login'
    USER_LOGOUT = '/user/logout'
