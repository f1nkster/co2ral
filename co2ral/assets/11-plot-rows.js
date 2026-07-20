/* Row-based drag layout for the explorer plots: tiles snap to half width when they share
   a row and to the full width when they stand alone. Empty drop zones before, between and
   after the rows accept a tile to give it a row — and so the full width — of its own.
   Widths follow purely from the row structure (CSS flex), so a drop never needs a rebuild:
   the arrangement is only persisted to the layout store, which the server reads on the
   next render. */
window.co2ralPlotRows = (function () {
    function tilesIn(row) {
        return Array.from(row.children).filter(function (child) {
            return child.classList.contains('plot-tile');
        });
    }

    function rowKeys(flow) {
        return Array.from(flow.querySelectorAll('.plot-row'))
            .map(function (row) {
                return tilesIn(row).map(function (tile) { return tile.getAttribute('data-key'); });
            })
            .filter(function (keys) { return keys.length > 0; });
    }

    function makeZone() {
        var zone = document.createElement('div');
        zone.className = 'plot-row plot-drop-zone';
        return zone;
    }

    /* Removes emptied rows and rebuilds the drop zones, so there is exactly one before,
       between and after the rows; then (re)attaches the drag behaviour everywhere. */
    function normalize(flow) {
        Array.from(flow.querySelectorAll('.plot-row')).forEach(function (row) {
            if (row._sortable) {
                row._sortable.destroy();
                row._sortable = null;
            }
            if (tilesIn(row).length === 0) {
                row.remove();
            } else {
                row.classList.remove('plot-drop-zone');
            }
        });
        var rows = Array.from(flow.querySelectorAll('.plot-row'));
        flow.insertBefore(makeZone(), flow.firstChild);
        rows.forEach(function (row) {
            flow.insertBefore(makeZone(), row.nextSibling);
        });
        attach(flow);
    }

    function attach(flow) {
        Array.from(flow.querySelectorAll('.plot-row')).forEach(function (row) {
            row._sortable = window.Sortable.create(row, {
                group: 'co2ral-plots',
                handle: '.plot-title-badge',
                draggable: '.plot-tile',
                animation: 150,
                onMove: function (evt) {
                    // A row is full with two tiles; block a third instead of overflowing.
                    var resident = tilesIn(evt.to).filter(function (tile) { return tile !== evt.dragged; });
                    return resident.length < 2;
                },
                onStart: function () {
                    flow.classList.add('plot-dragging');
                },
                onEnd: function () {
                    flow.classList.remove('plot-dragging');
                    window.dash_clientside.set_props('plot-layout-store', { data: rowKeys(flow) });
                    normalize(flow);
                }
            });
        });
    }

    /* Runs after every render of the plots container; normalize() is idempotent, so
       re-running it on a reused flow element just refreshes zones and drag handlers. */
    function init() {
        var flow = document.getElementById('plot-flow');
        if (!flow || !window.Sortable) { return; }
        normalize(flow);
    }

    return { init: init };
})();
