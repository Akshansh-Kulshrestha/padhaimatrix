const dropdowns = document.querySelectorAll(".dropdown-toggle");

dropdowns.forEach((toggle) => {
  toggle.addEventListener("click", function () {
    const parent = this.parentElement;

    // close others
    document.querySelectorAll(".dropdown-item").forEach((item) => {
      if (item !== parent) {
        item.classList.remove("active");
      }
    });

    // toggle current
    parent.classList.toggle("active");
  });
});
document.querySelectorAll(".submenu a").forEach(link => {
  link.addEventListener("click", function() {
    document.querySelectorAll(".submenu a").forEach(l => l.classList.remove("active"));
    this.classList.add("active");
  });
});