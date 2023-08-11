function openDrawer() {
  const drawer = document.querySelector(".drawer");
  const isOpen = drawer.style.left === "0px";
  drawer.style.left = isOpen ? "-250px" : "0px";
}

function updateConsoleContent(consoleId, content) {
  const consoleContent = document.getElementById(consoleId);
  consoleContent.innerText = content;
}

function handleCardClick(title) {
  // alert("You clicked on: " + title);
  updateConsoleContent(
    "console-content-1",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras enim metus, volutpat id nisl at, mollis luctus magna. Vestibulum eget risus eget arcu accumsan consectetur eget iaculis ligula. Maecenas turpis ante, pulvinar non commodo sit amet, venenatis quis odio. Suspendisse at maximus turpis. Duis condimentum nisl sit amet ultricies tincidunt. Sed finibus quam a lectus sagittis, sed dapibus mi lacinia. Ut ac consequat ipsum, nec pretium ex. Morbi consequat ligula nunc, eget euismod purus lacinia commodo. Aenean at quam non velit lacinia sagittis at eu magna. Mauris efficitur nisl euismod magna viverra imperdiet."
  );
  updateConsoleContent(
    "console-content-2",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras enim metus, volutpat id nisl at, mollis luctus magna. Vestibulum eget risus eget arcu accumsan consectetur eget iaculis ligula. Maecenas turpis ante, pulvinar non commodo sit amet, venenatis quis odio. Suspendisse at maximus turpis. Duis condimentum nisl sit amet ultricies tincidunt. Sed finibus quam a lectus sagittis, sed dapibus mi lacinia. Ut ac consequat ipsum, nec pretium ex. Morbi consequat ligula nunc, eget euismod purus lacinia commodo. Aenean at quam non velit lacinia sagittis at eu magna. Mauris efficitur nisl euismod magna viverra imperdiet."
  );
}

function generateTextAnimation(consoleId, text) {
  updateConsoleContent(consoleId, text);
}

// Start the generated-text animations
generateTextAnimation(
  "console-content-1",
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras enim metus, volutpat id nisl at, mollis luctus magna. Vestibulum eget risus eget arcu accumsan consectetur eget iaculis ligula. Maecenas turpis ante, pulvinar non commodo sit amet, venenatis quis odio. Suspendisse at maximus turpis. Duis condimentum nisl sit amet ultricies tincidunt. Sed finibus quam a lectus sagittis, sed dapibus mi lacinia. Ut ac consequat ipsum, nec pretium ex. Morbi consequat ligula nunc, eget euismod purus lacinia commodo. Aenean at quam non velit lacinia sagittis at eu magna. Mauris efficitur nisl euismod magna viverra imperdiet. Mauris viverra id mi sit amet cursus. Pellentesque faucibus ornare libero a consequat. Nulla pellentesque justo at eros pharetra, sit amet interdum est dignissim. Etiam sem sapien, molestie non rutrum ut, ullamcorper id lorem. Quisque fringilla ultricies nulla ornare auctor. Proin lacinia eleifend erat vel mattis. Phasellus placerat ut libero nec posuere. Quisque eu quam eget risus sodales sodales. Cras consectetur odio ac sapien mattis sollicitudin sed ut nibh. Ut lacinia augue in felis placerat, eget aliquam tortor feugiat. Integer euismod mauris a metus mattis, vitae aliquam massa convallis. Suspendisse scelerisque ex in elit efficitur congue. Aenean quis dolor tempus, sodales metus in, placerat mauris. Aenean commodo euismod elit, a vestibulum dui eleifend nec. Vivamus non interdum ipsum. Vestibulum eget fermentum neque. Integer viverra luctus lacus eget semper. Praesent in metus quis erat auctor rutrum. Nulla ac arcu massa. Sed placerat consequat dui quis tincidunt. Suspendisse potenti. Aenean vel rhoncus diam, in tempor ex. Pellentesque porta dolor sem, et tempus dolor feugiat quis. Suspendisse laoreet pretium suscipit. Nam consequat orci eget eros fermentum, eget tempor eros cursus. Fusce consequat, orci eu faucibus convallis, velit turpis finibus diam, in dapibus sapien est ut purus. Fusce iaculis posuere faucibus. "
);
generateTextAnimation(
  "console-content-2",
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras enim metus, volutpat id nisl at, mollis luctus magna. Vestibulum eget risus eget arcu accumsan consectetur eget iaculis ligula. Maecenas turpis ante, pulvinar non commodo sit amet, venenatis quis odio. Suspendisse at maximus turpis. Duis condimentum nisl sit amet ultricies tincidunt. Sed finibus quam a lectus sagittis, sed dapibus mi lacinia. Ut ac consequat ipsum, nec pretium ex. Morbi consequat ligula nunc, eget euismod purus lacinia commodo. Aenean at quam non velit lacinia sagittis at eu magna. Mauris efficitur nisl euismod magna viverra imperdiet. Mauris viverra id mi sit amet cursus. Pellentesque faucibus ornare libero a consequat. Nulla pellentesque justo at eros pharetra, sit amet interdum est dignissim. Etiam sem sapien, molestie non rutrum ut, ullamcorper id lorem. Quisque fringilla ultricies nulla ornare auctor. Proin lacinia eleifend erat vel mattis. Phasellus placerat ut libero nec posuere. Quisque eu quam eget risus sodales sodales. Cras consectetur odio ac sapien mattis sollicitudin sed ut nibh. Ut lacinia augue in felis placerat, eget aliquam tortor feugiat. Integer euismod mauris a metus mattis, vitae aliquam massa convallis. Suspendisse scelerisque ex in elit efficitur congue. Aenean quis dolor tempus, sodales metus in, placerat mauris. Aenean commodo euismod elit, a vestibulum dui eleifend nec. Vivamus non interdum ipsum. Vestibulum eget fermentum neque. Integer viverra luctus lacus eget semper. Praesent in metus quis erat auctor rutrum. Nulla ac arcu massa. Sed placerat consequat dui quis tincidunt. Suspendisse potenti. Aenean vel rhoncus diam, in tempor ex. Pellentesque porta dolor sem, et tempus dolor feugiat quis. Suspendisse laoreet pretium suscipit. Nam consequat orci eget eros fermentum, eget tempor eros cursus. Fusce consequat, orci eu faucibus convallis, velit turpis finibus diam, in dapibus sapien est ut purus. Fusce iaculis posuere faucibus. "
);

function getCheckedCheckboxes() {
  const cardList = document.querySelectorAll(".card");
  const checkedCardTitles = [];

  cardList.forEach((card) => {
    const checkbox = card.querySelector(".card-checkbox");
    if (checkbox.checked) {
      const title = card.querySelector("p").innerText;
      checkedCardTitles.push(title);
    }
  });

  // console.log("Checked Card Titles:", checkedCardTitles);
  return checkedCardTitles;
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
function checkAllCards(transactionCheckbox) {
  const cardCheckboxes = document.querySelectorAll(".card-checkbox");

  cardCheckboxes.forEach((checkbox) => {
    checkbox.checked = transactionCheckbox.checked;
  });
}

function sendRequest(url) {
  let participantData; // Declare participantData outside the fetch to make it accessible in both fetches

  fetch("/getParticipantData")
    .then((response) => response.json()) // Chain a .then() to get the JSON data from response
    .then((data) => {
      console.log("Participant Data:", data); // Log the fetched data
      participantData = data; // Save the data in the variable

      // POST Request
      fetch(`${url}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(participantData),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Response Data:", data); // Log the response data from the second fetch
          return data; // You can return the response data if needed
        })
        .catch((error) => {
          console.error("Error:", error);
          throw error;
        });
    })
    .catch((error) => console.error("Error:", error));

  // console.log("Database:", participantData); // Log the fetched data
}

function sanityTest() {
  // requestDataArray = getCardsData();
  
  // requestHandler('/AccountEnquiryOFI')
  // requestHandler('/CreditTransferOFI')
  // requestHandler('/CreditTransferProxyOFI') TODO: Not yet developed
  requestHandler('/RequestForPayByAccountOFI')

}

async function requestHandler(payment_url) {
  const startTime = Date.now() / 1000;

  try {
    const participantResponse = await fetch("/getParticipantData");
    const participantData = await participantResponse.json();
    console.log("Participant Data:", participantData);

    const response = await fetch(payment_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(participantData),
    });
    
    const duration = (Date.now() / 1000 - startTime).toFixed(2);
    const jsonResponse = await response.json();
    console.log(jsonResponse);
    const msgNmId = jsonResponse.BusMsg.AppHdr.MsgDefIdr;
    const messageType = {
      "pacs.002.001.10": () => this.pacs0200110(jsonResponse),
      "pain.012.001.06": () => this.pain01200106(jsonResponse),
    };
    const result = messageType[msgNmId]();
      
    console.log(`${new Date().toISOString()} (${duration} seconds) ${payment_url} ${result.endToEndId} ${result.txSts} ${result.stsRsnInf}`);
    return result;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

function pacs0200110(jsonResponse) {
  const orgnlMsgId = jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.OrgnlGrpInfAndSts[0].OrgnlMsgId;
  const orgnlEndToEndId = jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0].OrgnlEndToEndId;
  const txSts = jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0].TxSts;
  const stsRsnInf = jsonResponse.BusMsg.Document.FIToFIPmtStsRpt.TxInfAndSts[0].StsRsnInf[0].Rsn.Prtry;
  const mndtId = jsonResponse.BusMsg?.Document?.FIToFIPmtStsRpt?.TxInfAndSts[0]?.OrgnlTxRef?.MndtRltdInf?.MndtId;
  
  return {
      msgId: orgnlMsgId,
      endToEndId: orgnlEndToEndId,
      txSts: txSts,
      stsRsnInf: stsRsnInf,
      mndtId: mndtId
  };
}

function pain01200106(jsonResponse) {
  const exclude_tags = ["BusMsg", "Document"];
  const exclude_path = "Document_MndtAccptncRpt_UndrlygAccptncDtls0".split("_");

  const json_string = JSON.stringify(jsonResponse);
  const resultExtract = extractValues(json_string);

  resultExtract.endToEndId = resultExtract.MndtReqId;
  resultExtract.txSts = resultExtract.SplmtryData0_Envlp_Dtl_Rslt_TxSts;
  resultExtract.stsRsnInf = resultExtract.SplmtryData0_Envlp_Dtl_Rslt_StsRsnInf_Rsn_Prtry;

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