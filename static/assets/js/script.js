document.addEventListener("DOMContentLoaded", function () {

  // ✅ Search click
  const searchIcon = document.querySelector(".search-icon");
  if (searchIcon) {
    searchIcon.addEventListener("click", function() {
      let input = document.querySelector(".search-box input");
      if (input) {
        alert("Searching for: " + input.value);
      }
    });
  }

  // ✅ Typing animation
  const el = document.getElementById("changing-text");
  if (el) {
    const texts = [
      "नमस्ते, आप क्या सीखना चाहते हैं?",
      "Hello, what do you want to learn?",
      "नई पढ़ाई, नया नज़रिया",
      "Nayi Padhai, New Perspective"
    ];

    let index1 = 0;
    let charIndex1 = 0;

    function typeText1() {
      if (charIndex1 < texts[index1].length) {
        el.innerHTML += texts[index1].charAt(charIndex1);
        charIndex1++;
        setTimeout(typeText1, 50);
      } else {
        setTimeout(eraseText1, 1500);
      }
    }

    function eraseText1() {
      if (charIndex1 > 0) {
        el.innerHTML = texts[index1].substring(0, charIndex1 - 1);
        charIndex1--;
        setTimeout(eraseText1, 30);
      } else {
        index1 = (index1 + 1) % texts.length;
        setTimeout(typeText1, 500);
      }
    }

    typeText1();
  }

  // ✅ Placeholder animation
  const placeholder = document.getElementById("search-placeholder");
  if (placeholder) {
    const texts1 = [
      "Search DSA...",
      "Search Web Development...",
      "Search Machine Learning...",
      "Search Python..."
    ];

    let index = 0;
    placeholder.innerText = texts1[0];

    setInterval(() => {
      placeholder.innerText = texts1[index];
      index = (index + 1) % texts1.length;
    }, 2500);
  }

  // ✅ User dropdown
  document.querySelectorAll('.user-toggle').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      this.parentElement.classList.toggle('active');
    });
  });

  document.addEventListener('click', function (e) {
    document.querySelectorAll('.user-dropdown').forEach(drop => {
      if (!drop.contains(e.target)) {
        drop.classList.remove('active');
      }
    });
  });

  // ✅ Course submenu
  document.querySelectorAll('.course-toggle').forEach(item => {
    item.addEventListener('click', function (e) {
      e.preventDefault();

      const parent = this.parentElement;

      document.querySelectorAll('.course-item').forEach(el => {
        if (el !== parent) {
          el.classList.remove('active');
        }
      });

      parent.classList.toggle('active');
    });
  });

});