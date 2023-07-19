import unittest
import logging
from flask import Flask
from flask.testing import FlaskClient
from app import app
import random
from datetime import datetime, timedelta
import logging
import time
import json
import unittest
import requests
# from unittest.mock import patch, Mock


class HTTPServerUnitTest(unittest.TestCase):
    # @patch('requests.Session.post')
    def setUp(self):
        app.config['TESTING'] = True

        logging.basicConfig(level=logging.INFO)
        # self.logger = app.logger
        self.client = app.test_client()

        self.logger = logging.getLogger("test_result")
        handler = logging.FileHandler('custom.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def tearDown(self):
        pass

    def test_regression(self):
        CONFIG = {
            'LOCAL_URL': 'http://127.0.0.1',
            'HOST_URL': '10.170.137.115',
            'HOST_PORT': '18947'
        }

        session = requests.Session()

        # # Account Enquiry
        # accountEnquiryRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18947',
        #     'Fr': 'BANKDMY7',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.008.001.08",
        #     'NbOfTxs': "1",
        #     'SttlmMtd': "CLRG",
        #     'CtgyPurp': "51001",
        #     'IntrBkSttlmAmt_value': 123.12,
        #     'IntrBkSttlmAmt_ccy': "IDR",
        #     'ChrgBr': "DEBT",
        #     'Dbtr_nm': "Naufal Afif",
        #     'DbtrAcct_value': '123456789',
        #     'DbtrAcct_type': 'SVGS',
        #     'DbtrAgt': 'BANKDMY7',
        #     'CdtrAgt': 'BANKDMY8',
        #     'Cdtr_nm': 'Bunyamin',
        #     'CdtrAcct_value': '987654321'
        # }
        # accountEnquiryStartTime = time.time()
        # accountEnquiryResponse = self.client.post(
        #     '/AccountEnquiryOFI', data=accountEnquiryRequestForm)
        # aeduration = "{:.2f}".format(time.time() - accountEnquiryStartTime)
        # aeJsonResponse = json.loads(accountEnquiryResponse.data)
        # aeEndToEndId = aeJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        # aeTxSts = aeJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        # aeStsRsnInf = aeJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+f" ({aeduration} seconds) {aeEndToEndId} {aeTxSts} {aeStsRsnInf}")

        # # Credit Transfer
        # time.sleep(10)
        # creditTransferRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18947',
        #     'Fr': 'BANKDMY7',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.008.001.08",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     'NbOfTxs': "1",
        #     'SttlmMtd': "CLRG",
        #     'CtgyPurp': "01001",
        #     'LclInstrm': "01",
        #     'IntrBkSttlmAmt_value': 123.12,
        #     'IntrBkSttlmAmt_ccy': "IDR",
        #     'ChrgBr': "DEBT",
        #     'Dbtr_nm': "Naufal Afif",
        #     'Dbtr_orgid': "PT. Abhimata Persada",
        #     'DbtrAcct_value': '123456789',
        #     'DbtrAcct_type': 'SVGS',
        #     'DbtrAgt': 'BANKDMY7',
        #     'CdtrAgt': 'BANKDMY8',
        #     'Cdtr_nm': 'Bunyamin',
        #     'Cdtr_orgid': 'PT. Telkom Indonesia',
        #     'CdtrAcct_value': '987654321',
        #     'CdtrAcct_type': 'SVGS',
        #     'RmtInf': "Testing purpose",
        #     'SplmtryData_InitgAcctId': "123456789",
        #     'SplmtryData_Dbtr_tp': '01',
        #     'SplmtryData_Dbtr_rsdntsts': '01',
        #     'SplmtryData_Dbtr_twnnm': '0300',
        #     'SplmtryData_Cdtr_tp': '01',
        #     'SplmtryData_Cdtr_rsdntsts': '01',
        #     'SplmtryData_Cdtr_twnnm': '0300',
        # }
        # creditTransferStartTime = time.time()
        # creditTransferResponse = self.client.post(
        #     '/CreditTransferOFI', data=creditTransferRequestForm)
        # ctduration = "{:.2f}".format(time.time() - creditTransferStartTime)
        # ctJsonResponse = json.loads(creditTransferResponse.data)
        # ctEndToEndId = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        # ctTxSts = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        # ctStsRsnInf = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+f" ({ctduration} seconds) {ctEndToEndId} {ctTxSts} {ctStsRsnInf}")

        # ctPSRRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18947',
        #     'Fr': 'BANKDMY7',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.028.001.04",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     "OrgnlEndToEndId": ctEndToEndId

        # }
        # if ctTxSts == "ACTC":
        #     time.sleep(15)
        #     ctPSRStartTime = time.time()
        #     ctPSRResponse = self.client.post(f'/PaymentStatusOFI', data=ctPSRRequestForm)
        #     ctPSRduration = "{:.2f}".format(time.time() - ctPSRStartTime)
        #     ctJsonResponse = json.loads(ctPSRResponse.data)
        #     ctPSREndToEndId = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        #     ctPSRTxSts = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        #     ctPSRStsRsnInf = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        #     self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+f" ({ctPSRduration} seconds) {ctPSREndToEndId} {ctPSRTxSts} {ctPSRStsRsnInf}")

        # # Credit Transfer Reversal
        # time.sleep(10)
        # creditTransferReversalRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18948',
        #     'Fr': 'BANKDMY8',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.008.001.08",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     'NbOfTxs': "1",
        #     'SttlmMtd': "CLRG",
        #     'CtgyPurp': "01101",
        #     'LclInstrm': "01",
        #     'IntrBkSttlmAmt_value': 123.12,
        #     'IntrBkSttlmAmt_ccy': "IDR",
        #     'ChrgBr': "DEBT",
        #     'Cdtr_nm': "Naufal Afif",
        #     'Cdtr_orgid': "PT. Abhimata Persada",
        #     'CdtrAcct_value': '123456789',
        #     'CdtrAcct_type': 'SVGS',
        #     'DbtrAgt': 'BANKDMY8',
        #     'CdtrAgt': 'BANKDMY7',
        #     'Dbtr_nm': 'Bunyamin',
        #     'Dbtr_orgid': 'PT. Telkom Indonesia',
        #     'DbtrAcct_value': '987654321',
        #     'DbtrAcct_type': 'SVGS',
        #     'RmtInf': "Testing purpose",
        #     'SplmtryData_InitgAcctId': "123456789",
        #     'SplmtryData_Dbtr_tp': '01',
        #     'SplmtryData_Dbtr_rsdntsts': '01',
        #     'SplmtryData_Dbtr_twnnm': '0300',
        #     'SplmtryData_Cdtr_tp': '01',
        #     'SplmtryData_Cdtr_rsdntsts': '01',
        #     'SplmtryData_Cdtr_twnnm': '0300',
        #     'SplmtryData_rltdEndToEndId': "20230718BANKDMY7010O0189145385"
        # }

        # creditTransferReversalStartTime = time.time()
        # creditTransferReversalResponse = self.client.post(
        #     '/CreditTransferReversalOFI', data=creditTransferReversalRequestForm)
        # ctReverseduration = "{:.2f}".format(
        #     time.time() - creditTransferReversalStartTime)
        # ctReverseJsonResponse = json.loads(creditTransferReversalResponse.data)
        # ctReverseEndToEndId = ctReverseJsonResponse["BusMsg"]["Document"][
        #     "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        # ctReverseTxSts = ctReverseJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        # ctReverseStsRsnInf = ctReverseJsonResponse["BusMsg"]["Document"][
        #     "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
        #                  f" ({ctReverseduration} seconds) {ctReverseEndToEndId} {ctReverseTxSts} {ctReverseStsRsnInf}")

        # ctReversePSRRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18948',
        #     'Fr': 'BANKDMY8',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.028.001.04",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     "OrgnlEndToEndId": ctReverseEndToEndId

        # }
        # if ctReverseTxSts == "ACTC":
        #     time.sleep(15)
        #     ctReversePSRStartTime = time.time()
        #     ctReversePSRResponse = self.client.post(
        #         f'/PaymentStatusOFI', data=ctReversePSRRequestForm)
        #     ctReversePSRduration = "{:.2f}".format(
        #         time.time() - ctReversePSRStartTime)
        #     ctReverseJsonResponse = json.loads(ctReversePSRResponse.data)
        #     ctReversePSREndToEndId = ctReverseJsonResponse["BusMsg"]["Document"][
        #         "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        #     ctReversePSRTxSts = ctReverseJsonResponse["BusMsg"][
        #         "Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        #     ctReversePSRStsRsnInf = ctReverseJsonResponse["BusMsg"]["Document"][
        #         "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        #     self.logger.info(datetime.now().strftime(
        #         "%Y-%m-%d %H:%M:%S")+f" ({ctReversePSREndToEndId} seconds) {ctReversePSRTxSts} {ctReversePSRStsRsnInf} {ctReversePSRStsRsnInf}")

        # # Credit Transfer Proxy
        # time.sleep(10)
        # creditTransferRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18947',
        #     'Fr': 'BANKDMY7',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.008.001.08",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     'NbOfTxs': "1",
        #     'SttlmMtd': "CLRG",
        #     'CtgyPurp': "01001",
        #     'LclInstrm': "01",
        #     'IntrBkSttlmAmt_value': 123.12,
        #     'IntrBkSttlmAmt_ccy': "IDR",
        #     'ChrgBr': "DEBT",
        #     'Dbtr_nm': "Naufal Afif",
        #     'Dbtr_orgid': "PT. Abhimata Persada",
        #     'DbtrAcct_value': '123456789',
        #     'DbtrAcct_type': 'SVGS',
        #     'DbtrAgt': 'BANKDMY7',
        #     'CdtrAgt': 'BANKDMY8',
        #     'Cdtr_nm': 'Bunyamin',
        #     'Cdtr_orgid': 'PT. Telkom Indonesia',
        #     'CdtrAcct_value': '987654321',
        #     'CdtrAcct_type': 'SVGS',
        #     'CdtrAcct_Prxy_tp': '02',
        #     'CdtrAcct_Prxy_id': '',
        #     'RmtInf': "Testing purpose",
        #     'SplmtryData_InitgAcctId': "123456789",
        #     'SplmtryData_Dbtr_tp': '01',
        #     'SplmtryData_Dbtr_rsdntsts': '01',
        #     'SplmtryData_Dbtr_twnnm': '0300',
        #     'SplmtryData_Cdtr_tp': '01',
        #     'SplmtryData_Cdtr_rsdntsts': '01',
        #     'SplmtryData_Cdtr_twnnm': '0300',
        # }
        # creditTransferStartTime = time.time()
        # creditTransferResponse = self.client.post(
        #     '/CreditTransferOFI', data=creditTransferRequestForm)
        # ctduration = "{:.2f}".format(time.time() - creditTransferStartTime)
        # ctJsonResponse = json.loads(creditTransferResponse.data)
        # ctEndToEndId = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        # ctTxSts = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        # ctStsRsnInf = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+f" ({ctduration} seconds) {ctEndToEndId} {ctTxSts} {ctStsRsnInf}")

        # ctPSRRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18947',
        #     'Fr': 'BANKDMY7',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.028.001.04",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     "OrgnlEndToEndId": ctEndToEndId

        # }
        # if ctTxSts == "ACTC":
        #     time.sleep(15)
        #     ctPSRStartTime = time.time()
        #     ctPSRResponse = self.client.post(f'/PaymentStatusOFI', data=ctPSRRequestForm)
        #     ctPSRduration = "{:.2f}".format(time.time() - ctPSRStartTime)
        #     ctJsonResponse = json.loads(ctPSRResponse.data)
        #     ctPSREndToEndId = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        #     ctPSRTxSts = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        #     ctPSRStsRsnInf = ctJsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        #     self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+f" ({ctPSRduration} seconds) {ctPSREndToEndId} {ctPSRTxSts} {ctPSRStsRsnInf}")

        # # Proxy Register
        # time.sleep(10)
        # uniqueId = random.randint(10000, 99999)

        # proxyRegisterRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18948',
        #     'Fr': 'BANKDMY8',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "prxy.001.001.01",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     'MsgSndr_agt': "BANKDMY8",
        #     'MsgSndr_acct': f'312{uniqueId}',
        #     'RegnTp': 'NEWR',
        #     'Prxy_tp': '02',
        #     'Prxy_val': f'Proxy Value {uniqueId}',
        #     'DsplNm': f'Proxy Display Name {uniqueId}',
        #     'PrxyRegn_Agt_nm': 'PT. Abhimata Persada',
        #     'PrxyRegn_Agt_id': 'BANKDMY8',
        #     'PrxyRegn_acct': f'312{uniqueId}',
        #     'PrxyRegn_tp': 'CACC',
        #     'PrxyRegn_nm': f'Proxy Name {uniqueId}',
        #     'ScndId_tp': '01',
        #     'ScndId_val': f'6812345{uniqueId}',
        #     'RegnSts': 'ACTV',
        #     'SplmtryData_Cstmr_tp': '01',
        #     'SplmtryData_Cstmr_id': f'10203040{uniqueId}',
        #     'SplmtryData_Cstmr_rsdntsts': '01',
        #     'SplmtryData_Cstmr_twnnm': '0300',
        # }
        # proxyRegisterStartTime = time.time()
        # proxyRegisterResponse = self.client.post(
        #     '/ProxyRegistrationOFI', data=proxyRegisterRequestForm)
        # proxyRegisterduration = "{:.2f}".format(
        #     time.time() - proxyRegisterStartTime)
        # proxyRegisterJsonResponse = json.loads(proxyRegisterResponse.data)
        # proxyRegisterMsgId = proxyRegisterJsonResponse["BusMsg"][
        #     "Document"]["PrxyRegnRspn"]["OrgnlGrpInf"]["OrgnlMsgId"]
        # proxyRegisterTxSts = proxyRegisterJsonResponse["BusMsg"][
        #     "Document"]["PrxyRegnRspn"]["RegnRspn"]["PrxRspnSts"]
        # proxyRegisterStsRsnInf = proxyRegisterJsonResponse["BusMsg"][
        #     "Document"]["PrxyRegnRspn"]["RegnRspn"]["StsRsnInf"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
        #                  f" ({proxyRegisterduration} seconds) {proxyRegisterMsgId} {proxyRegisterTxSts} {proxyRegisterStsRsnInf}")

        # # Proxy Register Lookup
        # time.sleep(10)
        # proxyLookupRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18948',
        #     'Fr': 'BANKDMY8',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "prxy.003.001.01",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     'MsgSndr_agt': "BANKDMY8",
        #     'MsgSndr_acct': proxyRegisterRequestForm.get('MsgSndr_acct'),
        #     'PrxyOnly_LkUpTp': "PXRS",
        #     'PrxyRtrvl_tp': proxyRegisterRequestForm.get('Prxy_tp'),
        #     'PrxyRtrvl_value': proxyRegisterRequestForm.get('Prxy_val'),
        # }
        # proxyLookupStartTime = time.time()
        # proxyLookupResponse = self.client.post(
        #     '/ProxyLookupOFI', data=proxyLookupRequestForm)
        # proxyLookupduration = "{:.2f}".format(
        #     time.time() - proxyLookupStartTime)
        # proxyLookupJsonResponse = json.loads(proxyLookupResponse.data)
        # # self.logger.info(proxyLookupResponse.data)
        # proxyLookupMsgId = proxyLookupJsonResponse["BusMsg"][
        #     "Document"]["PrxyLookUpRspn"]["LkUpRspn"]["OrgnlId"]
        # proxyLookupTxSts = proxyLookupJsonResponse["BusMsg"][
        #     "Document"]["PrxyLookUpRspn"]["LkUpRspn"]["RegnRspn"]["PrxRspnSts"]
        # proxyLookupStsRsnInf = proxyLookupJsonResponse["BusMsg"][
        #     "Document"]["PrxyLookUpRspn"]["LkUpRspn"]["RegnRspn"]["StsRsnInf"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
        #                  f" ({proxyLookupduration} seconds) {proxyLookupMsgId} {proxyLookupTxSts} {proxyLookupStsRsnInf}")

        # # Proxy Register Enquiry
        # time.sleep(10)
        # proxyEnquiryRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18948',
        #     'Fr': 'BANKDMY8',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "prxy.005.001.01",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     'MsgSndr_agt': "BANKDMY8",
        #     'MsgSndr_acct': proxyRegisterRequestForm.get('MsgSndr_acct'),
        #     'ScndId_tp': proxyRegisterRequestForm.get('ScndId_tp'),
        #     'ScndId_val': proxyRegisterRequestForm.get('ScndId_val')
        # }
        # proxyEnquiryStartTime = time.time()
        # proxyEnquiryResponse = self.client.post(
        #     '/ProxyEnquiryOFI', data=proxyEnquiryRequestForm)
        # proxyEnquiryduration = "{:.2f}".format(
        #     time.time() - proxyEnquiryStartTime)
        # proxyEnquiryJsonResponse = json.loads(proxyEnquiryResponse.data)
        # # self.logger.info(proxyEnquiryResponse.data)
        # proxyEnquiryMsgId = proxyEnquiryJsonResponse["BusMsg"]["Document"]["PrxyNqryRspn"]["OrgnlGrpInf"]["OrgnlMsgId"]
        # proxyEnquiryTxSts = proxyEnquiryJsonResponse["BusMsg"]["Document"]["PrxyNqryRspn"]["NqryRspn"]["PrxRspnSts"]
        # proxyEnquiryStsRsnInf = proxyEnquiryJsonResponse["BusMsg"]["Document"]["PrxyNqryRspn"]["NqryRspn"]["StsRsnInf"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
        #                  f" ({proxyEnquiryduration} seconds) {proxyEnquiryMsgId} {proxyEnquiryTxSts} {proxyEnquiryStsRsnInf}")

        # # Proxy Porting
        # proxyPortingResponse = self.client.post(
        #     '/ProxyPortingOFI', data=proxyData)

        # # Proxy Porting Lookup
        # # Proxy Porting Enquiry

        # # Proxy Deactivate

        # # Proxy Deactivate Lookup
        # # Proxy Deactivate Enquiry

        # Request For Payment by Account
        timestamp_now = datetime.now()
        timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
        timestamp_future = timestamp_now + timedelta(days=14)

        timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')
        delta_str = str(timedelta(days=14))

        rfpAccountRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pain.013.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'NbOfTxs': "1",
            'InitgPty_nm': "Naufal Afif",
            'InitgPty_pstladr': 'ID',
            'PmtMtd': "TRF",
            'CtgyPurp': '85301',
            'ReqdExctnDt': timestamp_formatted,
            'XpryDt': timestamp_future_formatted,
            'DbtrAcct_value': '123456789',
            'DbtrAgt': 'BANKDMY8',
            'InstdAmt_value': 853.01,
            'InstdAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'CdtrAgt': 'BANKDMY7',
            'Cdtr_orgid': 'PT. Telkom Indonesia',
            'CdtrAcct_value': '987654321',
            'CdtrAcct_type': 'SVGS',
            'CdtrAcct_nm': 'Raline',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
        }
        rfpAccountStartTime = time.time()
        rfpAccountResponse = self.client.post(
            '/RequestForPayByAccountOFI', data=rfpAccountRequestForm)
        rfpAccountduration = "{:.2f}".format(
            time.time() - rfpAccountStartTime)
        rfpAccountJsonResponse = json.loads(rfpAccountResponse.data)
        rfpAccountMsgId = rfpAccountJsonResponse["BusMsg"]["Document"][
            "FIToFIPmtStsRpt"]["OrgnlGrpInfAndSts"][0]["OrgnlMsgId"]
        rfpAccountEndToEndId = rfpAccountJsonResponse["BusMsg"]["Document"][
            "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        rfpAccountTxSts = rfpAccountJsonResponse["BusMsg"][
            "Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        rfpAccountStsRsnInf = rfpAccountJsonResponse["BusMsg"]["Document"][
            "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                         f" ({rfpAccountduration} seconds) {rfpAccountEndToEndId} {rfpAccountTxSts} {rfpAccountStsRsnInf}")
        self.logger.info(rfpAccountResponse.data)

        # # Request For Payment Rejection by Account
        # time.sleep(15)
        # rfpAccountRejectRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18948',
        #     'Fr': 'BANKDMY8',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pain.014.001.08",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": False,
        #     'CdtrAgt': "BANKDMY7",
        #     "OrgnlMsgId": rfpAccountMsgId,
        #     "OrgnlMsgNmId": "pain.013.001.08",
        #     "OrgnlPmtInfId": rfpAccountMsgId,
        #     "OrgnlEndToEndId": rfpAccountEndToEndId,
        #     "TxSts": "RJCT",
        #     "StsRsnInf": "U110",
        # }
        # rfpAccountRejectStartTime = time.time()
        # rfpAccountRejectResponse = self.client.post(
        #     '/RequestForPayRejectByAccountOFI', data=rfpAccountRejectRequestForm)
        # rfpAccountRejectduration = "{:.2f}".format(
        #     time.time() - rfpAccountRejectStartTime)
        # rfpAccountRejectJsonResponse = json.loads(rfpAccountRejectResponse.data)
        # rfpAccountRejectEndToEndId = rfpAccountRejectJsonResponse["BusMsg"]["Document"][
        #     "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        # rfpAccountRejectTxSts = rfpAccountRejectJsonResponse["BusMsg"][
        #     "Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        # rfpAccountRejectStsRsnInf = rfpAccountRejectJsonResponse["BusMsg"]["Document"][
        #     "FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        # self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
        #                  f" ({rfpAccountRejectduration} seconds) {rfpAccountRejectEndToEndId} {rfpAccountRejectTxSts} {rfpAccountRejectStsRsnInf}")
        # self.logger.info(rfpAccountRejectResponse.data)

        # # Request For Payment by Proxy

        # # Request For Payment Rejection by Proxy

        # # Credit Transfer RFP
        # rfpForCTResponse = self.client.post(
        #     '/RequestForPayByAccountOFI', data=requestForPaymentRequestForm)
        # rfpAccountEndToEndId = rfpForCTResponse.json().get('OrgnlEndToEndId')
        # rfpCTPSRResponse = self.client.post(f'/PaymentStatusOFI/{rfpAccountEndToEndId}')
        # # TODO: Put RFP data in this variable to match original RFP for CT
        # proxySecondaryType = ""
        # proxySecondaryValue = ""
        # proxyData = {
        #     'proxyAccountNumber': proxyAccountNumber,
        #     'proxyPrimaryType': proxyPrimaryType,
        # }
        # ctRFPRequestForm = {
        #     'Host_url': '10.170.137.115',
        #     'Host_port': '18907',
        #     'Fr': 'ARTGIDJA',
        #     'To': 'FASTIDJA',
        #     'MsgDefIdr': "pacs.008.001.08",
        #     "BizSvc": "BI",
        #     "CpyDplct": "CODU",
        #     "PssblDplct": "false",
        #     'NbOfTxs': "1",
        #     'SttlmMtd': "CLRG",
        #     'CtgyPurp': "51001",
        #     'LclInstrm': "01",
        #     'IntrBkSttlmAmt_value': 123.12,
        #     'IntrBkSttlmAmt_ccy': "IDR",
        #     'ChrgBr': "DEBT",
        #     'Dbtr_nm': "Naufal Afif",
        #     'Dbtr_orgid': "PT. Abhimata Persada",
        #     'DbtrAcct_value': '123456789',
        #     'DbtrAcct_type': 'SVGS',
        #     'DbtrAgt': 'ARTGIDJA',
        #     'CdtrAgt': 'ATOSIDJ1',
        #     'Cdtr_nm': 'Bunyamin',
        #     'Cdtr_orgid': 'PT. Telkom Indonesia',
        #     'CdtrAcct_value': '987654321',
        #     'CdtrAcct_type': 'SVGS',
        #     'RmtInf': "Testing purpose",
        #     'SplmtryData_InitgAcctId': "123456789",
        #     'SplmtryData_Dbtr_tp': '01',
        #     'SplmtryData_Dbtr_rsdntsts': '01',
        #     'SplmtryData_Dbtr_twnnm': '0300',
        #     'SplmtryData_Cdtr_tp': '01',
        #     'SplmtryData_Cdtr_rsdntsts': '01',
        #     'SplmtryData_Cdtr_twnnm': '0300',
        #     'SplmtryData_rltdEndToEndId': rfpAccountEndToEndId
        # }
        # ctRFPResponse = self.client.post(
        #     '/CreditTransferRFPOFI', data=ctRFPRequestForm)
        # ctRFPEndToEndId = ctRFPResponse.json().get('OrgnlEndToEndId')
        # rfpCTPSRResponse = self.client.post(f'/PaymentStatusOFI/{ctRFPEndToEndId}')


if __name__ == '__main__':
    unittest.main()
