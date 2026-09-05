(function () {
    "use strict";

    function boot() {
        document
            .querySelectorAll(
                "[data-pf-league-selector='398T']"
            )
            .forEach(function (selector) {
                var buttons = Array.from(
                    selector.querySelectorAll(
                        ".pf-league-selector__item"
                    )
                );

                buttons.forEach(function (button) {
                    button.addEventListener(
                        "click",
                        function () {
                            buttons.forEach(
                                function (item) {
                                    item.classList.remove(
                                        "is-active"
                                    );
                                    item.setAttribute(
                                        "aria-pressed",
                                        "false"
                                    );
                                }
                            );

                            button.classList.add(
                                "is-active"
                            );
                            button.setAttribute(
                                "aria-pressed",
                                "true"
                            );

                            var detail = {
                                leagueId:
                                    button.dataset
                                        .leagueId || "",
                                leagueSlug:
                                    button.dataset
                                        .leagueSlug || "",
                                leagueName:
                                    button.dataset
                                        .leagueName || ""
                            };

                            selector.dataset
                                .selectedLeague =
                                detail.leagueSlug;

                            selector.dispatchEvent(
                                new CustomEvent(
                                    "pf:league-selected",
                                    {
                                        bubbles: true,
                                        detail: detail
                                    }
                                )
                            );
                        }
                    );
                });
            });
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            boot
        );
    } else {
        boot();
    }
})();
