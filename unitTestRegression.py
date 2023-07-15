import unittest
import logging
from flask import Flask
from flask.testing import FlaskClient
from app import app


class HTTPServerUnitTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True

        logging.basicConfig(level=logging.DEBUG)
        self.logger = app.logger
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_regression(self):

        # Account Enquiry
        accountEnquiryRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18907',
            'Fr': 'ARTGIDJA',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            'NbOfTxs': "1",
            'SttlmMtd': "CLRG",
            'CtgyPurp': "51001",
            'IntrBkSttlmAmt_value': 123.12,
            'IntrBkSttlmAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'Dbtr_nm': "Naufal Afif",
            'DbtrAcct_value': '123456789',
            'DbtrAcct_type': 'SVGS',
            'DbtrAgt': 'ARTGIDJA',
            'CdtrAgt': 'ATOSIDJ1',
            'Cdtr_nm': 'Bunyamin',
            'CdtrAcct_value': '987654321'
        }
        accountEnquiryResponse = self.client.post(
            '/AccountEnquiryOFI', data=accountEnquiryRequestForm)

        # Credit Transfer
        creditTransferRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18907',
            'Fr': 'ARTGIDJA',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": false,
            'NbOfTxs': "1",
            'SttlmMtd': "CLRG",
            'CtgyPurp': "51001",
            'LclInstrm': "01",
            'IntrBkSttlmAmt_value': 123.12,
            'IntrBkSttlmAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'Dbtr_nm': "Naufal Afif",
            'Dbtr_orgid': "PT. Abhimata Persada",
            'DbtrAcct_value': '123456789',
            'DbtrAcct_type': 'SVGS',
            'DbtrAgt': 'ARTGIDJA',
            'CdtrAgt': 'ATOSIDJ1',
            'Cdtr_nm': 'Bunyamin',
            'Cdtr_orgid': 'PT. Telkom Indonesia',
            'CdtrAcct_value': '987654321',
            'CdtrAcct_type': 'SVGS',
            'RmtInf': "Testing purpose",
            'SplmtryData_Dbtr_tp': '01',
            'SplmtryData_Dbtr_rsdntsts': '01',
            'SplmtryData_Dbtr_twnnm': '0300',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
        }
        creditTransferResponse = self.client.post('/CreditTransferOFI')
        ctEndToEndId = creditTransferResponse.json().get('OrgnlEndToEndId')
        ctPSRResponse = self.client.post(f'/PaymentStatusOFI/{ctEndToEndId}')

        # Credit Transfer Reversal
        creditTransferReversalResponse = self.client.post(
            '/CreditTransferReversalOFI')
        ctReverseEndToEndId = creditTransferReversalResponse.json().get('OrgnlEndToEndId')
        ctReversePSRResponse = self.client.post(
            f'/PaymentStatusOFI/{ctReverseEndToEndId}')

        # Credit Transfer Proxy
        creditTransferProxyResponse = self.client.post(
            '/CreditTransferProxyOFI')
        ctProxyEndToEndId = creditTransferProxyResponse.json().get('OrgnlEndToEndId')
        ctProxyPSRResponse = self.client.post(
            f'/PaymentStatusOFI/{ctProxyEndToEndId}')

        # Proxy Register
        proxyRegisterResponse = self.client.post('/ProxyRegistrationOFI')
        proxyAccountNumber = ""
        proxyPrimaryType = ""
        proxyPrimaryValue = ""
        proxySecondaryType = ""
        proxySecondaryValue = ""
        proxyData = {
            'proxyAccountNumber': proxyAccountNumber,
            'proxyPrimaryType': proxyPrimaryType,
            'proxyPrimaryValue': proxyPrimaryValue,
            'proxySecondaryType': proxySecondaryType,
            'proxySecondaryValue': proxySecondaryValue
        }

        # Proxy Register Lookup
        proxyRegsiterLookupResponse = self.client.post(
            '/ProxyLookupOFI', data=proxyData)

        # Proxy Register Enquiry
        proxyRegisterEnquiryResponse = self.client.post(
            '/ProxyEnquiryOFI', data=proxyData)

        # Proxy Porting
        proxyPortingResponse = self.client.post(
            '/ProxyPortingOFI', data=proxyData)

        # Proxy Porting Lookup

        # Proxy Porting Enquiry

        # Proxy Deactivate

        # Proxy Deactivate Lookup

        # Proxy Deactivate Enquiry

        # Request For Payment
        requestForPaymentResponse = self.client.post()

    def test_proxyRegistrationOFI(self):
        response = self.client.post('/ProxyRegistrationOFI')
        self.assertEqual(response.status_code, 200)
        response_body = response.data
        self.logger.debug(response_body)


if __name__ == '__main__':
    unittest.main()
