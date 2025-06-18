import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.148.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.148.0/examples/jsm/controls/OrbitControls.js';



// main.js
const scene = new THREE.Scene();
scene.background = new THREE.CubeTextureLoader().load([
  'assets/textures/space_right.png',
  'assets/textures/space_left.png',
  'assets/textures/space_top.png',
  'assets/textures/space_bottom.png',
  'assets/textures/space_front.png',
  'assets/textures/space_back.png'
]);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("solarCanvas"), antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
scene.add(ambientLight);
const pointLight = new THREE.PointLight(0xffffff, 1.5, 300);
scene.add(pointLight);

// Helper: create planet with orbit
function createPlanet({ name, size, distance, color, speed }) {
  const geometry = new THREE.SphereGeometry(size, 64, 64);
  const material = new THREE.MeshStandardMaterial({ color });
  const planet = new THREE.Mesh(geometry, material);

  planet.userData = { name, speed, distance };
  planet.position.x = distance;

  scene.add(planet);
  return planet;
}

// Planets
const planets = [
  createPlanet({ name: "Mercury", size: 0.3, distance: 4, color: 0xaaaaaa, speed: 0.04 }),
  createPlanet({ name: "Venus", size: 0.5, distance: 6, color: 0xffddaa, speed: 0.015 }),
  createPlanet({ name: "Earth", size: 0.55, distance: 8, color: 0x2266ff, speed: 0.01 }),
  createPlanet({ name: "Mars", size: 0.4, distance: 10, color: 0xff3300, speed: 0.008 }),
  createPlanet({ name: "Jupiter", size: 1.2, distance: 13, color: 0xffaa66, speed: 0.005 }),
  createPlanet({ name: "Saturn", size: 1, distance: 16, color: 0xffcc99, speed: 0.004 }),
  createPlanet({ name: "Uranus", size: 0.8, distance: 19, color: 0x66ffff, speed: 0.002 }),
  createPlanet({ name: "Neptune", size: 0.8, distance: 22, color: 0x3366ff, speed: 0.001 })
];

// Sun
const sunGeometry = new THREE.SphereGeometry(2, 64, 64);
const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
const sun = new THREE.Mesh(sunGeometry, sunMaterial);
scene.add(sun);

// Orbit Rings
planets.forEach(planet => {
  const ringGeometry = new THREE.RingGeometry(planet.userData.distance - 0.01, planet.userData.distance + 0.01, 64);
  const ringMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
  const ring = new THREE.Mesh(ringGeometry, ringMaterial);
  ring.rotation.x = Math.PI / 2;
  scene.add(ring);
});

// Asteroid belt (between Mars and Jupiter)
for (let i = 0; i < 300; i++) {
  const asteroid = new THREE.Mesh(
    new THREE.SphereGeometry(Math.random() * 0.05, 6, 6),
    new THREE.MeshStandardMaterial({ color: 0x888888 })
  );
  const angle = Math.random() * Math.PI * 2;
  const radius = 11 + Math.random() * 2;
  asteroid.position.set(
    Math.cos(angle) * radius,
    (Math.random() - 0.5) * 0.5,
    Math.sin(angle) * radius
  );
  scene.add(asteroid);
}

// Camera
camera.position.z = 30;

// Animate
function animate() {
  requestAnimationFrame(animate);
  planets.forEach((planet, i) => {
    const t = Date.now() * 0.0001 * planet.userData.speed;
    planet.position.x = Math.cos(t) * planet.userData.distance;
    planet.position.z = Math.sin(t) * planet.userData.distance;
    planet.rotation.y += 0.01;
  });
  sun.rotation.y += 0.002;
  controls.update();
  renderer.render(scene, camera);
}
animate();

// Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
