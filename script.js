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

// =========================
// Modal Video Handler
// =========================
function openModal(videoSrc, title) {
  const modal = document.getElementById("videoModal");
  const video = document.getElementById("modalVideo");
  const videoTitle = document.getElementById("videoTitle");

  // Convert relative path (like 'models/arm.mp4') to full GitHub raw URL
  const githubBase = "https://raw.githubusercontent.com/Kweesi360/aero-portfolio/main/";
  const fullVideoSrc = githubBase + videoSrc;

  video.src = fullVideoSrc;
  videoTitle.innerText = title;

  // Ensure video plays normally (no rotation for now)
  video.style.transform = "none";

  modal.style.display = "flex";
  video.play(); // auto-start playback
}


// Close modal when user clicks outside video or presses ESC
window.addEventListener("click", (e) => {
  const modal = document.getElementById("videoModal");
  const video = document.getElementById("modalVideo");
  if (e.target === modal) {
    modal.style.display = "none";
    video.pause();
    video.src = ""; // stop playback completely
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
// Live WebSocket Subtitles (optional feature)
// =========================
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
