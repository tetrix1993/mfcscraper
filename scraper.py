import requests
from bs4 import BeautifulSoup as bs
import constants
from models import Item, ItemEntry, ItemRelease, Category


class MfcScraper:
    session_id = None

    def __init__(self, username=None, password=None):
        if username is None or password is None:
            return

        if len(username) > 0 or len(password) > 0:
            try:
                form_data = {'commit': 'signIn', 'from': '', 'username': username, 'password': password}
                r = requests.post(constants.LOGIN_URL, data=form_data)
                r.raise_for_status()
                self.session_id = r.cookies.get_dict()['PHPSESSID']
            except requests.HTTPError:
                pass

    def get_soup(self, url, headers=None):
        """Returns BeautifulSoup object of the webpage from the url"""

        if self.session_id and len(self.session_id) > 0:
            if not headers:
                headers = {'Cookie': 'PHPSESSID=' + self.session_id}
            else:
                headers['Cookie'] = 'PHPSESSID=' + self.session_id
        r = requests.get(url, headers=headers)
        return bs(str(r.content.decode()), 'html.parser')

    def get_json(self, url, headers=None, data=None):
        if self.session_id and len(self.session_id) > 0:
            if not headers:
                headers = {'Cookie': 'PHPSESSID=' + self.session_id}
            else:
                headers['Cookie'] = 'PHPSESSID=' + self.session_id
        try:
            if data:
                r = requests.post(url, headers=headers, data=data)
            else:
                r = requests.post(url, headers=headers)
            return r.json()
        except:
            return None

    def get_item_by_id(self, item_id):
        """Returns an Item object of item ID"""
        try:
            id_ = int(item_id)
            item = Item(id_)
            soup = self.get_soup(constants.ITEM_URL_PREFIX + str(item_id))

            # Database
            db_a_tag = soup.select('ul.secondary a.selected')
            if len(db_a_tag) > 0:
                item.database = db_a_tag[0].text.strip()

            # Details
            form_fields = soup.select('div.form-field')
            for form_field in form_fields:
                form_label = form_field.find('div', 'form-label')
                form_input = form_field.find('div', 'form-input')
                if form_label and form_input:
                    label_text = form_label.text.strip()
                    if label_text == constants.ITEM_CATEGORY:
                        a_tags = form_input.select('a')
                        if len(a_tags) > 0:
                            if a_tags[0].has_attr('href'):
                                category_id = None
                                try:
                                    category_id = int(a_tags[0]['href'].split('=')[-1])
                                except:
                                    pass
                                category_name = a_tags[0].text.strip()
                                item.category = Category(category_id, category_name)
                    elif label_text in constants.ITEM_FORM_LABELS_MULTIPLE:
                        a_tags = form_input.select('a')
                        entries = []
                        for a_tag in a_tags:
                            if a_tag.has_attr('href'):
                                entry_id = None
                                try:
                                    entry_id = int(a_tag['href'].split('/')[-1])
                                except:
                                    pass
                                span_tag = a_tag.find('span')
                                if span_tag:
                                    name_jp = None
                                    if span_tag.has_attr('switch'):
                                        name_jp = span_tag['switch'].strip()
                                    name = span_tag.text.strip()
                                    entry_type = None
                                    if label_text in constants.ITEM_FORM_LABELS_WITH_TYPES:
                                        small_tag = a_tag.find('small')
                                        if small_tag and len(small_tag.text.strip()) > 3:
                                            entry_type = small_tag.text.strip()[3:]
                                    entry = ItemEntry(entry_id, name, name_jp, entry_type)
                                    entries.append(entry)
                        if label_text in constants.ITEM_CLASSIFICATIONS_:
                            item.classifications = entries
                        elif label_text in constants.ITEM_ORIGINS_:
                            item.origins = entries
                        elif label_text in constants.ITEM_CHARACTERS_:
                            item.characters = entries
                        elif label_text in constants.ITEM_COMPANIES_:
                            item.companies = entries
                        elif label_text in constants.ITEM_ARTISTS_:
                            item.artists = entries
                        elif label_text in constants.ITEM_MATERIALS_:
                            item.materials = entries
                        elif label_text in constants.ITEM_EVENTS_:
                            item.events = entries
                    elif label_text == constants.ITEM_SCALE_AND_DIMENSION:
                        a_tag = form_input.find('a')
                        if a_tag and a_tag.has_attr('href'):
                            try:
                                item.scale = a_tag['href'].split('=')[-1]
                            except:
                                pass
                        small_tags = form_input.select('small')
                        for small_tag in small_tags:
                            try:
                                small_tag_text = small_tag.string.strip()
                                if small_tag_text == 'W=':
                                    item.width = int(small_tag.nextSibling.string.strip().replace(',', ''))
                                elif small_tag_text == 'L=':
                                    item.length = int(small_tag.nextSibling.string.strip().replace(',', ''))
                                elif small_tag_text == 'H=':
                                    item.height = int(small_tag.nextSibling.string.strip().replace(',', ''))
                            except:
                                pass
                    elif label_text == constants.ITEM_PRICE:
                        span_tag = form_input.find('span', class_='item-price')
                        if span_tag:
                            try:
                                item.price = int(span_tag.text.strip()[1:].replace(',', ''))
                            except:
                                pass
                    elif label_text == constants.ITEM_JAN:
                        a_tag = form_input.find('a')
                        if a_tag:
                            try:
                                item.jan = int(a_tag.text.strip())
                            except:
                                pass

            # Release Dates
            item.releases = self.get_item_release_date(item_id)

            # Other Information
            other_div = soup.select('div.object-description.item-information div.bbcode')
            if other_div:
                html_content = str(other_div)
                try:
                    item.further_info = html_content[21:len(html_content) - 7]
                except:
                    pass

            return item
        except:
            pass
        return None

    def get_item_release_date(self, item_id):
        releases = []
        form_data = {'commit': 'loadWindow', 'window': 'showAllReleases'}
        json_obj = self.get_json(constants.ITEM_URL_PREFIX + str(item_id), data=form_data)
        try:
            date_soup = bs(json_obj['htmlValues']['WINDOW'], 'html.parser')
            listing_items = date_soup.select('li.listing-item')
            for item in listing_items:
                release = ItemRelease()
                stamp_anchor = item.find('div', class_='stamp-anchor')
                if stamp_anchor:
                    a_tag = stamp_anchor.find('a')
                    if a_tag:
                        try:
                            full_date = a_tag.text.strip()
                            date_split = full_date.split('/')
                            if len(date_split) == 3:
                                release.day = int(date_split[0])
                                release.month = int(date_split[1])
                                release.year = int(date_split[2])
                            elif len(date_split) == 2:
                                release.month = int(date_split[0])
                                release.year = int(date_split[1])
                            else:
                                release.year = int(date_split[0])
                        except:
                            pass
                    em_tags = stamp_anchor.select('em')
                    if len(em_tags) > 0:
                        release.run = em_tags[0].text.strip()
                    if len(em_tags) > 1:
                        additional_info = em_tags[1].text.strip()
                        if len(additional_info) > 2:
                            release.additional_info = additional_info[1:len(additional_info) - 1]
                stamp_meta = item.find('div', class_='stamp-meta')
                if stamp_meta:
                    span_icon_tag = stamp_meta.find('span', class_='icon-tag')
                    if span_icon_tag:
                        try:
                            release.price = int(span_icon_tag.next_element.string[1:].replace(',', ''))
                        except:
                            pass
                    span_icon_barcode = stamp_meta.find('span', class_='icon-barcode')
                    if span_icon_barcode:
                        try:
                            release.barcode = span_icon_barcode.next_element.text
                        except:
                            pass
                releases.append(release)
        except:
            pass
        return releases
