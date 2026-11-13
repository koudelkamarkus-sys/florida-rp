"""Reflective Interceptor v2. Preserves the first model and generator.
Run Blender --background --python generate_interceptor_reflective.py.
"""
from pathlib import Path
source=(Path(__file__).parent/'generate_interceptor.py').read_text()
source=source.replace("paint=material('Pearl ceramic police white',(.66,.72,.78),.45,.22)","paint=material('Midnight blue metallic lacquer',(.018,.033,.065),.82,.145)\nletter=material('Police ivory enamel',(.82,.87,.92),.12,.24)")
source=source.replace("black=material('Obsidian metallic paint',(.006,.009,.014),.25,.30)","black=material('Obsidian metallic paint',(.004,.007,.012),.65,.11)")
source=source.replace("glass=material('Deep blue automotive glass',(.008,.019,.028),.4,.12)","glass=material('Deep blue automotive glass',(.006,.012,.020),.15,.045)")
source=source.replace("rim=material('Satin forged aluminium',(.24,.29,.34),.94,.24)","rim=material('Polished forged aluminium',(.55,.59,.65),.98,.14)")
source=source.replace("t.data.materials.append(trim)","t.data.materials.append(letter)")
source=source.replace("p.inputs['Coat Weight'].default_value=.8;p.inputs['Coat Roughness'].default_value=.12","p.inputs['Coat Weight'].default_value=1;p.inputs['Coat Roughness'].default_value=.045")
# Correct the shell winding before Boolean operations, rather than after them.
source=source.replace("for y in [-1.38,1.38]:", """bpy.context.view_layer.objects.active=shell;shell.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');shell.select_set(False)
for y in [-1.38,1.38]:""",1)
insert="""
# Radiator cavities: body topology is checked after the cuts.
# Recessed mesh grille, small vertically spaced slats and metallic towing eye.
for xx in [-.32,-.24,-.16,-.08,0,.08,.16,.24,.32]:
 box('Radiator_vertical_mesh',(xx,-2.31,.386),(.008,.007,.12),rim,bevel=.001)
for zz in [.34,.38,.42]:box('Radiator_horizontal_mesh',(0,-2.31,zz),(.72,.007,.006),trim,bevel=.001)
for side in [-1,1]:
 line('Hood_crease',[(side*.41,-1.94,.682),(side*.46,-1.65,.776),(side*.49,-1.36,.804),(side*.54,-1.10,.752)],black,.0025)
 # Small flush fasteners and a windscreen wiper introduce scale cues.
 for yy in [1.07,1.85]:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.008,location=(side*.87,yy,.79));o=bpy.context.object;o.scale.z=.25;finish(o,'Aero_fastener',rim)
line('Windscreen_wiper',[(0,-.99,.744),(.11,-.78,.92),(.38,-.57,1.03)],trim,.008)
"""
source=source.replace('# Correct normals; metallic clearcoat',insert+'\n# Correct normals; metallic clearcoat')
source=source.replace('florida-interceptor.blend','florida-interceptor-reflective.blend').replace('florida-interceptor.glb','florida-interceptor-reflective.glb').replace('interceptor-previews','reflective-previews').replace('interceptor-spec.json','reflective-spec.json').replace('interceptor-static.png','interceptor-reflective-static.png')
# Studio renders include the exact same HDR reflection asset as the website.
source=source.replace("exec(preview)","""preview=preview.replace(\"for loc,power,size in\",\"env=world.node_tree.nodes.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(str(ROOT.parent/'dist/environments/suburban-parking-1k.hdr'));world.node_tree.links.new(env.outputs['Color'],world.node_tree.nodes['Background'].inputs[0]);world.node_tree.nodes['Background'].inputs[1].default_value=.7\\nfor loc,power,size in\")
exec(preview)""")
# Recessed trapezoidal grille replaces the protruding rectangular bumper block.
source=source.replace("box('Main_radiator_recess',(0,-2.282,.375),(.82,.06,.16),trim,bevel=.035)", "mesh('Inset_trapezoidal_radiator',[(-.48,-2.306,.455),(.48,-2.306,.455),(.37,-2.306,.323),(-.37,-2.306,.323)],[(0,1,2,3)],trim)")
source=source.replace("box('Brake_cooling_intake',(x,-2.19,.385),(.33,.09,.15),trim,bevel=.03)", "box('Brake_cooling_intake',(x,-2.19,.385),(.25,.025,.105),trim,bevel=.035)")
source=source.replace("(.28,.013,.009)","(.21,.008,.006)").replace("(x,-2.244,.34+k*.045)","(x,-2.208,.354+k*.033)")
exec(compile(source,__file__,'exec'))
