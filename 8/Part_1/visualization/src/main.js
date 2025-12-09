import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

async function initScene() {
    // Load data
    const response = await fetch("/circuit_data.json");
    const data = await response.json();
    const points = data.points;
    const edges = data.edges;

    // Compute bounding box
    let minX = Infinity, minY = Infinity, minZ = Infinity;
    let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;

    points.forEach(([x, y, z]) => {
        minX = Math.min(minX, x); minY = Math.min(minY, y); minZ = Math.min(minZ, z);
        maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); maxZ = Math.max(maxZ, z);
    });

    const centerX = (minX + maxX) / 2;
    const centerY = (minY + maxY) / 2;
    const centerZ = (minZ + maxZ) / 2;

    const sizeX = maxX - minX;
    const sizeY = maxY - minY;
    const sizeZ = maxZ - minZ;
    const maxSize = Math.max(sizeX, sizeY, sizeZ);

    // Center points
    const centeredPoints = points.map(([x, y, z]) => [
        x - centerX,
        y - centerY,
        z - centerZ,
    ]);

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x202020);

    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        maxSize * 10 // ajusté pour graphe très grand
    );

    // Position camera loin pour voir tout le graphe
    camera.position.set(0, 0, maxSize * 1.5);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = maxSize * 5; // pour permettre zoom arrière
    controls.minDistance = maxSize * 0.1; // pour zoom avant

    // Axes helper
    scene.add(new THREE.AxesHelper(maxSize));

    // Points
    const sphereGeometry = new THREE.SphereGeometry(maxSize * 0.01, 16, 16);
    const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0xffaa00 });
    centeredPoints.forEach((p) => {
        const mesh = new THREE.Mesh(sphereGeometry, sphereMaterial);
        mesh.position.set(...p);
        scene.add(mesh);
    });

    // Edges
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x00aaff });
    edges.forEach(([i, j]) => {
        const geometry = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(...centeredPoints[i]),
            new THREE.Vector3(...centeredPoints[j]),
        ]);
        const line = new THREE.Line(geometry, lineMaterial);
        scene.add(line);
    });

    // Animate
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

await initScene();
