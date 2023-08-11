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
        # E-Mandate Registration by Crediting
        customForm = {
            'tags_to_remove': [
                'BusMsg.Document.MndtInitnReq.Mndt.0.FrstColltnAmt',
                'BusMsg.Document.MndtInitnReq.Mndt.0.Ocrncs.FrstColltnAmt',
                'BusMsg.Document.MndtInitnReq.Mndt.0.Ocrncs.FrstColltnDt'
            ]
        }
        eMandateRegistrationCrediting = self.eMandateRegistrationByCreditingTest()

        # # # E-Mandate Registration by Debiting

        # # E-Mandate Approval by Crediting
        # time.sleep(10)
        # eMandateApprovalCrediting = self.eMandateApproveByCreditingTest(
        #     eMandateRegistrationCrediting)

        # # E-Mandate Approval by Debiting

        # # E-Mandate Amendment by Crediting
        # time.sleep(10)
        # eMandateAmendmentByCreditingTest = self.eMandateAmendmentByCreditingTest(
        #     eMandateRegistrationCrediting)

        # # # E-Mandate Amendment by Debiting

        # # E-Mandate Amendment Approval by Crediting
        # time.sleep(10)
        # eMandateAmendApproveByCreditingTest = self.eMandateAmendApproveByCreditingTest(
        #     eMandateRegistrationCrediting)

        # Direct Debit
        # time.sleep(10)
        # mandateDirectDebitForm = {
        #     "MNDTID_VALUE": "BANKDMY8_MERCH_1000001920025", # Manually fill this field
        #     # "MNDT_CTGYPURP_VALUE": mandateForm.get('MNDT_CTGYPURP_VALUE')
        # }
        # directDebitTest = self.directDebitTest(mandateDirectDebitForm)

        # Test Cases
        # success
        directDebit = {
            "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920046",  # Manually fill this field
        }
        # TC4A01 = self.directDebitTest(directDebit)

        # # Suspend the bank 1st
        # TC4A02 = self.directDebitTest(mandateDirectDebitForm)

        # PSR || merged with TC4A01
        # directDebit = {
        #     "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920046",  # Manually fill this field
        # }
        # TC4A03 = ""

        # Reversal DD U000
        # directDebitNoRFIResponse = {
        #     "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920047",
        #     "INTR_BK_STTLM_AMT_VALUE": 13002.01,
        # }
        # TC4A04 = self.directDebitTest(directDebitNoRFIResponse)

        # # Duplicate U149
        # directDebitDuplicate = {
        #     "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920046",
        #     "BIZ_MSG_IDR_VALUE": "20230808BANKDMY8210O0153304507",
        #     "MSG_ID_VALUE": "20230808BANKDMY821053304507",
        #     "END_TO_END_ID_VALUE": "20230808BANKDMY8210O0153304507"
        # }
        # TC4A07 = self.directDebitTest(directDebitDuplicate)

        # # Mandate ID not found
        # directDebitNotFound = {
        #     "MNDT_MNDTID_VALUE": "asdfasdfasdf",
        # }
        # TC4A08 = self.directDebitTest(directDebitNotFound)

        # Mandate is not active (suspend or pndg)
        # directDebitPending = {
        #     "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920097",
        # }
        # TC4A09 = self.directDebitTest(directDebitPending)

        # Creditor Customer are different
        # directDebitDifferentAccount = {
        #     **directDebit,
        #     "CDTR_ACCT_VALUE": "123412341234",
        # }
        # TC4A11 = self.directDebitTest(directDebitDifferentAccount)

        # DD Req Date > E-Mandate start date
        directDebitStartDateGreater = {
            "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920105",

        }
        # TC4A12 = self.directDebitTest(directDebitStartDateGreater)

        # # Payment is different (FixedAmt)
        # directDebitDifferentAmt = {
        #     "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920055",
        # }
        # TC4A14 = self.directDebitTest(directDebitDifferentAmt)

        # Set value without .00
        directDebitWrongAmt = {
            "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920046",
            "INTR_BK_STTLM_AMT_VALUE": 13001

        }
        # TC4A17 = self.directDebitTest(directDebitWrongAmt)

        # # invalid crediting BIC CdtrAgt
        # directDebitWrongCrBIC = {
        #     "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920046",
        #     "CDTR_AGT_VALUE": "CENAIDJA"
        # }
        # TC4A20 = self.directDebitTest(directDebitWrongCrBIC)

        # # invalid RFI response
        # TC4A22 = ""

        # # missing mandatory field
        # TC4A24 = ""

        # # missing mandatory field but in RFI
        # TC4A25 = ""

        # # Insufficient fund
        # TC4A27 = ""

        # # RFI suspend
        # TC4A28 = ""

        # # First amt is different than dd amt
        # TC4A31 = ""

        # # late response
        # TC4A34 = ""

    def pacs0200110(self, jsonResponse):
        # TODO: Change this with extract method version
        msgId = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["OrgnlGrpInfAndSts"][0]["OrgnlMsgId"]
        msgNmId = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["OrgnlGrpInfAndSts"][0]["OrgnlMsgNmId"]
        endToEndId = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
        txSts = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["TxSts"]
        stsRsnInf = jsonResponse["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["StsRsnInf"][0]["Rsn"]["Prtry"]
        mndtId = jsonResponse.get("BusMsg", {}).get("Document", {}).get("FIToFIPmtStsRpt", {}).get(
            "TxInfAndSts", [])[0].get("OrgnlTxRef", {}).get("MndtRltdInf", {}).get("MndtId")
        return {
            'msgId': msgId,
            'msgNmId': msgNmId,
            'endToEndId': endToEndId,
            'txSts': txSts,
            'stsRsnInf': stsRsnInf,
            'MNDTID_VALUE': mndtId
        }

    def pain01200106(self, jsonResponse):
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

    def paymentStatusRequestTestHandler(self, paymentData):
        paymentData['Payment_url'] = '/PaymentStatusOFI'
        self.requestHandler(paymentData)

    def eMandateEnquiryByMandateID(self, mandateForm):
        mandateForm['Payment_url'] = '/MandateEnquiry'
        return self.requestHandler(mandateForm)

    def eMandateRegistrationByCreditingTest(self, customForm=None):
        mandateRegistRequestForm = {
            'Payment_url': '/MandateRegistByCreditOFI',
        }
        if customForm is not None:
            mandateRegistRequestForm.update(customForm)

        result = self.requestHandler(mandateRegistRequestForm)
        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                result["ORGNAGT"] = "DBTRAGT"
                result["MNDT_CTGYPURP_VALUE"] = "802"
                customApproveForm = {
                    'tags_to_remove': [
                        'BusMsg.Document.MndtAccptncRpt.UndrlygAccptncDtls.0.OrgnlMndt.OrgnlMndt.Ocrncs.FrstColltnAmt',
                        'BusMsg.Document.MndtAccptncRpt.UndrlygAccptncDtls.0.OrgnlMndt.OrgnlMndt.Ocrncs.FrstColltnDt'
                    ]
                }
                # self.eMandateApproveByCreditingTest(result, customApproveForm)
                return result
            else:
                return self.eMandateRegistrationByCreditingTest()
        except AttributeError as e:
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

    def eMandateApproveByCreditingTest(self, mandateForm, customApproveForm=None):
        mandate = self.eMandateEnquiryByMandateID(mandateForm)
        # self.logger.info(mandate)
        mandateApproveRequestForm = {
            'Payment_url': '/MandateApprovalByCreditOFI',
            "ORGNL_MSG_ID_VALUE": mandate.get('OrgnlMsgInf_MsgId'),
            "ORGNL_MSG_NM_VALUE": "pain.009.001.06",
            "ACCPTNCRSLT_VALUE": True,
            "ORGNL_MNDT_ID_VALUE": mandate.get('MndtId'),
            "ORGNL_MNDT_REQ_ID_VALUE": mandate.get('MndtReqId'),
            "ORGNL_SEQTP_VALUE": mandate.get('Ocrncs_SeqTp'),
            "ORGNL_FR_DT_VALUE": mandate.get('Ocrncs_Drtn_FrDt'),
            "ORGNL_TO_DT_VALUE": mandate.get('Ocrncs_Drtn_ToDt'),
            "ORGNL_FRST_COLLTN_DT_VALUE": mandate.get('Ocrncs_FrstColltnDt'),
            "ORGNL_FNL_COLLTN_DT_VALUE": mandate.get('Ocrncs_FnlColltnDt'),
            "ORGNL_MNDT_STS_VALUE": "ACTV",
            **customApproveForm
        }
        result = self.requestHandler(mandateApproveRequestForm)
        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                # self.eMandateAmendmentByCreditingTest(mandateForm)
                return result
        except AttributeError as e:
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

    def eMandateAmendmentByCreditingTest(self, mandateForm):
        mandate = self.eMandateEnquiryByMandateID(mandateForm)
        mandateAmendRequestForm = {
            'Payment_url': '/MandateAmendByCreditOFI',
            "MNDT_MNDTID_VALUE": mandate.get('MndtId'),
            "ORGNLMNDT_MNDTID_VALUE": mandate.get('MndtId'),
            "ORGNLMNDT_REQ_ID_VALUE": mandate.get('MndtReqId'),
            "ORGNLMNDT_LCLINSTRM_VALUE": mandate.get('Tp_LclInstrm_Prtry'),
            "ORGNLMNDT_CTGYPURP_VALUE": mandate.get('Tp_CtgyPurp_Prtry'),
            "ORGNLMNDT_OCRNCS_SEQTP_VALUE": mandate.get('Ocrncs_SeqTp'),
            "ORGNLMNDT_OCRNCS_FRQCY_VALUE": mandate.get('Ocrncs_Frqcy_Prd_Tp'),
            "ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE": mandate.get('Ocrncs_Frqcy_Prd_CntPerPrd'),
            "ORGNLMNDT_DRTN_FRDT_VALUE": mandate.get('Ocrncs_Drtn_FrDt'),
            "ORGNLMNDT_DRTN_TODT_VALUE": mandate.get('Ocrncs_Drtn_ToDt'),
            "ORGNLMNDT_FRST_COLLTNDT_VALUE": mandate.get('Ocrncs_FrstColltnDt'),
            "ORGNLMNDT_FNL_COLLTNDT_VALUE": mandate.get('Ocrncs_FnlColltnDt'),
            "ORGNLMNDT_TRCKGIND_VALUE": mandate.get('TrckgInd'),
            "ORGNLMNDT_FRST_COLLTNAMT_CCY_VALUE": mandate.get('FrstColltnAmt_Ccy'),
            "ORGNLMNDT_FRST_COLLTNAMT_VALUE": mandate.get('FrstColltnAmt_value'),
            "ORGNLMNDT_COLLTNAMT_CCY_VALUE": mandate.get('ColltnAmt_Ccy'),
            "ORGNLMNDT_COLLTNAMT_VALUE": mandate.get('ColltnAmt_value'),
            "ORGNLMNDT_MAX_AMT_CCY_VALUE": mandate.get('MaxAmt_Ccy'),
            "ORGNLMNDT_MAX_AMT_VALUE": mandate.get('MaxAmt_value'),
            "ORGNLMNDT_MNDT_RSN_VALUE": mandate.get('Rsn_Prtry'),
            "ORGNLMNDT_CDTR_NM_VALUE": mandate.get('Cdtr_Nm'),
            "ORGNLMNDT_CDTR_ORG_ID_VALUE": mandate.get('Cdtr_Id_OrgId_Othr0_Id'),
            "ORGNLMNDT_CDTR_ACCT_VALUE": mandate.get('CdtrAcct_Id_Othr_Id'),
            "ORGNLMNDT_CDTR_ACCT_TP_VALUE": mandate.get('CdtrAcct_Tp_Prtry'),
            "ORGNLMNDT_CDTR_ACCT_NM_VALUE": mandate.get('CdtrAcct_Nm'),
            "ORGNLMNDT_CDTR_AGT_VALUE": mandate.get('CdtrAgt_FinInstnId_Othr_Id'),
            "ORGNLMNDT_DBTR_NM_VALUE": mandate.get('Dbtr_Nm'),
            "ORGNLMNDT_DBTR_PRVT_ID_VALUE": mandate.get('Dbtr_Id_PrvtId_Othr0_Id'),
            "ORGNLMNDT_DBTR_ACCT_VALUE": mandate.get('DbtrAcct_Id_Othr_Id'),
            "ORGNLMNDT_DBTR_ACCT_TP_VALUE": mandate.get('DbtrAcct_Tp_Prtry'),
            "ORGNLMNDT_DBTR_ACCT_NM_VALUE": mandate.get('DbtrAcct_Nm'),
            "ORGNLMNDT_DBTR_AGT_VALUE": mandate.get('DbtrAgt_FinInstnId_Othr_Id'),
            "ORGNLMNDT_RFRD_DOC_CDTR_REF_VALUE": mandate.get('RfrdDoc0_CdtrRef'),
        }
        result = self.requestHandler(mandateAmendRequestForm)
        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                # result["ORGNAGT"] = "DBTRAGT"
                # result["MNDT_CTGYPURP_VALUE"] = "802"
                # self.eMandateApproveByCreditingTest(result)
                return result
            else:
                return self.eMandateAmendmentByCreditingTest(mandateForm)
        except AttributeError as e:
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)

    def directDebitTest(self, mandateForm, customForm=None):
        # mandate = self.eMandateEnquiryByMandateID(mandateForm)
        directDebitRequestForm = {
            'Payment_url': '/DirectDebitOFI',
            **mandateForm
            # "MNDT_MNDTID_VALUE": "BANKDMY8_MERCH_1000001920025",
        }
        if customForm is not None:
            result = self.requestHandler(directDebitRequestForm, customForm)
        else:
            result = self.requestHandler(directDebitRequestForm)

        time.sleep(15)
        try:
            if result.get('txSts') == "ACTC":
                result["ORGNAGT"] = "CDTRAGT"
                result["ORGNL_MSG_NM_ID_VALUE"] = result.get('msgNmId')
                result["ORGNL_END_TO_END_ID_VALUE"] = result.get('endToEndId')
                # self.paymentStatusRequestTestHandler(result)
                return result
            else:
                pass
                # return self.directDebitTest(mandateForm)
        except AttributeError as e:
            print("Attribute occurred!")
            print("Attribute that caused the error:", e.args[0])
            print("Error message:", e)
            print("Full traceback:", e.__traceback__)


if __name__ == '__main__':
    unittest.main()
