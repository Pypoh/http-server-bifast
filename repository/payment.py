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
    "DBTR_ACCT_VALUE": generalData.sampleData.get('DBTRACCT_VALUE'),
    "DBTR_ACCT_TP_VALUE": generalData.sampleData.get('DBTRACCT_TYPE'),
}

cdtrData = {
    "CDTR_AGT_VALUE": generalData.sampleData.get('CDTRAGT'),
    "CDTR_NM_VALUE": generalData.sampleData.get('CDTR_NM'),
    "CDTR_ORG_ID_VALUE": generalData.sampleData.get('CDTR_ORGID'),
    "CDTR_ACCT_VALUE": generalData.sampleData.get('CDTRACCT_VALUE'),
    "CDTR_ACCT_TP_VALUE": generalData.sampleData.get('CDTRACCT_TYPE'),
}

splmtryData = {
    "SPLMNTR_INITACCTID_VALUE": "123456789",
    "SPLMNTR_DBTR_TP_VALUE": "01",
    "SPLMNTR_DBTR_RSDNTSTS_VALUE": "01",
    "SPLMNTR_DBTR_TWNNM_VALUE": "0300",
    "SPLMNTR_CDTR_TP_VALUE": "01",
    "SPLMNTR_CDTR_RSDNTSTS_VALUE": "01",
    "SPLMNTR_CDTR_TWNNM_VALUE": "0300",
}

accountEnquiry = {
    "PAYMENT_TYPE": "510",
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