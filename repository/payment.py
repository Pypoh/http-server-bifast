import handler.general as handler
import repository.data as generalData

base = {
    "TO_BIC_VALUE": "FASTIDJA",
    "BIZ_SVC_VALUE": "BI",
    "CRE_DT_VALUE": handler.getCreDt(),
    "CPYDPLCT_VALUE": "CODU",
    "PSSBLDPLCT_VALUE": False,
    "CRE_DT_TM_VALUE": handler.getCreDtTm(),
    "NM_OF_TXS_VALUE": "1",
}

dbtrData = {
    "DBTR_AGT_VALUE": generalData.sampleData.get('DBTRAGT'),
    "DBTR_NM_VALUE": generalData.sampleData.get('DBTR_NM'),
    "DBTR_ORG_ID_VALUE": generalData.sampleData.get('DBTR_ORGID'),
    "DBTR_PRVT_ID_VALUE": generalData.sampleData.get('DBTR_PRVTID'),
    "DBTR_ACCT_VALUE": generalData.sampleData.get('DBTRACCT_VALUE'),
    "DBTR_ACCT_TP_VALUE": generalData.sampleData.get('DBTRACCT_TYPE'),
    "DBTR_ACCT_NM_VALUE": generalData.sampleData.get('DBTRACCT_NAME')
}

dbtrProxyData = {
    "DBTR_ACCT_PRXY_TP": generalData.sampleData.get('DBTRACCT_PRXY_TYPE'),
    "DBTR_ACCT_PRXY_ID": generalData.sampleData.get('DBTRACCT_PRXY_ID'),
}

cdtrData = {
    "CDTR_AGT_VALUE": generalData.sampleData.get('CDTRAGT'),
    "CDTR_NM_VALUE": generalData.sampleData.get('CDTR_NM'),
    "CDTR_ORG_ID_VALUE": generalData.sampleData.get('CDTR_ORGID'),
    "CDTR_PRVT_ID_VALUE": generalData.sampleData.get('CDTR_PRVTID'),
    "CDTR_ACCT_VALUE": generalData.sampleData.get('CDTRACCT_VALUE'),
    "CDTR_ACCT_TP_VALUE": generalData.sampleData.get('CDTRACCT_TYPE'),
    "CDTR_ACCT_NM_VALUE": generalData.sampleData.get('CDTRACCT_NAME')
}

cdtrProxyData = {
    "CDTR_ACCT_PRXY_TP": generalData.sampleData.get('CDTRACCT_PRXY_TYPE'),
    "CDTR_ACCT_PRXY_ID": generalData.sampleData.get('CDTRACCT_PRXY_ID'),
}

splmtryData = {
    "SPLMNTR_INITACCTID_VALUE": "123456789",
    "SPLMNTR_DBTR_TP_VALUE": "01",
    "SPLMNTR_DBTR_RSDNTSTS_VALUE": "01",
    "SPLMNTR_DBTR_TWNNM_VALUE": "0300",
    "SPLMNTR_CDTR_TP_VALUE": "01",
    "SPLMNTR_CDTR_RSDNTSTS_VALUE": "01",
    "SPLMNTR_CDTR_TWNNM_VALUE": "0300",
    "SPLMNTR_RLTD_END_TO_END_ID": ""  # template
}

accountEnquiry = {
    "FR_BIC_VALUE": dbtrData.get('DBTR_AGT_VALUE'),
    "PAYMENT_TYPE": "510",
    "STTLMTD_VALUE": "CLRG",
    "MSG_DEF_IDR_VALUE": "pacs.008.001.08",
    "PMT_TP_INF_CTGYPURP_VALUE": "51001",
    "PMT_TP_INF_LCLINSTRM_VALUE": "01",
    "INTR_BK_STTLM_AMT_VALUE": 510.01,
    "INTR_BK_STTLM_CCY_VALUE": "IDR",
    "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
    "CHRGBR_VALUE": "DEBT",
    "RMTINF_USTRD_VALUE": "Testing Purpose",
}

creditTransfer = {
    "FR_BIC_VALUE": dbtrData.get('DBTR_AGT_VALUE'),
    "PAYMENT_TYPE": "010",
    "STTLMTD_VALUE": "CLRG",
    "MSG_DEF_IDR_VALUE": "pacs.008.001.08",
    "PMT_TP_INF_CTGYPURP_VALUE": "01001",
    "PMT_TP_INF_LCLINSTRM_VALUE": "01",
    "INTR_BK_STTLM_AMT_VALUE": 910.01,
    "INTR_BK_STTLM_CCY_VALUE": "IDR",
    "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
    "CHRGBR_VALUE": "DEBT",
    "RMTINF_USTRD_VALUE": "Testing Purpose",
}

creditTransferReversal = {
    "FR_BIC_VALUE": dbtrData.get('CDTR_AGT_VALUE'),
    "PAYMENT_TYPE": "011",
    "STTLMTD_VALUE": "CLRG",
    "MSG_DEF_IDR_VALUE": "pacs.008.001.08",
    "PMT_TP_INF_CTGYPURP_VALUE": "01101",
    "PMT_TP_INF_LCLINSTRM_VALUE": "01",
    "INTR_BK_STTLM_AMT_VALUE": 911.01,
    "INTR_BK_STTLM_CCY_VALUE": "IDR",
    "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
    "CHRGBR_VALUE": "DEBT",
    "RMTINF_USTRD_VALUE": "Testing Purpose",
}

creditTransferProxy = {
    "FR_BIC_VALUE": dbtrData.get('DBTR_AGT_VALUE'),
    "PAYMENT_TYPE": "110",
    "STTLMTD_VALUE": "CLRG",
    "MSG_DEF_IDR_VALUE": "pacs.008.001.08",
    "PMT_TP_INF_CTGYPURP_VALUE": "01001",
    "PMT_TP_INF_LCLINSTRM_VALUE": "01",
    "INTR_BK_STTLM_AMT_VALUE": 110.01,
    "INTR_BK_STTLM_CCY_VALUE": "IDR",
    "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
    "CHRGBR_VALUE": "DEBT",
    "RMTINF_USTRD_VALUE": "Testing Purpose",
}

requestForPaymentByAccount = {
    "FR_BIC_VALUE": cdtrData.get('CDTR_AGT_VALUE'),
    "PAYMENT_TYPE": "853",
    "MSG_DEF_IDR_VALUE": "pain.013.001.08",
    "PMTTPINF_CTGYPURP_VALUE": "85301",
    "PMTINF_PMTMTD_VALUE": "TRF",
    "INSTDAMT_VALUE": 853.01,
    "INSTDAMT_CCY_VALUE": "IDR",
    "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
    "CHRGBR_VALUE": "DEBT",
    "RMTINF_USTRD_VALUE": "Testing Purpose",
    "INITG_PTY_NM_VALUE": generalData.sampleData.get('DBTR_NM'),
    "PSTLADR_CTRY_VALUE": "ID",
    "REQD_EXCTN_DT_VALUE": "",
    "XPRY_DT_VALUE": ""
}

requestForPaymentByProxy = {
    "FR_BIC_VALUE": dbtrData.get('CDTR_AGT_VALUE'),
    "PAYMENT_TYPE": "851",
    "MSG_DEF_IDR_VALUE": "pain.013.001.08",
    "PMTTPINF_CTGYPURP_VALUE": "85101",
    "PMTINF_PMTMTD_VALUE": "TRF",
    "INSTDAMT_VALUE": 851.01,
    "INSTDAMT_CCY": "IDR",
    "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
    "CHRGBR_VALUE": "DEBT",
    "RMTINF_USTRD_VALUE": "Testing Purpose",
    "INITG_PTY_NM_VALUE": generalData.sampleData.get('DBTR_NM'),
    "PSTLADR_CTRY_VALUE": "ID",
    "REQD_EXCTN_DT_VALUE": "",
    "XPRY_DT_VALUE": ""
}

emandateRegistrationByCreditor = {
    "FR_BIC_VALUE": cdtrData.get('CDTR_AGT_VALUE'),
    "PAYMENT_TYPE": "802",
    "MSG_DEF_IDR_VALUE": "pain.009.001.06",
    "MNDT_LCLINSTRM_VALUE": "FixedAmt",
    "MNDT_CTGYPURP_VALUE": "01",
    "OCRNCS_SEQTP_VALUE": "RCUR",
    "OCRNCS_FRQCY_VALUE": "MNTH",
    "OCRNCS_CNTPERPRD_VALUE": "12",
    "DRTN_FRDT_VALUE": "",
    "DRTN_TODT_VALUE": "",
    "FRST_COLLTNDT_VALUE": "",
    "FNL_COLLTNDT_VALUE": "",
    "TRCKGIND_VALUE": True,
    "FRST_COLLTNAMT_CCY_VALUE": "IDR",
    "FRST_COLLTNAMT_VALUE": 13001.01,
    "COLLTNAMT_CCY_VALUE": "IDR",
    "COLLTNAMT_VALUE": 13001.01,
    "MAX_AMT_CCY_VALUE": "IDR",
    "MAX_AMT_VALUE": 13001.01,
    "MNDT_RSN_VALUE": "Credit Pay Insurance",
    "RFRD_DOC_CDTR_REF_VALUE": "Test"
}

emandateRegistApprovalByCreditor = {
    "FR_BIC_VALUE": dbtrData.get('DBTR_AGT_VALUE'),
    "PAYMENT_TYPE": "803",
    "MSG_DEF_IDR_VALUE": "pain.012.001.06",
    "TRCKGIND_VALUE": True,
}

emandateAmendmentByCreditor = {
    "FR_BIC_VALUE": cdtrData.get('CDTR_AGT_VALUE'),
    "PAYMENT_TYPE": "761",
    "MSG_DEF_IDR_VALUE": "pain.010.001.06",
    "AMDMNTRSN_RSN_VALUE": "MD18",
    "AMDMNTRSN_ADDTLINF_VALUE": "Additional Information",
    # "MNDT_MNDTID_VALUE": "",
    "MNDT_LCLINSTRM_VALUE": "FixedAmt",
    "MNDT_CTGYPURP_VALUE": "01",
    "OCRNCS_SEQTP_VALUE": "RCUR",
    "OCRNCS_FRQCY_VALUE": "YEAR",
    "OCRNCS_CNTPERPRD_VALUE": 1,
    "DRTN_FRDT_VALUE": "",
    "DRTN_TODT_VALUE": "",
    "FRST_COLLTNDT_VALUE": "",
    "FNL_COLLTNDT_VALUE": "",
    "TRCKGIND_VALUE": True,
    "FRST_COLLTNAMT_CCY_VALUE": "IDR",
    "FRST_COLLTNAMT_VALUE": 13001.01,
    "COLLTNAMT_CCY_VALUE": "IDR",
    "COLLTNAMT_VALUE": 13001.01,
    "MAX_AMT_CCY_VALUE": "IDR",
    "MAX_AMT_VALUE": 13001.01,
    "MNDT_RSN_VALUE": "Credit Pay Insurance",
    "RFRD_DOC_CDTR_REF_VALUE": "Test",
    "SPLMTRYDATA_ORGNLMNDT_STS": "ACTV",
    "SPLMTRYDATA_MNDT_STS": "ACTV"
}

emandateEnquiry = {
    "PAYMENT_TYPE": "000",
    "MSG_DEF_IDR_VALUE": "pain.017.001.02",
}

paymentStatusRequest = {
    "PAYMENT_TYPE": "000",
    "MSG_DEF_IDR_VALUE": "pacs.028.001.04",
}

directDebit = {
    "FR_BIC_VALUE": cdtrData.get('CDTR_AGT_VALUE'),
    "PAYMENT_TYPE": "210",
    "STTLMTD_VALUE": "CLRG",
    "MSG_DEF_IDR_VALUE": "pacs.003.001.08",
    "INTR_BK_STTLM_AMT_VALUE": 13001.01,
    "INTR_BK_STTLM_CCY_VALUE": "IDR",
    "INTR_BK_STTLM_DT_VALUE": "",
    "CHRGBR_VALUE": "SLEV",
    "RMTINF_USTRD_VALUE": "Testing Purpose",
}