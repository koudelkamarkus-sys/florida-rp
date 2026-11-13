"""Original Florida RP Interceptor. Reproducible Blender 5.2 source.
Uses helper definitions from generate_coupe.py and smooth loft/wheel helpers from
 generate_coupe_realistic.py. No downloaded geometry, branding or textures.
"""
from pathlib import Path
base=(Path(__file__).parent/'generate_coupe.py').read_text()
refined=(Path(__file__).parent/'generate_coupe_realistic.py').read_text()
exec(base[:base.index('# Half body shell:')])
exec(refined[refined.index('def sample('):refined.index('profiles=[(-2.25')])
paint=material('Pearl ceramic police white',(.66,.72,.78),.45,.22)
black=material('Obsidian metallic paint',(.006,.009,.014),.25,.30)
glass=material('Deep blue automotive glass',(.008,.019,.028),.4,.12)
rim=material('Satin forged aluminium',(.24,.29,.34),.94,.24)
lime=material('Blue ceramic caliper',(.025,.16,.3),.45,.3)
blue=material('Police blue optical lens',(.015,.08,.65),.2,.18,1.3)
red=material('Police red optical lens',(.7,.012,.016),.2,.18,1.1)
white=material('Headlight phosphor',(.8,.9,1),.15,.2,1.7)
profiles=[(-2.30,.69,.49),(-2.18,.86,.56),(-1.92,.97,.66),(-1.45,1.015,.81),(-1.1,.99,.75),(-.65,.91,.65),(.05,.91,.64),(.65,.96,.69),(1.30,1.04,.83),(1.72,1.02,.82),(2.10,.95,.73),(2.30,.86,.62)]
shell=loft_half('Sculpted_interceptor_body',profiles,body_cross,paint,89)
for y in [-1.38,1.38]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.391,depth=2.8,location=(0,y,.355),rotation=(0,math.pi/2,0));cut=bpy.context.object
 mod=shell.modifiers.new('Wheel arch clearance','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=shell;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
b=shell.modifiers.new('Paint edge radii','BEVEL');b.width=.009;b.segments=3
# Compact teardrop cabin, distinct curved glass, roof and structural frames.
cab_profiles=[(-1.05,.70,.70),(-.82,.67,.88),(-.42,.60,1.105),(-.05,.60,1.145),(.35,.62,1.13),(.68,.68,.96),(1.02,.77,.77)]
def cabin_cross(w,h):
 pts=[(0,h),(.45*w,h-.008),(.85*w,h-.04),(w,h-.075),(w+.10,.70),(0,.70)]
 return [(sample([p[0] for p in pts],i*5/24),sample([p[1] for p in pts],i*5/24)) for i in range(25)]
cabin=loft_half('Wraparound_glass',cab_profiles,cabin_cross,glass,57)
def line(name,points,mat,r=.006,parent=bodyroot):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.parent=parent;o.data.materials.append(mat);return o
# Roof patch has a gentle compound curve, not a bevelled box.
rp=interp_profiles([(-.41,.585,1.119),(-.1,.589,1.157),(.25,.61,1.148),(.49,.639,1.088)],25)
vs=[(-w+2*w*i/20,y,h-.04*((-w+2*w*i/20)/w)**2) for y,w,h in rp for i in range(21)]
fs=[(j*21+i,j*21+i+1,(j+1)*21+i+1,(j+1)*21+i) for j in range(24) for i in range(20)]
o=mesh('Carbon_roof',vs,fs,black);o.modifiers.new('Roof skin','SOLIDIFY').thickness=.012
# Conforming decals sample the actual body surface to prevent intersecting patches.
body_sections=interp_profiles(profiles,89)
def section_at(y):
 for a,b in zip(body_sections,body_sections[1:]):
  if a[0]<=y<=b[0]:
   t=(y-a[0])/(b[0]-a[0]);return (a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t)
 return body_sections[0][1:]
def side_x(y,z):
 w,h=section_at(y);cross=body_cross(w,h);candidates=[]
 for (x1,z1),(x2,z2) in zip(cross,cross[1:]):
  if min(z1,z2)<=z<=max(z1,z2) and abs(z2-z1)>1e-8:candidates.append(x1+(x2-x1)*(z-z1)/(z2-z1))
 return max(candidates) if candidates else w
def top_z(x,y):
 w,h=section_at(y);cross=body_cross(w,h);candidates=[];x=abs(x)
 for (x1,z1),(x2,z2) in zip(cross,cross[1:]):
  if min(x1,x2)<=x<=max(x1,x2) and abs(x2-x1)>1e-8:candidates.append(z1+(z2-z1)*(x-x1)/(x2-x1))
 return max(candidates) if candidates else h
for sign in [-1,1]:
 # Fine panel gaps and A/B pillars give depth without thick graphic outlines.
 line('A_pillar',[(sign*.79,-1.02,.71),(sign*.70,-.82,.88),(sign*.62,-.42,1.08)],paint,.018)
 line('Rear_flying_buttress',[(sign*.65,.4,1.08),(sign*.76,.86,.86),(sign*.84,1.35,.81)],paint,.035)
 line('Window_sill',[(sign*.80,-1,.70),(sign*.79,-.2,.705),(sign*.82,.65,.72)],black,.016)
 line('Door_shutline',[(sign*.93,-.92,.63),(sign*.925,-.73,.37),(sign*.925,.50,.34),(sign*.96,.73,.64)],trim,.003)
 line('Side_skirt',[(sign*.92,-.92,.25),(sign*.98,.20,.23),(sign*1.02,.96,.27)],black,.035)
 # Side cooling intake with deep dark recess and a sculpted blade.
 verts=[(sign*.955,.47,.38),(sign*.98,.72,.69),(sign*1.025,1.07,.76),(sign*1.025,1.03,.39)]
 mesh('Side_intake_recess',verts,[(0,1,2,3)],trim)
 line('Intake_blade',[(sign*.966,.50,.39),(sign*.99,.78,.53),(sign*1.03,1.05,.68)],paint,.016)
 box('Flush_handle',(sign*.935,.30,.65),(.018,.14,.022),rim,bevel=.009)
 line('Mirror_support',[(sign*.73,-.75,.84),(sign*.96,-.72,.84)],trim,.018)
 box('Aerodynamic_mirror',(sign*1.01,-.73,.86),(.15,.24,.07),black,bevel=.033)
 box('Mirror_inset',(sign*1.012,-.608,.862),(.11,.006,.042),rim,bevel=.01)
 # Flush dark livery stripe on door, not a flat protruding decal plate.
 v=[]
 for k in range(33):
  y=-.73+1.12*k/32
  for z in [.40,.59]:v.append((sign*(side_x(y,z)+.016),y,z))
 mesh('Police_door_band',v,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(32)],trim)
 # White livery lettering remains editable geometry, no texture dependencies.
 bpy.ops.object.text_add(location=(sign*(side_x(-.58,.465)+.025),-.58,.465),rotation=(math.pi/2,0,sign*math.pi/2));t=bpy.context.object;t.name='POLICE_door_lettering';t.data.body='POLICE';t.data.size=.105;t.data.extrude=.0003;t.data.materials.append(trim);t.parent=bodyroot
 # Fender vents as slender inset strips.
 for k in range(4):
  vent=box('Fender_pressure_vent',(sign*.79,-1.51+k*.052,.804),(.20,.018,.009),trim,bevel=.004)
# Real bumper openings, a low splitter, layered optics.
box('Front_splitter',(0,-2.19,.255),(1.81,.35,.034),trim,bevel=.012)
box('Main_radiator_recess',(0,-2.282,.375),(.82,.06,.16),trim,bevel=.035)
for x in [-.70,.70]:
 box('Brake_cooling_intake',(x,-2.19,.385),(.33,.09,.15),trim,bevel=.03)
 for k in range(3):box('Intake_horizontal_vane',(x,-2.244,.34+k*.045),(.28,.013,.009),rim,bevel=.003)
 # Lamps sit on the sloping bonnet and have individual projector optics.
 v=[]
 for j in range(13):
  y=-2.11+j*.22/12
  for i in range(9):
   px=x-.145+i*.29/8;v.append((px,y,top_z(px,y)+.006))
 mesh('Flush_headlamp_lens',v,[(j*9+i,j*9+i+1,(j+1)*9+i+1,(j+1)*9+i) for j in range(12) for i in range(8)],glass)
 for dx in [-.07,.07]:
  px=x+dx;y=-2.045
  bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.032,location=(px,y,top_z(px,y)+.012));o=bpy.context.object;o.scale=(1,.72,.18);finish(o,'Projector_lens',white)
 points=[(x-.13,-2.10),(x-.13,-1.92),(x+.12,-1.90)]
 line('Daylight_signature',[(px,y,top_z(px,y)+.013) for px,y in points],white,.006)
 box('Rear_smoked_lamp',(x,2.255,.615),(.42,.06,.065),glass,bevel=.026)
 line('Rear_LED_signature',[(x-.18,2.29,.626),(x,2.29,.626),(x+.18,2.28,.64)],red,.008)
box('Rear_diffuser',(0,2.20,.30),(1.73,.24,.10),trim,bevel=.018)
for x in [-.6,-.3,0,.3,.6]:box('Diffuser_strake',(x,2.24,.255),(.018,.30,.10),trim,bevel=.004)
for x in [-.34,.34]:
 bpy.ops.mesh.primitive_torus_add(major_radius=.055,minor_radius=.008,major_segments=32,minor_segments=8,location=(x,2.34,.39),rotation=(math.pi/2,0,0));finish(bpy.context.object,'Titanium_exhaust_tip',rim)
# Rear deck louvers and a restrained aero wing.
for k in range(9):box('Engine_deck_louver',(0,1.12+k*.095,.845-k*.007),(1.13,.035,.013),trim,bevel=.005)
for x in [-.65,.65]:box('Wing_mount',(x,1.98,.82),(.035,.12,.20),trim,bevel=.012)
box('Aero_rear_wing',(0,2.02,.93),(1.86,.24,.032),black,bevel=.015)
# Low-profile emergency bar, with actual clear-lens subdivisions.
box('Emergency_bar_mount',(0,.10,1.17),(.94,.14,.025),trim,bevel=.015)
for x in [-.52,.52]:box('Roof_mount_foot',(x,.10,1.145),(.10,.09,.045),trim,bevel=.012)
for i in range(12):
 x=-.44+i*.08;box('Emergency_optical_cell',(x,.10,1.201),(.068,.12,.034),red if i<6 else blue,bevel=.009)
# Detailed independently rigged wheels from the original project, with rounded tires.
exec(refined[refined.index('wheel_code=base['):refined.index('# Add drilled disc detail')])
# Tire tread ribs, fine outer sidewall rings and machined disc holes.
for side,x in [('L',.94),('R',-.94)]:
 for end,y in [('F',-1.38),('R',1.38)]:
  wheel=bpy.data.objects['Wheel_'+end+side];outside=.13 if x>0 else -.13
  for offset in [-.055,0,.055]:ring('Tire_longitudinal_rib',.354,.0016,offset,rubber,wheel)
  for i in range(32):
   a=i*math.tau/32
   tread=box('Tire_sipe',(0,math.sin(a)*.353,math.cos(a)*.353),(.21,.003,.002),trim,wheel,.0005);tread.rotation_euler.x=-a
  for i in range(16):
   a=i*math.tau/16;cylinder('Disc_cross_drilling',.007,.002,(outside*.5,math.sin(a)*.19,math.cos(a)*.19),trim,wheel,8)
# Correct normals; metallic clearcoat stays export-compatible through Principled BSDF.
for o in list(bpy.context.scene.objects):
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
bpy.context.scene.unit_settings.system='METRIC';root['wheel_radius_m']=.355;root['wheelbase_m']=2.76;root['forward']='-Y Blender / +Z glTF'
for m in [paint,black]:
 p=m.node_tree.nodes['Principled BSDF'];p.inputs['Coat Weight'].default_value=.8;p.inputs['Coat Roughness'].default_value=.12
# Convert text/curves and consolidate by rig parent and material, preserving pivots.
# This reduces hundreds of tiny objects to a small set of rendering batches.
bpy.ops.object.select_all(action='DESELECT')
for o in list(bpy.context.scene.objects):
 if o.type in {'MESH','CURVE','FONT'}:
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
groups={}
for o in list(bpy.context.scene.objects):
 if o.type=='MESH':groups.setdefault((o.parent.name if o.parent else '',o.data.materials[0].name if o.data.materials else ''),[]).append(o)
for (parent,mat),items in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in items:o.select_set(True)
 bpy.context.view_layer.objects.active=items[0]
 if len(items)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name=parent+'__'+mat.replace(' ','_');o.select_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'florida-interceptor.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT.parent/'dist/models/florida-interceptor.glb'),export_format='GLB',export_apply=True,export_yup=True,export_materials='EXPORT',export_cameras=False,export_lights=False)
preview=base[base.index('# Studio preview scene only;'):].replace("ROOT/'previews'","ROOT/'interceptor-previews'").replace("ROOT/'model-spec.json'","ROOT/'interceptor-spec.json'")
exec(preview)


# Static fallback is rendered from this same model with an alpha background.
scene.render.film_transparent=True
floor.hide_render=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.render.filepath=str(ROOT.parent/'dist/interceptor-static.png');bpy.ops.render.render(write_still=True)

