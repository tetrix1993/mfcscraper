import constants


class Item:
    id = None
    database = None
    category = None
    classifications = []
    origins = []
    characters = []
    companies = []
    artists = []
    materials = []
    events = []
    width = None
    length = None
    height = None
    weight = None
    releases = []
    is_canceled = False
    price = None
    version = None
    original_version = None
    numbering = None
    scale = None
    num_of_parts = None
    is_cast_off = False
    is_counterfeit = False
    title = None
    original_title = None
    pages = None
    paper_size = None
    episodes = None
    tracks = None
    discs = None
    run_time = None
    is_region_free = False
    rating = '-'
    further_info = None

    def __init__(self, item_id):
        self.id = item_id


# Classification, Origin, Character, Company, Material, Event
class ItemEntry:
    id = None
    name = None
    name_jp = None
    type = None

    def __init__(self, entry_id, name, name_jp, entry_type=None):
        self.id = entry_id
        self.name = name
        self.name_jp = name_jp
        self.type = entry_type


class ItemRelease:
    year = None
    month = None
    day = None
    run = None
    price = None
    barcode = None
    catalog_id = None
    additional_info = None


class Category:
    id = None
    name = None

    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name
