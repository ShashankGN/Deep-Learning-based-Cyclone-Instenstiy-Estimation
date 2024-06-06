// Auto slide carousel items
let currentIndex = 0;
const items = document.querySelectorAll(".carousel-item");
const totalItems = items.length;

function slideCarousel() {
  items[currentIndex].classList.remove("active");
  currentIndex = (currentIndex + 1) % totalItems;
  items[currentIndex].classList.add("active");
}

setInterval(slideCarousel, 5000); // Change slide every 5 seconds
