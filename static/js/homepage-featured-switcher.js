(() => {
    const heroImage = document.getElementById("pf-featured-hero-image");
    const heroLink = document.getElementById("pf-featured-hero-link");
    const cardImage = document.getElementById("pf-featured-card-image");
    const cardLink = document.getElementById("pf-featured-link");
    const dots = Array.from(document.querySelectorAll(".pf-featured-dot"));
    const transfers = Array.isArray(window.PF_FEATURED_TRANSFERS)
        ? window.PF_FEATURED_TRANSFERS
        : [];

    if (!heroImage || !heroLink || dots.length === 0 || transfers.length === 0) {
        return;
    }

    const fallbackHero = heroImage.getAttribute("src") || "";
    const fallbackCard = cardImage ? (cardImage.getAttribute("src") || fallbackHero) : fallbackHero;

    const setText = (id, value) => {
        if (value === undefined || value === null) return;
        const element = document.getElementById(id);
        if (element) element.textContent = String(value);
    };

    const setImage = (element, src, alt, fallback) => {
        if (!element) return;
        element.onerror = () => {
            element.onerror = null;
            element.src = fallback;
        };
        element.src = src || fallback;
        element.alt = alt || "";
    };

    const setSlide = (index) => {
        const safeIndex = Number.isFinite(index) && index >= 0 && index < transfers.length
            ? index
            : 0;
        const item = transfers[safeIndex] || transfers[0];
        if (!item) return;

        setImage(heroImage, item.heroImage, item.alt || item.name, fallbackHero);
        heroLink.href = item.link || "#";
        heroLink.setAttribute("aria-label", `Открыть трансфер ${item.name || ""}`);

        setImage(cardImage, item.cardImage || item.heroImage, item.alt || item.name, fallbackCard);
        if (cardLink) cardLink.href = item.link || "#";

        setText("pf-featured-name", item.name);
        setText("pf-featured-route", item.route);
        setText("pf-featured-fee", item.fee);
        setText("pf-featured-source", item.source);
        setText("pf-featured-chart-value", item.chartValue);
        setText("pf-featured-chart-label", item.chartLabel);
        setText("pf-featured-status", item.status);

        const statusElement = document.getElementById("pf-featured-status");
        if (statusElement && item.statusClass) {
            Array.from(statusElement.classList)
                .filter((name) => name.startsWith("pf-badge--"))
                .forEach((name) => statusElement.classList.remove(name));
            statusElement.classList.add(item.statusClass);
        }

        dots.forEach((dot, dotIndex) => {
            const active = dotIndex === safeIndex;
            dot.classList.toggle("is-active", active);
            dot.setAttribute("aria-pressed", active ? "true" : "false");
        });
    };

    dots.forEach((dot) => {
        dot.addEventListener("click", () => {
            setSlide(Number(dot.dataset.featuredIndex || 0));
        });
    });

    // Every page load starts from slot 0. This guarantees that the art
    // approved in the local admin remains the first slide after F5/Ctrl+F5.
    setSlide(0);
})();
