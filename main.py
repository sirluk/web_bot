import os
from flask import Flask

from checkers import MindFactoryChecker, CyberportChecker
from utils import str2bool, on_off_check


app = Flask(__name__)


# get env vars
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SEND_TO = os.getenv("EMAIL_SEND_TO")
API_KEY = os.getenv("API_KEY")
ON_OFF = str2bool(os.getenv('ON_OFF', default='True'))

API_URL = 'https://app.zenscrape.com/api/v1/get'
API_PARAMS = {"location": "eu"}


@app.route('/', methods=['GET', 'POST'])
@on_off_check(ON_OFF)
def main():
    
    url = "https://www.mindfactory.de/product_info.php/16GB-PowerColor-Radeon-RX-6900-XT-Red-Devil-Aktiv-PCIe-4-0-x16--Retail-_1388403.html"
    checker = MindFactoryChecker()
    checker.get_website_data(url, use_api=False)
    checker.send_email(
        threshold = 1500, 
        email_address = EMAIL_ADDRESS, 
        email_password = EMAIL_PASSWORD, 
        email_send_to = EMAIL_SEND_TO, 
        product_name = "16GB PowerColor Radeon RX 6900 XT Red Devil"
    )

    url = "https://www.cyberport.at/pc-und-zubehoer/komponenten/grafikkarten/powercolor/pdp/2e23-16v/powercolor-amd-radeon-rx-6900-xt-red-devil-16gb-gddr6-grafikkarte-hdmi-3xdp.html"
    checker = CyberportChecker()
    checker.get_website_data(url, use_api=True, api_url=API_URL, api_key=API_KEY, api_params=API_PARAMS)
    checker.send_email(
        threshold = 1500, 
        email_address = EMAIL_ADDRESS, 
        email_password = EMAIL_PASSWORD, 
        email_send_to = EMAIL_SEND_TO, 
        product_name = "16GB PowerColor Radeon RX 6900 XT Red Devil"
    )



if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))