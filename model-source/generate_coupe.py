"""Original Florida RP coupe. Run with Blender --background --python this_file.
Blender: metres, Z up, -Y forward. GLB: Y up, +Z forward. No external assets.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def material(name,color,metal=0,rough=.3,emission=0):
 m=bpy.data.materials.new(name);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
 if metal>.4:p.inputs['Coat Weight'].default_value=.5;p.inputs['Coat Roughness'].default_value=.17
 return m
paint=material('Graphite enamel',(.055,.09,.075),.75,.24)
glass=material('Smoked glass',(.012,.029,.04),.45,.14)
rubber=material('Tire rubber',(.012,.014,.016),0,.68)
trim=material('Carbon satin',(.018,.023,.024),.3,.4)
rim=material('Machined titanium',(.38,.43,.46),.9,.24)
disc=material('Brake steel',(.16,.18,.19),.75,.46)
lime=material('Lime ceramic caliper',(.62,.82,.19),.35,.3)
white=material('LED white',(.8,.94,1),.1,.25,2)
red=material('Tail light red',(.75,.015,.008),.15,.25,1.4)
def empty(name,parent=None,loc=(0,0,0)):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;o.location=loc;return o
root=empty('VehicleRoot');bodyroot=empty('BodyLean',root)
def finish(o,name,mat,parent=bodyroot,bevel=0):
 o.name=name;o.parent=parent
 if mat:o.data.materials.append(mat)
 if bevel:
  mod=o.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=3
 for f in o.data.polygons:f.use_smooth=True
 return o
def box(name,loc,scale,mat,parent=bodyroot,bevel=.025):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,mat,parent,bevel)
def mesh(name,verts,faces,mat,parent=bodyroot):
 m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o);return finish(o,name,mat,parent)
# Half body shell: profiled sections, mirrored for exact symmetry.
sections=[(-2.24,.69,.58),(-1.94,.88,.74),(-1.42,.96,.82),(-.65,.94,.78),(.55,.95,.79),(1.38,.98,.85),(1.98,.89,.77),(2.2,.73,.64)]
verts=[]
for y,w,h in sections:verts += [(0,y,h+.025),(.62*w,y,h),(w,y,h-.12),(w,y,.38),(.82*w,y,.26),(0,y,.26)]
faces=[]
for i in range(len(sections)-1):
 for j in range(5):a=i*6+j;faces.append((a,a+1,a+7,a+6))
faces += [tuple(range(5,-1,-1)),tuple(range((len(sections)-1)*6,len(sections)*6))]
shell=mesh('Sculpted_body_shell',verts,faces,paint)
mir=shell.modifiers.new('Mirror symmetry','MIRROR');mir.use_axis[0]=True;mir.use_clip=True
bpy.context.view_layer.objects.active=shell;bpy.ops.object.modifier_apply(modifier=mir.name)
for y in [-1.38,1.38]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.425,depth=2.6,location=(0,y,.355),rotation=(0,math.pi/2,0));cut=bpy.context.object
 mod=shell.modifiers.new('Wheel arch','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=shell;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
bev=shell.modifiers.new('Bevel body edges','BEVEL');bev.width=.035;bev.segments=3
# A raked glasshouse with separate roof, quarter windows and windshield.
cab=[(-.78,.77,.81),(-.18,.66,1.24),(.73,.66,1.23),(1.35,.79,.82)]
cv=[]
for y,w,z in cab:cv += [(-w,y,z),(w,y,z)]
cabin=mesh('Continuous_dark_glass',cv,[(0,1,3,2),(2,3,5,4),(4,5,7,6),(0,2,4,6),(1,7,5,3),(0,6,7,1)],glass)
b=cabin.modifiers.new('Glass edge bevel','BEVEL');b.width=.025;b.segments=3
roof=box('Floating_roof',(0,.28,1.255),(1.32,.95,.045),paint,bevel=.04)
for x in [-.68,.68]:
 pillar=box('B_pillar',(x,.38,1.02),(.045,.085,.42),trim,bevel=.01)
 sill=box('Side_skirt',(x/abs(x)*.94,.05,.25),(.08,1.9,.09),trim,bevel=.025)
 handle=box('Flush_handle',(x/abs(x)*.965,.6,.76),(.015,.18,.025),rim,bevel=.01)
 mirror=box('Mirror_housing',(x/abs(x)*1.025,-.53,.94),(.18,.22,.09),paint,bevel=.04)
 box('Mirror_glass',(x/abs(x)*1.035,-.42,.94),(.13,.015,.05),glass,bevel=.01)
box('Front_splitter',(0,-2.16,.28),(1.56,.26,.065),trim)
box('Rear_diffuser',(0,2.13,.29),(1.48,.26,.09),trim)
box('Front_intake',(0,-2.228,.43),(1.04,.035,.16),trim)
for x in [-.6,.6]:
 lamp=box('Headlight_LED',(x,-2.04,.665),(.43,.065,.045),white,bevel=.018);lamp.rotation_euler.z=x*.18
 box('Tail_LED',(x,2.13,.61),(.47,.035,.04),red,bevel=.012)
box('Rear_spoiler',(0,1.98,.855),(1.6,.17,.06),trim)
for x in [-.72,.72]:box('Spoiler_mount',(x,1.98,.79),(.05,.1,.12),trim)
def cylinder(name,radius,depth,loc,mat,parent,vertices=48):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc,rotation=(0,math.pi/2,0));o=bpy.context.object
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=False);return finish(o,name,mat,parent,.008)
for side,x in [('L',.94),('R',-.94)]:
 for end,y in [('F',-1.38),('R',1.38)]:
  # Parent locations are local: wheel geometry is created at origin.
  steering=empty('Steer_'+end+side,root,(x,y,.355))
  wheel=empty('Wheel_'+end+side,steering)
  cylinder('Tire_'+end+side,.355,.25,(0,0,0),rubber,wheel)
  outside=.137 if x>0 else -.137
  cylinder('Brake_disc_'+end+side,.233,.025,(outside*.55,0,0),disc,wheel)
  cylinder('Rim_barrel_'+end+side,.262,.04,(outside,0,0),trim,wheel)
  cylinder('Rim_lip_'+end+side,.264,.012,(outside*1.03,0,0),rim,wheel)
  cylinder('Rim_dark_center_'+end+side,.235,.015,(outside*1.08,0,0),trim,wheel)
  for i in range(10):
   a=i*math.tau/10
   spoke=box('Forged_spoke',(outside*1.17,math.sin(a)*.145,math.cos(a)*.145),(.025,.035,.19),rim,wheel,.007);spoke.rotation_euler.x=-a
  cylinder('Center_cap_'+end+side,.061,.026,(outside*1.26,0,0),rim,wheel,32)
  for i in range(5):
   a=i*math.tau/5;cylinder('Lug',.009,.008,(outside*1.4,math.sin(a)*.043,math.cos(a)*.043),trim,wheel,12)
  # Caliper stays on steering parent, not on spinning wheel.
  box('Caliper_'+end+side,(outside*.6,.18,.02),(.055,.065,.19),lime,steering,.018)
# Mesh normals, units, named pivots, and export constraints.
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o;o.select_set(True)
  bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
bpy.context.scene.unit_settings.system='METRIC'
root['forward']='-Y Blender / +Z glTF';root['wheel_radius_m']=.355;root['wheelbase_m']=2.76
# Save asset source without preview floor/lights.
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'florida-coupe.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT.parent/'dist/models/florida-coupe.glb'),export_format='GLB',export_apply=True,export_yup=True,export_materials='EXPORT',export_cameras=False,export_lights=False)
# Studio preview scene only; source remains clean.
floor=box('Preview_floor',(0,0,-.08),(200,200,.1),material('Studio',(.045,.055,.06),0,.85),None)
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.14,.17,.2,1);world.node_tree.nodes['Background'].inputs[1].default_value=.5
for loc,power,size in [((3,-4,6),1500,5),((-4,-1,3),1000,4),((0,5,5),1800,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,.5))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;bpy.context.scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=6.5
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=650;scene.render.resolution_percentage=100
for name,loc in [('front',(0,-8,2.8)),('side',(8,0,2.3)),('three-quarter',(6,-7,4.3))]:
 camera.location=loc;camera.rotation_euler=(Vector((0,0,.6))-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(ROOT/'previews'/f'{name}.png');bpy.ops.render.render(write_still=True)
(ROOT/'model-spec.json').write_text(json.dumps({'dimensions_m':[2.2,4.5,1.3],'wheel_radius_m':.355,'wheelbase_m':2.76,'forward_gltf':'+Z','up_gltf':'+Y','original':True,'generator':'generate_coupe.py'},indent=2))
print('MODEL_COMPLETE')
