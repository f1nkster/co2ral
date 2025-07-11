window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        select_all_or_none: function (selectNone, selectAll, options, value) {
            let out = [];
            const triggered_id = dash_clientside.callback_context.triggered[0].prop_id;

            if (triggered_id.includes("select-all")) {
                if (options.length > 0) {
                    if (typeof options[0] === 'object') {
                        out = options.map(i => i.value);
                    } else {
                        out = options;
                    }
                }
            }

            // if selected-none is clicked it will return an empty array automatically, no need for condition
            return out;
        },
        reset_all_checklists: function (reset, filter_options) {
            const triggered_id = dash_clientside.callback_context.triggered[0].prop_id;

            if (triggered_id.includes("reset")) {
                out = filter_options.map(innerArray => innerArray.map(d => d.value));
                return out;
            }
            else {
                return dash_clientside.no_update;
            }
        },
        get_checklist_color: function (value, options) {
            let color = "gray";
            if (options.length > 0) {
                if (typeof options[0] === 'object') {
                    options = options.map(i => i.value);
                }
            }
            if (JSON.stringify(value.sort()) === JSON.stringify(options.sort())) {
                color = "gray";
            } else {
                color = "green";
            }
            if (value.length === 0 && options.length !== 0) {
                color = "red";
            }
            return color;
        },
        reset_slider: function (masterReset, minVal, maxVal, value) {
            const triggered_id = dash_clientside.callback_context.triggered[0].prop_id;

            if (triggered_id.includes("reset")) {
                value = minVal.map((item, index) => [item, maxVal[index]]);
            }
            return value;
        },
        format_gate_text: function (val) {
            const relativeValue = parseInt(val);
            const absoluteValue = (relativeValue / 10).toFixed(1);

            const text = `Relative: ${relativeValue} %\n` +
                `Absolute: ${absoluteValue} m\n`;

            const scaleFactor = val / 30;
            const dimension = (3 * scaleFactor).toFixed(2);
            const leftPosition = (20.8 - (dimension / 2)).toFixed(2);

            const style = {
                position: "absolute",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                left: `${leftPosition}vw`,
                backgroundColor: "rgba(46, 221, 40, 0.15)",
                width: `${dimension}vw`,
                height: `${dimension}vw`,
                marginTop: "-65px",
                borderRadius: "3px"
            };

            return [text, style];
        },
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
        change_ag_theme: function (switch_on) {
            let theme;
            if (switch_on) {
                theme = "ag-theme-alpine";
            } else {
                theme = "ag-theme-alpine-dark";
            }
            return theme;
        },
        dropdown_navigation: function (prev, next, value, options) {
            let optionsList = options.map(i => i.value);
            let index;
            const triggered_id = dash_clientside.callback_context.triggered[0].prop_id;

            if (!optionsList.includes(value)) {
                index = 0;
            } else {
                index = optionsList.indexOf(value);
            }

            if (triggered_id.includes("prev")) {
                index -= 1;
            }

            if (triggered_id.includes("next")) {
                index += 1;
            }

            value = optionsList[index];
            return value;
        },
        limit_checkbox_selection: function (selected_branch) {
            if (selected_branch.length > 2) {
                return selected_branch.slice(0, 2);
            }
            return selected_branch;
        },
        toggle_map_fullscreen: function (n_clicks) {
            if (n_clicks) {
                return [true];
            }
            return [false];
        },

    },

});
