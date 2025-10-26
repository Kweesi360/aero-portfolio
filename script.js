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

// Smooth Scroll for Internal Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth"
    });
  });
});

// Simple Contact Form Handler (Front-end Only)
const form = document.querySelector("form");
form.addEventListener("submit", function(e) {
  e.preventDefault();
  alert("Message Sent! I will get back to you soon.");
  form.reset();
});


function openModal(videoSrc, title) {
  const modal = document.getElementById("videoModal");
  const video = document.getElementById("modalVideo");
  const videoTitle = document.getElementById("videoTitle");

  video.src = videoSrc;
  videoTitle.innerText = title;

  // Rotate video 90 degrees for landscape display
  video.style.transform = "rotate(90deg)";

  modal.style.display = "flex";
}

// Live WebSocket subtitles
const subtitleBox = document.getElementById('subtitle-box');
const socket = new WebSocket("ws://localhost:8765");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  subtitleBox.innerHTML = `<strong>${data.speaker}:</strong> ${data.text}`;
  subtitleBox.style.display = 'block';

  // hide subtitle automatically after a few seconds
  setTimeout(() => {
    subtitleBox.style.display = 'none';
  }, 5000);
};
