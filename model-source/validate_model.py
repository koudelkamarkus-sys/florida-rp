import json,struct,sys
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'dist/models'/(sys.argv[1] if len(sys.argv)>1 else 'florida-coupe.glb')
b=p.read_bytes();assert b[:4]==b'glTF'
j=json.loads(b[20:20+struct.unpack_from('<I',b,12)[0]])
nodes={n.get('name'):n for n in j['nodes']}
required=['VehicleRoot','BodyLean','Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR','Steer_FL','Steer_FR']
assert all(n in nodes for n in required)
for name in ['Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR']:
 assert nodes[name].get('translation',[0,0,0])==[0,0,0]
for name in ['Steer_FL','Steer_FR']:
 assert abs(nodes[name]['translation'][1]-.355)<1e-5
 assert abs(nodes[name]['translation'][2]-1.38)<1e-5
triangles=sum(j['accessors'][p['indices']]['count']//3 for m in j['meshes'] for p in m['primitives'])
print(json.dumps({'passed':True,'bytes':len(b),'triangles':triangles,'required_nodes':required,'wheel_pivots_centered':True,'up':'+Y','forward':'+Z','external_textures':len(j.get('images',[]))},indent=2))

