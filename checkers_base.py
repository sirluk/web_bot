import requests
import smtplib
from jinja2 import Template
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional


class _ProductAvailabilityCheckerBase(ABC):

    @abstractmethod
    def get_website_data(
        self,
        url: str,
        use_api: bool = False,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_params: Optional[str] = None
        ):
        """Get html code from url and save retun as beautifulsoup object
        Args:
            url (str): The url to crawl
            use_api (bool, optional): Wheather or not to use a proxy service for crawling. Defaults to False.
        """

    @abstractmethod
    def send_email(self, threshold: int, product_name: str):
        """add docstring"""

    @abstractmethod
    def is_available(self):
        """add docstring"""

    @abstractmethod
    def get_price(self):
        """add docstring"""

    @abstractmethod
    def _send_email(
        self, 
        email_address: str,
        email_password: str,
        email_send_to: str,
        product_name: str
        ):
        """add docstring"""


class ProductAvailabilityChecker(_ProductAvailabilityCheckerBase):

    def get_website_data(
        self,
        url: str,
        use_api: bool = False,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_params: Optional[str] = None
        ):
        if use_api:
            api_params = {"url": url, "apikey": api_key, **api_params}
            r = requests.get(api_url, params=api_params)
        else:
            r = requests.get(url, timeout=5)
        
        if r.status_code == 200:
            source = r.text
        else:
            raise Exception(r.status_code)

        self.url = url
        self.soup = BeautifulSoup(source, "lxml")

    def send_email(self, threshold: int, *args, **kwargs):
        if self.is_available() and self.get_price() < threshold:
            self._send_email(*args, **kwargs)

    def is_available(self):
        raise NotImplementedError

    def get_price(self):
        raise NotImplementedError

    def _send_email(
        self, 
        email_address: str,
        email_password: str,
        email_send_to: str,
        product_name: str
        ):
        # configure email
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login(email_address, email_password)

        with open('message.html') as f:
            message_template = Template(f.read())

        # create a message
        msg = MIMEMultipart()

        # add in the actual person name to the message template
        params = {
            "product_name": product_name,
            "price": self.get_price(),
            "url": self.url,
            "website_name": self.website_name
        }
        message = message_template.render(**params)

        # setup the parameters of the message
        msg['From'] = email_address
        msg['To'] = email_send_to
        msg['Subject']="PRICE ALERT for {}".format(product_name)

        # add in the message body
        msg.attach(MIMEText(message, 'html'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        
        del msg
