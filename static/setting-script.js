function openDrawer() {
  const drawer = document.querySelector(".drawer");
  const isOpen = drawer.style.left === "0px";
  drawer.style.left = isOpen ? "-250px" : "0px";
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

