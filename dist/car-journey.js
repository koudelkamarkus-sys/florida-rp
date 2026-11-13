import * as THREE from './vendor/three.module.js';
import {GLTFLoader} from './vendor/GLTFLoader.js';
import {HDRLoader} from './vendor/HDRLoader.js';
import {RoomEnvironment} from './vendor/RoomEnvironment.js';
import {makeRoute,sampleRoute,pageProgress,clamp} from './route-state.js';
import {sampleTailTrail} from './tail-trail-state.js';
const dock=document.querySelector('.car-3d'),root=document.documentElement;
const reduced=matchMedia('(prefers-reduced-motion: reduce)'),narrow=matchMedia('(max-width: 799px)');
const stage=document.querySelector('.drive-stage'),sequence=document.querySelector('.drive-sequence');
const fallback=document.createElement('img');fallback.src='./interceptor-reflective-static.png';fallback.alt='Original Florida RP police supercar';fallback.className='car-static';dock.append(fallback);
let renderer,scene,camera,rig,body,shadow,ready=false,failed=false,queued=false,initializing=false;
let sceneLights={},tailTrails=[],travelDirection=1,lastScrollY=scrollY;
let route=makeRoute(narrow.matches,innerWidth/innerHeight),wheels=[],steering=[];
const readingSurfaces=[...document.querySelectorAll('main p,main h1,main h2,main h3,main summary,main .button,footer')];
const disabled=new URLSearchParams(location.search).get('car3d')==='off';
function paused(){return reduced.matches||root.classList.contains('motion-paused');}
function fallbackState(reason){failed=true;dock.dataset.loaded=reason;dock.classList.add('static-alternative');root.classList.remove('car-3d-ready');}
function requestRender(){if(!queued){queued=true;requestAnimationFrame(render)}}
function makeTailTrails(){
 for(const layer of [{width:.055,color:0xff8c96,opacity:.85},{width:.23,color:0xff153e,opacity:.28}]){
  const geometry=new THREE.BufferGeometry(),count=44*2*6;
  geometry.setAttribute('position',new THREE.BufferAttribute(new Float32Array(count*3),3).setUsage(THREE.DynamicDrawUsage));
  geometry.setAttribute('color',new THREE.BufferAttribute(new Float32Array(count*3),3).setUsage(THREE.DynamicDrawUsage));
  const material=new THREE.MeshBasicMaterial({color:layer.color,vertexColors:true,transparent:true,opacity:layer.opacity,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide,toneMapped:false});
  const mesh=new THREE.Mesh(geometry,material);mesh.frustumCulled=false;mesh.renderOrder=1;scene.add(mesh);tailTrails.push({mesh,width:layer.width});
 }
}
function updateTailTrails(progress){
 const samples=sampleTailTrail(route,progress,44,travelDirection),blocks=readingSurfaces.map(e=>e.getBoundingClientRect());
 for(const layer of tailTrails){
  const positions=layer.mesh.geometry.attributes.position,colors=layer.mesh.geometry.attributes.color;let index=0;
  for(let side=0;side<2;side++)for(let i=0;i<samples.length-1;i++){
   for(const [offset,edge] of [[0,-1],[0,1],[1,1],[0,-1],[1,1],[1,-1]]){
    const sample=samples[i+offset],centre=sample.centres[side],width=layer.width*route.scale*(.35+.65*sample.fade)/2;
    const point=new THREE.Vector3(centre[0]+sample.normal[0]*edge*width,centre[1],centre[2]+sample.normal[2]*edge*width);
    positions.setXYZ(index,point.x,point.y,point.z);
    const screen=point.clone().project(camera),x=(screen.x+1)*innerWidth/2,y=(1-screen.y)*innerHeight/2;
    const onText=blocks.some(b=>x>b.left-4&&x<b.right+4&&y>b.top-4&&y<b.bottom+4),fade=sample.fade*(onText?.08:1);
    colors.setXYZ(index,fade,fade,fade);index++;
   }
  }
  positions.needsUpdate=true;colors.needsUpdate=true;
 }
 dock.dataset.trails=String(progress>0&&progress<1);
}
function render(){
 queued=false;const progress=pageProgress(scrollY,root.scrollHeight,innerHeight);root.style.setProperty('--journey-progress',progress);dock.dataset.progress=progress.toFixed(9);
 const max=Math.max(1,root.scrollHeight-innerHeight),start=(sequence.offsetTop-document.querySelector('header').offsetHeight)/max,end=(sequence.offsetTop+sequence.offsetHeight-stage.offsetHeight)/max,local=clamp((progress-start)/Math.max(.001,end-start));
 stage.style.setProperty('--night-reveal',`${clamp((local-.25)/.5)*100}%`);stage.style.setProperty('--day-scale',String(1.05+local*.05));stage.style.setProperty('--copy-y',`${-local*24}px`);
 if(!ready||failed||paused()){dock.classList.toggle('static-alternative',failed||paused());return;}
 dock.classList.remove('static-alternative');const pose=sampleRoute(route,progress);
 if(travelDirection<0){pose.heading+=Math.PI;pose.steering*=-1;pose.lean*=-1;pose.wheel*=-1;}
 dock.dataset.direction=String(travelDirection);
 const lightStops=[[0,0x9ec9ff,2.1],[.2,0xffdfbd,3],[.42,0xf0f7ff,3.2],[.62,0xffcfaa,2.6],[.82,0x8eb8f0,1.8],[1,0xa5c7ff,2.1]];
 let lightIndex=0;while(lightIndex<lightStops.length-2&&progress>lightStops[lightIndex+1][0])lightIndex++;
 const aLight=lightStops[lightIndex],bLight=lightStops[lightIndex+1],blend=(progress-aLight[0])/(bLight[0]-aLight[0]);
 sceneLights.key.color.lerpColors(new THREE.Color(aLight[1]),new THREE.Color(bLight[1]),blend);sceneLights.key.intensity=THREE.MathUtils.lerp(aLight[2],bLight[2],blend)*.58;
 rig.position.fromArray(pose.position);rig.rotation.y=pose.heading;rig.scale.setScalar(pose.scale);body.rotation.z=pose.lean;
 steering.forEach(o=>o.rotation.y=pose.steering);wheels.forEach(o=>o.rotation.x=pose.wheel);
 shadow.position.set(pose.position[0],.003,pose.position[2]);shadow.scale.setScalar(pose.scale);
 updateTailTrails(progress);
 dock.dataset.pose=JSON.stringify({p:pose.p,distance:pose.distance,position:pose.position,heading:pose.heading,wheel:pose.wheel,steering:pose.steering,lean:pose.lean});
 // Fade by projected overlap, not by a timed transition. Copy remains readable.
 rig.updateMatrixWorld(true);const box=new THREE.Box3().setFromObject(rig),screen=[];
 for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){const v=new THREE.Vector3(x,y,z).project(camera);screen.push([(v.x+1)*innerWidth/2,(1-v.y)*innerHeight/2]);}
 const left=Math.min(...screen.map(p=>p[0])),right=Math.max(...screen.map(p=>p[0])),top=Math.min(...screen.map(p=>p[1])),bottom=Math.max(...screen.map(p=>p[1]));
 let overlap=0;for(const element of readingSurfaces){const b=element.getBoundingClientRect();const area=Math.max(0,Math.min(right,b.right)-Math.max(left,b.left))*Math.max(0,Math.min(bottom,b.bottom)-Math.max(top,b.top));overlap=Math.max(overlap,area/Math.max(1,(right-left)*(bottom-top)));}
 renderer.domElement.style.opacity=String(1-.7*clamp(overlap*3));renderer.render(scene,camera);
}
function resize(){route=makeRoute(narrow.matches,innerWidth/innerHeight);if(renderer){renderer.setPixelRatio(Math.min(devicePixelRatio,narrow.matches?1.25:1.5));renderer.setSize(innerWidth,innerHeight,false);camera.aspect=innerWidth/innerHeight;camera.fov=narrow.matches?37:34;camera.position.set(0,narrow.matches?6.5:6,narrow.matches?15:14);camera.lookAt(0,1.1,0);camera.updateProjectionMatrix();}requestRender();}
async function initialize(){
 if(initializing)return;initializing=true;
 if(disabled){fallbackState('disabled-for-test');return;}
 if(reduced.matches){dock.classList.add('static-alternative');dock.dataset.loaded='reduced-motion';initializing=false;return;}
 try{
  renderer=new THREE.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});renderer.setClearColor(0x000000,0);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.0;renderer.domElement.setAttribute('aria-hidden','true');dock.append(renderer.domElement);
  renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();fallbackState('context-lost')});
  scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(34,innerWidth/innerHeight,.1,100);
  const room=new RoomEnvironment(),pmrem=new THREE.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(room,.04).texture;room.dispose();dock.dataset.environment='studio-fallback';
  try{const hdr=await new HDRLoader().loadAsync('./environments/suburban-parking-1k.hdr');hdr.mapping=THREE.EquirectangularReflectionMapping;const oldEnvironment=scene.environment;scene.environment=pmrem.fromEquirectangular(hdr).texture;scene.environmentRotation.y=.55;scene.environmentIntensity=1.1;oldEnvironment.dispose();hdr.dispose();dock.dataset.environment='outdoor-hdr';}catch{console.warn('Outdoor reflections unavailable; studio fallback retained.');}finally{pmrem.dispose();}
  scene.add(new THREE.HemisphereLight(0xcadfff,0x182a46,.7));const key=new THREE.DirectionalLight(0xe4efff,3);key.position.set(-4,9,5);scene.add(key);const rim=new THREE.DirectionalLight(0x93c5f2,1.1);rim.position.set(5,5,-4);scene.add(rim);sceneLights={key,rim};
  const c=document.createElement('canvas');c.width=128;c.height=128;const ctx=c.getContext('2d'),g=ctx.createRadialGradient(64,64,4,64,64,62);g.addColorStop(0,'rgba(0,0,0,.65)');g.addColorStop(.45,'rgba(0,0,0,.35)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,128,128);
  shadow=new THREE.Mesh(new THREE.PlaneGeometry(3.6,5.6),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false}));shadow.rotation.x=-Math.PI/2;scene.add(shadow);
  const modelURL=new URLSearchParams(location.search).get('car3d')==='fail'?'./models/intentional-missing-test.glb':'./models/florida-interceptor-reflective.glb';
  const gltf=await new GLTFLoader().loadAsync(modelURL);gltf.scene.traverse(o=>{if(!o.isMesh)return;for(const m of (Array.isArray(o.material)?o.material:[o.material])){
   if(/metallic lacquer|Obsidian metallic/i.test(m.name)){m.envMapIntensity=1.65;m.metalness=/Midnight/.test(m.name)?.82:.65;m.roughness=/Midnight/.test(m.name)?.145:.11;if(m.isMeshPhysicalMaterial){m.clearcoat=1;m.clearcoatRoughness=.045;m.ior=1.5;}}
   if(/automotive glass/i.test(m.name)){m.envMapIntensity=1.8;m.roughness=.045;}
   if(/forged aluminium|Machined titanium/i.test(m.name)){m.envMapIntensity=1.15;m.roughness=.14;}
  }});rig=gltf.scene.getObjectByName('VehicleRoot');if(!rig)throw Error('Missing movement root');scene.add(gltf.scene);body=gltf.scene.getObjectByName('BodyLean');
  for(const name of ['Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR']){const o=gltf.scene.getObjectByName(name);if(!o)throw Error(`Missing ${name}`);wheels.push(o);}
  for(const name of ['Steer_FL','Steer_FR']){const o=gltf.scene.getObjectByName(name);if(!o)throw Error(`Missing ${name}`);steering.push(o);}
  makeTailTrails();ready=true;dock.dataset.loaded='true';root.classList.add('car-3d-ready');dock.classList.add('is-ready');resize();
 }catch(error){fallbackState('failed');console.warn('Static car alternative active:',error.message);}
}
addEventListener('scroll',()=>{const delta=scrollY-lastScrollY;if(Math.abs(delta)>.1)travelDirection=Math.sign(delta);lastScrollY=scrollY;requestRender();},{passive:true});addEventListener('resize',resize);addEventListener('pageshow',requestRender);new ResizeObserver(requestRender).observe(document.body);
new MutationObserver(()=>{if(!renderer&&!failed&&!paused())initialize();requestRender()}).observe(root,{attributes:true,attributeFilter:['class']});
reduced.addEventListener('change',()=>{if(!renderer&&!failed&&!reduced.matches)initialize();requestRender()});document.fonts?.ready.then(resize);initialize();requestRender();








