window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        set_mantine_theme: function (update_theme) {
            if (update_theme) {
                theme = 'light'
            }
            else {
                theme = 'dark'
            }
            return theme
        },
        set_bootstrap_theme: function (switch_on) {
            document.documentElement.setAttribute("data-bs-theme", switch_on ? "light" : "dark");
            return window.dash_clientside.no_update
        },
    },
});
