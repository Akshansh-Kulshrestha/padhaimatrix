document.querySelector(".next-btn").onclick = () => {
  alert("Next Page");
};

document.querySelector(".prev-btn").onclick = () => {
  alert("Previous Page");
};
// document.querySelector(".next-btn").onclick = () => {
//   window.location.href = "next-page.html";
// };

let progress = 60; // change dynamically

document.querySelector(".progress-fill").style.width = progress + "%";
document.getElementById("progress-percent").innerText = progress + "%";
