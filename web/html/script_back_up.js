var svgManager = new THREE.LegacySVGLoader();
var url = 'models/svg/white-output.svg';

function svg_loading_done_callback(doc) {
  init(new THREE.SVGObject(doc));
  console.log('Loaded')
  animate();
};

svgManager.load(url,
  svg_loading_done_callback,
  function() {
    console.log("Loading SVG...");
  },
  function() {
    console.log("Error loading SVG!");
  });

var camera, scene, renderer;

function init(svgObject) {
  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 100000);
  camera.position.z = 1500;

  svgObject.position.x = Math.random() * innerWidth;
  svgObject.position.y = 200;
  svgObject.position.z = Math.random() * 10000 - 5000;
  svgObject.scale.x = svgObject.scale.y = svgObject.scale.z = 0.01;

  scene = new THREE.Scene();
  scene.add(svgObject);

  var ambient = new THREE.AmbientLight(0x80ffff);
  scene.add(ambient);
  var directional = new THREE.DirectionalLight(0xffff00);
  directional.position.set(-1, 0.5, 0);
  scene.add(directional);
  renderer = new THREE.SVGRenderer();
  renderer.setClearColor(0xf0f0f0);
  renderer.setSize(window.innerWidth, window.innerHeight - 5);
  document.body.appendChild(renderer.domElement);

  window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
  requestAnimationFrame(animate);
  render();
}

function render() {
  camera.position.x = 0;
  camera.position.z = 0;
  camera.lookAt(scene.position);
  renderer.render(scene, camera);
}