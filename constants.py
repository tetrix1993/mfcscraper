WEB_PREFIX = 'https://myfigurecollection.net/'
LOGIN_URL = WEB_PREFIX + 'session/signin/'
ITEM_URL_PREFIX = WEB_PREFIX + 'item/'

DATABASE_FIGURES = 'Figures'
DATABASE_GOODS = 'Goods'
DATABASE_MEDIA = 'Media'

IMAGE_TYPE_OFFICIAL = 'Official'
IMAGE_TYPE_CHAN = 'Chan'

ITEM_CATEGORY = 'Category'
ITEM_CLASSIFICATION = 'Classification'
ITEM_CLASSIFICATIONS = 'Classifications'
ITEM_ORIGIN = 'Origin'
ITEM_ORIGINS = 'Origins'
ITEM_CHARACTER = 'Character'
ITEM_CHARACTERS = 'Characters'
ITEM_COMPANY = 'Company'
ITEM_COMPANIES = 'Companies'
ITEM_ARTIST = 'Artist'
ITEM_ARTISTS = 'Artists'
ITEM_VERSION = 'Version'
ITEM_MATERIAL = 'Material'
ITEM_MATERIALS = 'Materials'
ITEM_SCALE_AND_DIMENSION = 'Scale & Dimensions'
ITEM_RELEASE_DATE = 'Release date'
ITEM_RELEASE_DATES = 'Release dates'
ITEM_PRICE = 'Price'
ITEM_JAN = 'JAN'
ITEM_EVENT = 'Event'
ITEM_EVENTS = 'Events'
ITEM_INFORMATION = 'Information'

ITEM_CLASSIFICATIONS_ = [ITEM_CLASSIFICATION, ITEM_CLASSIFICATIONS]
ITEM_ORIGINS_ = [ITEM_ORIGIN, ITEM_ORIGINS]
ITEM_CHARACTERS_ = [ITEM_CHARACTER, ITEM_CHARACTERS]
ITEM_COMPANIES_ = [ITEM_COMPANY, ITEM_COMPANIES]
ITEM_ARTISTS_ = [ITEM_ARTIST, ITEM_ARTISTS]
ITEM_MATERIALS_ = [ITEM_MATERIAL, ITEM_MATERIALS]
ITEM_RELEASE_DATES_ = [ITEM_RELEASE_DATE,ITEM_RELEASE_DATES]
ITEM_EVENTS_ = [ITEM_EVENT, ITEM_EVENTS]

ITEM_FORM_LABELS_MULTIPLE = ITEM_CLASSIFICATIONS_ + ITEM_ORIGINS_ + ITEM_CHARACTERS_ + ITEM_COMPANIES_ + \
    ITEM_ARTISTS_ + ITEM_MATERIALS_ + ITEM_EVENTS_
ITEM_FORM_LABELS_WITH_TYPES = ITEM_COMPANIES_ + ITEM_ARTISTS_ + ITEM_MATERIALS_ + ITEM_EVENTS_
