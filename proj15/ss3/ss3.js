const infoBox = document.getElementById("infoBox");

document.querySelectorAll(".planet").forEach(planet => {
  planet.addEventListener("mouseenter", () => {
    infoBox.style.display = "block";
    infoBox.innerText = "Planet: " + planet.classList[1];
  });
  planet.addEventListener("mouseleave", () => {
    infoBox.style.display = "none";
  });
});
