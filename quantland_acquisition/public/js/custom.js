// console.log("Custom login JS loaded!");


(function() {
    const observer = new MutationObserver((mutations, obs) => {
        const nav = document.querySelector(".navbar.navbar-expand");
        if (nav && !document.querySelector("#home-custom-btn")) {
            let firstChild = nav.firstElementChild;
            const btn = document.createElement("button");
            btn.id = "home-custom-btn";
            btn.className = "btn btn-primary btn-sm";
            btn.style.marginRight = "10px";
            btn.style.marginLeft = "10px";
            btn.innerText = frappe._("Land Acquisition Workspace");

            btn.addEventListener("click", () => {
                window.location.href = "/app/jalsampada";
            });

            if (firstChild) {
                nav.insertBefore(btn, firstChild);
            } else {
                nav.appendChild(btn);
            }
            obs.disconnect();
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
})();

