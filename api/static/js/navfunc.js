// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the navbar
var navbar1 = document.getElementById("navbar1");

// Get the offset position of the navbar
var sticky = navbar1.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar1.classList.add("sticky")
  } else {
    navbar1.classList.remove("sticky");
  }
}