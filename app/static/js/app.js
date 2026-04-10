// Dark Mode Toggle
const darkModeToggle = document.getElementById("darkModeToggle");
const htmlElement = document.documentElement;
const DARK_MODE_KEY = "darkmode";

// Initialize dark mode from localStorage
function initDarkMode() {
  const savedDarkMode = localStorage.getItem(DARK_MODE_KEY);
  if (savedDarkMode === "true") {
    enableDarkMode();
  }
}

function enableDarkMode() {
  htmlElement.setAttribute("data-theme", "dark");
  darkModeToggle.textContent = "☀️";
  localStorage.setItem(DARK_MODE_KEY, "true");
}

function disableDarkMode() {
  htmlElement.removeAttribute("data-theme");
  darkModeToggle.textContent = "🌙";
  localStorage.setItem(DARK_MODE_KEY, "false");
}

// Dark mode toggle event
if (darkModeToggle) {
  darkModeToggle.addEventListener("click", function () {
    if (htmlElement.getAttribute("data-theme") === "dark") {
      disableDarkMode();
    } else {
      enableDarkMode();
    }
  });
}

// Task completion animation
document.addEventListener("DOMContentLoaded", function () {
  initDarkMode();

  // Add smooth transitions for list items
  const listItems = document.querySelectorAll(".list-group-item");
  listItems.forEach((item) => {
    item.addEventListener("mouseenter", function () {
      this.style.transition = "all 0.3s ease";
    });
  });

  // Calendar hover effects
  const calendarDays = document.querySelectorAll(".calendar-day");
  calendarDays.forEach((day) => {
    day.addEventListener("mouseenter", function () {
      if (!this.classList.contains("empty")) {
        this.style.backgroundColor = "#e7f3ff";
      }
    });

    day.addEventListener("mouseleave", function () {
      this.style.backgroundColor = "";
    });
  });

  // Form validation
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const title = form.querySelector('input[name="title"]');
      if (title && title.value.trim() === "") {
        e.preventDefault();
        alert("Task title is required");
      }
    });
  });

  // Easter Eggs
  setupEasterEggs();
});

// Easter Eggs Functions
function setupEasterEggs() {
  const konamiCode = [
    "ArrowUp",
    "ArrowUp",
    "ArrowDown",
    "ArrowDown",
    "ArrowLeft",
    "ArrowRight",
    "ArrowLeft",
    "ArrowRight",
    "b",
    "a",
  ];
  let konamiIndex = 0;

  document.addEventListener("keydown", function (e) {
    if (e.key === konamiCode[konamiIndex]) {
      konamiIndex++;
      if (konamiIndex === konamiCode.length) {
        triggerKonamiEasterEgg();
        konamiIndex = 0;
      }
    } else {
      konamiIndex = 0;
    }
  });

  // Click on logo for surprise
  const navbar = document.querySelector(".navbar-brand");
  if (navbar) {
    navbar.addEventListener("click", function (e) {
      if (e.detail === 3) {
        // Triple click
        triggerLogoEasterEgg();
      }
    });
  }

  // Random compliment on profile
  if (window.location.pathname.includes("profile")) {
    setTimeout(() => {
      showRandomCompliment();
    }, 2000);
  }
}

function triggerKonamiEasterEgg() {
  const popup = document.createElement("div");
  popup.className = "easter-egg-popup";
  popup.innerHTML = `
    <h1>🎮 EASTER EGG UNLOCKED! 🎮</h1>
    <p>You found the Konami code! You're a true gamer!</p>
    <p style="font-size: 2em; margin: 20px 0;">🎉 +100 BONUS POINTS 🎉</p>
  `;
  document.body.appendChild(popup);

  setTimeout(() => {
    popup.remove();
  }, 3000);

  // Trigger confetti effect
  triggerConfetti();
}

function triggerLogoEasterEgg() {
  const navbar = document.querySelector(".navbar-brand");
  if (navbar) {
    navbar.classList.add("konami-easter");
    navbar.textContent = "🐳 WHALE MODE 🐳";

    setTimeout(() => {
      navbar.textContent = "🐳 Flask Docker";
      navbar.classList.remove("konami-easter");
    }, 2000);

    // Show notification
    alert("You've unlocked Whale Mode! 🐳");
  }
}

function showRandomCompliment() {
  const compliments = [
    "You're doing amazing! 🌟",
    "Keep up the great work! 💪",
    "You're crushing it! 🚀",
    "Awesome effort! 🎉",
    "You're a superstar! ⭐",
    "Fantastic progress! 🔥",
    "Legend status! 👑",
  ];

  const randomCompliment =
    compliments[Math.floor(Math.random() * compliments.length)];
  const notification = document.createElement("div");
  notification.className = "alert alert-success alert-dismissible fade show";
  notification.innerHTML = `
    <strong>${randomCompliment}</strong>
    <button type="button" class="btn-close" data-bs-dismiss="alert">
  `;

  const mainContent = document.querySelector("main");
  if (mainContent) {
    mainContent.insertBefore(notification, mainContent.firstChild);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
}

function triggerConfetti() {
  // Simple confetti effect using emoji
  const confetti = ["🎉", "🎊", "🎈", "⭐", "✨", "🌟"];
  const container = document.createElement("div");

  for (let i = 0; i < 20; i++) {
    const emoji = document.createElement("div");
    emoji.textContent = confetti[Math.floor(Math.random() * confetti.length)];
    emoji.style.position = "fixed";
    emoji.style.left = Math.random() * 100 + "%";
    emoji.style.top = "-20px";
    emoji.style.fontSize = "2em";
    emoji.style.pointerEvents = "none";
    emoji.style.zIndex = "9998";
    document.body.appendChild(emoji);

    // Animate falling
    let top = -20;
    const interval = setInterval(() => {
      top += Math.random() * 5 + 2;
      emoji.style.top = top + "px";
      if (top > window.innerHeight) {
        clearInterval(interval);
        emoji.remove();
      }
    }, 20);
  }
}

