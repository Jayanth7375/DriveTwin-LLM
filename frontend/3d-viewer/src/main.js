import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { ViewHelper } from 'three/addons/helpers/ViewHelper.js';
import { applyIndustrialMaterials } from './materials.js';
import { getPartInfo, ZONES } from './partInfo.js';
import './style.css';

// --- DOM refs -----------------------------------------------------------
const canvas       = document.getElementById('viewport');
const loadingEl    = document.getElementById('loading');
const progressBar  = document.getElementById('progress-bar');
const loadingDetail= document.getElementById('loading-detail');
const statsEl      = document.getElementById('stats');
const explodeSlider  = document.getElementById('explode-slider');
const explodeValueEl = document.getElementById('explode-value');
const rotateBtnAuto  = document.getElementById('rotate-auto');
const rotateBtnLeft  = document.getElementById('rotate-left');
const rotateBtnRight = document.getElementById('rotate-right');
const infoPanel    = document.getElementById('info-panel');
const infoPanelClose = document.getElementById('info-close');
const infoBadge    = document.getElementById('info-zone-badge');
const infoName     = document.getElementById('info-name');
const infoDesc     = document.getElementById('info-desc');
const infoSpecsTbody = document.querySelector('#info-specs tbody');
const hoverLabel   = document.getElementById('hover-label');

// --- State --------------------------------------------------------------
const modelCenter  = new THREE.Vector3();
let   modelRadius  = 0;
const initCamPos   = new THREE.Vector3();
const initCamTarget = new THREE.Vector3();

const raycaster    = new THREE.Raycaster();
raycaster.firstHitOnly = true;
const pointer      = new THREE.Vector2(-9999, -9999);
let   allMeshes    = [];
let   hoveredMesh  = null;
let   selectedMesh = null;
let   pointerDownX = 0;
let   pointerDownY = 0;

// --- Renderer -----------------------------------------------------------
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
const basePixelRatio = Math.min(window.devicePixelRatio, 2);
renderer.setPixelRatio(basePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.shadowMap.autoUpdate = false;
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.toneMappingExposure = 0.9;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.autoClear = false;  // cleared manually so ViewHelper doesn't wipe scene

const clock = new THREE.Clock();

// --- Scene --------------------------------------------------------------
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0c0f14);
scene.fog = new THREE.Fog(0x0c0f14, 4000, 14000);

const pmremGenerator = new THREE.PMREMGenerator(renderer);
scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.7;

// --- Camera -------------------------------------------------------------
const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 1, 100000);
camera.position.set(2600, 1900, 2800);

// --- Controls -----------------------------------------------------------
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.screenSpacePanning = true;
controls.zoomToCursor = true;

controls.mouseButtons = {
  LEFT:   THREE.MOUSE.ROTATE,
  MIDDLE: THREE.MOUSE.ROTATE,
  RIGHT:  THREE.MOUSE.PAN,
};
controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };

canvas.addEventListener('pointerdown', (e) => {
  pointerDownX = e.clientX;
  pointerDownY = e.clientY;
  if (e.button === 1) {
    controls.mouseButtons.MIDDLE = e.shiftKey ? THREE.MOUSE.PAN : THREE.MOUSE.ROTATE;
  }
}, { capture: true });

// --- Navigation Gizmo ---------------------------------------------------
const viewHelper = new ViewHelper(camera, canvas);
viewHelper.setLabels('X', 'Y', 'Z');
viewHelper.location = { top: null, right: 20, bottom: 110, left: null };

canvas.addEventListener('pointerup', (e) => {
  if (viewHelper.handleClick(e)) {
    controls.enabled = false;
    requestRender();
  }
});

// Resolution drop during drag (HiDPI performance)
let resolutionRestoreTimer = null;
controls.addEventListener('start', () => {
  clearTimeout(resolutionRestoreTimer);
  renderer.setPixelRatio(1);
});
controls.addEventListener('end', () => {
  resolutionRestoreTimer = setTimeout(() => {
    renderer.setPixelRatio(basePixelRatio);
    requestRender();
  }, 150);
});

// --- Explode view -------------------------------------------------------
let explodeParts   = [];
const EXPLODE_SCALE = 1.4;
let targetExplode  = 0;
let currentExplode = 0;
let explodeSettled = true;

explodeSlider.addEventListener('input', () => {
  targetExplode = Number(explodeSlider.value) / 100;
  explodeValueEl.textContent = `${explodeSlider.value}%`;
  requestRender();
});

// --- Auto-rotation controls ---------------------------------------------
controls.autoRotate = false;
controls.autoRotateSpeed = 1.5;

function setAutoSpin(on) {
  controls.autoRotate = on;
  rotateBtnAuto.classList.toggle('spinning', on);
  if (on) requestRender();
}

rotateBtnAuto.addEventListener('click', () => setAutoSpin(!controls.autoRotate));

function nudge(sign) {
  const angle = ((2 * Math.PI) / 60) * sign * 0.8;
  controls.object.position.sub(controls.target);
  const cos = Math.cos(angle), sin = Math.sin(angle);
  const { x, z } = controls.object.position;
  controls.object.position.x = cos * x + sin * z;
  controls.object.position.z = -sin * x + cos * z;
  controls.object.position.add(controls.target);
  controls.object.lookAt(controls.target);
  requestRender();
}
rotateBtnLeft.addEventListener('click',  () => nudge(1));
rotateBtnRight.addEventListener('click', () => nudge(-1));

function orbitStep(dTheta, dPhi) {
  const offset = new THREE.Vector3().subVectors(camera.position, controls.target);
  const sph = new THREE.Spherical().setFromVector3(offset);
  sph.theta += dTheta;
  sph.phi = Math.max(0.01, Math.min(Math.PI - 0.01, sph.phi + dPhi));
  offset.setFromSpherical(sph);
  camera.position.copy(controls.target).add(offset);
  camera.lookAt(controls.target);
  controls.update();
  requestRender();
}

function zoomStep(factor) {
  const dir = new THREE.Vector3().subVectors(camera.position, controls.target);
  const newLen = Math.max(controls.minDistance, Math.min(controls.maxDistance, dir.length() * factor));
  camera.position.copy(controls.target).addScaledVector(dir.normalize(), newLen);
  controls.update();
  requestRender();
}

function setPresetView(type) {
  if (!modelRadius) return;
  const d = modelRadius * 2.5;
  const c = modelCenter;
  const presets = {
    front:  [c.x,       c.y,       c.z + d        ],
    back:   [c.x,       c.y,       c.z - d        ],
    right:  [c.x + d,   c.y,       c.z            ],
    left:   [c.x - d,   c.y,       c.z            ],
    top:    [c.x,       c.y + d,   c.z + d * 0.001],
    bottom: [c.x,       c.y - d,   c.z + d * 0.001],
    home:   [initCamPos.x, initCamPos.y, initCamPos.z],
  };
  const p = presets[type];
  if (!p) return;
  camera.position.set(p[0], p[1], p[2]);
  controls.target.copy(type === 'home' ? initCamTarget : c);
  controls.update();
  requestRender();
}

let autoSpinWasOn = false;
controls.addEventListener('start', () => {
  autoSpinWasOn = controls.autoRotate;
  if (controls.autoRotate) setAutoSpin(false);
});
controls.addEventListener('end', () => {
  if (autoSpinWasOn) setAutoSpin(true);
});

const STEP = Math.PI / 12;
window.addEventListener('keydown', (e) => {
  if (e.target !== document.body && e.target !== canvas) return;
  if (e.key === 'Escape') { deselectPart(); return; }
  if (e.key === 'r' || e.key === 'R') { setAutoSpin(!controls.autoRotate); return; }
  if (e.key === 'ArrowLeft')  { nudge(1);  return; }
  if (e.key === 'ArrowRight') { nudge(-1); return; }

  if (e.code === 'Numpad1') { e.preventDefault(); setPresetView(e.ctrlKey ? 'back'   : 'front');  return; }
  if (e.code === 'Numpad3') { e.preventDefault(); setPresetView(e.ctrlKey ? 'left'   : 'right');  return; }
  if (e.code === 'Numpad7') { e.preventDefault(); setPresetView(e.ctrlKey ? 'bottom' : 'top');    return; }
  if (e.code === 'Numpad0') { e.preventDefault(); setPresetView('home'); return; }
  if (e.key === '.' && !e.ctrlKey && !e.altKey) { setPresetView('home'); return; }

  if (e.code === 'Numpad4') { e.preventDefault(); orbitStep( STEP, 0);     return; }
  if (e.code === 'Numpad6') { e.preventDefault(); orbitStep(-STEP, 0);     return; }
  if (e.code === 'Numpad8') { e.preventDefault(); orbitStep(0, -STEP);     return; }
  if (e.code === 'Numpad2') { e.preventDefault(); orbitStep(0,  STEP);     return; }

  if (e.code === 'NumpadAdd')      { e.preventDefault(); zoomStep(1 / 1.25); return; }
  if (e.code === 'NumpadSubtract') { e.preventDefault(); zoomStep(1.25);     return; }
});

// --- Lighting -----------------------------------------------------------
const hemiLight = new THREE.HemisphereLight(0xcfe0ff, 0x33312c, 0.5);
scene.add(hemiLight);

// Key light — warm sun from top-front-right
const sunLight = new THREE.DirectionalLight(0xfff8f0, 1.6);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);

// Fill light — cool from left
const fillLight = new THREE.DirectionalLight(0xcfe8ff, 0.4);
scene.add(fillLight);

// Rim / back light — cool blue from behind, creates edge definition on metallic parts
const rimLight = new THREE.DirectionalLight(0xb0ccff, 0.5);
scene.add(rimLight);

// --- Ground + grid ------------------------------------------------------
const groundMat = new THREE.MeshStandardMaterial({ color: 0x14181f, roughness: 0.95, metalness: 0.0 });
const ground = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), groundMat);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

let grid = new THREE.GridHelper(1, 1, 0x3a4250, 0x1c222c);
scene.add(grid);

// --- Loading ------------------------------------------------------------
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/gltf/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

gltfLoader.load(
  '/models/c18.glb',
  (gltf) => onModelLoaded(gltf),
  (xhr) => {
    if (xhr.total) {
      const pct = (xhr.loaded / xhr.total) * 100;
      progressBar.style.width = `${pct.toFixed(1)}%`;
      loadingDetail.textContent = `${pct.toFixed(0)}%  (${(xhr.loaded / 1048576).toFixed(1)} / ${(xhr.total / 1048576).toFixed(1)} MB)`;
    } else {
      loadingDetail.textContent = `${(xhr.loaded / 1048576).toFixed(1)} MB loaded`;
    }
  },
  (err) => {
    loadingDetail.textContent = 'Failed to load model — see console';
    console.error('GLTF load error:', err);
  }
);

function onModelLoaded(gltf) {
  const model = gltf.scene;

  applyIndustrialMaterials(model);

  let triangles = 0;
  let meshCount = 0;
  allMeshes = [];

  model.traverse((obj) => {
    if (obj.isMesh) {
      obj.castShadow = true;
      obj.receiveShadow = true;
      allMeshes.push(obj);
      meshCount++;
      const geo = obj.geometry;
      if (geo.index) triangles += geo.index.count / 3;
      else if (geo.attributes.position) triangles += geo.attributes.position.count / 3;
    }
  });

  scene.add(model);

  const box = new THREE.Box3().setFromObject(model);
  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);

  const maxDim = Math.max(size.x, size.y, size.z);
  const radius = box.getBoundingSphere(new THREE.Sphere()).radius;

  explodeParts = [];
  model.traverse((obj) => {
    if (!obj.isMesh) return;
    const partCenter = new THREE.Box3().setFromObject(obj).getCenter(new THREE.Vector3());
    explodeParts.push({
      obj,
      home: obj.position.clone(),
      dir: partCenter.sub(center),
    });
  });

  const dist = radius * 2.1;
  camera.position.set(center.x + dist * 0.55, center.y + dist * 0.5, center.z + dist * 0.7);
  camera.near = Math.max(maxDim / 1000, 0.1);
  camera.far = maxDim * 12;
  camera.updateProjectionMatrix();

  controls.target.copy(center);
  controls.minDistance = radius * 0.05;
  controls.maxDistance = radius * 6;
  controls.update();

  modelCenter.copy(center);
  modelRadius = radius;
  initCamPos.copy(camera.position);
  initCamTarget.copy(center);

  const sunDist = maxDim * 1.2;
  sunLight.position.set(center.x + sunDist * 0.6, center.y + sunDist * 1.1, center.z + sunDist * 0.8);
  sunLight.target.position.copy(center);
  scene.add(sunLight.target);

  const shadowExtent = maxDim * 0.75;
  sunLight.shadow.camera.left   = -shadowExtent;
  sunLight.shadow.camera.right  =  shadowExtent;
  sunLight.shadow.camera.top    =  shadowExtent;
  sunLight.shadow.camera.bottom = -shadowExtent;
  sunLight.shadow.camera.near   = maxDim * 0.05;
  sunLight.shadow.camera.far    = maxDim * 4;
  sunLight.shadow.camera.updateProjectionMatrix();

  fillLight.position.set(center.x - sunDist * 0.8, center.y + sunDist * 0.4, center.z - sunDist * 0.6);
  fillLight.target.position.copy(center);
  scene.add(fillLight.target);

  // Rim light from opposite/behind — slightly elevated, opposite side from sun
  rimLight.position.set(center.x - sunDist * 0.4, center.y + sunDist * 0.2, center.z - sunDist * 1.0);
  rimLight.target.position.copy(center);
  scene.add(rimLight.target);

  const groundSize = maxDim * 4;
  ground.geometry.dispose();
  ground.geometry = new THREE.PlaneGeometry(groundSize, groundSize);
  ground.position.set(center.x, box.min.y - maxDim * 0.001, center.z);

  scene.remove(grid);
  grid.geometry.dispose();
  grid = new THREE.GridHelper(groundSize, 40, 0x4a5568, 0x1c222c);
  grid.position.set(center.x, box.min.y - maxDim * 0.0008, center.z);
  grid.material.opacity = 0.35;
  grid.material.transparent = true;
  scene.add(grid);

  scene.fog.near = radius * 2.5;
  scene.fog.far  = radius * 9;

  statsEl.textContent = [
    `Objects: ${meshCount}`,
    `Triangles: ${Math.round(triangles).toLocaleString()}`,
    `Format: GLB (Draco compressed)`,
  ].join('\n');

  renderer.compile(scene, camera);
  renderer.shadowMap.needsUpdate = true;

  explodeSlider.disabled = false;
  explodeSlider.value = '0';
  explodeValueEl.textContent = '0%';

  // Wire up part interaction now that allMeshes is ready
  canvas.addEventListener('pointermove', onPointerMove);
  canvas.addEventListener('click', onCanvasClick);
  infoPanelClose.addEventListener('click', deselectPart);

  loadingEl.classList.add('hidden');
  requestRender();
}

// --- Resize -------------------------------------------------------------
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  requestRender();
});

// ═══════════════════════════════════════════════════════════════════════════
// Part interaction — hover label + info panel
// ═══════════════════════════════════════════════════════════════════════════

function getTopLevelMesh(mesh) {
  // Prefer the parent node name if it looks like a real part name (has spaces or letters)
  // to handle cases where GLTF wraps meshes in group nodes.
  let node = mesh;
  while (node.parent && !node.parent.isScene) {
    if (node.parent.name && node.parent.name.length > 2) return node.parent;
    node = node.parent;
  }
  return mesh;
}

function partDisplayName(mesh) {
  const node = getTopLevelMesh(mesh);
  return node.name || mesh.name || 'Unknown Part';
}

function setEmissive(mesh, hexColor, intensity) {
  if (!mesh.material) return;
  if (!mesh.userData._origMat) {
    mesh.userData._origMat = mesh.material;
    mesh.material = mesh.material.clone();
  }
  mesh.material.emissive = new THREE.Color(hexColor);
  mesh.material.emissiveIntensity = intensity;
}

function clearEmissive(mesh) {
  if (!mesh || !mesh.userData._origMat) return;
  mesh.material.dispose();
  mesh.material = mesh.userData._origMat;
  delete mesh.userData._origMat;
}

function setHoverMesh(mesh) {
  if (mesh === hoveredMesh) return;
  // Clear previous hover (unless it's the selected mesh — selection highlight wins)
  if (hoveredMesh && hoveredMesh !== selectedMesh) clearEmissive(hoveredMesh);
  hoveredMesh = mesh;
  if (mesh && mesh !== selectedMesh) setEmissive(mesh, 0xffffff, 0.06);
  requestRender();
}

function selectPart(mesh) {
  if (selectedMesh === mesh) return;
  // Remove highlight from previous selection
  if (selectedMesh) clearEmissive(selectedMesh);
  selectedMesh = mesh;
  if (!mesh) { hideInfoPanel(); return; }
  setEmissive(mesh, 0xffcd00, 0.18);
  showInfoPanel(mesh);
  requestRender();
}

function deselectPart() {
  if (selectedMesh) {
    clearEmissive(selectedMesh);
    selectedMesh = null;
  }
  hideInfoPanel();
  requestRender();
}

function showInfoPanel(mesh) {
  const name = partDisplayName(mesh);
  const info = getPartInfo(name);
  const zone = ZONES[info.zone] || ZONES.structure;

  infoBadge.textContent = zone.label;
  infoBadge.style.background  = zone.color + '22';
  infoBadge.style.borderColor = zone.color + '55';
  infoBadge.style.color       = zone.color;
  infoBadge.className = 'zone-badge';

  infoName.textContent = info.name;
  infoDesc.textContent = info.desc;

  infoSpecsTbody.innerHTML = '';
  const entries = Object.entries(info.specs);
  if (entries.length) {
    for (const [k, v] of entries) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td class="spec-key">${k}</td><td class="spec-val">${v}</td>`;
      infoSpecsTbody.appendChild(tr);
    }
  }

  infoPanel.classList.add('open');
}

function hideInfoPanel() {
  infoPanel.classList.remove('open');
}

function onPointerMove(e) {
  // Normalised device coords
  pointer.x =  (e.clientX / window.innerWidth)  * 2 - 1;
  pointer.y = -(e.clientY / window.innerHeight) * 2 + 1;

  if (allMeshes.length === 0) return;

  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(allMeshes);

  if (hits.length > 0) {
    const hit = hits[0].object;
    setHoverMesh(hit);
    const name = partDisplayName(hit);
    hoverLabel.textContent = name;
    hoverLabel.style.display = 'block';
    hoverLabel.style.left = e.clientX + 'px';
    hoverLabel.style.top  = e.clientY + 'px';
  } else {
    setHoverMesh(null);
    hoverLabel.style.display = 'none';
  }
}

function onCanvasClick(e) {
  // Ignore drag releases (more than 5 px movement = orbit, not click)
  const dx = e.clientX - pointerDownX;
  const dy = e.clientY - pointerDownY;
  if (Math.sqrt(dx * dx + dy * dy) > 5) return;

  pointer.x =  (e.clientX / window.innerWidth)  * 2 - 1;
  pointer.y = -(e.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(allMeshes);

  if (hits.length > 0) {
    selectPart(hits[0].object);
  } else {
    deselectPart();
  }
}

// --- Render loop (on-demand) -------------------------------------------
let renderNeeded = false;
function requestRender() { renderNeeded = true; }

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();

  // Pulse selected part's highlight with a slow sine wave
  if (selectedMesh && selectedMesh.material && selectedMesh.userData._origMat) {
    const pulse = 0.14 + 0.08 * Math.sin(clock.elapsedTime * 3.5);
    selectedMesh.material.emissiveIntensity = pulse;
    requestRender();
  }

  // Smooth explode — lerp currentExplode toward targetExplode
  const explodeDiff = targetExplode - currentExplode;
  if (Math.abs(explodeDiff) > 0.0002) {
    currentExplode += explodeDiff * Math.min(1, delta * 10);
    for (const part of explodeParts) {
      part.obj.position.copy(part.home).addScaledVector(part.dir, currentExplode * EXPLODE_SCALE);
    }
    explodeSettled = false;
    requestRender();
  } else if (!explodeSettled) {
    currentExplode = targetExplode;
    for (const part of explodeParts) {
      part.obj.position.copy(part.home).addScaledVector(part.dir, currentExplode * EXPLODE_SCALE);
    }
    renderer.shadowMap.needsUpdate = true;
    explodeSettled = true;
    requestRender();
  }

  // Drive the gizmo's smooth camera-snap animation
  const wasAnimating = viewHelper.animating;
  if (viewHelper.animating) {
    viewHelper.update(delta);
    requestRender();
  }
  if (wasAnimating && !viewHelper.animating) {
    controls.enabled = true;
  }

  const moved = controls.update();
  if (moved || renderNeeded) {
    viewHelper.center.copy(controls.target);
    renderer.clear();                        // explicit clear (autoClear = false)
    renderer.render(scene, camera);
    viewHelper.render(renderer);             // gizmo drawn on top without clearing
    renderNeeded = false;
  }
}
animate();
