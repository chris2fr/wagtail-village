window.addEventListener(
  "pagehide",
  (event) => {
    if (document.getElementById('menu-checkbox')) {
      if (document.getElementById('menu-checkbox').checked) {
        localStorage.setItem('menuopen', true);
        localStorage.removeItem('menuclosed');
        window.scrollTo(0, 0);
      } else {
        localStorage.setItem('menuclosed', true);
        localStorage.removeItem('menuopen');
      }
    }
  },
  false,
);

if (document.getElementById('menu-checkbox')) {
  if (localStorage.getItem('menuopen')) {
    document.getElementById('menu-checkbox').checked=true;
  } else if (! localStorage.getItem('menuclosed')) { // Default is open
    document.getElementById('menu-checkbox').checked=true;
  }
}

