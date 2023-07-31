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
import handler.general as generalHandler
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
        # # Account Enquiry
        # self.accountEnquiryTestHandler()

        # # # Credit Transfer (pause for 10 seconds)
        # time.sleep(10)
        # ct = self.creditTransferTestHandler()

        # # # Credit Transfer Reversal (pause for 40 seconds)
        # time.sleep(40)
        # if (ct.get('txSts') == "ACTC"):
        #     self.creditTransferReversalTestHandler(ct.get('endToEndId'))

        # # # Credit Transfer Proxy
        # # time.sleep(10)
        # # self.creditTransferProxyHandler()

        # # # Proxy Registration
        # # time.sleep(10)
        # # proxy = self.proxyRegisterTestHandler()

        # # # Proxy Resolution
        # # time.sleep(10)
        # # self.proxyLookupTestHandler(proxy)

        # # # Proxy Enquiry
        # # time.sleep(10)
        # # self.proxyEnquiryTestHandler(proxy)

        # # Proxy Porting

        # # Proxy Deactivate

        # # # Request for Payment by Account
        # time.sleep(10)
        # rfpAccountRequest, rfpAccountResult = self.requestForPaymentAccountTestHandler()

        # # # Request for Payment Rejection by Account
        # time.sleep(15)
        # self.requestForPaymentAccountRejectTestHandler(rfpAccountResult)

        # # # Request for Payment by Proxy
        # time.sleep(10)
        # proxy = self.proxyRegisterTestHandler()
        # time.sleep(10)
        # rfpProxyRequest, rfpProxyResult = self.requestForPaymentProxyTestHandler(
        #     proxy)

        # # # Request for Payment Rejection by Proxy
        # time.sleep(10)
        # self.requestForPaymentProxyRejectTestHandler(rfpProxyResult)

        # # Credit Transfer RFP
        # time.sleep(10)
        # rfpAccountRequest, rfpAccountResult = self.requestForPaymentAccountTestHandler()
        # time.sleep(10)
        # self.creditTransferRFPTestHandler(rfpAccountRequest, rfpAccountResult)

        # # E-Mandate Registration by Crediting
        # time.sleep(10)
        eMandateRegistrationCrediting = self.eMandateRegistrationByCreditingTest()

        # # E-Mandate Registration by Debiting

        # E-Mandate Approval by Crediting
        time.sleep(10)
        eMandateApprovalCrediting = self.eMandateApproveByCreditingTest(
            eMandateRegistrationCrediting)

        # E-Mandate Approval by Debiting

        # E-Mandate Amendment by Crediting
        time.sleep(10)
        eMandateAmendmentByCreditingTest = self.eMandateAmendmentByCreditingTest(
            eMandateRegistrationCrediting)

        # # E-Mandate Amendment by Debiting

        # E-Mandate Amendment Approval by Crediting
        time.sleep(10)
        eMandateAmendApproveByCreditingTest = self.eMandateAmendApproveByCreditingTest(
            eMandateRegistrationCrediting)

        # E-Mandate Amendment Approval by Debiting

        # E-Mandate Termination by Crediting

        # E-Mandate Termintation by Debiting

        # E-Mandate Enquiry by EndToEndId

        # E-Mandate Enquiry by MandateID

        # Direct Debit

        # PSR Direct Debit

        pass

    def pacs0200110(self, jsonResponse):
        # TODO: Change this with extract method version
        msgId = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["OrgnlGrpInfAndSts"][0]["OrgnlMsgId"]
        endToEndId = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        txSts = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        stsRsnInf = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        mndtId = jsonResponse.get("BusMsg", {}).get("Document", {}).get("FIToFIPmtStsRpt", {}).get(
            "TxInfAndSts", [])[0].get("OrgnlTxRef", {}).get("MndtRltdInf", {}).get("MndtId")
        return {
            'msgId': msgId,
            'endToEndId': endToEndId,
            'txSts': txSts,
            'stsRsnInf': stsRsnInf,
            'mndtId': mndtId
        }

    def pain01200106(self, jsonResponse):
        # resultForm = {
        #     'msgId': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMsgInf"]["MsgId"],
        #     'msgNmId': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMsgInf"]["MsgNmId"],
        #     'mndtId': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtId"],
        #     'mndtReqId': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtReqId"],
        #     'seqTp': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["SeqTp"],
        #     'frDt': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Drtn"]["FrDt"],
        #     'toDt': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Drtn"]["ToDt"],
        #     'frstColltnDt': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["FrstColltnDt"],
        #     'fnlColltnDt': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["FnlColltnDt"],
        #     'cdtrNm': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Cdtr"]["Nm"],
        #     'cdtrOrgId': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Cdtr"]["Id"]["OrgId"]["Othr"][0]["Id"],
        #     'cdtrAgt': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["CdtrAgt"]["FinInstnId"]["Othr"]["Id"],
        #     'dbtrAgt': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["DbtrAgt"]["FinInstnId"]["Othr"]["Id"],
        #     'dbtrNm': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Dbtr"]["Nm"],
        #     'txSts': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["SplmtryData"][0]["Envlp"]["Dtl"]["Rslt"]["TxSts"],
        #     'stsRsnInf': jsonResponse["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["SplmtryData"][0]["Envlp"]["Dtl"]["Rslt"]["StsRsnInf"]["Rsn"]["Prtry"],
        # }

        # self.logger.info(resultForm)
        exclude_tags = ["BusMsg", "Document"]
        exclude_path = "Document_MndtAccptncRpt_UndrlygAccptncDtls0".split(
            "_")  # Convert the path to a list of keys

        json_string = json.dumps(jsonResponse)
        resultExtract = generalHandler.extract_values(json_string)
        resultExtract["endToEndId"] = resultExtract.get(
            'MndtReqId')
        resultExtract["txSts"] = resultExtract.get(
            'SplmtryData0_Envlp_Dtl_Rslt_TxSts')
        resultExtract["stsRsnInf"] = resultExtract.get(
            'SplmtryData0_Envlp_Dtl_Rslt_StsRsnInf_Rsn_Prtry')
        # self.logger.info(f"resultExtract: {resultExtract}")

        return resultExtract

    def requestHandler(self, form):
        startTime = time.time()
        response = self.client.post(form.get('Payment_url'), data=form)
        duration = "{:.2f}".format(time.time() - startTime)
        jsonResponse = json.loads(response.data)
        # self.logger.info(jsonResponse)
        try:
            msgNmId = jsonResponse["BusMsg"]["AppHdr"]["MsgDefIdr"]
            messageType = {
                "pacs.002.001.10": lambda: self.pacs0200110(jsonResponse),
                "pain.012.001.06": lambda: self.pain01200106(jsonResponse)
            }
            result = messageType[msgNmId]()
            self.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                             f" ({duration} seconds) {form.get('Payment_url')} {(result.get('endToEndId'))} {result.get('txSts')} {result.get('stsRsnInf')}")
            return result
        except KeyError as e:
            self.logger.info(response.data)
            print("KeyError occurred!")
            print("Key that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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
        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18947',
                    'Fr': 'BANKDMY7',
                    "OrgnlEndToEndId": result.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
                return result
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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

        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18948',
                    'Fr': 'BANKDMY8',
                    "OrgnlEndToEndId": result.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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
        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18947',
                    'Fr': 'BANKDMY7',
                    "OrgnlEndToEndId": result.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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
        paymentData['To'] = 'FASTIDJA'
        paymentData['MsgDefIdr'] = 'pacs.028.001.04'
        paymentData['CpyDplct'] = 'CODU'
        paymentData['PssblDplct'] = False
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
            'Ustrd': 'RFP Reason',
            'SplmtryData_Cdtr_tp': '01',
            'SplmtryData_Cdtr_rsdntsts': '01',
            'SplmtryData_Cdtr_twnnm': '0300',
        }
        result = self.requestHandler(rfpAccountRequestForm)
        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18947',
                    'Fr': 'BANKDMY7',
                    "OrgnlEndToEndId": result.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
                return rfpAccountRequestForm, result
            else:
                time.sleep(15)
                return self.requestForPaymentAccountTestHandler()
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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
        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18948',
                    'Fr': 'BANKDMY8',
                    "OrgnlEndToEndId": form.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
                return result
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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

        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18947',
                    'Fr': 'BANKDMY7',
                    "OrgnlEndToEndId": result.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
                return rfpProxyRequestForm, result
            else:
                self.requestForPaymentProxyTestHandler(proxyForm)
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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

        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18948',
                    'Fr': 'BANKDMY8',
                    "OrgnlEndToEndId": form.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
                return result
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

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
        try:
            if result.get('txSts') == "ACTC":
                time.sleep(15)
                psrRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18948',
                    'Fr': 'BANKDMY8',
                    "OrgnlEndToEndId": result.get('endToEndId')
                }
                self.paymentStatusRequestTestHandler(psrRequestForm)
            else:
                self.creditTransferRFPTestHandler(rfpForm, rfpResult)
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

    def eMandateEnquiryByMandateID(self, mandateForm):
        mandateForm['Payment_url'] = '/MandateEnquiry'
        mandateForm['To'] = 'FASTIDJA'
        mandateForm['MsgDefIdr'] = 'pain.017.001.02'
        mandateForm['BizSvc'] = 'BI'
        mandateForm['CpyDplct'] = 'CODU'
        mandateForm['PssblDplct'] = False
        mandateForm['TrckgInd'] = True
        return self.requestHandler(mandateForm)

    def eMandateRegistrationByCreditingTest(self):
        mandateRegistRequestForm = {
            'Payment_url': '/MandateRegistByCreditOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
            'To': 'FASTIDJA',
            'Payment_type': '802',
            'MsgDefIdr': "pain.009.001.06",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            'CtgyPurp': "01",
            'LclInstrm': "FixedAmt",
            'SeqTp': "RCUR",
            'Frqcy_tp': "MNTH",
            'Frqcy_cntPerPrd': "12",
            'FrDt': "",  # Fill if need a custom date
            'ToDt': "",  # Fill if need a custom date
            'FrstColltnDt': "",  # Fill if need a custom date
            'FnlColltnDt': "",  # Fill if need a custom date
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
        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                mandateEnquiryRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18947',
                    'Fr': 'BANKDMY7',
                    "MndtId": result.get('mndtId'),
                    "CtgyPurp": "802",  # TODO: Change later to dynamic
                    # "CtgyPurp": mandateRegistRequestForm.get('CtgyPurp'),
                    "Cdtr_nm": mandateRegistRequestForm.get('Cdtr_nm'),
                    "Dbtr_nm": mandateRegistRequestForm.get('Dbtr_nm'),
                    "DbtrAgt": mandateRegistRequestForm.get('DbtrAgt')
                }
                # self.eMandateEnquiryByMandateID(mandateEnquiryRequestForm)
                return result
            else:
                return self.eMandateRegistrationByCreditingTest()
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

    def eMandateApproveByCreditingTest(self, mandateResultForm):
        # Mandate Enquiry to get mandate info
        mandateEnquiryRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            "MndtId": mandateResultForm.get('mndtId'),
            "CtgyPurp": "802",  # TODO: Change later to dynamic
            # "CtgyPurp": mandateRegistRequestForm.get('CtgyPurp'),
            "DbtrAgt": "BANKDMY7"  # TODO: Change later
        }
        mandate = self.eMandateEnquiryByMandateID(mandateEnquiryRequestForm)
        mandateApproveRequestForm = {
            'Payment_url': '/MandateApprovalByCreditOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'Payment_type': '803',
            'MsgDefIdr': "pain.012.001.06",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            "OrgnlMsgInf_msgid": mandate.get('msgId'),
            # "OrgnlMsgInf_msgnmid": mandate.get('msgNmId'),
            "OrgnlMsgInf_msgnmid": "pain.009.001.06",
            "AccptncRslt": True,
            "OrgnlMndt_mndtid": mandate.get('MndtId'),
            "OrgnlMndt_mndtreqid": mandate.get('MndtReqId'),
            "SeqTp": mandate.get('Ocrncs_SeqTp'),
            "FrDt": mandate.get('Ocrncs_Drtn_FrDt'),
            "ToDt": mandate.get('Ocrncs_Drtn_ToDt'),
            "FrstColltnDt": mandate.get('Ocrncs_FrstColltnDt'),
            "FnlColltnDt": mandate.get('Ocrncs_FnlColltnDt'),
            "TrckgInd": True,
            "Cdtr_nm": mandate.get('Cdtr_Nm'),
            "Cdtr_orgid": mandate.get('Cdtr_Id_OrgId_Othr0_Id'),
            "CdtrAgt": mandate.get('CdtrAgt_FinInstnId_Othr_Id'),
            "Dbtr_nm": mandate.get('Dbtr_Nm'),
            "DbtrAgt": mandate.get('DbtrAgt_FinInstnId_Othr_Id'),
            "OrgnlMndt_sts": "ACTV"
        }
        result = self.requestHandler(mandateApproveRequestForm)
        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                mandateEnquiryRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18948',
                    'Fr': 'BANKDMY8',
                    "MndtId": mandateResultForm.get('mndtId'),
                    "CtgyPurp": "802",
                    # "CtgyPurp": mandateRegistRequestForm.get('CtgyPurp'),
                    "Cdtr_nm": mandateApproveRequestForm.get('Cdtr_nm'),
                    "Dbtr_nm": mandateApproveRequestForm.get('Dbtr_nm'),
                    "DbtrAgt": mandateApproveRequestForm.get('DbtrAgt')
                }
                # self.eMandateEnquiryByMandateID(mandateEnquiryRequestForm)
                return result
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

    def eMandateAmendmentByCreditingTest(self, mandateForm):
        # Mandate Enquiry to get mandate info
        mandateEnquiryRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
            "MndtId": mandateForm.get('mndtId'),
            "CtgyPurp": "802",  # TODO: Change later to dynamic
            # "CtgyPurp": mandateRegistRequestForm.get('CtgyPurp'),
            "DbtrAgt": "BANKDMY8"  # TODO: Change later
        }
        mandate = self.eMandateEnquiryByMandateID(mandateEnquiryRequestForm)

        mandateAmendRequestForm = {
            'Payment_url': '/MandateAmendByCreditOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18947',
            'Fr': 'BANKDMY7',
            'To': 'FASTIDJA',
            'Payment_type': '761',
            'MsgDefIdr': "pain.010.001.06",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            "AmdmntRsn_rsn": "MD18",
            "AmdmntRsn_addtlInf": "1234",
            "Mndt_MndtId": mandate.get('MndtId'),
            "Mndt_MndtReqId": mandate.get('endToEndId'),
            'Mndt_CtgyPurp': "01",
            'Mndt_LclInstrm': "FixedAmt",
            'Mndt_SeqTp': "RCUR",
            'Mndt_Frqcy_tp': "YEAR",
            'Mndt_Frqcy_cntPerPrd': "1",
            'Mndt_FrDt': mandate.get('Ocrncs_Drtn_FrDt'),
            'Mndt_ToDt': mandate.get('Ocrncs_Drtn_ToDt'),
            'Mndt_FrstColltnDt': mandate.get('Ocrncs_FrstColltnDt'),
            'Mndt_FnlColltnDt': mandate.get('Ocrncs_FnlColltnDt'),
            'Mndt_TrckgInd': True,
            'Mndt_FrstColltnAmt_ccy': mandate.get('FrstColltnAmt_Ccy'),
            'Mndt_FrstColltnAmt_value': mandate.get('FrstColltnAmt_value'),
            'Mndt_ColltnAmt_ccy': mandate.get('ColltnAmt_Ccy'),
            'Mndt_ColltnAmt_value': mandate.get('ColltnAmt_value'),
            'Mndt_MaxAmt_ccy': mandate.get('MaxAmt_Ccy'),
            'Mndt_MaxAmt_value': mandate.get('MaxAmt_value'),
            'Mndt_Rsn':  mandate.get('Rsn_Prtry'),
            'Mndt_Cdtr_nm': mandate.get('Cdtr_Nm'),
            'Mndt_Cdtr_orgid': mandate.get('Cdtr_Id_OrgId_Othr0_Id'),
            'Mndt_CdtrAcct_id': mandate.get('CdtrAcct_Id_Othr_Id'),
            'Mndt_CdtrAcct_tp': mandate.get('CdtrAcct_Tp_Prtry'),
            'Mndt_CdtrAcct_nm': mandate.get('CdtrAcct_Nm'),
            'Mndt_CdtrAgt': mandate.get('CdtrAgt_FinInstnId_Othr_Id'),
            'Mndt_Dbtr_nm': mandate.get('Dbtr_Nm'),
            'Mndt_Dbtr_prvtid': mandate.get('Dbtr_Id_PrvtId_Othr0_Id'),
            'Mndt_DbtrAcct_id': mandate.get('DbtrAcct_Id_Othr_Id'),
            'Mndt_DbtrAcct_tp': mandate.get('DbtrAcct_Tp_Prtry'),
            'Mndt_DbtrAcct_nm': mandate.get('DbtrAcct_Nm'),
            'Mndt_DbtrAgt': mandate.get('DbtrAgt_FinInstnId_Othr_Id'),
            'Mndt_CdtrRef': mandate.get('RfrdDoc0_CdtrRef'),
            "OrgnlMndt_MndtId": mandate.get('mndtId'),
            "OrgnlMndt_MndtReqId": mandate.get('endToEndId'),
            'OrgnlMndt_CtgyPurp': mandate.get('Tp_CtgyPurp_Prtry'),
            'OrgnlMndt_LclInstrm': mandate.get('Tp_LclInstrm_Prtry'),
            'OrgnlMndt_SeqTp': mandate.get('Ocrncs_SeqTp'),
            'OrgnlMndt_Frqcy_tp': mandate.get('Ocrncs_Frqcy_Prd_Tp'),
            'OrgnlMndt_Frqcy_cntPerPrd': mandate.get('Ocrncs_Frqcy_Prd_CntPerPrd'),
            'OrgnlMndt_FrDt': mandate.get('Ocrncs_Drtn_FrDt'),
            'OrgnlMndt_ToDt': mandate.get('Ocrncs_Drtn_ToDt'),
            'OrgnlMndt_FrstColltnDt': mandate.get('Ocrncs_FrstColltnDt'),
            'OrgnlMndt_FnlColltnDt': mandate.get('Ocrncs_FnlColltnDt'),
            'OrgnlMndt_TrckgInd': True,
            'OrgnlMndt_FrstColltnAmt_ccy': mandate.get('FrstColltnAmt_Ccy'),
            'OrgnlMndt_FrstColltnAmt_value': mandate.get('FrstColltnAmt_value'),
            'OrgnlMndt_ColltnAmt_ccy': mandate.get('ColltnAmt_Ccy'),
            'OrgnlMndt_ColltnAmt_value': mandate.get('ColltnAmt_value'),
            'OrgnlMndt_MaxAmt_ccy': mandate.get('MaxAmt_Ccy'),
            'OrgnlMndt_MaxAmt_value': mandate.get('MaxAmt_value'),
            'OrgnlMndt_Rsn':  mandate.get('Rsn_Prtry'),
            'OrgnlMndt_Cdtr_nm': mandate.get('Cdtr_Nm'),
            'OrgnlMndt_Cdtr_orgid': mandate.get('Cdtr_Id_OrgId_Othr0_Id'),
            'OrgnlMndt_CdtrAcct_id': mandate.get('CdtrAcct_Id_Othr_Id'),
            'OrgnlMndt_CdtrAcct_tp': mandate.get('CdtrAcct_Tp_Prtry'),
            'OrgnlMndt_CdtrAcct_nm': mandate.get('CdtrAcct_Nm'),
            'OrgnlMndt_CdtrAgt': mandate.get('CdtrAgt_FinInstnId_Othr_Id'),
            'OrgnlMndt_Dbtr_nm': mandate.get('Dbtr_Nm'),
            'OrgnlMndt_Dbtr_prvtid': mandate.get('Dbtr_Id_PrvtId_Othr0_Id'),
            'OrgnlMndt_DbtrAcct_id': mandate.get('DbtrAcct_Id_Othr_Id'),
            'OrgnlMndt_DbtrAcct_tp': mandate.get('DbtrAcct_Tp_Prtry'),
            'OrgnlMndt_DbtrAcct_nm': mandate.get('DbtrAcct_Nm'),
            'OrgnlMndt_DbtrAgt': mandate.get('DbtrAgt_FinInstnId_Othr_Id'),
            'OrgnlMndt_CdtrRef': mandate.get('RfrdDoc0_CdtrRef'),
            'OrgnlMndt_Sts': "ACTV",
            'Mndt_Sts': "ACTV",

        }
        # self.logger.info(mandateAmendRequestForm)
        result = self.requestHandler(mandateAmendRequestForm)
        # self.logger.info(f'Mandate enquiry result after amend : {result}')
        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                mandateEnquiryRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18947',
                    'Fr': 'BANKDMY7',
                    "MndtId": mandate.get('MndtId'),
                    "CtgyPurp": "761",  # TODO: Change later to dynamic
                    # "CtgyPurp": mandateAmendRequestForm.get('CtgyPurp'),
                    "Cdtr_nm": mandateAmendRequestForm.get('Cdtr_nm'),
                    "Dbtr_nm": mandateAmendRequestForm.get('Dbtr_nm'),
                    "DbtrAgt": mandateAmendRequestForm.get('DbtrAgt')
                }
                self.eMandateEnquiryByMandateID(mandateEnquiryRequestForm)
                return result
            else:
                return self.eMandateAmendmentByCreditingTest(mandateForm)
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

    def eMandateAmendApproveByCreditingTest(self, mandateForm):
        # Mandate Enquiry to get mandate info
        mandateEnquiryRequestForm = {
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            "MndtId": mandateForm.get('mndtId'),
            "CtgyPurp": "761",  # TODO: Change later to dynamic
            # "CtgyPurp": mandateRegistRequestForm.get('CtgyPurp'),
            "DbtrAgt": "BANKDMY8"  # TODO: Change later
        }
        mandate = self.eMandateEnquiryByMandateID(mandateEnquiryRequestForm)
        mandateApproveRequestForm = {
            'Payment_url': '/MandateApprovalByCreditOFI',
            'Host_url': '10.170.137.115',
            'Host_port': '18948',
            'Fr': 'BANKDMY8',
            'To': 'FASTIDJA',
            'Payment_type': '771',
            'MsgDefIdr': "pain.012.001.06",
            "BizSvc": "BI",
            "CpyDplct": "CODU",
            "PssblDplct": "false",
            "OrgnlMsgInf_msgid": mandate.get('msgId'),
            # "OrgnlMsgInf_msgnmid": mandate.get('msgNmId'),
            "OrgnlMsgInf_msgnmid": "pain.010.001.06",
            "AccptncRslt": True,
            "OrgnlMndt_mndtid": mandate.get('MndtId'),
            "OrgnlMndt_mndtreqid": mandate.get('MndtReqId'),
            "SeqTp": mandate.get('Ocrncs_SeqTp'),
            "FrDt": mandate.get('Ocrncs_Drtn_FrDt'),
            "ToDt": mandate.get('Ocrncs_Drtn_ToDt'),
            "FrstColltnDt": mandate.get('Ocrncs_FrstColltnDt'),
            "FnlColltnDt": mandate.get('Ocrncs_FnlColltnDt'),
            "TrckgInd": True,
            "Cdtr_nm": mandate.get('Cdtr_Nm'),
            "Cdtr_orgid": mandate.get('Cdtr_Id_OrgId_Othr0_Id'),
            "CdtrAgt": mandate.get('CdtrAgt_FinInstnId_Othr_Id'),
            "Dbtr_nm": mandate.get('Dbtr_Nm'),
            "DbtrAgt": mandate.get('DbtrAgt_FinInstnId_Othr_Id'),
            "OrgnlMndt_sts": "ACTV"
        }
        result = self.requestHandler(mandateApproveRequestForm)
        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                mandateEnquiryRequestForm = {
                    'Host_url': '10.170.137.115',
                    'Host_port': '18948',
                    'Fr': 'BANKDMY8',
                    "MndtId": mandateForm.get('mndtId'),
                    "CtgyPurp": "761",
                    # "CtgyPurp": mandateRegistRequestForm.get('CtgyPurp'),
                    "Cdtr_nm": mandateApproveRequestForm.get('Cdtr_nm'),
                    "Dbtr_nm": mandateApproveRequestForm.get('Dbtr_nm'),
                    "DbtrAgt": mandateApproveRequestForm.get('DbtrAgt')
                }
                self.eMandateEnquiryByMandateID(mandateEnquiryRequestForm)
        except AttributeError as e:
            # self.logger.info(response.data)
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)



if __name__ == '__main__':
    unittest.main()
