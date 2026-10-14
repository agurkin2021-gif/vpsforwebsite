// main script
(function () {
  "use strict";

  // Testimonial Slider
  // ----------------------------------------
  if (typeof Swiper !== "undefined" && document.querySelector(".testimonial-slider")) new Swiper(".testimonial-slider", {
    spaceBetween: 24,
    loop: true,
    pagination: {
      el: ".testimonial-slider-pagination",
      type: "bullets",
      clickable: true,
    },
    breakpoints: {
      768: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 3,
      },
    },
  });
})();
