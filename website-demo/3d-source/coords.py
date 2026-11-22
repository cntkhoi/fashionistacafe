import bpy, sys, json, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
sys.argv=['x','--','{"out":"/tmp/fc3d/none","jobs":[]}']
exec(open('/tmp/fc3d/seq.py').read())
S.render.resolution_x,S.render.resolution_y=1280,960
def proj(u,pts):
    setcam(u); bpy.context.view_layer.update(); r=[]
    for p in pts:
        c=world_to_camera_view(S,cam,Vector(p)); r.append([round(c.x,4),round(1-c.y,4)])
    return r
ob=bpy.data.objects
def top(n,dz=0):
    o=ob[n]; bb=[o.matrix_world@Vector(c) for c in o.bound_box]; return (sum(b.x for b in bb)/8,sum(b.y for b in bb)/8,max(b.z for b in bb)+dz)
spots=proj(3,[top('A_knife_main'),top('A_glass_water',-.03),top('A_napkin')])
lamp=proj(0,[top('lamp_shade',-.02)])[0]
json.dump({"n":48,"spots":spots,"lamp":lamp,"mcrop":[280,720,1280]},open('/tmp/fc3d/cfg.json','w')); print(open('/tmp/fc3d/cfg.json').read())
