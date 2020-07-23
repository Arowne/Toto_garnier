import { OrbitControls } from './jsm/controls/OrbitControls.js';

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

var camera, scene, renderer, orbit;

function init(svgObject) {
  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 100000);
  camera.position.z = 1500;

  scene = new THREE.Scene();

  var ambient = new THREE.AmbientLight(0x80ffff);
  scene.add(ambient);
  

  var directional = new THREE.DirectionalLight(0xffff00);
  directional.position.set(-1, 0.5, 0);
  scene.add(directional);

  renderer = new THREE.SVGRenderer();

  orbit = new OrbitControls( camera, renderer.domElement );
  orbit.update();

  renderer.setClearColor(0xf0f0f0);
  renderer.setSize(window.innerWidth, window.innerHeight - 5);
  document.body.appendChild(renderer.domElement);

  window.addEventListener('resize', onWindowResize, false);

  // instantiate a loader
  var loader = new THREE.TextureLoader();

  // load a resource
  loader.load(
    // resource URL
    'models/svg/colored-output.png',

    // onLoad callback
    ( texture )  => {

      console.log('load');

      // var geometry = new THREE.PlaneGeometry( 1000, 1000, 32 );
      // var material = new THREE.MeshBasicMaterial( { color: 0x567d46, side: THREE.DoubleSide, wireframe: true } );
      // var plane = new THREE.Mesh( geometry, material );
      // plane.position.z -= 50
      // scene.add( plane );
    },

    // onProgress callback currently not supported
    undefined,

    // onError callback
    function ( err ) {
      console.error( 'An error happened.' );
    }
  );
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


// instantiate a loader
var loader = new THREE.SVGLoader();

// load a SVG resource
loader.load(
	// resource URL
	'models/svg/white-output.svg',
	// called when the resource is loaded
	function ( data ) {

        var paths = data.paths;
		var group = new THREE.Group();

		for ( var i = 0; i < paths.length; i ++ ) {

			var path = paths[ i ];
            
            var material = new THREE.MeshBasicMaterial( {
              color: 0xf4a460,
              opacity: path.userData.style.fillOpacity,
              depthWrite: false,
              wireframe: false
            } );

			var shapes = path.toShapes( false );

			for ( var j = 0; j < shapes.length; j ++ ) {
                
        var shape = shapes[ j ];
        
        const geometry = new THREE.ExtrudeGeometry(shape, {
            depth: 50,
            bevelEnabled: false
        });

        var mesh = new THREE.Mesh( geometry, material );
        
				group.add( mesh );

			}

		}

		scene.add( group );

	},
	// called when loading is in progresses
	function ( xhr ) {

		console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );

	},
	// called when loading has errors
	function ( error ) {

		console.log( 'An error happened' );

	}
);




function render() {
//   camera.position.x = 0;
//   camera.position.z = 0;
  camera.lookAt(scene.position);
  renderer.render(scene, camera);
}