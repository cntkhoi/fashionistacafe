import bpy, sys, math, json, os
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; P=json.loads(a[0])
bpy.ops.wm.open_mainfile(filepath='/tmp/fc3d/scene.blend'); bpy.ops.preferences.addon_enable(module='cycles')
S=bpy.context.scene; S.render.engine='CYCLES'; cam=S.camera
nt=S.world.node_tree
def setenv(h,rot,strength):
    nt.nodes['env'].image=bpy.data.images.load('/tmp/fc3d/assets/hdri/%s.hdr'%h,check_existing=True)
    nt.nodes['envmap'].inputs['Rotation'].default_value=(0,0,math.radians(rot)); nt.nodes['Background'].inputs['Strength'].default_value=strength
led=bpy.data.materials['led'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
K=[dict(p=(-1.9,-3.0,1.25),t=(0.0,0.1,0.98),lens=42,fp=(.02,.12,1.0),f=2.0),
   dict(p=(-1.78,-1.7,1.3),t=(0.05,0.08,0.92),lens=42,fp=(.02,.12,1.0),f=2.0),
   dict(p=(-1.3,-0.4,1.22),t=(0.3,0.12,0.88),lens=36,fp=(.02,.12,1.0),f=2.0),
   dict(p=(-0.95,-0.12,1.36),t=(-0.33,0.0,0.76),lens=46,fp=(-.36,0,.77),f=2.8)]
def cr(p0,p1,p2,p3,t):
    return tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t) for a,b,c,d in zip(p0,p1,p2,p3))
def at(u):
    i=min(int(u),len(K)-2); t=u-i; k=[K[max(i-1,0)],K[i],K[i+1],K[min(i+2,len(K)-1)]]
    g=lambda key: cr(*[x[key] if isinstance(x[key],tuple) else (x[key],) for x in k],t)
    return g('p'),g('t'),g('lens')[0],g('fp'),g('f')[0]
def ss(x): return x*x*x*(x*(x*6-15)+10)
N=P.get('n',48); SPLIT=P.get('split',32)
def u_of(fr):
    if fr<=SPLIT: return 2*ss(fr/SPLIT)
    return 2+ss((fr-SPLIT)/(N-1-SPLIT))
def setcam(u):
    p,t,lens,fp,f=at(u); cam.location=p; bpy.data.objects['tgt'].location=t; cam.data.lens=lens
    cam.data.dof.focus_distance=(Vector(p)-Vector(fp)).length; cam.data.dof.aperture_fstop=f; cam.data.dof.use_dof=True
S.render.resolution_x,S.render.resolution_y=P.get('res',[1280,960]); S.cycles.samples=P.get('spp',44); S.view_settings.exposure=P.get('ev',.45)
S.render.use_persistent_data=True
os.makedirs(P['out'],exist_ok=True)
for job in P['jobs']:
    name=job['name']; out=os.path.join(P['out'],name+'.png')
    if os.path.exists(out): continue
    setenv(job.get('hdri','stuttgart_suburbs'),job.get('rot',300),job.get('env',.45)); led.default_value=job.get('lamp',260)
    if 'frame' in job: setcam(u_of(job['frame']))
    elif 'u' in job: setcam(job['u'])
    else:
        cam.location=job['pos']; bpy.data.objects['tgt'].location=job['tgt']; cam.data.lens=job.get('lens',42); cam.data.dof.focus_distance=job.get('focus',3.5); cam.data.dof.aperture_fstop=job.get('f',2.0)
    if 'res' in job: S.render.resolution_x,S.render.resolution_y=job['res']
    if 'spp' in job: S.cycles.samples=job['spp']
    if 'ev' in job: S.view_settings.exposure=job['ev']
    S.render.filepath=out; bpy.ops.render.render(write_still=True); print('DONE',name,flush=True)
