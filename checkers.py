import re
from checkers_base import ProductAvailabilityChecker


class MindFactoryChecker(ProductAvailabilityChecker):
    website_name: str = "MindFactory"

    def is_available(self):
        return 'lagernd' in self.soup.find(
            'a', {'href': 'https://www.mindfactory.de/popup_lagerstatus_help.php'}
        ).text.lower()

    def get_price(self):
        price_pattern = re.compile("\d{0,3}\.?\d{1,3}")
        price_text = self.soup.find('div', {'class': re.compile('.*price')}).text
        return int(re.search(price_pattern, price_text).group(0).replace(".", ""))


class CyberportChecker(ProductAvailabilityChecker):
    website_name: str = "Cyberport"

    def is_available(self):
        return "nicht verfügbar" not in self.soup.find(
            "div", {"class": "availabilityWrapper"}
        ).text

    def get_price(self):
        price_str = self.soup.find("div", {"class": "price delivery-price"}).text.strip()
        pattern = re.compile("\d{0,3}\.?\d{1,3}\,\d{2}")
        if (s := re.search(pattern, price_str)):
            _price = re.sub("[^0-9]", "", s.group(0))
            return int(_price) // 100