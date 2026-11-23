# adds the room around the main table: a second laid table, a gilt mirror, two wall sconces
import bpy, math
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
bpy.ops.wm.open_mainfile(filepath='/tmp/fc3d/scene_base.blend'); bpy.ops.preferences.addon_enable(module='cycles')
S=bpy.context.scene; C=S.collection; WY=1.55
MAT=bpy.data.materials
# ---- second table, same setting (linked meshes) ----
pref=('table_top','table_base','tablecloth','A_','B_','lamp_','vase','rose','stem','leaf','chair_')
src=[o for o in list(S.objects) if o.type in('MESH','CURVE') and o.name.startswith(pref)]
T=Matrix.Translation((2.55,0.58,0))@Matrix.Rotation(math.radians(8),4,'Z')
T3=Matrix.Translation((4.05,-1.0,0))@Matrix.Rotation(math.radians(95),4,'Z')
for o in src:
    for tag,M_ in (('T2_',T),('T3_',T3)):
        n=o.copy(); n.name=tag+o.name; C.objects.link(n); n.matrix_world=M_@o.matrix_world
# ---- materials ----
def pm(name,**kw):
    m=MAT.new(name); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    for k,v in kw.items(): b.inputs[k].default_value=v
    return m
gilt=pm('gilt',**{'Base Color':(.72,.52,.25,1),'Metallic':1,'Roughness':.38})
mirror=pm('mirror',**{'Base Color':(.62,.60,.56,1),'Metallic':1,'Roughness':.04})
shade=pm('shade',**{'Base Color':(.92,.84,.70,1),'Roughness':.8,'Emission Color':(1,.66,.36,1),'Emission Strength':3.5})
brass=MAT['brass']
def box(name,size,loc,m):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.active_object; o.name=name; o.scale=size
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    bv=o.modifiers.new('bv','BEVEL'); bv.width=min(.004,min(size)/3); bv.segments=2
    return o
# ---- gilt mirror centred in the panel between x=3.0 and 4.0 ----
MX,MZ0,MZ1,MW,FW=3.5,1.40,2.62,.86,.06
box('mirror_pane',(MW-2*FW-.002,.006,MZ1-MZ0-2*FW-.004),(MX,WY-.007,(MZ0+MZ1)/2),mirror)
for i,(sx,sz,lx,lz) in enumerate([(MW,FW,MX,MZ0+FW/2),(MW,FW,MX,MZ1-FW/2),(FW,MZ1-MZ0-2*FW-.002,MX-MW/2+FW/2,(MZ0+MZ1)/2),(FW,MZ1-MZ0-2*FW-.002,MX+MW/2-FW/2,(MZ0+MZ1)/2)]):
    box('mirror_frame%d'%i,(sx,.032,sz),(lx,WY-.0172,lz),gilt)
# ---- sconces in the gaps either side of the mirror panel ----
for k,x in enumerate((2.9,4.1)):
    z=1.98
    box('sconce_plate%d'%k,(.07,.016,.17),(x,WY-.0092,z-.06),brass)
    bpy.ops.mesh.primitive_cylinder_add(radius=.008,depth=.13,location=(x,WY-.017-.065,z-.06),rotation=(math.pi/2,0,0)); a=bpy.context.active_object; a.name='sconce_arm%d'%k; a.data.materials.append(brass)
    bpy.ops.mesh.primitive_cylinder_add(radius=.012,depth=.07,location=(x,WY-.15,z-.02)); c=bpy.context.active_object; c.name='sconce_cup%d'%k; c.data.materials.append(brass)
    bpy.ops.mesh.primitive_cone_add(radius1=.075,radius2=.048,depth=.12,end_fill_type='NOTHING',location=(x,WY-.15,z+.07)); s=bpy.context.active_object; s.name='sconce_shade%d'%k; s.data.materials.append(shade)
    so=s.modifiers.new('so','SOLIDIFY'); so.thickness=.003
    l=bpy.data.lights.new('sconce_l%d'%k,'POINT'); l.energy=14; l.shadow_soft_size=.02; l.color=(1,.62,.32)
    lo=bpy.data.objects.new('sconce_l%d'%k,l); C.objects.link(lo); lo.location=(x,WY-.15,z+.06)
bpy.ops.wm.save_as_mainfile(filepath='/tmp/fc3d/scene.blend')
# ---- intersection audit (same rules as stage2, extended to the new parts) ----
dg=bpy.context.evaluated_depsgraph_get(); trees={}
for o in S.collection.objects:
    if o.type not in('MESH','CURVE') or o.name.startswith('bokeh'): continue
    eo=o.evaluated_get(dg); me=eo.to_mesh(); me.transform(o.matrix_world)
    vs=[v.co.copy() for v in me.vertices]; ps=[tuple(p.vertices) for p in me.polygons]
    if ps: trees[o.name]=(BVHTree.FromPolygons(vs,ps,epsilon=0.0),[min(v.x for v in vs),max(v.x for v in vs),min(v.y for v in vs),max(v.y for v in vs),min(v.z for v in vs),max(v.z for v in vs)])
    eo.to_mesh_clear()
names=sorted(trees); bad=[]
arch=('wall','ceiling','floor','skirt','rail','panel','casing','sill','sash','muntin','glass','transom','rod')
base=lambda n: n[3:] if n.startswith(('T2_','T3_')) else n
for i,a in enumerate(names):
    for b in names[i+1:]:
        if a.startswith(arch) and b.startswith(arch): continue
        ba,bb=trees[a][1],trees[b][1]
        if ba[0]>bb[1] or bb[0]>ba[1] or ba[2]>bb[3] or bb[2]>ba[3] or ba[4]>bb[5] or bb[4]>ba[5]: continue
        A,B=base(a),base(b); same=a[:3]==b[:3] or not (a.startswith(('T2_','T3_')) or b.startswith(('T2_','T3_')))
        if same and A[:4] in('rose','leaf','stem') and B[:4] in('rose','leaf','stem') and A[-1]==B[-1]: continue
        if same and {A,B}=={'table_base','table_top'}: continue
        if a.startswith('sconce') and b.startswith('sconce') and a[-1]==b[-1]: continue
        if a.startswith('mirror_frame') and b.startswith('mirror_frame'): continue
        ov=trees[a][0].overlap(trees[b][0])
        if ov: bad.append((a,b,len(ov)))
print('INTERSECTIONS',len(bad))
for x in bad: print('  ',x)
