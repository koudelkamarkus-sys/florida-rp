"""Refined original grand-touring coupe, using the same rig and dimensions as v1.
Run in Blender --background --python generate_coupe_realistic.py.
"""
from pathlib import Path
base=(Path(__file__).parent/'generate_coupe.py').read_text()
exec(base[:base.index('# Half body shell:')])
paint.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.025,.039,.042,1)
paint.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.28
glass.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.009,.018,.023,1)
glass.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.19
def sample(values,t):
 i=min(int(t),len(values)-2);f=t-i
 a=values[max(0,i-1)];b=values[i];c=values[i+1];d=values[min(len(values)-1,i+2)]
 return .5*((2*b)+(-a+c)*f+(2*a-5*b+4*c-d)*f*f+(-a+3*b-3*c+d)*f*f*f)
def interp_profiles(profiles,n):
 return [tuple(sample([p[k] for p in profiles],i*(len(profiles)-1)/(n-1)) for k in range(len(profiles[0]))) for i in range(n)]
def loft_half(name,profiles,cross,mat,n=65):
 profiles=interp_profiles(profiles,n);row=len(cross(1,1));vs=[]
 for y,w,h in profiles:vs += [(x,y,z) for x,z in cross(w,h)]
 fs=[]
 for i in range(n-1):
  for j in range(row-1):a=i*row+j;fs.append((a,a+1,a+row+1,a+row))
 fs += [tuple(range(row-1,-1,-1)),tuple(range((n-1)*row,n*row))]
 o=mesh(name,vs,fs,mat);m=o.modifiers.new('Mirror precision','MIRROR');m.use_clip=True;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=m.name);return o
def body_cross(w,h):
 pts=[(0,h),(.35*w,h+.018),(.68*w,h),(.91*w,h-.045),(w,h-.14),(w,.45),(.97*w,.32),(.76*w,.265),(0,.265)]
 return [(sample([p[0] for p in pts],i*(len(pts)-1)/32),sample([p[1] for p in pts],i*(len(pts)-1)/32)) for i in range(33)]
profiles=[(-2.25,.76,.60),(-2.12,.88,.70),(-1.9,.94,.79),(-1.45,.985,.86),(-.9,.96,.82),(-.4,.935,.79),(.5,.95,.79),(1.3,.995,.89),(1.8,.96,.85),(2.12,.88,.77),(2.24,.77,.68)]
shell=loft_half('Sculpted_GT_body',profiles,body_cross,paint)
for y in [-1.38,1.38]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.403,depth=2.7,location=(0,y,.355),rotation=(0,math.pi/2,0));cut=bpy.context.object
 mod=shell.modifiers.new('Precision wheel arch','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=shell;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
b=shell.modifiers.new('Body edge radii','BEVEL');b.width=.012;b.segments=3
# Rounded glasshouse. Roof is a separate curved painted surface, not a cube.
cab_profiles=[(-.83,.765,.84),(-.57,.73,1.04),(-.12,.665,1.255),(.28,.66,1.295),(.69,.68,1.245),(1.07,.735,1.045),(1.43,.79,.86)]
def cabin_cross(w,h):
 pts=[(0,h),(.45*w,h-.005),(.82*w,h-.035),(w,max(.85,h-.045)),(w+.12,.835),(0,.835)]
 return [(sample([p[0] for p in pts],i*5/20),sample([p[1] for p in pts],i*5/20)) for i in range(21)]
cabin=loft_half('Curved_smoked_glasshouse',cab_profiles,cabin_cross,glass,49)
roof_profiles=interp_profiles([(-.15,.65,1.272),(.1,.652,1.31),(.4,.66,1.306),(.72,.676,1.253)],25)
rv=[]
for y,w,h in roof_profiles:
 for i in range(17):x=-w+2*w*i/16;rv.append((x,y,h-.04*(x/w)**2))
rf=[]
for j in range(24):
 for i in range(16):a=j*17+i;rf.append((a,a+1,a+18,a+17))
roof=mesh('Arched_painted_roof',rv,rf,paint);s=roof.modifiers.new('Roof skin','SOLIDIFY');s.thickness=.018
def line(name,points,mat,r=.006,parent=bodyroot):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.parent=parent;o.data.materials.append(mat);return o
for sign in [-1,1]:
 x=sign*.94
 line('Door_panel_seam',[(x,-.55,.76),(x,-.55,.42),(sign*.93,-.4,.31),(sign*.94,.9,.31),(sign*.955,1.05,.48),(sign*.97,1.05,.78)],trim,.004)
 line('Window_frame',[(sign*w,y,max(.85,h-.045)) for y,w,h in cab_profiles],trim,.009)
 line('Window_sill',[(sign*.77,-.79,.85),(sign*.78,.2,.835),(sign*.795,1.42,.86)],paint,.013)
 line('B_pillar',[(sign*.67,.5,1.24),(sign*.79,.59,.84)],trim,.026)
 line('Hood_character_line',[(sign*.48,-2.1,.72),(sign*.53,-1.8,.82),(sign*.53,-1.25,.865),(sign*.48,-.9,.831)],trim,.003)
 box('Flush_door_handle',(sign*.955,.74,.75),(.022,.16,.026),trim,bevel=.012)
 mirror=box('Sculpted_mirror',(sign*1.02,-.6,.97),(.17,.24,.085),paint,bevel=.04)
 line('Mirror_stalk',[(sign*.79,-.52,.88),(sign*.96,-.58,.96)],trim,.025)
 box('Mirror_reflector',(sign*1.025,-.48,.967),(.125,.015,.05),glass,bevel=.016)
 box('Sill_aero_trim',(sign*.955,.05,.265),(.065,1.95,.06),trim,bevel=.022)
# Bumper depth and inset lamp housings anchor the front rather than flat strips.
box('Front_splitter',(0,-2.14,.275),(1.7,.30,.045),trim,bevel=.03)
box('Central_grille',(0,-2.235,.44),(.94,.045,.18),trim,bevel=.05)
for x in [-.66,.66]:
 box('Side_intake',(x,-2.17,.43),(.27,.06,.15),trim,bevel=.045)
 housing=box('Headlamp_smoked_housing',(x,-2.08,.695),(.43,.09,.092),glass,bevel=.035);housing.rotation_euler.z=x*.12
 for z in [.684,.713]:line('LED_signature',[(x-.17,-2.137,z),(x,-2.14,z+.005),(x+.17,-2.123,z+.012)],white,.009)
 box('Rear_lamp_housing',(x,2.15,.665),(.45,.055,.085),trim,bevel=.028)
 line('Rear_LED',[(x-.19,2.183,.68),(x,2.187,.675),(x+.19,2.17,.665)],red,.012)
box('Rear_diffuser',(0,2.14,.29),(1.65,.24,.085),trim,bevel=.028)
for x in [-.52,-.26,0,.26,.52]:box('Diffuser_fin',(x,2.18,.25),(.027,.30,.10),trim,bevel=.007)
box('Integrated_deck_lip',(0,2.08,.79),(1.55,.13,.025),paint,bevel=.012)
# Use the proven rig dimensions, with rounded tires and hollow forged rims.
wheel_code=base[base.index('def cylinder('):base.index('# Mesh normals,')]
wheel_code=wheel_code.replace("cylinder('Tire_'+end+side,.355,.25,(0,0,0),rubber,wheel)","rounded_tire('Tire_'+end+side,wheel)")
wheel_code=wheel_code.replace("cylinder('Rim_lip_'+end+side,.264,.012,(outside*1.03,0,0),rim,wheel)","ring('Rim_lip_'+end+side,.259,.009,outside*1.03,rim,wheel)")
wheel_code=wheel_code.replace("cylinder('Rim_dark_center_'+end+side,.235,.015,(outside*1.08,0,0),trim,wheel)","cylinder('Rim_dark_center_'+end+side,.235,.008,(outside*.92,0,0),trim,wheel)")
def rounded_tire(name,parent):
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=16,major_radius=.283,minor_radius=.072,rotation=(0,math.pi/2,0));o=bpy.context.object;o.scale.z=1.65;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);finish(o,name,rubber,parent)
 for offset in [-.075,.075]:ring('Sidewall_bead',.311,.003,offset,trim,parent)
def ring(name,major,minor,x,mat,parent):
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=8,major_radius=major,minor_radius=minor,location=(x,0,0),rotation=(0,math.pi/2,0));o=bpy.context.object;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return finish(o,name,mat,parent)
wheel_code=wheel_code.replace("cylinder('Rim_barrel_'+end+side,.262,.04,(outside,0,0),trim,wheel)","ring('Rim_barrel_'+end+side,.251,.016,outside,trim,wheel)")
wheel_code=wheel_code.replace("cylinder('Rim_dark_center_'+end+side,.235,.008,(outside*.92,0,0),trim,wheel)","")
exec(wheel_code)
# Add drilled disc detail and tread blocks with instanced geometry.
for side,x in [('L',.94),('R',-.94)]:
 for end,y in [('F',-1.38),('R',1.38)]:
  wheel=bpy.data.objects['Wheel_'+end+side];outside=.115 if x>0 else -.115
  for i in range(20):
   a=i*math.tau/20
   cylinder('Disc_drill',.009,.003,(outside,math.sin(a)*.19,math.cos(a)*.19),trim,wheel,8)
  # Delicate sidewall lettering is intentionally omitted for export size.
# Normalize and export. This creates siblings, preserving the first model.
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
bpy.context.scene.unit_settings.system='METRIC';root['forward']='-Y Blender / +Z glTF';root['wheel_radius_m']=.355;root['wheelbase_m']=2.76
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'florida-coupe-realistic.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT.parent/'dist/models/florida-coupe-realistic.glb'),export_format='GLB',export_apply=True,export_yup=True,export_materials='EXPORT',export_cameras=False,export_lights=False)
# Studio previews use the same lighting as v1 for a fair visual comparison.
preview=base[base.index('# Studio preview scene only;'):]
preview=preview.replace("ROOT/'previews'","ROOT/'realistic-previews'").replace("(ROOT/'model-spec.json')","(ROOT/'model-spec-realistic.json')")
exec(preview)

