"""Independent checks of the saved native scene, including swept nominal cap shells.
Run: Blender --background keypad-fit-v1.blend --python verify_scene.py
"""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).resolve().parent;S=json.loads((OUT.parent.parent/'spec/resolved.json').read_text());sc=bpy.context.scene
assert sc['sourceSpecHash']==S['sourceSpecHash'];assert sc['geometryHash']==S['geometryHash']
sc.frame_set(1);bpy.context.view_layer.update()
assembly=bpy.data.objects['Assembly | common frozen datum'];board=bpy.data.objects['Soldered PCB + plate + switches | never desoldered']
checks=[]
def add(name,ok,detail):checks.append({'id':name,'status':'PASS' if ok else 'FAIL','details':detail})
def bv(o,shift=Vector((0,0,0))):
    mw=assembly.matrix_world.inverted()@o.matrix_world
    vertices=[mw@v.co+shift for v in o.data.vertices]
    return BVHTree.FromPolygons(vertices,[list(p.vertices) for p in o.data.polygons],all_triangles=False,epsilon=1e-6)
add('native_28_caps',len([o for o in sc.objects if o.name.startswith('cap.')])==28,28)
add('native_28_nonempty_inlays',len([o for o in sc.objects if o.name.startswith('insert.') and len(o.data.polygons)>0])==28,28)
legend_top=[]
for key in S['layout']['keys']:
    obj=bpy.data.objects['insert.'+key['id']];cap=bpy.data.objects['cap.'+key['id']];capb=bv(cap);mm=assembly.matrix_world.inverted()@obj.matrix_world;area=0;faces=0
    for face in obj.data.polygons:
        if face.normal.z>.5 and obj.data.materials[face.material_index].name=='White translucent inlays':
            pos=mm@face.center;hit=capb.ray_cast(pos+Vector((0,0,1)),Vector((0,0,-1)))
            if hit[0] is None or hit[0].z<=pos.z+.003:area+=face.area;faces+=1
    legend_top.append({'key':key['id'],'visibleUpwardWhiteArea':area,'roofFaces':faces})
add('visible_emissive_roof_for_all_28_legends',all(i['visibleUpwardWhiteArea']>.02 and i['roofFaces']>0 for i in legend_top),legend_top)

add('source_controller_solids',len([o for o in sc.objects if o.name.startswith('controller.CADsolid.')])==58,58)
add('source_adapter_solids',len([o for o in sc.objects if o.name.startswith('usb_adapter.CADsolid.')])==34,34)
# Actual cap shell mesh against exterior envelope, every key, sampled full swept range.
collisions=[];samples=[i*3.9/13 for i in range(14)]
for k in S['layout']['keys']:
    cap=bpy.data.objects['cap.'+k['id']];housing=bpy.data.objects['switch.upper.'+k['id']];hb=bv(housing)
    for travel in samples:
        if bv(cap,Vector((0,0,-travel))).overlap(hb):collisions.append({'key':k['id'],'travel':travel})
add('actual_cap_shell_sweep_all_28',not collisions,{'travelSamples':samples,'collisions':collisions,'excludes':'provisional stem bosses and purchased BOX internals'})
# Caps and stems return to the same pose; source soldered solids remain on the board group.
add('stems_remain_on_board_during_cap_removal',all(bpy.data.objects['Stem motion '+k['id']].parent==board for k in S['layout']['keys']),True)
sc.frame_set(48);add('screws_released_before_soldered_assembly_lift',abs(bpy.data.objects['Removable case screws'].location.z-50)<1e-5 and abs(board.location.z)<1e-5,{'screwLift':bpy.data.objects['Removable case screws'].location.z,'boardLift':board.location.z})
sc.frame_set(120);bpy.context.view_layer.update()
add('ordinary_explosion_separates_cap_not_switch_stem',bpy.data.objects['Removable caps and inserts'].location.z>board.location.z and all(abs(bpy.data.objects['Stem motion '+k['id']].location.z)<1e-6 for k in S['layout']['keys']),{'capLift':bpy.data.objects['Removable caps and inserts'].location.z,'solderedLift':board.location.z})
sc.frame_set(324);add('A_full_nominal_travel',abs(bpy.data.objects['Cap motion a'].location.z+3.6)<1e-5 and abs(bpy.data.objects['Stem motion a'].location.z+3.6)<1e-5,{'cap':bpy.data.objects['Cap motion a'].location.z,'stem':bpy.data.objects['Stem motion a'].location.z})
sc.frame_set(360);add('Space_full_nominal_travel',abs(bpy.data.objects['Cap motion space'].location.z+3.6)<1e-5 and abs(bpy.data.objects['Stem motion space'].location.z+3.6)<1e-5,{'cap':bpy.data.objects['Cap motion space'].location.z})
sc.frame_set(1);bpy.context.view_layer.update()
# Static integration envelope checks use actual triangles of the full source CAD.
fpc=bpy.data.objects['FPC | provisional ribbon envelope'];fb=bv(fpc);hits=[]
for o in sc.objects:
    if o.name.startswith('controller.CADsolid.') and fb.overlap(bv(o)):hits.append(o.name)
add('FPC_envelope_controller_clearance',not hits,{'triangleIntersections':hits,'contactEngagement':'UNKNOWN'})
# Actual mesh rays establish the blind pocket wall, independently of parameter arithmetic.
usb=S['custom']['components']['usb_adapter'];rear=S['custom']['case']['depth']/2;lb=bv(bpy.data.objects['case.lower']);origin=Vector((usb['centerX']+7.5,rear+1,-13.6));direction=Vector((0,-1,0))
hit1=lb.ray_cast(origin,direction);hit2=lb.ray_cast(hit1[0]+direction*.0001,direction) if hit1[0] else (None,None,None,None)
thickness=hit1[0].y-hit2[0].y if hit1[0] and hit2[0] else -1
add('actual_USB_blind_pocket_wall',thickness>=usb['minimumOuterWallSkin'],{'measuredRayThickness':thickness,'minimum':usb['minimumOuterWallSkin']})
cradle=bpy.data.objects['USB cradle'];cv=[assembly.matrix_world.inverted()@cradle.matrix_world@v.co for v in cradle.data.vertices]
add('actual_USB_cradle_within_case',max(v.y for v in cv)<=rear-S['custom']['case']['wall']+.0001,{'maximumY':max(v.y for v in cv),'caseInteriorRearY':rear-S['custom']['case']['wall']})
fv=[assembly.matrix_world.inverted()@fpc.matrix_world@v.co for v in fpc.data.vertices]
add('actual_FPC_floor_clearance',min(v.z for v in fv)-(-20.5)>=.3,{'mm':min(v.z for v in fv)+20.5})
add('actual_FPC_route_length',fpc['routeLength']<=S['custom']['components']['fpc_cable']['maximumRouteLength'],{'meshCentrelineLength':fpc['routeLength'],'limit':S['custom']['components']['fpc_cable']['maximumRouteLength']})
# Source controller floor and carrier clearance from actual CAD vertices.
verts=[assembly.matrix_world.inverted()@o.matrix_world@v.co for o in sc.objects if o.name.startswith('controller.CADsolid.') for v in o.data.vertices]
add('actual_controller_floor_gap',min(v.z for v in verts)-(-20.5)>=.3,{'mm':min(v.z for v in verts)+20.5})
# Rear plug envelope is a selected modelling reference only.
plug=S['custom']['fpcCablePlugEnvelope'];mc=S['custom']['components']['usb_adapter']['mouthCenter'];ground=[]
for a,p in S['poses'].items():
    aa=p['rotationX'];z=p['translation'][2]+mc[1]*math.sin(aa)+(mc[2]-plug['height']/2)*math.cos(aa)
    ground.append({'angle':a,'minimumConservativeGroundGap':z})
add('reference_USB_plug_ground_clearance_0_4_7',all(p['minimumConservativeGroundGap']>=.3 for p in ground),ground)
# Evaluate each alternative visibly in its actual source pose, avoiding stale hidden matrices.
sc.frame_set(1);oldaction=assembly.animation_data.action;assembly.animation_data.action=None
oldvis={name:bpy.data.collections[name].hide_viewport for name in ['Riser 4','Riser 7']}
for angle,pose in S['poses'].items():
    a=int(angle);assembly.location=pose['translation'];assembly.rotation_euler=(pose['rotationX'],0,0)
    for n in [4,7]:bpy.data.collections['Riser '+str(n)].hide_viewport=n!=a
    bpy.context.view_layer.update();contacts=[]
    for o in sc.objects:
        use=o.name.startswith('case foot') and (a==0 or o.location.y<0)
        use=use or (a!=0 and o.name.startswith('riser foot ('+angle+','))
        if use:contacts.append({'id':o.name,'minimumZ':min((o.matrix_world@v.co).z for v in o.data.vertices)})
    add('actual_nominal_foot_contacts_'+angle,all(-.001<=v['minimumZ']<=.03 for v in contacts),contacts)
assembly.animation_data.action=oldaction
for name,value in oldvis.items():bpy.data.collections[name].hide_viewport=value
assembly.rotation_euler=(S['poses']['4']['rotationX'],0,0);sc.frame_set(1)
report={'sourceSpecHash':S['sourceSpecHash'],'geometryHash':S['geometryHash'],'physicalFitValidated':False,'checks':checks,'failures':[c['id'] for c in checks if c['status']=='FAIL']}
(OUT/'native-verification.json').write_text(json.dumps(report,indent=2)+'\n')
base=json.loads((OUT/'model-report.json').read_text());base['nativeChecks']=checks;base['failures']=[c['id'] for c in base['checks'] if c['status']=='FAIL']+report['failures'];(OUT/'model-report.json').write_text(json.dumps(base,indent=2)+'\n')
print('NATIVE_VERIFY',json.dumps(report));assert not report['failures'],report['failures']
