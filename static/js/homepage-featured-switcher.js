(() => {
    const heroImage = document.getElementById("pf-featured-hero-image");
    const heroLink = document.getElementById("pf-featured-hero-link");
    const dots = Array.from(document.querySelectorAll(".pf-featured-dot"));
    const transfers = Array.isArray(window.PF_FEATURED_TRANSFERS) ? window.PF_FEATURED_TRANSFERS : [];

    if (!heroImage || !heroLink || dots.length === 0 || transfers.length === 0) {
        return;
    }

    const fallbackHero = heroImage.getAttribute("src");

    const setHeroSlide = (index, save = true) => {
        const item = transfers[index] || transfers[0];
        if (!item) return;

        heroImage.onerror = () => {
            heroImage.onerror = null;
            heroImage.src = fallbackHero;
        };

        heroImage.src = item.heroImage || fallbackHero;
        heroImage.alt = item.alt || "";
        heroLink.href = item.link || "#";
        heroLink.setAttribute("aria-label", `Открыть трансфер ${item.name || ""}`);

        dots.forEach((dot, dotIndex) => {
            const active = dotIndex === index;
            dot.classList.toggle("is-active", active);
            dot.setAttribute("aria-pressed", active ? "true" : "false");
        });

        if (save) {
            try {
                sessionStorage.setItem("pfHomepageHeroSliderIndex", String(index));
            } catch (_) {}
        }
    };

    dots.forEach((dot) => {
        dot.addEventListener("click", () => {
            const index = Number(dot.dataset.featuredIndex || 0);
            setHeroSlide(index);
        });
    });

    let savedIndex = 0;
    try {
        savedIndex = Number(sessionStorage.getItem("pfHomepageHeroSliderIndex") || 0);
    } catch (_) {
        savedIndex = 0;
    }

    if (!Number.isFinite(savedIndex) || savedIndex < 0 || savedIndex >= transfers.length) {
        savedIndex = 0;
    }

    setHeroSlide(savedIndex, false);
})();
