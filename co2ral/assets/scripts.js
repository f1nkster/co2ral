// This snippet below replaces the favicon.ico of dash - a black filled circle - with the UI icon
window.onload = function () {
    console.log('Document loading...');
    var link = document.querySelector("link[rel~='icon']");
    if (!link) {
        link = document.createElement('link');
        link.rel = 'icon';
        document.head.appendChild(link);
    }
    link.href = 'assets/favicon.ico';
}
