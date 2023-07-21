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
    def setUp(self):
        app.config['TESTING'] = True
        logging.basicConfig(level=logging.INFO)
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
        # Account Enquiry
        # self.accountEnquiryTestHandler()

        # # Credit Transfer (pause for 10 seconds)
        # time.sleep(10)
        # ct = self.creditTransferTestHandler()

        # # Credit Transfer Reversal (pause for 40 seconds)
        # time.sleep(40)
        # if (ct.get('txSts') == "ACTC"):
        #     self.creditTransferReversalTestHandler(ct.get('endToEndId'))

        # # Credit Transfer Proxy
        # time.sleep(10)
        # self.creditTransferProxyHandler()

        # # Proxy Registration
        # time.sleep(10)
        # proxy = self.proxyRegisterTestHandler()

        # # Proxy Resolution
        # time.sleep(10)
        # self.proxyLookupTestHandler(proxy)

        # # Proxy Enquiry
        # time.sleep(10)
        # self.proxyEnquiryTestHandler(proxy)

        # Proxy Porting

        # Proxy Deactivate

        # # Request for Payment by Account
        # time.sleep(10)
        # rfpAccountRequest, rfpAccountResult = self.requestForPaymentAccountTestHandler()

        # # Request for Payment Rejection by Account
        # time.sleep(15)
        # self.requestForPaymentAccountRejectTestHandler(rfpAccountResult)

        # # Request for Payment by Proxy
        # time.sleep(10)
        # proxy = self.proxyRegisterTestHandler()
        # time.sleep(10)
        # rfpProxyRequest, rfpProxyResult = self.requestForPaymentProxyTestHandler(proxy)

        # # Request for Payment Rejection by Proxy
        # time.sleep(10)
        # self.requestForPaymentProxyRejectTestHandler(rfpProxyResult)

        # # Credit Transfer RFP
        # time.sleep(10)
        # rfpAccountRequest, rfpAccountResult = self.requestForPaymentAccountTestHandler()
        # time.sleep(10)
        # self.creditTransferRFPTestHandler(rfpAccountRequest, rfpAccountResult)

        # E-Mandate Registration by Crediting
        # time.sleep(10)
        emandateRegistrationCrediting = self.eMandateRegistrationByCreditingTest()


        # E-Mandate Registration by Debiting
         
        # E-Mandate Approval by Crediting
         
        # E-Mandate Approval by Debiting
         
        # E-Mandate Amendment by Crediting
         
        # E-Mandate Amendment by Debiting
         
        # E-Mandate Amendment Approval by Crediting
         
        # E-Mandate Amendment Approval by Debiting
         
        # E-Mandate Termination by Crediting
         
        # E-Mandate Termintation by Debiting
         
        # E-Mandate Enquiry by EndToEndId
         
        # E-Mandate Enquiry by MandateID
         
        # Direct Debit
         
        # PSR Direct Debit


        pass

    def requestHandler(self, form):
        startTime = time.time()
        response = self.client.post(form.get('Payment_url'), data=form)
        duration = "{:.2f}".format(time.time() - startTime)
        # self.logger.info(response.data)
        jsonResponse = json.loads(response.data)
        try:
            msgId = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["OrgnlGrpInfAndSts"][0]["OrgnlMsgId"]
            endToEndId = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
            txSts = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
            stsRsnInf = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
            self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                             f" ({duration} seconds) {form.get('Payment_url')} {endToEndId} {txSts} {stsRsnInf}")
            resultForm = {
                'msgId': msgId,
                'endToEndId': endToEndId,
                'txSts': txSts,
                'stsRsnInf': stsRsnInf
            }
            return resultForm
        except KeyError:
            self.logger.info(response.data)

        # return resultForm

    def accountEnquiryTestHandler(self):
        accountEnquiryRequestForm = {
            'Payment_url': '/AccountEnquiryOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
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
            'DbtrAgt': 'BANKDMY7',
            'CdtrAgt': 'BANKDMY8',
            'Cdtr_nm': 'Bunyamin',
            'CdtrAcct_value': '987654321'
        }
        return self.requestHandler(accountEnquiryRequestForm)

    def creditTransferTestHandler(self):
        creditTransferRequestForm = {
            'Payment_url': '/CreditTransferOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'NbOfTxs': "1",
            'SttlmMtd': "CLRG",
            'CtgyPurp': "01001",
            'LclInstrm': "01",
            'IntrBkSttlmAmt_value': 123.12,
            'IntrBkSttlmAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'Dbtr_nm': "Naufal Afif",
            'Dbtr_orgid': "PT. Abhimata Persada",
            'DbtrAcct_value': '123456789',
            'DbtrAcct_type': 'SVGS',
            'DbtrAgt': 'BANKDMY7',
            'CdtrAgt': 'BANKDMY8',
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
        result = self.requestHandler(creditTransferRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18947',
                'Fr': 'BANKDMY7',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": result.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)
            return result

    def creditTransferReversalTestHandler(self, rltdEndToEndId=None):
        creditTransferReversalRequestForm = {
            'Payment_url': '/CreditTransferReversalOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'NbOfTxs': "1",
            'SttlmMtd': "CLRG",
            'CtgyPurp': "01101",
            'LclInstrm': "01",
            'IntrBkSttlmAmt_value': 123.12,
            'IntrBkSttlmAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'Cdtr_nm': "Naufal Afif",
            'Cdtr_orgid': "PT. Abhimata Persada",
            'CdtrAcct_value': '123456789',
            'CdtrAcct_type': 'SVGS',
            'DbtrAgt': 'BANKDMY8',
            'CdtrAgt': 'BANKDMY7',
            'Dbtr_nm': 'Bunyamin',
            'Dbtr_orgid': 'PT. Telkom Indonesia',
            'DbtrAcct_value': '987654321',
            'DbtrAcct_type': 'SVGS',
            'RmtInf': "Testing purpose",
            'SplmtryData_InitgAcctId': "123456789",
            'SplmtryData_Dbtr_tp': '01',
            'SplmtryData_Dbtr_rsdntsts': '01',
            'SplmtryData_Dbtr_twnnm': '0300',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
            'SplmtryData_rltdEndToEndId': rltdEndToEndId
        }
        result = self.requestHandler(creditTransferReversalRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18948',
                'Fr': 'BANKDMY8',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": result.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)

    def creditTransferProxyHandler(self):
        creditTransferRequestForm = {
            'Payment_url': '/CreditTransferOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'NbOfTxs': "1",
            'SttlmMtd': "CLRG",
            'CtgyPurp': "01001",
            'LclInstrm': "01",
            'IntrBkSttlmAmt_value': 123.12,
            'IntrBkSttlmAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'Dbtr_nm': "Naufal Afif",
            'Dbtr_orgid': "PT. Abhimata Persada",
            'DbtrAcct_value': '123456789',
            'DbtrAcct_type': 'SVGS',
            'DbtrAgt': 'BANKDMY7',
            'CdtrAgt': 'BANKDMY8',
            'Cdtr_nm': 'Bunyamin',
            'Cdtr_orgid': 'PT. Telkom Indonesia',
            'CdtrAcct_value': '987654321',
            'CdtrAcct_type': 'SVGS',
            'CdtrAcct_Prxy_tp': '02',
            'CdtrAcct_Prxy_id': '',
            'RmtInf': "Testing purpose",
            'SplmtryData_InitgAcctId': "123456789",
            'SplmtryData_Dbtr_tp': '01',
            'SplmtryData_Dbtr_rsdntsts': '01',
            'SplmtryData_Dbtr_twnnm': '0300',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
        }
        result = self.requestHandler(creditTransferRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18947',
                'Fr': 'BANKDMY7',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": result.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)

    def proxyRegisterTestHandler(self):
        uniqueId = random.randint(10000, 99999)
        proxyRegisterRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'MsgDefIdr': "prxy.001.001.01",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'MsgSndr_agt': "BANKDMY8",
            'MsgSndr_acct': f'312{uniqueId}',
            'RegnTp': 'NEWR',
            'Prxy_tp': '02',
            'Prxy_val': f'Proxy Value {uniqueId}',
            'DsplNm': f'Proxy Display Name {uniqueId}',
            'PrxyRegn_Agt_nm': 'PT. Abhimata Persada',
            'PrxyRegn_Agt_id': 'BANKDMY8',
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
        startTime = time.time()
        response = self.client.post(
            '/ProxyRegistrationOFI', data=proxyRegisterRequestForm)
        duration = "{:.2f}".format(time.time() - startTime)
        jsonResponse = json.loads(response.data)
        msgId = jsonResponse["BusMsg"]["Document"]["PrxyRegnRspn"]["OrgnlGrpInf"]["OrgnlMsgId"]
        txSts = jsonResponse["BusMsg"]["Document"]["PrxyRegnRspn"]["RegnRspn"]["PrxRspnSts"]
        stsRsnInf = jsonResponse["BusMsg"]["Document"]["PrxyRegnRspn"]["RegnRspn"]["StsRsnInf"]["Prtry"]
        self.logger.info(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + f" ({duration} seconds) {msgId} {txSts} {stsRsnInf}")
        return proxyRegisterRequestForm

    def proxyLookupTestHandler(self, form):
        proxyLookupRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'MsgDefIdr': "prxy.003.001.01",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'MsgSndr_agt': "BANKDMY8",
            'MsgSndr_acct': form.get('MsgSndr_acct'),
            'PrxyOnly_LkUpTp': "PXRS",
            'PrxyRtrvl_tp': form.get('Prxy_tp'),
            'PrxyRtrvl_value': form.get('Prxy_val'),
        }
        startTime = time.time()
        response = self.client.post(
            '/OFI', data=proxyLookupRequestForm)
        duration = "{:.2f}".format(time.time() - startTime)
        jsonResponse = json.loads(response.data)
        msgId = jsonResponse["BusMsg"]["Document"]["PrxyLookUpRspn"]["LkUpRspn"]["OrgnlId"]
        txSts = jsonResponse["BusMsg"]["Document"]["PrxyLookUpRspn"]["LkUpRspn"]["RegnRspn"]["PrxRspnSts"]
        stsRsnInf = jsonResponse["BusMsg"]["Document"]["PrxyLookUpRspn"]["LkUpRspn"]["RegnRspn"]["StsRsnInf"]["Prtry"]
        self.logger.info(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + f" ({duration} seconds) {msgId} {txSts} {stsRsnInf}")

    def proxyEnquiryTestHandler(self, form):
        time.sleep(10)
        proxyEnquiryRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'MsgDefIdr': "prxy.005.001.01",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'MsgSndr_agt': "BANKDMY8",
            'MsgSndr_acct': form.get('MsgSndr_acct'),
            'ScndId_tp': form.get('ScndId_tp'),
            'ScndId_val': form.get('ScndId_val')
        }
        startTime = time.time()
        response = self.client.post(
            '/ProxyEnquiryOFI', data=proxyEnquiryRequestForm)
        duration = "{:.2f}".format(time.time() - startTime)
        jsonResponse = json.loads(response.data)
        msgId = jsonResponse["BusMsg"]["Document"]["PrxyNqryRspn"]["OrgnlGrpInf"]["OrgnlMsgId"]
        txSts = jsonResponse["BusMsg"]["Document"]["PrxyNqryRspn"]["NqryRspn"]["PrxRspnSts"]
        stsRsnInf = jsonResponse["BusMsg"]["Document"]["PrxyNqryRspn"]["NqryRspn"]["StsRsnInf"]["Prtry"]
        self.logger.info(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + f" ({duration} seconds) {msgId} {txSts} {stsRsnInf}")

    def proxyPortingTestHandler(self):
        # TODO: Not Developed Yet
        pass

    def proxyDeactivateTestHandler(self):
        # TODO: Not Developed Yet
        pass

    def paymentStatusRequestTestHandler(self, paymentData):
        paymentData['Payment_url'] = '/PaymentStatusOFI'
        self.requestHandler(paymentData)

    def requestForPaymentAccountTestHandler(self):
        # TODO: Change the date with default value
        timestamp_now = datetime.now()
        timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
        timestamp_future = timestamp_now + timedelta(days=14)
        timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')

        rfpAccountRequestForm = {
            'Payment_url': '/RequestForPayByAccountOFI',
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
        result = self.requestHandler(rfpAccountRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18947',
                'Fr': 'BANKDMY7',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": result.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)
            return rfpAccountRequestForm, result

    def requestForPaymentAccountRejectTestHandler(self, form):
        rfpAccountRejectRequestForm = {
            'Payment_url': '/RequestForPayRejectByAccountOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pain.014.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'CdtrAgt': "BANKDMY7",
            "OrgnlMsgId": form.get('msgId'),
            "OrgnlMsgNmId": "pain.013.001.08",
            "OrgnlPmtInfId": form.get('msgId'),
            "OrgnlEndToEndId": form.get('endToEndId'),
            "TxSts": "RJCT",
            "StsRsnInf": "U110",
        }
        result = self.requestHandler(rfpAccountRejectRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18948',
                'Fr': 'BANKDMY8',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": form.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)
            return result

    def requestForPaymentProxyTestHandler(self, proxyForm):
        timestamp_now = datetime.now()
        timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
        timestamp_future = timestamp_now + timedelta(days=14)
        timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')

        rfpProxyRequestForm = {
            'Payment_url': '/RequestForPayByProxyOFI',
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
            'CtgyPurp': '85101',
            'ReqdExctnDt': timestamp_formatted,
            'XpryDt': timestamp_future_formatted,
            'DbtrAcct_value': proxyForm.get('MsgSndr_acct'),
            'DbtrAcct_Prxy_tp': proxyForm.get('Prxy_tp'),
            'DbtrAcct_Prxy_id': proxyForm.get('Prxy_val'),
            'DbtrAgt': 'BANKDMY8',
            'InstdAmt_value': 851.01,
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
        result = self.requestHandler(rfpProxyRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18947',
                'Fr': 'BANKDMY7',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": result.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)
            return rfpProxyRequestForm, result

    def requestForPaymentProxyRejectTestHandler(self, form):
        rfpProxyRejectRequestForm = {
            'Payment_url': '/RequestForPayRejectByProxyOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pain.014.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": False,
            'CdtrAgt': "BANKDMY7",
            "OrgnlMsgId": form.get('msgId'),
            "OrgnlMsgNmId": "pain.013.001.08",
            "OrgnlPmtInfId": form.get('msgId'),
            "OrgnlEndToEndId": form.get('endToEndId'),
            "TxSts": "RJCT",
            "StsRsnInf": "U110",
        }
        result = self.requestHandler(rfpProxyRejectRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18948',
                'Fr': 'BANKDMY8',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": form.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)
            return result

    def creditTransferRFPTestHandler(self, rfpForm, rfpResult):
        ctRFPRequestForm = {
            'Payment_url': '/CreditTransferRFPOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            'NbOfTxs': "1",
            'SttlmMtd': "CLRG",
            'CtgyPurp': "31001",
            'LclInstrm': "01",
            'IntrBkSttlmAmt_value': rfpForm.get('InstdAmt_value'),
            'IntrBkSttlmAmt_ccy': "IDR",
            'ChrgBr': "DEBT",
            'Dbtr_nm': rfpForm.get('InitgPty_nm'),
            'Dbtr_orgid': "PT. Abhimata Persada",
            'DbtrAcct_value': rfpForm.get('DbtrAcct_value'),
            'DbtrAcct_type': rfpForm.get('DbtrAcct_type'),
            'DbtrAgt': rfpForm.get('DbtrAgt'),
            'CdtrAgt': rfpForm.get('CdtrAgt'),
            'Cdtr_nm': rfpForm.get('InitgPty_nm'),
            'Cdtr_orgid': 'PT. Bank Dummy 7',
            'CdtrAcct_value': rfpForm.get('CdtrAcct_value'),
            'CdtrAcct_type': rfpForm.get('CdtrAcct_type'),
            'RmtInf': "Testing purpose",
            'SplmtryData_InitgAcctId': rfpForm.get('DbtrAcct_value'),
            'SplmtryData_Dbtr_tp': '01',
            'SplmtryData_Dbtr_rsdntsts': '01',
            'SplmtryData_Dbtr_twnnm': '0300',
            'SplmtryData_Cdtr_tp': rfpForm.get('SplmtryData_Cdtr_tp'),
            'SplmtryData_Cdtr_rsdntsts': rfpForm.get('SplmtryData_Cdtr_rsdntsts'),
            'SplmtryData_Cdtr_twnnm': rfpForm.get('SplmtryData_Cdtr_twnnm'),
            'SplmtryData_rltdEndToEndId': rfpResult.get('endToEndId')
        }
        result = self.requestHandler(ctRFPRequestForm)

        if result.get('txSts') == "ACTC":
            time.sleep(15)
            psrRequestForm = {
                'Host_url': '10.170.137.115',
                'Host_port': '18948',
                'Fr': 'BANKDMY8',
                'To': 'FASTIDJA',
                'MsgDefIdr': "pacs.028.001.04",
                "CpyDplct": "CODU",
                "PssblDplct": False,
                "OrgnlEndToEndId": result.get('endToEndId')
            }
            self.paymentStatusRequestTestHandler(psrRequestForm)

    def eMandateEnquiryByMandateID(self):
        pass

    def eMandateRegistrationByCreditingTest(self):
        mandateRegistRequestForm = {
            'Payment_url': '/MandateRegistByCreditOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
            'To': 'FASTIDJA',
            'MsgDefIdr': "pacs.008.001.08",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            'CtgyPurp': "01",
            'LclInstrm': "FixedAmt",
            'SeqTp' : "RCUR",
            'Frqcy_tp': "MNTH",
            'Frqcy_cntPerPrd': "12",
            'FrDt': "", # Fill if need a custom date
            'ToDt': "", # Fill if need a custom date
            'FrstColltnDt': "", # Fill if need a custom date
            'FnlColltnDt': "", # Fill if need a custom date
            'TrckgInd': True,
            'FrstColltnAmt_ccy': "IDR",
            'FrstColltnAmt_value': "13001.01",
            'ColltnAmt_ccy': "IDR",
            'ColltnAmt_value': "13001.01",
            'MaxAmt_ccy': "IDR",
            'MaxAmt_value': "13001.01",
            'Rsn':  "Credit Pay Insurance",
            'Cdtr_nm': "PT. Bank Dummy 7",
            'Cdtr_orgid': "BANKDMY7_MERCH_100",
            'CdtrAcct_id': "12345677789",
            'CdtrAcct_tp': "CACC",
            'CdtrAcct_nm': "Dummy Account 7",
            'CdtrAgt': "BANKDMY7",
            'Dbtr_nm': "PT. Pypoh",
            'Dbtr_prvtid': "3171234567890",
            'DbtrAcct_id': "12347856999",
            'DbtrAcct_tp': "SVGS",
            'DbtrAcct_nm': "Naufal Afif",
            'DbtrAgt': "BANKDMY8",
            'CdtrRef': "BANKDMY7_MERCH_100"

        }
        result = self.requestHandler(mandateRegistRequestForm)

        # if result.get('txSts') == "ACTC":
        #     time.sleep(15)
        #     mandateEnquiryRequestForm = {
        #         'Host_url': '10.170.137.115',
        #         'Host_port': '18948',
        #         'Fr': 'BANKDMY8',
        #         'To': 'FASTIDJA',
        #         'MsgDefIdr': "pacs.028.001.04",
        #         "CpyDplct": "CODU",
        #         "PssblDplct": False,
        #         "OrgnlEndToEndId": result.get('endToEndId')
        #     }
        #     self.paymentStatusRequestTestHandler(psrRequestForm)



if __name__ == '__main__':
    unittest.main()
