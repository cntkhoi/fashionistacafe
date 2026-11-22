import bpy, bmesh, math, random, sys
from mathutils import Vector, Matrix, Euler
from mathutils.bvhtree import BVHTree
A='/tmp/fc3d/assets/'
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_enable(module='cycles')
S=bpy.context.scene; S.render.engine='CYCLES'
col=S.collection
def link(o): col.objects.link(o); return o

# ---------- materials ----------
def mat(name, **kw):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes['Principled BSDF']
    for k,v in kw.items(): b.inputs[k].default_value=v
    return m
def add_bump(m, scale=400, strength=.1, kind='NOISE', detail=4, dist=.001, coord='Object', stretch=None, rough_var=0):
    nt=m.node_tree; b=nt.nodes['Principled BSDF']
    tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); nt.links.new(tc.outputs[coord],mp.inputs['Vector'])
    if stretch: mp.inputs['Scale'].default_value=stretch
    if kind=='NOISE':
        t=nt.nodes.new('ShaderNodeTexNoise'); t.inputs['Scale'].default_value=scale; t.inputs['Detail'].default_value=detail; out=t.outputs['Fac']
    else:
        t=nt.nodes.new('ShaderNodeTexWave'); t.inputs['Scale'].default_value=scale; t.inputs['Distortion'].default_value=1.5; t.inputs['Detail'].default_value=2
        t2=nt.nodes.new('ShaderNodeTexWave'); t2.inputs['Scale'].default_value=scale; t2.bands_direction='Y'; t2.inputs['Distortion'].default_value=1.5
        nt.links.new(mp.outputs[0],t2.inputs['Vector'])
        mx=nt.nodes.new('ShaderNodeMath'); mx.operation='MULTIPLY'; nt.links.new(t.outputs['Fac'],mx.inputs[0]); nt.links.new(t2.outputs['Fac'],mx.inputs[1]); out=mx.outputs[0]
    nt.links.new(mp.outputs[0],t.inputs['Vector'])
    bp=nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value=strength; bp.inputs['Distance'].default_value=dist
    nt.links.new(out,bp.inputs['Height']); nt.links.new(bp.outputs[0],b.inputs['Normal'])
    if rough_var:
        r=b.inputs['Roughness'].default_value
        mr=nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value=max(0,r-rough_var); mr.inputs['To Max'].default_value=r+rough_var
        n2=nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value=18; n2.inputs['Detail'].default_value=6
        nt.links.new(tc.outputs['Object'],n2.inputs['Vector']); nt.links.new(n2.outputs['Fac'],mr.inputs['Value']); nt.links.new(mr.outputs[0],b.inputs['Roughness'])
    return m
M={}
M['porcelain']=mat('porcelain',**{'Base Color':(.9,.88,.83,1),'Roughness':.1,'Coat Weight':.6,'Coat Roughness':.05})
M['silver']=add_bump(mat('silver',**{'Base Color':(.93,.91,.87,1),'Metallic':1,'Roughness':.13}),scale=3,strength=0,rough_var=.05)
M['crystal']=mat('crystal',**{'Base Color':(1,1,1,1),'Roughness':0,'Transmission Weight':1,'IOR':1.5})
_nt=M['crystal'].node_tree; _b=_nt.nodes['Principled BSDF']; _o=_nt.nodes['Material Output']; _lp=_nt.nodes.new('ShaderNodeLightPath'); _t=_nt.nodes.new('ShaderNodeBsdfTransparent'); _t.inputs['Color'].default_value=(.9,.9,.9,1); _m=_nt.nodes.new('ShaderNodeMixShader')
_nt.links.new(_lp.outputs['Is Shadow Ray'],_m.inputs[0]); _nt.links.new(_b.outputs[0],_m.inputs[1]); _nt.links.new(_t.outputs[0],_m.inputs[2]); _nt.links.new(_m.outputs[0],_o.inputs['Surface'])
M['linen']=add_bump(mat('linen',**{'Base Color':(.80,.77,.71,1),'Roughness':.92,'Sheen Weight':.35}),scale=900,strength=.25,kind='WAVE',dist=.0004,coord='UV')
M['napkin']=add_bump(mat('napkin',**{'Base Color':(.83,.80,.74,1),'Roughness':.95,'Sheen Weight':.4}),scale=2600,strength=.35,kind='WAVE',dist=.0004)
M['brass']=add_bump(mat('brass',**{'Base Color':(.80,.58,.28,1),'Metallic':1,'Roughness':.27}),scale=60,strength=.04,stretch=(1,1,40),rough_var=.06)
M['wall']=add_bump(mat('wall',**{'Base Color':(.46,.41,.35,1),'Roughness':.82}),scale=45,strength=.12,detail=8,dist=.002,rough_var=.05)
M['trim']=add_bump(mat('trim',**{'Base Color':(.50,.45,.37,1),'Roughness':.42}),scale=30,strength=.05,dist=.001,rough_var=.08)
M['drape']=add_bump(mat('drape',**{'Base Color':(.20,.165,.13,1),'Roughness':.9,'Sheen Weight':.8,'Sheen Roughness':.4}),scale=1500,strength=.3,kind='WAVE',dist=.0005)
M['sheer']=mat('sheer',**{'Base Color':(.9,.87,.8,1),'Roughness':.9,'Transmission Weight':.0,'Alpha':.28})
M['vase']=add_bump(mat('vase',**{'Base Color':(.72,.70,.64,1),'Roughness':.32,'Coat Weight':.3}),scale=220,strength=.06,dist=.0006,rough_var=.08)
M['petal']=mat('petal',**{'Base Color':(.93,.87,.78,1),'Roughness':.55,'Subsurface Weight':.35,'Subsurface Radius':(.02,.012,.008),'Subsurface Scale':.3})
M['petal2']=mat('petal2',**{'Base Color':(.90,.74,.66,1),'Roughness':.55,'Subsurface Weight':.35,'Subsurface Radius':(.02,.012,.008),'Subsurface Scale':.3})
M['leaf']=mat('leaf',**{'Base Color':(.06,.11,.045,1),'Roughness':.45,'Subsurface Weight':.1})
M['dark']=mat('dark',**{'Base Color':(.03,.027,.025,1),'Roughness':.5})
M['led']=mat('led'); nt=M['led'].node_tree; b=nt.nodes['Principled BSDF']; b.inputs['Emission Color'].default_value=(1,.56,.24,1); b.inputs['Emission Strength'].default_value=1; b.inputs['Base Color'].default_value=(1,.8,.6,1)
# architectural glass (no caustics noise)
g=bpy.data.materials.new('pane'); g.use_nodes=True; nt=g.node_tree; nt.nodes.clear()
o=nt.nodes.new('ShaderNodeOutputMaterial'); tr=nt.nodes.new('ShaderNodeBsdfTransparent'); gl=nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value=0.0
fr=nt.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value=1.25; mx=nt.nodes.new('ShaderNodeMixShader'); tr.inputs['Color'].default_value=(.93,.96,.97,1)
mx.inputs[0].default_value=0.0; nt.links.new(tr.outputs[0],mx.inputs[1]); nt.links.new(gl.outputs[0],mx.inputs[2]); nt.links.new(mx.outputs[0],o.inputs['Surface']); M['pane']=g
# floor
fm=bpy.data.materials.new('floor'); fm.use_nodes=True; nt=fm.node_tree; b=nt.nodes['Principled BSDF']
tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(1.1,1.1,1.1); mp.inputs['Rotation'].default_value=(0,0,math.radians(45)); nt.links.new(tc.outputs['Object'],mp.inputs[0])
def img(p,cs='sRGB'):
    n=nt.nodes.new('ShaderNodeTexImage'); n.image=bpy.data.images.load(p); n.image.colorspace_settings.name=cs; nt.links.new(mp.outputs[0],n.inputs[0]); return n
d=img(A+'floor/Diffuse.jpg'); r=img(A+'floor/Rough.jpg','Non-Color'); n=img(A+'floor/nor_gl.jpg','Non-Color')
hs=nt.nodes.new('ShaderNodeHueSaturation'); hs.inputs['Value'].default_value=.42; hs.inputs['Saturation'].default_value=.9; nt.links.new(d.outputs[0],hs.inputs['Color']); nt.links.new(hs.outputs[0],b.inputs['Base Color'])
mr=nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value=.12; mr.inputs['To Max'].default_value=.38; nt.links.new(r.outputs[0],mr.inputs[0]); nt.links.new(mr.outputs[0],b.inputs['Roughness'])
nm=nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value=.7; nt.links.new(n.outputs[0],nm.inputs['Color']); nt.links.new(nm.outputs[0],b.inputs['Normal']); M['floor']=fm

# ---------- mesh helpers ----------
def obj_from(name, verts, faces, m=None, smooth=True, sub=0):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    o=bpy.data.objects.new(name,me); link(o)
    if smooth:
        for p in me.polygons: p.use_smooth=True
    if m: me.materials.append(m)
    if sub:
        s=o.modifiers.new('sub','SUBSURF'); s.levels=1; s.render_levels=sub
    return o
def lathe(name, prof, m, seg=64, sub=2):
    V=[];F=[];n=len(prof)
    for (r,z) in prof:
        for j in range(seg):
            a=2*math.pi*j/seg; V.append((max(r,1e-5)*math.cos(a),max(r,1e-5)*math.sin(a),z))
    for i in range(n-1):
        for j in range(seg):
            a=i*seg+j; b_=i*seg+(j+1)%seg; F.append((a,b_,b_+seg,a+seg))
    return obj_from(name,V,F,m,sub=sub)
def box(name, size, loc, m, bevel=.004, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1); o=bpy.context.active_object; o.name=name
    o.scale=size; o.location=loc; o.rotation_euler=rot
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bv=o.modifiers.new('bv','BEVEL'); bv.width=bevel; bv.segments=3
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth=True
    return o
def place(o, loc, rz=0):
    o.location=loc; o.rotation_euler=(0,0,rz); return o
def join(objs,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]; bpy.ops.object.join(); objs[0].name=name; return objs[0]
def apply_mods(o):
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
    for md in list(o.modifiers): bpy.ops.object.modifier_apply(modifier=md.name)

TABLE_R=.525; TABLE_H=.75
# ---------- room ----------
WY=1.55            # window wall plane (inner face)
WIN_L,WIN_R,WIN_B,WIN_T=-1.05,1.05,.42,2.75
def wallbox(n,x0,x1,z0,z1,y0=WY,y1=WY+.3): return box(n,(x1-x0,y1-y0,z1-z0),((x0+x1)/2,(y0+y1)/2,(z0+z1)/2),M['wall'],bevel=0)
wallbox('wall_l',-5,WIN_L,0,3.6); wallbox('wall_r',WIN_R,5,0,3.6); wallbox('wall_b',WIN_L,WIN_R,0,WIN_B); wallbox('wall_t',WIN_L,WIN_R,WIN_T,3.6)
box('wall_left',(.3,9,3.6),(-5.15,-2.8,1.8),M['wall'],bevel=0); box('wall_right',(.3,9,3.6),(5.15,-2.8,1.8),M['wall'],bevel=0)
box('wall_back',(10.6,.3,3.6),(0,-7.3,1.8),M['wall'],bevel=0); box('ceiling',(10.6,9.2,.2),(0,-2.8,3.7),M['wall'],bevel=0)
fl=box('floor',(10.6,9.2,.1),(0,-2.8,-.05),M['floor'],bevel=0)
# skirting, chair rail, wall panels (mouldings)
for x0,x1 in ((-5,WIN_L-.12),(WIN_R+.12,5)):
    box('skirt',(x1-x0,.025,.16),((x0+x1)/2,WY-.0127,.0801),M['trim'],bevel=.006)
    box('rail',(x1-x0,.03,.05),((x0+x1)/2,WY-.0152,.95),M['trim'],bevel=.01)
def frame(n,x0,x1,z0,z1,w=.035,d=.018,y=WY):
    parts=[box(n,(x1-x0,d,w),((x0+x1)/2,y-d/2-.0002,z0+w/2),M['trim'],bevel=.006),box(n,(x1-x0,d,w),((x0+x1)/2,y-d/2-.0002,z1-w/2),M['trim'],bevel=.006),
           box(n,(w,d,z1-z0-2*w-.0006),(x0+w/2,y-d/2-.0002,(z0+z1)/2),M['trim'],bevel=.006),box(n,(w,d,z1-z0-2*w-.0006),(x1-w/2,y-d/2-.0002,(z0+z1)/2),M['trim'],bevel=.006)]
    return parts
for sx in (-1,1):
    for k in range(3):
        x0=sx*(WIN_R+.75+k*1.2); x1=sx*(WIN_R+.75+k*1.2+1.0); a,b_=min(x0,x1),max(x0,x1)
        frame('panel',a,b_,1.12,3.0); frame('panel_low',a,b_,.26,.84)
# window casing + sashes
CD=.14  # casing depth into room
box('casing_l',(.12,CD,WIN_T-WIN_B+.24),(WIN_L-.0602,WY-CD/2-.0002,(WIN_T+WIN_B)/2),M['trim'],bevel=.012)
box('casing_r',(.12,CD,WIN_T-WIN_B+.24),(WIN_R+.0602,WY-CD/2-.0002,(WIN_T+WIN_B)/2),M['trim'],bevel=.012)
box('casing_t',(WIN_R-WIN_L,CD,.12),(0,WY-CD/2-.0002,WIN_T+.0602),M['trim'],bevel=.012)
box('sill',(WIN_R-WIN_L+.3,.2,.045),(0,WY-.0202,WIN_B-.0227),M['trim'],bevel=.012)
GY=WY+.12  # glass plane y
def sash(x0,x1,z0,z1,rows):
    st=.07
    box('sash',(x1-x0,.05,st),((x0+x1)/2,GY,z0+st/2),M['trim'],bevel=.008); box('sash',(x1-x0,.05,st),((x0+x1)/2,GY,z1-st/2),M['trim'],bevel=.008)
    box('sash',(st,.05,z1-z0-2*st-.0004),(x0+st/2,GY,(z0+z1)/2),M['trim'],bevel=.008); box('sash',(st,.05,z1-z0-2*st-.0004),(x1-st/2,GY,(z0+z1)/2),M['trim'],bevel=.008)
    h=(z1-z0-2*st)/rows
    for i in range(1,rows): box('muntin',(x1-x0-2*st-.0004,.03,.022),((x0+x1)/2,GY,z0+st+i*h),M['trim'],bevel=.005)
    box('glass',(x1-x0-2*st-.0004,.004,z1-z0-2*st-.0004),((x0+x1)/2,GY+.004,(z0+z1)/2),M['pane'],bevel=0)
TR=2.12
sash(WIN_L+.0003,-.0003,WIN_B+.0003,TR-.0153,3); sash(.0003,WIN_R-.0003,WIN_B+.0003,TR-.0153,3)
box('transom_bar',(WIN_R-WIN_L-.0006,.07,.03),(0,GY,TR),M['trim'],bevel=.008)
sash(WIN_L+.0003,-.0003,TR+.0153,WIN_T-.0003,1); sash(.0003,WIN_R-.0003,TR+.0153,WIN_T-.0003,1)
# drapes
def drape(name,xc,width,m,y,amp,folds,z0=.012,z1=2.98,gather=0):
    nx=140; nz=24; V=[];F=[]
    for k in range(nz+1):
        t=k/nz; z=z0+(z1-z0)*t
        for i in range(nx+1):
            u=i/nx; x=xc+(u-.5)*width*(1-gather*math.sin(math.pi*min(1,t*1.0))*0)
            ph=u*folds*2*math.pi
            yy=y-amp*(math.sin(ph)+.25*math.sin(2.3*ph+1.3))*(.75+.25*math.sin(u*9+t*1.5))-amp*1.3
            V.append((x,yy,z))
    for k in range(nz):
        for i in range(nx):
            a=k*(nx+1)+i; F.append((a,a+1,a+nx+2,a+nx+1))
    o=obj_from(name,V,F,m,sub=1); s=o.modifiers.new('so','SOLIDIFY'); s.thickness=.003; return o
drape('drape_l',WIN_L-.36,.62,M['drape'],WY-CD-.06,.04,6.5); drape('drape_r',WIN_R+.36,.62,M['drape'],WY-CD-.06,.04,6.5)
box('rod',(3.6,.02,.02),(0,WY-CD-.115,3.03),M['brass'],bevel=.009)

# ---------- table + cloth ----------
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=TABLE_R,depth=.03,location=(0,0,TABLE_H-.015)); top=bpy.context.active_object; top.name='table_top'; top.data.materials.append(M['dark'])
ped=lathe('table_base',[(0,0),(.26,0),(.26,.02),(.06,.06),(.045,.3),(.05,.68),(.2,.72),(.2,.735)],M['dark'],seg=48,sub=1); ped.location=(0,0,.0003)
# cloth: disc, simulated
CR=1.02; rings=70; segs=220; V=[(0,0,0)];F=[]
for i in range(1,rings+1):
    r=CR*i/rings
    for j in range(segs):
        a=2*math.pi*j/segs; V.append((r*math.cos(a),r*math.sin(a),0))
for j in range(segs): F.append((0,1+j,1+(j+1)%segs))
for i in range(1,rings):
    for j in range(segs):
        a=1+(i-1)*segs+j; b_=1+(i-1)*segs+(j+1)%segs; F.append((a,b_,b_+segs,a+segs))
cloth=obj_from('tablecloth',V,F,M['linen'],sub=0); cloth.location=(0,0,TABLE_H+.005)
vg=cloth.vertex_groups.new(name='pin'); vg.add([v.index for v in cloth.data.vertices if v.co.xy.length<TABLE_R-.015],1.0,'REPLACE')
uv=cloth.data.uv_layers.new(name='UVMap')
for l in cloth.data.loops:
    v=cloth.data.vertices[l.vertex_index].co; uv.data[l.index].uv=(v.x,v.y)
for o in (top,ped):
    c=o.modifiers.new('col','COLLISION'); o.collision.thickness_outer=.006; o.collision.cloth_friction=8
cm=cloth.modifiers.new('cloth','CLOTH'); cs=cm.settings; cs.quality=7; cs.mass=.25; cs.tension_stiffness=18; cs.compression_stiffness=18; cs.shear_stiffness=6; cs.bending_stiffness=.35
cs.vertex_group_mass='pin'; cs.tension_damping=6; cs.compression_damping=6; cs.bending_damping=.6; cs.air_damping=.6
cm.collision_settings.use_self_collision=True; cm.collision_settings.self_distance_min=.004; cm.collision_settings.distance_min=.004; cm.collision_settings.collision_quality=3
S.frame_start=1; S.frame_end=170; cm.point_cache.frame_start=1; cm.point_cache.frame_end=170
for f in range(1,171): S.frame_set(f)
apply_mods(cloth)
ztop=0.0
for v in cloth.data.vertices:
    if v.co.z>0: v.co.z=0.0
top.scale=(.955,.955,1); top.location.z-=.012
bm=bmesh.new(); bm.from_mesh(cloth.data)
kill=[v for v in bm.verts if v.co.xy.length<.30]; bmesh.ops.delete(bm,geom=kill,context='VERTS')
bm.edges.ensure_lookup_table(); be=[e for e in bm.edges if e.is_boundary and e.verts[0].co.xy.length<.4]
bmesh.ops.contextual_create(bm,geom=be); bm.normal_update(); bm.to_mesh(cloth.data); bm.free()
so=cloth.modifiers.new('so','SOLIDIFY'); so.thickness=.0012; so.offset=-1; so.use_rim=True
for p in cloth.data.polygons: p.use_smooth=True
TZ=cloth.location.z+ztop+.0012+.0006   # resting plane for tableware
print('cloth top',TZ, 'min z', min((cloth.matrix_world@v.co).z for v in cloth.data.vertices))

# ---------- tableware ----------
def plate(name,R):
    k=R/.135
    prof=[(0,.0045),(.09*k,.0045),(.1*k,.0052),(.112*k,.0085),(.129*k,.0135),(.1338*k,.0146),(.135*k,.014),(.1345*k,.013),(.113*k,.0045),(.1*k,.001),(.094*k,0),(.07*k,0),(.068*k,.0015),(0,.0015)]
    return lathe(name,prof,M['porcelain'],seg=96,sub=2)
def stemglass(name,bowl,stem_h=.085,foot=.037,th=.0011):
    outer=[(0,.0018),(foot*.6,.0018),(foot,.0012),(foot+.0006,.0006),(foot,0),(0,0)]
    outer=[(0,0),(foot,0),(foot+.0005,.0007),(foot,.0014),(foot*.5,.003),(.0045,.009),(.0036,.02),(.0036,stem_h-.012),(.0048,stem_h-.003)]
    out=[(r,stem_h+z) for r,z in bowl]
    inn=[(max(r-th,0),stem_h+z+(th if i==0 else 0)) for i,(r,z) in enumerate(bowl)][::-1]
    rim=[(bowl[-1][0]-th/2,stem_h+bowl[-1][1]+th*.6)]
    prof=outer+out+rim+inn+[(0,stem_h+bowl[0][1]+th*2.2)]
    return lathe(name,prof,M['crystal'],seg=72,sub=2)
RED=[(.006,0),(.02,.006),(.036,.022),(.044,.045),(.045,.065),(.041,.095),(.0345,.125)]
WHT=[(.006,0),(.018,.006),(.03,.022),(.035,.045),(.0345,.07),(.031,.098),(.028,.112)]
WAT=[(.006,0),(.022,.004),(.034,.016),(.039,.04),(.04,.07),(.0395,.085)]
def ribbon(name, L, wfun, zfun, m, cols=8, rows=44, th=.0022, gaps=None):
    V=[];F=[]
    for i in range(rows+1):
        t=i/rows; w=wfun(t)
        for j in range(cols+1):
            u=j/cols*2-1; V.append((u*w,(t-.5)*L,zfun(t,u)))
    for i in range(rows):
        t=(i+.5)/rows
        for j in range(cols):
            if gaps and gaps(t,j): continue
            a=i*(cols+1)+j; F.append((a,a+1,a+cols+2,a+cols+1))
    o=obj_from(name,V,F,m,sub=2); s=o.modifiers.new('so','SOLIDIFY'); s.thickness=th; s.offset=1
    o.modifiers.move(1,0); return o
def sstep(a,b,x):
    t=max(0,min(1,(x-a)/(b-a))); return t*t*(3-2*t)
def handle_w(t,end=.0085,neck=.0032,n0=.55,n1=.68):
    # t 0 = handle end ... n0..n1 neck
    return end*(1-.25*sstep(0,.03,.03-t)*0)*(.55+.45*sstep(0,.06,t))*(1-sstep(.1,n0,t))+neck*sstep(.1,n0,t) if t<n1 else None
def fork(name,L=.205):
    def w(t):
        if t<.66: return .0034+.0056*(1-sstep(.08,.62,t))*(.6+.4*sstep(0,.05,t))
        return .0034+.0086*sstep(.66,.76,t)*(1-.18*sstep(.9,1,t))
    def z(t,u): return .004*math.sin(math.pi*sstep(.5,.8,t))*1.0+.0035*sstep(.8,1,t)-.0008*sstep(.7,.8,t)*0+.0016*(1-sstep(0,.3,t))*0 - .002*(u*u)*sstep(.7,.85,t)
    return ribbon(name,L,w,z,M['silver'],cols=7,rows=48,gaps=lambda t,j: t>.80 and j in (1,3,5))
def spoon(name,L=.185):
    def w(t):
        if t<.68: return .003+.0052*(1-sstep(.08,.6,t))*(.6+.4*sstep(0,.05,t))
        x=(t-.84)/.16; return .0032+.0158*math.sqrt(max(0,1-x*x))**.9*sstep(.68,.74,t)
    def z(t,u):
        base=.0045*math.sin(math.pi*sstep(.45,.75,t))
        if t>.69:
            x=(t-.845)/.155; d=max(0,1-x*x-u*u*.9); return base-.0062*d**.6+.004*sstep(.69,.8,t)*0
        return base
    return ribbon(name,L,w,z,M['silver'],cols=8,rows=56)
def knife(name,L=.225):
    # solid of elliptical cross-sections: hollow handle -> bolster -> blade with straight spine and curved edge
    st=56; rg=16; V=[];F=[]
    for i in range(st+1):
        t=i/st
        if t<.46:   # handle
            w=.0062+.0026*math.sin(math.pi*(t/.46)**.8)*.9+.0006; h=.0030+.0016*math.sin(math.pi*(t/.46)**.85); cx=0
            e=sstep(0,.035,t); w*=(.35+.65*e); h*=(.35+.65*e)
        elif t<.52: # bolster / neck
            k=sstep(.46,.52,t); w=.0068-.0010*k; h=.0030-.0020*k; cx=0
        else:       # blade
            k=(t-.52)/.48; w=.0058+.0050*math.sin(math.pi*min(1,k*1.15)**.7)*(1 if k<.87 else 1) ; w*=(1-sstep(.82,1,k)**2*.97); h=.0010-.00045*k; cx=(w-.0058)*.9
        y=(t-.5)*L
        for j in range(rg):
            a=2*math.pi*j/rg; V.append((cx+w*math.cos(a),y,h+h*math.sin(a)))
    for i in range(st):
        for j in range(rg):
            a=i*rg+j; b_=i*rg+(j+1)%rg; F.append((a,b_,b_+rg,a+rg))
    F.append(tuple(range(rg-1,-1,-1))); F.append(tuple(range(st*rg,st*rg+rg)))
    return obj_from(name,V,F,M['silver'],sub=2)
def napkin(name):
    objs=[]
    for k,(sx,sy,sz,z0) in enumerate(((.072,.168,.0042,0),(.069,.162,.0042,.0046))):
        bpy.ops.mesh.primitive_cube_add(size=1); o=bpy.context.active_object; o.scale=(sx,sy,sz); o.location=(0,(.002 if k else 0),z0+sz/2); bpy.ops.object.transform_apply(location=True,scale=True)
        bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.subdivide_edges(bm,edges=bm.edges[:],cuts=7,use_grid_fill=True)
        for v in bm.verts:
            if v.co.z>z0+sz*.5: v.co.z+= .0005*math.sin(v.co.y*85+v.co.x*50+k)+.0004*math.sin(v.co.x*190+k*2)+ .0009*k*(1-abs(v.co.x)/.036)
        bm.to_mesh(o.data); bm.free()
        bv=o.modifiers.new('bv','BEVEL'); bv.width=.0018; bv.segments=3; s_=o.modifiers.new('s','SUBSURF'); s_.levels=1; s_.render_levels=2
        o.data.materials.append(M['napkin'])
        for p in o.data.polygons: p.use_smooth=True
        objs.append(o)
    return join(objs,name)
SET=[]
def setting(tag, cx, rz):
    # local frame: diner sits at -Y looking +Y (table centre at +Y). lateral = X (right hand +X)
    R=Matrix.Rotation(rz,4,'Z'); T=Matrix.Translation((cx,0,0))
    def put(o,x,y,z=0,r=0,rest=True):
        o.matrix_world=T@R@Matrix.Translation((x,y,z))@Matrix.Rotation(r,4,'Z'); o.name=tag+'_'+o.name; SET.append(o)
        if rest:
            bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get(); eo=o.evaluated_get(dg); me=eo.to_mesh()
            mz=min((eo.matrix_world@v.co).z for v in me.vertices); eo.to_mesh_clear()
            o.matrix_world=Matrix.Translation((0,0,z-mz))@o.matrix_world
        return o
    put(plate('plate',.135),0,0,TZ)
    put(napkin('napkin'),0,0,TZ+.0045+.0004)
    put(fork('fork_main'),-.178,-.005,TZ+.0003); put(fork('fork_starter',.185),-.208,-.012,TZ+.0003)
    put(knife('knife_main'),.178,-.005,TZ+.0003); put(knife('knife_starter',.205),.208,-.012,TZ+.0003)
    put(spoon('spoon_dessert',.17),.0,.178,TZ+.0003,r=-math.pi/2)
    put(plate('plate_bread',.078),-.262,.15,TZ)
    bk=put(knife('knife_butter',.16),-.262,.15,TZ+.0158,r=math.radians(-35),rest=False)
    put(stemglass('glass_red',RED),.10,.235,TZ+.0002); put(stemglass('glass_white',WHT,stem_h=.08,foot=.034),.25,.115,TZ+.0002); put(stemglass('glass_water',WAT,stem_h=.055,foot=.036),.165,.165,TZ+.0002)
SCEN=.365
setting('A',-SCEN,-math.pi/2); setting('B',SCEN,math.pi/2)

# ---------- lamp ----------
LX,LY=.02,.12
base=lathe('lamp_body',[(0,0),(.048,0),(.05,.002),(.05,.006),(.046,.012),(.02,.03),(.0105,.05),(.0095,.12),(.0095,.262),(.012,.27),(.0,.272)],M['brass'],seg=64,sub=2)
shade=lathe('lamp_shade',[(.0125,.2705),(.03,.262),(.058,.228),(.0605,.222),(.0595,.2215),(.0575,.2255),(.03,.2585),(.0125,.2665)],M['brass'],seg=96,sub=2)
led=lathe('lamp_led',[(0.0135,.2578),(.026,.2578),(.0262,.2572),(.026,.2566),(.0135,.2566)],M['led'],seg=48,sub=1)
for o in (base,shade,led): o.location=(LX,LY,TZ+.0003)
# ---------- vase + roses ----------
VX,VY=-.02,-.12
vase=lathe('vase',[(0,0),(.026,0),(.03,.003),(.038,.03),(.036,.06),(.022,.088),(.0165,.1),(.0185,.108),(.0165,.1085),(.0145,.1),(.0195,.088),(.033,.06),(.035,.03),(.027,.006),(0,.005)],M['vase'],seg=72,sub=2)
vase.location=(VX,VY,TZ+.0003)
def rose(name,size=1.0,m=None,n=30):
    V=[];F=[]; nu,nv=6,7
    for i in range(n):
        t=i/(n-1); ang=i*2.39996+random.uniform(-.15,.15)
        Lp=(.02+.02*t)*size; W=(.011+.017*t)*size; tilt=math.radians(4+62*t**1.6+random.uniform(-4,4)); rad=(.0015+.011*t)*size
        curl=1.5-1.0*t; base=len(V)
        for b_ in range(nv+1):
            v=b_/nv
            hw=W*(.3+.7*(v/.6)**.8) if v<.6 else W*math.sqrt(max(0,1-((v-.6)/.42)**2))
            for a in range(nu+1):
                u=a/nu*2-1; x=u*hw
                y=-curl*(x*x)/(W)*.9 + (.006*size)*t*(v**3)*1.2      # cup + lip roll-back
                z=v*Lp
                # tilt outward about x axis, then offset radially, rotate about z
                yy=y*math.cos(tilt)+z*math.sin(tilt)+rad; zz=-y*math.sin(tilt)+z*math.cos(tilt)-.004*size*t
                V.append((x*math.cos(ang)-yy*math.sin(ang), x*math.sin(ang)+yy*math.cos(ang), zz))
        for b_ in range(nv):
            for a in range(nu):
                p=base+b_*(nu+1)+a; F.append((p,p+1,p+nu+2,p+nu+1))
    o=obj_from(name,V,F,m or M['petal'],sub=2); s=o.modifiers.new('so','SOLIDIFY'); s.thickness=.0006; return o
def leaf(name,L=.05):
    V=[];F=[];nu,nv=4,10
    for b_ in range(nv+1):
        v=b_/nv; hw=.38*L*math.sin(math.pi*v**.75)**.9
        for a in range(nu+1):
            u=a/nu*2-1; V.append((u*hw,v*L,.006*abs(u)*hw/ (.38*L+1e-6)*3 - .012*v*v))
    for b_ in range(nv):
        for a in range(nu):
            p=b_*(nu+1)+a; F.append((p,p+1,p+nu+2,p+nu+1))
    o=obj_from(name,V,F,M['leaf'],sub=2); s=o.modifiers.new('so','SOLIDIFY'); s.thickness=.0005; return o
def stem(name,p0,p1,bend):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; sp=cu.splines.new('BEZIER'); sp.bezier_points.add(2)
    a,mid,b_=sp.bezier_points; a.co=p0; mid.co=(VX+(p0[0]-VX)*.8,VY+(p0[1]-VY)*.8,vz+.112); mid.handle_left=Vector(mid.co)-Vector((0,0,.03)); mid.handle_right=Vector(mid.co)+Vector((0,0,.03))
    a.handle_right=Vector(p0)+Vector((0,0,.03)); b_.co=p1; a.handle_left=Vector(p0)-Vector((0,0,.03))
    b_.handle_left=Vector(p1)-Vector(bend); b_.handle_right=Vector(p1)+Vector(bend)
    cu.bevel_depth=.0022; cu.bevel_resolution=4; cu.resolution_u=24
    o=bpy.data.objects.new(name,cu); link(o); cu.materials.append(M['leaf']); return o
vz=TZ+.0003
blooms=[((-.046,.018,.228),1.0,M['petal'],(.22,-.2)),((.052,.0,.196),.9,M['petal2'],(-.32,0)),((-.004,-.056,.172),.82,M['petal'],(0,.35)),((.032,.062,.27),.6,M['petal2'],(-.08,-.28))]
for i,(p,sz,m,tl) in enumerate(blooms):
    a=math.atan2(p[1],p[0]); p0=(VX+.0075*math.cos(a),VY+.0075*math.sin(a),vz+.012)
    P=Vector((VX+p[0],VY+p[1],vz+p[2]))
    ax=Vector((p[0],p[1],0)).normalized()
    r=rose('rose%d'%i,sz,m,n=30 if sz>.7 else 18)
    r.rotation_euler=Euler((tl[1],tl[0],i*1.3)); r.location=P
    stem('stem%d'%i,p0,tuple(P-Vector((p[0]*.08,p[1]*.08,.007*sz))),(p[0]*.3,p[1]*.3,.03))
    lf=leaf('leaf%d'%i,.036*sz+.01); lf.location=(VX+p[0]*.5,VY+p[1]*.5,vz+.118+p[2]*.12+ i*.006); lf.rotation_euler=Euler((math.radians(-20),0,math.atan2(p[1],p[0])-math.pi/2+ 1.3))

# ---------- chairs ----------
bpy.ops.import_scene.gltf(filepath=A+'chair/dining_chair_02.gltf')
ch=[o for o in bpy.context.selected_objects if o.type=='MESH'][0]
bpy.ops.object.select_all(action='DESELECT'); ch.select_set(True); bpy.context.view_layer.objects.active=ch
bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM'); bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bb=[Vector(c) for c in ch.bound_box]; mn=Vector((min(c.x for c in bb),min(c.y for c in bb),min(c.z for c in bb))); mx_=Vector((max(c.x for c in bb),max(c.y for c in bb),max(c.z for c in bb)))
print('chair bbox',mn,mx_)
ch.name='chair_A'
for o in list(bpy.data.objects):
    if o.type=='EMPTY': bpy.data.objects.remove(o)
bpy.context.scene.cursor.location=((mn.x+mx_.x)/2,(mn.y+mx_.y)/2,mn.z); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.data.texts.new('chairdims').write(repr((tuple(mn),tuple(mx_))))
ch.location=(0,0,.0004)
bpy.ops.wm.save_as_mainfile(filepath='/tmp/fc3d/stage1.blend')
print('OK objects',len(bpy.data.objects))
