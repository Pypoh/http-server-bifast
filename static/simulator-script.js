function openDrawer() {
  const drawer = document.querySelector(".drawer");
  const isOpen = drawer.style.left === "0px";
  drawer.style.left = isOpen ? "-250px" : "0px";
}

function updateConsoleContent(consoleId, content) {
  const consoleContent = document.getElementById(consoleId);
  consoleContent.innerText = content;
}

function clearConsole() {
  const consoleContent1 = document.getElementById("console-content-1");
  const consoleContent2 = document.getElementById("console-content-2");
  consoleContent1.innerText = "";
  consoleContent2.innerText = "";
}

function generateTextAnimation(consoleId, text) {
  updateConsoleContent(consoleId, text);
}

function getCardsData() {
  const cardList = document.querySelectorAll(".card");
  const checkedCardTitles = [];

  cardList.forEach((card) => {
    const title = card.querySelector("p").innerText;
    checkedCardTitles.push(title);
  });

  // console.log("Checked Card Titles:", checkedCardTitles);
  return checkedCardTitles;
}

function getInputValue(selector) {
  var input = document.querySelector(selector);
  return input ? input.value : "";
}

function checkInputData(payment_id) {
  var endtoendidValue = getInputValue(`#endtoendid_${payment_id}`);
  var mandateIdValue = getInputValue(".mandateid-input");

  var data = {
    SPLMNTR_RLTD_END_TO_END_ID: endtoendidValue,
    mandateIdValue: mandateIdValue,
  };

  return data;
}

async function requestJSONHandler(payment_url, payment_id) {
  var inputData = checkInputData(payment_id);

  const startTime = Date.now() / 1000;
  try {
    // Get Participant Data
    const participantResponse = await fetch("/getParticipantData");
    const participantData = await participantResponse.json();
    // console.log("Participant Data:", participantData);

    var data = Object.assign({}, inputData, participantData);

    // Build Message
    const buildResponse = await fetch(payment_url + "/json/build", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const jsonBuildResponse = await buildResponse.json();
    const jsonBuildString = JSON.stringify(jsonBuildResponse, null, 2);
    generateTextAnimation("console-content-1", jsonBuildString);

    // Send Request
    const sendResponse = await fetch(payment_url + "/json/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonBuildResponse),
    });
    const jsonSendResponse = await sendResponse.json();
    const jsonSendString = JSON.stringify(jsonSendResponse, null, 2);
    generateTextAnimation("console-content-2", jsonSendString);

    // const duration = (Date.now() / 1000 - startTime).toFixed(2);
    // const jsonResponse = await response.json();
    // // console.log(jsonResponse);
    // const msgNmId = jsonResponse.BusMsg.AppHdr.MsgDefIdr;
    // const messageType = {
    //   "pacs.002.001.10": () => this.pacs0200110(jsonResponse),
    //   "pain.012.001.06": () => this.pain01200106(jsonResponse),
    // };
    // const result = messageType[msgNmId]();
    // const jsonString = JSON.stringify(jsonResponse, null, 2);
    // generateTextAnimation('console-content-2', jsonString)
    // console.log(`${new Date().toISOString()} (${duration} seconds) ${payment_url} ${result.endToEndId} ${result.txSts} ${result.stsRsnInf}`);
    return result;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

async function requestXMLHandler(payment_url, payment_id) {
  var inputData = checkInputData(payment_id);

  const startTime = Date.now() / 1000;
  try {
    // Get Participant Data
    const participantResponse = await fetch("/getParticipantData");
    const participantData = await participantResponse.json();

    var data = Object.assign({}, inputData, participantData);

    // Build Message
    const buildResponse = await fetch(payment_url + "/xml/build", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const xmlResponseText = await buildResponse.text();
    generateTextAnimation("console-content-1", xmlResponseText);

    // // Send Request
    // const sendResponse = await fetch(payment_url + "/xml/request", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify(jsonBuildResponse),
    // });
    // const jsonSendResponse = await sendResponse.json();
    // const jsonSendString = JSON.stringify(jsonSendResponse, null, 2);
    // generateTextAnimation("console-content-2", jsonSendString);

    // const duration = (Date.now() / 1000 - startTime).toFixed(2);
    // const jsonResponse = await response.json();
    // // console.log(jsonResponse);
    // const msgNmId = jsonResponse.BusMsg.AppHdr.MsgDefIdr;
    // const messageType = {
    //   "pacs.002.001.10": () => this.pacs0200110(jsonResponse),
    //   "pain.012.001.06": () => this.pain01200106(jsonResponse),
    // };
    // const result = messageType[msgNmId]();
    // const jsonString = JSON.stringify(jsonResponse, null, 2);
    // generateTextAnimation('console-content-2', jsonString)
    // console.log(`${new Date().toISOString()} (${duration} seconds) ${payment_url} ${result.endToEndId} ${result.txSts} ${result.stsRsnInf}`);
    return result;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

function pacs0200110(jsonResponse) {
  const orgnlMsgId =
    jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.OrgnlGrpInfAndSts[0]
      .OrgnlMsgId;
  const orgnlEndToEndId =
    jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0].OrgnlEndToEndId;
  const txSts =
    jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0].TxSts;
  const stsRsnInf =
    jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0].StsRsnInf[0].Rsn
      .Prtry;
  const mndtId =
    jsonResponse.BusMsg?.Document?.FIToFIPmtStsRpt?.TxInfAndSts[0]?.OrgnlTxRef
      ?.MndtRltdInf?.MndtId;

  return {
    msgId: orgnlMsgId,
    endToEndId: orgnlEndToEndId,
    txSts: txSts,
    stsRsnInf: stsRsnInf,
    mndtId: mndtId,
  };
}

function pain01200106(jsonResponse) {
  const exclude_tags = ["BusMsg", "Document"];
  const exclude_path = "Document_MndtAccptncRpt_UndrlygAccptncDtls0".split("_");

  const json_string = JSON.stringify(jsonResponse);
  const resultExtract = extractValues(json_string);

  resultExtract.endToEndId = resultExtract.MndtReqId;
  resultExtract.txSts = resultExtract.SplmtryData0_Envlp_Dtl_Rslt_TxSts;
  resultExtract.stsRsnInf =
    resultExtract.SplmtryData0_Envlp_Dtl_Rslt_StsRsnInf_Rsn_Prtry;

  return resultExtract;
}

function extractValues(jsonString) {
  const data = JSON.parse(jsonString);

  function extract(obj, path) {
    for (const key of path) {
      if (obj.hasOwnProperty(key)) {
        obj = obj[key];
      } else {
        return undefined;
      }
    }
    return obj;
  }

  const result = {};

  for (const key in data) {
    if (!exclude_tags.includes(key)) {
      const value = extract(data[key], exclude_path);
      if (value !== undefined) {
        result[key] = value;
      }
    }
  }

  return result;
}
