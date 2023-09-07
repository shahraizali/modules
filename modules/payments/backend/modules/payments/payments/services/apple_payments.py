import json

import environ
import requests

env = environ.Env()


class ApplePaymentService:

    def __init__(self):
        self.APPLE_PRODUCT_VERIFY_URL = env.str('APPLE_PRODUCT_VERIFY_URL', '')
        self.APPLE_RECEIPT_VERIFY_URL = env.str('APPLE_RECEIPT_VERIFY_URL', '')
        self.APPLE_SANDBOX_MODE = env.bool('APPLE_SANDBOX_MODE', False)
        self.SUCCESS_STATUS_CODE = 21007

        if self.APPLE_SANDBOX_MODE:
            self.APPLE_RECEIPT_VERIFY_URL = 'https://sandbox.itunes.apple.com/verifyReceipt'

    @classmethod
    def validate_receipt_data(cls, receipt_data):
        is_valid = False
        if 'transactionReceipt' in receipt_data:
            is_valid = True
        # TODO: add more validation
        return is_valid

    def verify_apple_receipt(self, receipt_data):
        """
        Verify an Apple receipt.
        """
        # validate receipt
        if not self.validate_receipt_data(receipt_data):
            return False, False

        receipt_json = json.dumps({"receipt-data": receipt_data["transactionReceipt"]})

        # verify receipt
        verify_url = self.APPLE_PRODUCT_VERIFY_URL
        response = requests.request(
            method='POST',
            url=verify_url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=receipt_json
        )
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('status') == self.SUCCESS_STATUS_CODE:
                print("now calling sandbox")
                verify_url = self.APPLE_RECEIPT_VERIFY_URL
                response = requests.request(
                    method='POST',
                    url=verify_url,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    data=receipt_json
                )
                if response.status_code == 200:
                    res_json = response.json()

                return res_json, True
            else:
                return res_json, False
                # failure
        print("There is problem with service.", response.json())
        return False, False
