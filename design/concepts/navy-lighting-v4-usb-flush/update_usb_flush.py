"""Replace only the rear USB visual study in the accepted v4 native scene."""
from pathlib import Path
import bpy, math, json
from mathutils import Vector

OUT=Path(__file__).resolve().parent
BASE=OUT.parent/'navy-lighting-v4'/'navy-lighting-v4.blend'
bpy.ops.wm.open_mainfile(filepath=str(BASE))
scene=bpy.context.scene
scene.frame_set(1)
assembly=bpy.data.objects['Complete keypad · 4 degree default']
W,D=128.3,109.25
PIVOT=-D/2+5
CX=W/2-19
WALL=D/2
Z=9
for name in ['Rear USB-C surround','Rear USB-C cavity']:
    obj=bpy.data.objects.get(name)
    if obj:bpy.data.objects.remove(obj,do_unlink=True)
coll=bpy.data.collections.new('Flush rear USB-C · visual placeholders');scene.collection.children.link(coll)

def put(obj):
    for c in list(obj.users_collection):c.objects.unlink(obj)
    coll.objects.link(obj)
    obj.parent=assembly
    return obj

def box(name,center,size,mat,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(center[0],center[1]-PIVOT,center[2]))
    o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        m=o.modifiers.new('Rounded edges','BEVEL');m.width=bevel;m.segments=8
        o.modifiers.new('Surface normals','WEIGHTED_NORMAL')
    if mat:o.data.materials.append(mat)
    return put(o)

steel=bpy.data.materials['Black stainless fasteners']
black=bpy.data.materials['Black elastomer']
# True wall aperture. Cut entirely through the frosted rear wall, so no cap or
# translucent wall remains behind the visual socket mouth.
cut=box('Temporary rounded wall aperture cutter',(CX,WALL,Z),(12.6,12,5.2),None,1.5)
bpy.context.view_layer.objects.active=cut
for m in list(cut.modifiers):bpy.ops.object.modifier_apply(modifier=m.name)
lower=bpy.data.objects['Whole heavily frosted lower shell']
bpy.context.view_layer.objects.active=lower
mod=lower.modifiers.new('True rear USB-C wall aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cut,do_unlink=True)

def rounded(w,h,r):
    out=[]
    for x,z,angle in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
        for i in range(12):
            a=math.radians(angle+i*90/11)
            out.append((x+r*math.cos(a),z+r*math.sin(a)))
    return out
outer=rounded(12.2,4.8,2.0)
inner=rounded(10.6,3.5,1.45)
verts=[]
for y,outline in [(WALL,outer),(WALL,inner),(WALL-5.8,outer),(WALL-5.8,inner)]:
    verts.extend((CX+x,y-PIVOT,Z+z) for x,z in outline)
n=len(outer);faces=[]
for i in range(n):
    j=(i+1)%n
    faces += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
mesh=bpy.data.meshes.new('Rounded metal receptacle ring');mesh.from_pydata(verts,[],faces);mesh.update()
rim=bpy.data.objects.new('USB-C metal mouth · flush rear exterior plane',mesh);coll.objects.link(rim);rim.parent=assembly;rim.data.materials.append(steel)
rim['exterior_plane_local_y_mm']=WALL
rim['wall_plane_local_y_mm']=WALL
rim['projection_mm']=0.0
rim['note']='Visual receptacle approximation; no selected connector or manufacturing tolerance'
box('Socket dark interior back',(CX,WALL-5.85,Z),(10.6,.18,3.5),black,.08)
box('USB-C internal tongue',(CX,WALL-2.6,Z),(6.8,3.2,.65),black,.25)
# Subtle tongue edge represents contacts without pretending to define a real part.
box('Tongue contact edge',(CX,WALL-1.03,Z-.19),(5.8,.08,.12),steel,.04)

bpy.context.view_layer.update()
# Verify the ring's exterior is flush in keypad-local coordinates.
ys=[v.co.y+PIVOT for v in rim.data.vertices]
assert abs(max(ys)-WALL)<1e-5
assert min(ys)<WALL-5
assert len(bpy.data.collections['Keycaps — 28'].objects)==28
assert len(bpy.data.collections['Shine-through legends — 28'].objects)==28
scene['USB-C concept']='Flush close-fitting metal mouth at rear frosted exterior; true wall aperture; no external housing'
scene['USB-C dimensions']='Approximate visual mouth only; actual receptacle/cable/PCB mounting dimensions unselected'
# Keep the accepted camera and lighting animation active in the native file.
beauty=scene.camera
point=assembly.matrix_world@Vector((CX,WALL-PIVOT,Z))
bpy.ops.object.camera_add(location=point+Vector((25,47,19)))
rear=bpy.context.object;rear.name='Rear USB-C flush close-up camera'
rear.rotation_euler=(point-rear.location).to_track_quat('-Z','Y').to_euler()
rear.data.type='ORTHO';rear.data.ortho_scale=49
scene.camera=beauty
bpy.ops.object.select_all(action='DESELECT')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'navy-lighting-v4-usb-flush.blend'))
# Close-up only. Native accepted animation and all 72 frames are preserved.
scene.camera=rear
bpy.data.collections['Animation labels'].hide_render=True
scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.cycles.samples=48
scene.render.filepath=str(OUT/'rear-usb-flush-closeup.png')
bpy.ops.render.render(write_still=True)
print('USB_FLUSH_VERIFIED',json.dumps({'rear_wall_local_y_mm':WALL,'rim_exterior_local_y_mm':max(ys),'external_projection_mm':max(ys)-WALL,'ring_depth_mm':max(ys)-min(ys),'keys':28,'preserved_frames':[scene.frame_start,scene.frame_end]}))
