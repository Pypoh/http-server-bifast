from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Time between HTTP requests in seconds

    @task
    def make_post_request(self):
        # Define the URL of the target host where you want to make the POST request
        target_url = "http://localhost:5000/AccountEnquiry/json/request"  # Replace with your target URL

        message = "{'BusMsg': {'AppHdr': {'BizMsgIdr': '20230912BANKDMY7510O0147673618','BizSvc': 'BI','CpyDplct': 'CODU','CreDt': '2023-09-12T17:15:55Z','Fr': {'FIId': {'FinInstnId': {'Othr': {'Id': 'BANKDMY7'}}}},'MsgDefIdr': 'pacs.008.001.08','PssblDplct': false,'To': {'FIId': {'FinInstnId': {'Othr': {'Id': 'FASTIDJA'}}}}},'Document': {'FIToFICstmrCdtTrf': {'CdtTrfTxInf': [{'Cdtr': {'Nm': 'Valve8'},'CdtrAcct': {'Id': {'Othr': {'Id': '8483564635'}}},'CdtrAgt': {'FinInstnId': {'Othr': {'Id': 'BANKDMY8'}}},'ChrgBr': 'DEBT','Dbtr': {'Nm': 'PT. Bank Dummy 7'},'DbtrAcct': {'Id': {'Othr': {'Id': '12345677789'}},'Tp': {'Prtry': 'CACC'}},'DbtrAgt': {'FinInstnId': {'Othr': {'Id': 'BANKDMY7'}}},'IntrBkSttlmAmt': {'Ccy': 'IDR','value': 510.01},'PmtId': {'EndToEndId': '20230912BANKDMY7510O0147673618','TxId': '20230912BANKDMY7510877219296'},'PmtTpInf': {'CtgyPurp': {'Prtry': '51001'}}}],'GrpHdr': {'CreDtTm': '2023-09-12T17:15:55','MsgId': '20230912BANKDMY7510877219296','NbOfTxs': '1','SttlmInf': {'SttlmMtd': 'CLRG'}}}}}}"

        # Define the POST data (payload) to send to the target host
        payload = {
            "key1": "value1",
            "key2": "value2",
            # Add any other POST data as needed
        }

        # Make the POST request to the target host using the Locust HTTP client
        response = self.client.post(target_url, json=message)

        # You can optionally check the response for assertions or error handling
        if response.status_code != 200:
            self.environment.runner.quit("POST request failed with status code {}".format(response.status_code))
