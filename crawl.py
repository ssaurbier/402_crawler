""" 402 Crawler

    Crawl endpoints, check socket connection, and
    check 402 headers.

"""

import os
import json
import datetime
import logging
import socket
import requests

from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests


class Crawler402():
    """ Crawl endpoints to check status.

        Check server socket connection and query endpoints for
        price and recipient address.

    """


    def __init__(self, endpoint_list, log_file):
        """Set up logging & member vars"""

        # configure logging
        logging.basicConfig(level=logging.INFO,
                            filename=log_file,
                            filemode='a',
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M')

        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        logging.getLogger('402-crawler').addHandler(self.console)
        self.logger = logging.getLogger('402-crawler')
        self.endpoint_list = endpoint_list


    def check_endpoints(self):
        """Crawl 402 endpoints"""

        # create 402 client
        self.bitrequests = BitTransferRequests(Wallet(), Config().username)

        # crawl endpoints, check headers
        self.logger.info("\nCrawling machine-payable endpoints...")
        for endpoint in self.endpoint_list:

            # extract domain name
            name = endpoint.split('/',1)[0].split('.',1)[1]

            # get server ip
            server_ip = socket.gethostbyname(name)

            # self.logger.info("Checking {0} on port {1}".format(server_ip, port))
            self.logger.info("Checking {}...".format(endpoint))
            # configure socket module
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_state = sock.connect_ex((server_ip, 80))
            sock.close()

            if server_state == 0:
                try:
                    self.logger.info("Server state: {} is up!".format(endpoint))
                    response = self.bitrequests.get_402_info('https://'+endpoint)
                    self.logger.info("Price: {}".format(response['price']))
                    self.logger.info("Address: {}".format(response['bitcoin-address']))
                except Exception as e:
                    self.logger.info("Could not read 402 payment headers.")
            else:
                self.logger.info("Server state: {} is down!".format('https://'+endpoint))
            self.logger.info("Timestamp: {}\n".format(datetime.datetime.now()))


if __name__=='__main__':

    # 402 endpoints to crawl
    endpoint_list = [
        'market.21.co/search/bing',
        'market.21.co/phone/send-sms',
    ]

    crawler = Crawler402( endpoint_list, '402-crawler.log')
    crawler.check_endpoints()
