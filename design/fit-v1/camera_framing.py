"""Fit complete visible assemblies over every animation frame, without geometry edits."""
import bpy,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

def prepare_cameras(scene,out):
    results=[]
    for start,end,template,name in [(1,288,'CAM assembled and glow','CAM assembly full frame'),(289,384,'CAM switch travel','CAM switch full frame')]:
        cam=bpy.data.objects.get(name)
        if not cam:
            src=bpy.data.objects[template];cam=src.copy();cam.data=src.data.copy();scene.collection.objects.link(cam);cam.name=name
        # Reset to the fixed template, making this operation reproducible.
        cam.matrix_world=bpy.data.objects[template].matrix_world.copy()
        inv=cam.matrix_world.inverted();coords=[]
        for frame in range(start,end+1):
            scene.frame_set(frame);bpy.context.view_layer.update()
            for obj in scene.objects:
                if obj.type=='MESH' and obj.visible_get() and obj.get('partId')!='studio':
                    coords.extend(inv@(obj.matrix_world@Vector(v)) for v in obj.bound_box)
        xmin=min(v.x for v in coords);xmax=max(v.x for v in coords);ymin=min(v.y for v in coords);ymax=max(v.y for v in coords)
        cam.location+=cam.matrix_world.to_quaternion()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0))
        aspect=scene.render.resolution_x/scene.render.resolution_y
        cam.data.ortho_scale=max(xmax-xmin,(ymax-ymin)*aspect)*1.12
        scene.camera=cam;limits=[1,1,0,0];violations=[]
        for frame in range(start,end+1):
            scene.frame_set(frame);scene.camera=cam;bpy.context.view_layer.update()
            for obj in scene.objects:
                if obj.type=='MESH' and obj.visible_get() and obj.get('partId')!='studio':
                    for corner in obj.bound_box:
                        p=world_to_camera_view(scene,cam,obj.matrix_world@Vector(corner));limits=[min(limits[0],p.x),min(limits[1],p.y),max(limits[2],p.x),max(limits[3],p.y)]
                        if not(0<=p.x<=1 and 0<=p.y<=1):violations.append([frame,obj.name,p.x,p.y])
        assert not violations,violations[:5]
        results.append({'camera':name,'frames':[start,end],'orthoScale':cam.data.ortho_scale,'normalizedImageBounds':limits,'allFramesInside':True})
    for marker in scene.timeline_markers:
        if marker.frame==1:marker.camera=bpy.data.objects['CAM assembly full frame']
        elif marker.frame==289:marker.camera=bpy.data.objects['CAM switch full frame']
        elif marker.frame==385:marker.camera=bpy.data.objects['CAM assembled and glow']
    scene.frame_set(1);scene.camera=bpy.data.objects['CAM assembly full frame']
    (Path(out)/'framing-check.json').write_text(json.dumps({'sourceSpecHash':scene['sourceSpecHash'],'geometryHash':scene['geometryHash'],'checks':results},indent=2)+'\n')
    return results

def fit_still_camera(scene,cam,frame):
    scene.frame_set(frame);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();coords=[]
    for obj in scene.objects:
        if obj.type=='MESH' and obj.visible_get() and obj.get('partId')!='studio':coords.extend(inv@(obj.matrix_world@Vector(v)) for v in obj.bound_box)
    xmin=min(v.x for v in coords);xmax=max(v.x for v in coords);ymin=min(v.y for v in coords);ymax=max(v.y for v in coords)
    cam.location+=cam.matrix_world.to_quaternion()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));aspect=scene.render.resolution_x/scene.render.resolution_y;cam.data.ortho_scale=max(xmax-xmin,(ymax-ymin)*aspect)*1.12
