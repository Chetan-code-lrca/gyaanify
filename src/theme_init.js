/* Apply the saved theme before CSS paints, preventing a saved-theme flash. */
(function () {
  var theme = null;
  try {
    var saved = window.localStorage.getItem("gy-theme");
    if (saved === "light" || saved === "dark") theme = saved;
  } catch (e) {
    /* Storage can be disabled; fall back to the system preference. */
  }
  if (!theme) {
    theme = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }
  document.documentElement.setAttribute("data-theme", theme);
  document.documentElement.style.colorScheme = theme;
})();
