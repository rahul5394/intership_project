
const profileBtn = document.getElementById("profileBtn");
const profileBtnMobile = document.getElementById("profileBtnMobile");
const profileCard = document.getElementById("profileCard");
const hamburger = document.getElementById("hamburger");
const mobileMenu = document.getElementById("mobileMenu");
const detailPanel = document.getElementById("detailPanel");


// Convert dict → HTML list
function dictToHTML(obj) {
  if (!obj || typeof obj !== 'object') return "<p>No data available.</p>";

  let html = `<ul class="detail-list">`;
  for (const key in obj) {
    const displayKey = key.replace(/_/g, " ").toUpperCase();
    html += `
      <li>
        <strong>${displayKey}:</strong>
        ${obj[key]}
      </li>
    `;
  }
  html += `</ul>`;
  return html;
}


// Convert Food Suggestion array/text → Proper Horizontal List
function listToHTML(data) {
  if (!data) return "<p>No data available.</p>";

  let foods = [];

  // Handle if data is an array
  if (Array.isArray(data)) {
    foods = data
      .map(item => String(item).trim())
      .filter(item => item.length > 1); // Filter out empty or single char items
  }
  // Handle if data is a string
  else if (typeof data === 'string') {
    // Split by newlines, commas, or bullet points
    foods = data
      .split(/[\n,•\-*]+/)  // Split by newline, comma, bullet, dash, asterisk
      .map(f => f.trim())
      .filter(f => f.length > 1); // Filter out single characters
  }

  if (foods.length === 0) {
    return "<p>No food suggestions available.</p>";
  }

  // Create horizontal food tags
  return `
    <div class="food-list-horizontal">
      ${foods.map(f => `<span class="food-item">${f}</span>`).join("")}
    </div>
  `;
}


// DETAIL PANEL CONTENT (Dynamic from Flask)
const cardDetails = {
  diet: {
    icon: "❤",
    iconClass: "bg-gradient-red",
    title: "Your Diet Plan",
    content: dictToHTML(typeof realDiet !== 'undefined' ? realDiet : null)
  },

  routine: {
    icon: "💪",
    iconClass: "bg-gradient-orange",
    title: "Daily Routine",
    content: dictToHTML(typeof realRoutine !== 'undefined' ? realRoutine : null)
  },

  history: {
    icon: "🥗",
    iconClass: "bg-gradient-green",
    title: "Food Suggestions",
    content: listToHTML(typeof realFoods !== 'undefined' ? realFoods : null)
  }
};


// OPEN RIGHT PANEL
function showCardDetails(cardType) {
  const details = cardDetails[cardType];
  if (!details) return;

  document.getElementById('detailIcon').className =
    `detail-panel__icon ${details.iconClass}`;

  document.getElementById('detailIcon').textContent = details.icon;
  document.getElementById('detailTitle').textContent = details.title;
  document.getElementById('detailContent').innerHTML = details.content;

  profileCard.style.display = 'none';
  detailPanel.style.display = 'block';
}


// PROFILE PANEL SHOW/HIDE
function toggleProfile(e) {
  e.stopPropagation();
  const isVisible = profileCard.style.display === "block";

  detailPanel.style.display = "none";
  profileCard.style.display = isVisible ? "none" : "block";
}

profileBtn.onclick = toggleProfile;
if (profileBtnMobile) profileBtnMobile.onclick = toggleProfile;


// CLICK OUTSIDE → CLOSE PANELS
document.addEventListener("click", e => {
  if (!profileCard.contains(e.target) && e.target !== profileBtn && e.target !== profileBtnMobile) {
    profileCard.style.display = "none";
  }

  if (!detailPanel.contains(e.target) && !e.target.closest(".card")) {
    detailPanel.style.display = "none";
  }
});


// MOBILE MENU TOGGLE
hamburger.onclick = function (e) {
  e.stopPropagation();
  mobileMenu.style.display =
    mobileMenu.style.display === "flex" ? "none" : "flex";
};

document.addEventListener("click", e => {
  if (!mobileMenu.contains(e.target) && e.target !== hamburger) {
    mobileMenu.style.display = "none";
  }
});