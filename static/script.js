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

function sendMultipleRequests() {
  const requestDataArray = getCheckedCheckboxes();

  console.log(requestDataArray);
  // Create an array of Promises for each request
  const requestPromises = requestDataArray.map((data) => sendRequest(data));

  // Use Promise.all() to handle all the requests simultaneously
  Promise.all(requestPromises)
    .then((results) => {
      console.log("All requests completed:", results);
      // Handle the results of the requests here if needed
    })
    .catch((error) => {
      console.error("Error occurred:", error);
      // Handle errors if needed
    });
}
