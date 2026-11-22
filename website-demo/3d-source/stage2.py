import bpy, math, sys, json
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
A='/tmp/fc3d/assets/'
bpy.ops.wm.open_mainfile(filepath='/tmp/fc3d/stage1.blend')
bpy.ops.preferences.addon_enable(module='cycles')
S=bpy.context.scene; S.render.engine='CYCLES'
CHX=float(sys.argv[sys.argv.index('--chx')+1]) if '--chx' in sys.argv else .93
ch=bpy.data.objects['chair_A']
ch.location=(-CHX,0,.0004); ch.rotation_euler=(0,0,-math.pi/2)
ch2=ch.copy(); ch2.name='chair_B'; S.collection.objects.link(ch2); ch2.location=(CHX,0,.0004); ch2.rotation_euler=(0,0,math.pi/2)
# world
w=bpy.data.worlds.new('W'); S.world=w; w.use_nodes=True; nt=w.node_tree; bg=nt.nodes['Background']
env=nt.nodes.new('ShaderNodeTexEnvironment'); tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); mp.name='envmap'
nt.links.new(tc.outputs['Generated'],mp.inputs[0]); nt.links.new(mp.outputs[0],env.inputs[0]); nt.links.new(env.outputs[0],bg.inputs['Color']); env.name='env'
# warm room practicals (off-frame)
def light(name,loc,energy,size,color=(1,.62,.32)):
    l=bpy.data.lights.new(name,'AREA'); l.energy=energy; l.size=size; l.color=color; o=bpy.data.objects.new(name,l); S.collection.objects.link(o); o.location=loc; return o
p1=light('prac_left',(-3.6,-1.2,2.3),55,.5); p1.rotation_euler=(math.radians(60),0,math.radians(-70))
p2=light('prac_back',(2.8,-4.5,2.2),90,.6); p2.rotation_euler=(math.radians(65),0,math.radians(150))
import random; random.seed(11)
def bulb(loc,r,col,strength):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=12,ring_count=6); o=bpy.context.active_object; o.name='bokeh'
    m=bpy.data.materials.new('bk'); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear(); out=nt.nodes.new('ShaderNodeOutputMaterial'); e=nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value=col+(1,); e.inputs['Strength'].default_value=strength; nt.links.new(e.outputs[0],out.inputs['Surface']); o.data.materials.append(m)
    o.visible_shadow=False
for i in range(30):
    warm=random.random()<.72
    y=random.uniform(9,28); x=(-0.55+ (i+random.random())/30*1.1)*y*0.9; z=random.uniform(2.6,5.5) if warm else random.uniform(.5,1.1)
    col=(1,.62,.28) if warm else random.choice([(1,.12,.06),(1,.95,.85),(1,.12,.06)])
    bulb((x,y,z),random.uniform(.035,.075)*(y/14),col,random.uniform(18,45))
cam=bpy.data.cameras.new('cam'); co=bpy.data.objects.new('cam',cam); S.collection.objects.link(co); S.camera=co
tgt=bpy.data.objects.new('tgt',None); S.collection.objects.link(tgt)
c=co.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'
cam.sensor_width=36; cam.dof.use_dof=True; cam.dof.focus_object=None
S.cycles.use_denoising=True; S.cycles.denoiser='OPENIMAGEDENOISE'; S.cycles.max_bounces=10; S.cycles.transmission_bounces=10; S.cycles.glossy_bounces=6; S.cycles.transparent_max_bounces=16
S.cycles.caustics_reflective=False; S.cycles.caustics_refractive=False; S.cycles.sample_clamp_indirect=6
S.view_settings.view_transform='AgX'; S.view_settings.look='AgX - Medium High Contrast'
S.render.image_settings.file_format='PNG'; S.render.threads_mode='AUTO'
bpy.ops.wm.save_as_mainfile(filepath='/tmp/fc3d/scene.blend')
# ---- intersection audit ----
dg=bpy.context.evaluated_depsgraph_get(); trees={}
for o in S.collection.objects:
    if o.type not in('MESH','CURVE') or o.name.startswith('bokeh'): continue
    eo=o.evaluated_get(dg); me=eo.to_mesh(); me.transform(o.matrix_world)
    vs=[v.co.copy() for v in me.vertices]; ps=[tuple(p.vertices) for p in me.polygons]
    if ps: trees[o.name]=(BVHTree.FromPolygons(vs,ps,epsilon=0.0), min(v.z for v in vs), [min(v.x for v in vs),max(v.x for v in vs),min(v.y for v in vs),max(v.y for v in vs),min(v.z for v in vs),max(v.z for v in vs)])
    eo.to_mesh_clear()
names=sorted(trees); bad=[]
arch=('wall','ceiling','floor','skirt','rail','panel','casing','sill','sash','muntin','glass','transom','rod')
for i,a in enumerate(names):
    for b in names[i+1:]:
        if a.startswith(arch) and b.startswith(arch): continue
        ba,bb=trees[a][2],trees[b][2]
        if ba[0]>bb[1] or bb[0]>ba[1] or ba[2]>bb[3] or bb[2]>ba[3] or ba[4]>bb[5] or bb[4]>ba[5]: continue
        if a[:4] in('rose','leaf','stem') and b[:4] in('rose','leaf','stem') and a[-1]==b[-1]: continue
        if {a,b}=={'table_base','table_top'}: continue
        ov=trees[a][0].overlap(trees[b][0])
        if ov: bad.append((a,b,len(ov)))
print('INTERSECTIONS',len(bad))
for x in bad: print('  ',x)
for n in ('tablecloth','chair_A','A_plate','lamp_body','vase'): print(n,[round(v,3) for v in trees[n][2]])
