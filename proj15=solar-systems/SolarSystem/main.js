
/*
// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("solarCanvas"), antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);
const pointLight = new THREE.PointLight(0xffffff, 2, 100);
scene.add(pointLight);

// Sun (glowing yellow sphere)
const sunGeometry = new THREE.SphereGeometry(2, 64, 64);
const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
const sun = new THREE.Mesh(sunGeometry, sunMaterial);
scene.add(sun);

// Earth
const earthGeometry = new THREE.SphereGeometry(0.5, 32, 32);
const earthMaterial = new THREE.MeshStandardMaterial({ color: 0x2266ff });
const earth = new THREE.Mesh(earthGeometry, earthMaterial);
earth.position.x = 5;
scene.add(earth);

// Camera position
camera.position.z = 10;

// Animate
function animate() {
  requestAnimationFrame(animate);

  // Rotate Earth around Sun
  earth.position.x = 5 * Math.cos(Date.now() * 0.001);
  earth.position.z = 5 * Math.sin(Date.now() * 0.001);

  // Rotate Sun
  sun.rotation.y += 0.001;

  renderer.render(scene, camera);
}
animate();

// Handle Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// this includes only a blue sphere around a yellow sphere
*/
