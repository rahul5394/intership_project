   const profileBtn = document.getElementById("profile-btn");
    const profileBtnMobile = document.getElementById("profile-btn-mobile");
    const profileCard = document.getElementById("profile-card");
    const hamburger = document.getElementById("hamburger");
    const mobileMenu = document.getElementById("mobile-menu");

    function toggleProfile(e) { e.stopPropagation(); profileCard.style.display = profileCard.style.display == "block" ? "none" : "block"; }
    profileBtn.onclick = toggleProfile; profileBtnMobile && (profileBtnMobile.onclick = toggleProfile);

    document.addEventListener("click", e => { if (!profileCard.contains(e.target) && e.target !== profileBtn && e.target !== profileBtnMobile) { profileCard.style.display = "none"; } });

    hamburger.onclick = function (e) { e.stopPropagation(); mobileMenu.style.display = mobileMenu.style.display == "flex" ? "none" : "flex"; };

    document.addEventListener("click", e => { if (!mobileMenu.contains(e.target) && e.target !== hamburger) { mobileMenu.style.display = "none"; } });
