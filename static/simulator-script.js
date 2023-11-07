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
  var relatedValue = getInputValue(`#related_${payment_id}`);

  var data = null;
  if (!isEmpty(endtoendidValue)) {
    var data = {
      SPLMNTR_RLTD_END_TO_END_ID: endtoendidValue,
      RELATED_VALUE: relatedValue,
    };
  }

  return data;
}

function isEmpty(value) {
  return value === null || value === undefined || value === "";
}

async function requestPaymentReport(
  payment_url,
  payment_data,
  participant_data
) {
  var data = Object.assign({}, payment_data, participant_data);
  const buildResponse = await fetch(payment_url + "/json/build", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const jsonBuildResponse = await buildResponse.json();
  const jsonBuildString = JSON.stringify(jsonBuildResponse, null, 2);
  // generateTextAnimation("console-content-1", jsonBuildString);

  //   // Send Request
  const sendResponse = await fetch(payment_url + "/json/request", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonBuildResponse),
  });
  const jsonSendResponse = await sendResponse.json();
  const jsonSendString = JSON.stringify(jsonSendResponse, null, 2);
  // generateTextAnimation("console-content-2", jsonSendString);

  return jsonSendResponse;
}

async function requestJSONHandler(payment_url, payment_id, inquiry_url) {
  const startTime = Date.now() / 1000;
  try {
    // Get Participant Data
    const participantResponse = await fetch("/getParticipantData");
    const participantData = await participantResponse.json();
    // console.log("Participant Data:", participantData);

    var inputData = checkInputData(payment_id);
    var payment_data = {};
    if (!isEmpty(inputData)) {
      payment_data = await requestPaymentReport(
        inquiry_url,
        inputData,
        participantData
      );
      var inputData = {
        INPUT_DATA: inputData["SPLMNTR_RLTD_END_TO_END_ID"],
        RELATED_DATA: inputData["RELATED_VALUE"],
      };
    }

    if (payment_url == inquiry_url) {
      return;
    }

    removedTags = {
      // TAGS_TO_REMOVE: ["BusMsg.Document.MndtInitnReq.Mndt.0.ColltnAmt.Ccy"],
    };

    clearConsole();
    var data = Object.assign(
      {},
      payment_data,
      participantData,
      inputData,
      removedTags
    );

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

    // const numberOfRequestsInBatch = 5;

    // while (true) {
    //   const batch = [];

    //   // Create a batch of requests
    //   for (let i = 0; i < numberOfRequestsInBatch; i++) {
    //     const buildResponse = fetch(payment_url + "/json/build", {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(data),
    //     });
    //     batch.push(buildResponse);
    //   }

    //   // Send the batch of requests concurrently (without awaiting their responses)
    //   Promise.all(batch);

    //   // Add a delay before sending the next batch (e.g., 1 second)
    //   await new Promise((resolve) => setTimeout(resolve, 500));
    // }

    // return result;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

async function requestXMLHandler(payment_url, payment_id, inquiry_url) {
  const startTime = Date.now() / 1000;
  try {
    // Get Participant Data
    const participantResponse = await fetch("/getParticipantData");
    const participantData = await participantResponse.json();
    // console.log("Participant Data:", participantData);

    var inputData = checkInputData(payment_id);
    var payment_data = {};
    if (!isEmpty(inputData)) {
      payment_data = await requestPaymentReport(
        inquiry_url,
        inputData,
        participantData
      );
      var inputData = {
        INPUT_DATA: inputData["SPLMNTR_RLTD_END_TO_END_ID"],
        RELATED_DATA: inputData["RELATED_VALUE"],
      };
    }

    if (payment_url == inquiry_url) {
      return;
    }

    removedTags = {
      // TAGS_TO_REMOVE: ["BusMsg.Document.MndtInitnReq.Mndt.0.ColltnAmt.Ccy"],
    };

    clearConsole();
    var data = Object.assign(
      {},
      payment_data,
      participantData,
      inputData,
      removedTags
    );

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

    console.log(xmlResponseText);

    // Send Request
    const sendResponse = await fetch(payment_url + "/xml/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/xml",
      },
      body: xmlResponseText,
    });
    const xmlSendResponseText = await sendResponse.text();
    generateTextAnimation("console-content-2", xmlSendResponseText);

    // return result;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

async function optionalTagTest(payment_url, payment_id, inquiry_url) {
  try {
    removedTags1 = {
      TAGS_TO_REMOVE_REGIST: [
        "BusMsg.Document.MndtInitnReq.Mndt.0.Ocrncs/FnlColltnDt",
      ],
      TAGS_TO_REMOVE_AMEND: [
        "BusMsg.Document.MndtAmdmntReq.UndrlygAmdmntDtls.0.Mndt.Ocrncs.FnlColltnDt",
        "BusMsg.Document.MndtAmdmntReq.UndrlygAmdmntDtls.0.OrgnlMndt.OrgnlMndt.Ocrncs.FnlColltnDt",
      ],
    };

    removedTags2 = {
      TAGS_TO_REMOVE_REGIST: [
        "BusMsg.Document.MndtInitnReq.Mndt.0.Ocrncs.FrstColltnDt",
      ],
      TAGS_TO_REMOVE_AMEND: [
        "BusMsg.Document.MndtAmdmntReq.UndrlygAmdmntDtls.0.Mndt.Ocrncs.FrstColltnDt",
        "BusMsg.Document.MndtAmdmntReq.UndrlygAmdmntDtls.0.OrgnlMndt.OrgnlMndt.Ocrncs.FrstColltnDt",
      ],
    };

    removedTags3 = {
      TAGS_TO_REMOVE_REGIST: [
        "BusMsg.Document.MndtInitnReq.Mndt.0.Ocrncs.Drtn.ToDt",
      ],
      TAGS_TO_REMOVE_AMEND: [
        "BusMsg.Document.MndtAmdmntReq.UndrlygAmdmntDtls.0.Mndt.Ocrncs.Drtn.ToDt",
        "BusMsg.Document.MndtAmdmntReq.UndrlygAmdmntDtls.0.OrgnlMndt.OrgnlMndt.Ocrncs.Drtn.ToDt",
      ],
    };

    const removeTagsArray = [removedTags1, removedTags2, removedTags3];

    resultTest = [];

    // console.log(removeTagsArray);

    for (const removedTags in removeTagsArray) {
      console.log(removedTags);
    }

    // const participantResponse = await fetch("/getParticipantData");
    // const participantData = await participantResponse.json();

    // for (const removedTags in removeTagsArray) {
    //   // Mandate Regist
    //   payment_url = "/Mandate/regist/creditor";
    //   var data = Object.assign({}, participantData, inputData, removedTags);

    //   const buildRegistResponse = await fetch(payment_url + "/json/build", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(data),
    //   });
    //   const jsonBuildResponse = await buildRegistResponse.json();

    //   const sendRegistResponse = await fetch(payment_url + "/json/request", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(jsonBuildResponse),
    //   });
    //   const jsonSendResponse = await sendRegistResponse.json();
    //   const jsonSendString = JSON.stringify(jsonSendResponse, null, 2);

    //   const mndtId =
    //     jsonSendResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0]
    //       .OrgnlTxRef.MndtRltdInf.MndtId;

    //   // Mandate Approval
    //   payment_url = "/Mandate/approve/creditor";
    //   inquiry_url = "/Mandate/enquiry/creditor";
    //   var inputData = {};
    //   var enquiryData = {
    //     SPLMNTR_RLTD_END_TO_END_ID: mndtId,
    //   };
    //   var payment_data = {};
    //   payment_data = await requestPaymentReport(
    //     inquiry_url,
    //     enquiryData,
    //     participantData
    //   );
    //   inputData = {
    //     INPUT_DATA: enquiryData["SPLMNTR_RLTD_END_TO_END_ID"],
    //   };
    //   data = Object.assign({}, payment_data, participantData, inputData);
    //   const buildRegistApproveResponse = await fetch(
    //     payment_url + "/json/build",
    //     {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(data),
    //     }
    //   );
    //   const jsonBuildApproveRegistResponse =
    //     await buildRegistApproveResponse.json();
    //   // const jsonResponseDebug = JSON.stringify(
    //   //   buildRegistApproveResponse,
    //   //   null,
    //   //   2
    //   // );
    //   // generateTextAnimation("console-content-1", jsonResponseDebug);
    //   const sendRegistApproveResponse = await fetch(
    //     payment_url + "/json/request",
    //     {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(jsonBuildApproveRegistResponse),
    //     }
    //   );

    //   const jsonSendApproveRegistResponse =
    //     await sendRegistApproveResponse.json();
    //   const jsonBuildString = JSON.stringify(
    //     jsonSendApproveRegistResponse,
    //     null,
    //     2
    //   );
    //   // Mandate Amend
    //   payment_url = "/Mandate/amend/creditor";
    //   inquiry_url = "/Mandate/enquiry/creditor";
    //   var inputData = {};
    //   var enquiryData = {
    //     SPLMNTR_RLTD_END_TO_END_ID: mndtId,
    //     // RELATED_VALUE: relatedValue,
    //   };
    //   var payment_data = {};
    //   payment_data = await requestPaymentReport(
    //     inquiry_url,
    //     enquiryData,
    //     participantData
    //   );
    //   inputData = {
    //     INPUT_DATA: enquiryData["SPLMNTR_RLTD_END_TO_END_ID"],
    //     // RELATED_DATA: inputData["RELATED_VALUE"],
    //   };
    //   data = Object.assign(
    //     {},
    //     payment_data,
    //     participantData,
    //     inputData,
    //     removedTags
    //   );
    //   const buildAmendResponse = await fetch(payment_url + "/json/build", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(data),
    //   });
    //   const jsonBuildAmendResponse = await buildAmendResponse.json();
    //   const jsonResponseDebug = JSON.stringify(jsonBuildAmendResponse, null, 2);
    //   // generateTextAnimation("console-content-1", jsonResponseDebug);
    //   const sendAmendResponse = await fetch(payment_url + "/json/request", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(jsonBuildAmendResponse),
    //   });

    //   const jsonSendAmendResponse = await sendAmendResponse.json();
    //   const jsonBuildAmendString = JSON.stringify(
    //     jsonSendAmendResponse,
    //     null,
    //     2
    //   );
    //   const endToEndId =
    //     jsonSendAmendResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0]
    //       .OrgnlEndToEndId;

    //   // Mandate Amend Approve
    //   payment_url = "/Mandate/approve/creditor";
    //   inquiry_url = "/Mandate/enquiry/creditor";
    //   var inputData = {};
    //   var enquiryData = {
    //     SPLMNTR_RLTD_END_TO_END_ID: mndtId,
    //     RELATED_VALUE: endToEndId,
    //   };
    //   var payment_data = {};
    //   payment_data = await requestPaymentReport(
    //     inquiry_url,
    //     enquiryData,
    //     participantData
    //   );
    //   inputData = {
    //     INPUT_DATA: enquiryData["SPLMNTR_RLTD_END_TO_END_ID"],
    //     RELATED_DATA: enquiryData["RELATED_VALUE"],
    //   };
    //   data = Object.assign(
    //     {},
    //     payment_data,
    //     participantData,
    //     inputData
    //     // removedTags
    //   );
    //   const buildAmendApproveResponse = await fetch(
    //     payment_url + "/json/build",
    //     {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(data),
    //     }
    //   );
    //   const jsonBuildApproveAmendResponse =
    //     await buildAmendApproveResponse.json();
    //   // const jsonResponseDebug = JSON.stringify(
    //   //   buildRegistApproveResponse,
    //   //   null,
    //   //   2
    //   // );
    //   // generateTextAnimation("console-content-1", jsonResponseDebug);
    //   const sendAmendApproveResponse = await fetch(
    //     payment_url + "/json/request",
    //     {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(jsonBuildApproveAmendResponse),
    //     }
    //   );

    //   const jsonSendApproveAmendResponse =
    //     await sendAmendApproveResponse.json();
    //   const jsonAmendApproveResponseDebug = JSON.stringify(
    //     jsonSendApproveAmendResponse,
    //     null,
    //     2
    //   );

    //   const result =
    //     jsonSendApproveAmendResponse.BusMsg.Document.FIToFIPmtStsRpt
    //       .TxInfAndSts[0].StsRsnInf[0].Rsn.Prtry;

    //   const tagResult = removedTags;
    //   console.log(`${result} | ${tagResult}`);
    //   resultTest.push(`${result} | ${tagResult}`);
    // }
    // totalString = ""
    // for (const resultString in resultItem) {
    //   totalString += resultString
    // }

    // generateTextAnimation("console-content-1", totalString);
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}
