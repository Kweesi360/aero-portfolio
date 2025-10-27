// =========================
// script.js - Aerospace Portfolio
// =========================

// Typing Animation (same as before)
const typingElement = document.getElementById("typing");
const textArray = [
  "Future Aerospace Engineer 🚀",
  "Passionate About Flight ✈️",
  "Exploring Space Systems 🌌"
];
let textIndex = 0;
let charIndex = 0;

function typeText() {
  if (charIndex < textArray[textIndex].length) {
    typingElement.textContent += textArray[textIndex].charAt(charIndex);
    charIndex++;
    setTimeout(typeText, 100);
  } else {
    setTimeout(deleteText, 2000);
  }
}

function deleteText() {
  if (charIndex > 0) {
    typingElement.textContent = textArray[textIndex].substring(0, charIndex - 1);
    charIndex--;
    setTimeout(deleteText, 50);
  } else {
    textIndex = (textIndex + 1) % textArray.length;
    setTimeout(typeText, 500);
  }
}

typeText();

// =========================
// Smooth Scroll
// =========================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({ behavior: "smooth" });
  });
});

// =========================
// Contact Form
// =========================
const form = document.querySelector("form");
form.addEventListener("submit", function(e) {
  e.preventDefault();
  alert("Message Sent! I will get back to you soon.");
  form.reset();
});

// =========================
// Video Open in New Tab
// =========================
function openModal(videoUrl, title) {
  window.open(videoUrl, '_blank');
}
