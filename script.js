// =========================
// script.js - Aerospace Portfolio
// =========================

// Typing Animation in Hero Section
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
// Smooth Scroll for Internal Links
// =========================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth"
    });
  });
});

// =========================
// Simple Contact Form Handler (Front-end Only)
// =========================
const form = document.querySelector("form");
form.addEventListener("submit", function(e) {
  e.preventDefault();
  alert("Message Sent! I will get back to you soon.");
  form.reset();
});

// =========================
// Modal Video Handler (Local models folder)
// =========================
function openModal(videoSrc, title) {
  const modal = document.getElementById("videoModal");
  const video = document.getElementById("modalVideo");
  const videoTitle = document.getElementById("videoTitle");

  // Force lowercase path for consistency
  const fixedSrc = videoSrc.toLowerCase();

  video.src = fixedSrc;
  videoTitle.innerText = title;

  modal.style.display = "flex";
  video.load();   // reloads the source
  video.play();   // start playing automatically
}

// Close modal when clicking outside video or pressing ESC
window.addEventListener("click", (e) => {
  const modal = document.getElementById("videoModal");
  const video = document.getElementById("modalVideo");
  if (e.target === modal) {
    modal.style.display = "none";
    video.pause();
    video.src = "";
  }
});

window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const modal = document.getElementById("videoModal");
    const video = document.getElementById("modalVideo");
    modal.style.display = "none";
    video.pause();
    video.src = "";
  }
});

// =========================
// Live WebSocket Subtitles (optional)
// =========================
const subtitleBox = document.getElementById('subtitle-box');
const socket = new WebSocket("ws://localhost:8765");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  subtitleBox.innerHTML = `<strong>${data.speaker}:</strong> ${data.text}`;
  subtitleBox.style.display = 'block';

  // Hide subtitle automatically after a few seconds
  setTimeout(() => {
    subtitleBox.style.display = 'none';
  }, 5000);
};

