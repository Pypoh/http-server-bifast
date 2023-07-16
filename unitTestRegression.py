import unittest
import logging
from flask import Flask
from flask.testing import FlaskClient
from app import app
import random
from datetime import datetime, timedelta


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
            "PssblDplct": "false",
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
            'SplmtryData_InitgAcctId': "123456789",
            'SplmtryData_Dbtr_tp': '01',
            'SplmtryData_Dbtr_rsdntsts': '01',
            'SplmtryData_Dbtr_twnnm': '0300',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
        }
        creditTransferResponse = self.client.post(
            '/CreditTransferOFI', data=creditTransferRequestForm)
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
        uniqueId = random.randint(00000, 99999)

        proxyRegisterRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18907',
            'Fr': 'ARTGIDJA',
            'To': 'FASTIDJA',
            'MsgDefIdr': "prxy.001.001.01",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            'MsgSndr_agt': "51001",
            'MsgSndr_acct': 123.12,
            'RegnTp': 'NEWR',
            'Prxy_tp': '02',
            'Prxy_val': f'Proxy Value {uniqueId}',
            'DsplNm': f'Proxy Display Name {uniqueId}',
            'PrxyRegn_Agt_nm': 'PT. Abhimata Persada',
            'PrxyRegn_Agt_id': 'ARTGIDJA',
            'PrxyRegn_acct': f'312{uniqueId}',
            'PrxyRegn_tp': 'CACC',
            'PrxyRegn_nm': f'Proxy Name {uniqueId}',
            'ScndId_tp': '01',
            'ScndId_val': f'6812345{uniqueId}',
            'RegnSts': 'ACTV',
            'SplmtryData_Cstmr_tp': '01',
            'SplmtryData_Cstmr_id': f'10203040{uniqueId}',
            'SplmtryData_Cstmr_rsdntsts': '01',
            'SplmtryData_Cstmr_twnnm': '0300',

        }
        proxyRegisterResponse = self.client.post(
            '/ProxyRegistrationOFI', data=proxyRegisterRequestForm)
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

        # Request For Payment by Account
        timestamp_now = datetime.now().strftime('%Y-%m-%d')
        timestamp_future = (timestamp_now + timedelta(days=14)).strftime('%Y-%m-%d')
        requestForPaymentRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18907',
            'Fr': 'ARTGIDJA',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pain.013.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            'NbOfTxs': "1",
            'InitgPty_nm': "Naufal Afif",
            'InitgPty_pstladr': '0123',
            'PmtMtd': "TRF",
            'CtgyPurp': '85301',
            'ReqdExctnDt': timestamp_now,
            'XpryDt': timestamp_future,
            'DbtrAcct_value': '123456789',
            'DbtrAgt': 'ATOSIDJ1',
            'InstdAmt_value': 123.12,
            'InstdAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'CdtrAgt': 'ARTGIDJA',
            'Cdtr_orgid': 'PT. Telkom Indonesia',
            'CdtrAcct_value': '987654321',
            'CdtrAcct_type': 'SVGS',
            'CdtrAcct_nm': 'Raline',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
        }
        requestForPaymentResponse = self.client.post(
            '/RequestForPayByAccountOFI', data=requestForPaymentRequestForm)
        rfpAccountEndToEndId = requestForPaymentResponse.json().get('OrgnlEndToEndId')
        rfpAccountPSRResponse = self.client.post(f'/PaymentStatusOFI/{rfpAccountEndToEndId}')
        rfpAccountMsgId = ""
    
        # Request For Payment Rejection by Account
        requestForPaymentRejectRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18907',
            'Fr': 'ATOSIDJ1',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pain.014.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            'CdtrAgt': "ARTGIDJA",
            "OrgnlMsgId": rfpAccountMsgId,
            "OrgnlMsgNmId": "pain.013.001.08",
            "OrgnlPmtInfId": rfpAccountEndToEndId,
            "OrgnlEndToEndId": rfpAccountEndToEndId,
            "TxSts": "RJCT",
            "StsRsnInf": "U110",
        }
        requestForPaymentRejectResponse = self.client.post(
            '/RequestForPayRejectByAccountOFI', data=requestForPaymentRejectRequestForm)
        rfpAccountRejectEndToEndId = requestForPaymentRejectResponse.json().get('OrgnlEndToEndId')
        rfpAccountRejectPSRResponse = self.client.post(f'/PaymentStatusOFI/{rfpAccountRejectEndToEndId}')


        # Request For Payment by Proxy

        # Request For Payment Rejection by Proxy

        # Credit Transfer RFP
        rfpForCTResponse = self.client.post(
            '/RequestForPayByAccountOFI', data=requestForPaymentRequestForm)
        rfpAccountEndToEndId = rfpForCTResponse.json().get('OrgnlEndToEndId')
        rfpCTPSRResponse = self.client.post(f'/PaymentStatusOFI/{rfpAccountEndToEndId}')
        # TODO: Put RFP data in this variable to match original RFP for CT
        proxySecondaryType = ""
        proxySecondaryValue = ""
        proxyData = {
            'proxyAccountNumber': proxyAccountNumber,
            'proxyPrimaryType': proxyPrimaryType,
        }
        ctRFPRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18907',
            'Fr': 'ARTGIDJA',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
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
            'SplmtryData_InitgAcctId': "123456789",
            'SplmtryData_Dbtr_tp': '01',
            'SplmtryData_Dbtr_rsdntsts': '01',
            'SplmtryData_Dbtr_twnnm': '0300',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
            'SplmtryData_rltdEndToEndId': rfpAccountEndToEndId
        }
        ctRFPResponse = self.client.post(
            '/CreditTransferRFPOFI', data=ctRFPRequestForm)
        ctRFPEndToEndId = ctRFPResponse.json().get('OrgnlEndToEndId')
        rfpCTPSRResponse = self.client.post(f'/PaymentStatusOFI/{ctRFPEndToEndId}')
    

if __name__ == '__main__':
    unittest.main()
