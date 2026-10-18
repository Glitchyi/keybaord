"""Editable appearance study. All dimensions and mechanisms are provisional."""
from pathlib import Path
import math
import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in list(bpy.data.collections):
    if coll.name != 'Collection':
        bpy.data.collections.remove(coll)
bpy.data.collections['Collection'].name = 'Scene setup'
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene['status'] = 'Appearance concept only; not manufacturing CAD or a verified electronic design'
scene['layout_source'] = 'scripts/build.mjs: 28 original key positions at 19.05 mm pitch'
scene['envelope'] = '128.30 x 109.25 mm confirmed ortholinear visual concept'
scene['lighting'] = 'White legend emission illustrates 28 independently controlled LEDs; side volume preview is illustrative'

collections = {}
for name in ['Enclosure', 'Keycaps — 28', 'Switch placeholders — 28', 'Shine-through legends — 28', 'Rotary control', 'Diffused lighting', 'Hardware details', 'Magnetic rear bar · 4 degrees', 'Alternative rear bar · 7 degrees', 'Flat pads', 'Magnetic seat placeholders', 'Hidden electronics', 'Animation labels']:
    collections[name] = bpy.data.collections.new(name)
    scene.collection.children.link(collections[name])

def put(obj, collection):
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collections.get(collection, bpy.data.collections['Scene setup']).objects.link(obj)
    return obj

def material(name, color, metallic=0, roughness=.4, emission=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=roughness
    if emission:
        bs.inputs['Emission Color'].default_value=(*color,1)
        bs.inputs['Emission Strength'].default_value=emission
    return m

navy=material('Navy blue / opaque keycap shell',(.0025,.007,.022),.08,.25)
body=material('Deep graphite / enclosure',(.021,.026,.034),.25,.3)
deck=material('Mirror black upper panel',(.002,.002,.003),.65,.085)
rubber=material('Black elastomer',(.007,.009,.012),0,.8)
metal=material('Graphite anodised knob',(.055,.066,.08),.8,.24)
steel=material('Black stainless fasteners',(.12,.14,.17),.8,.27)
legend=material('White translucent legend / illumination preview',(.88,.95,1),0,.33,2.4)
frost=material('Frosted white diffuser / lit',(.76,.86,.97),0,.58,1.1)
unlit=material('Frosted diffuser / unlit segment',(.12,.16,.20),0,.7)
backdrop=material('Studio ground',(.045,.053,.068),0,.55)

def box(name, loc, size, mat, bevel=0, coll='Enclosure'):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    obj=bpy.context.object; obj.name=name
    obj.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=obj.modifiers.new('Soft edge radius','BEVEL');mod.width=bevel;mod.segments=5
        mod=obj.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL')
    obj.data.materials.append(mat)
    put(obj,coll)
    return obj

def cylinder(name,loc,radius,depth,mat,coll='Rotary control',vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    obj=bpy.context.object;obj.name=name
    obj.data.materials.append(mat)
    mod=obj.modifiers.new('Edge radii','BEVEL');mod.width=.65;mod.segments=3
    mod=obj.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    for p in obj.data.polygons:p.use_smooth=True
    put(obj,coll)
    return obj

PITCH=19.05
MARGIN=7
W=6*PITCH+2*MARGIN
D=5*PITCH+2*MARGIN
ANGLE=math.radians(4)
PIVOT_Y=-D/2+5
scene['layout_source']='Confirmed 6-column x 5-row ortholinear layout; 28 keys plus knob'
scene['envelope_mm']=[W,D]
scene['status']='Appearance and animation study only; no manufacturing geometry or working firmware'
scene['lighting']='Whole frosted base, underside LED strip placeholders, illustrative visible desk spill'
scene['riser']='Magnetic full-width triangular rear bar; installed 4 degrees; alternatives 7 degrees or flat'

def xy(x,y):return x-W/2,D/2-y

def mesh_object(name,verts,faces,mat,coll):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);collections[coll].objects.link(o);o.data.materials.append(mat)
    mod=o.modifiers.new('Softened edges','BEVEL');mod.width=.5;mod.segments=3
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

# Whole lower shell, hollow at the top and housing conceptual electronics.
frostbase=material('Heavy frost / whole translucent lower shell',(.26,.32,.40),0,.7,.25)
bs=frostbase.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.28;bs.inputs['IOR'].default_value=1.46
# Generated-X mask grows across the shell for host-volume feedback.
nt=frostbase.node_tree
tex=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ')
threshold=nt.nodes.new('ShaderNodeValue');threshold.name='Host volume fraction · illustrative';threshold.outputs[0].default_value=1
compare=nt.nodes.new('ShaderNodeMath');compare.operation='SUBTRACT'
nt.links.new(tex.outputs['Generated'],sep.inputs[0]);nt.links.new(threshold.outputs[0],compare.inputs[0]);nt.links.new(sep.outputs['X'],compare.inputs[1])
# Low emission on unlit region plus brighter diffused glow on lit region.
scale=nt.nodes.new('ShaderNodeMath');scale.operation='MULTIPLY_ADD';scale.inputs[1].default_value=.85;scale.inputs[2].default_value=.15
strength=nt.nodes.new('ShaderNodeValue');strength.name='Ambient / adjustment intensity'
mult=nt.nodes.new('ShaderNodeMath');mult.operation='MULTIPLY'
soft=nt.nodes.new('ShaderNodeMath');soft.operation='MULTIPLY_ADD';soft.inputs[1].default_value=15;soft.inputs[2].default_value=.5;soft.use_clamp=True
nt.links.new(compare.outputs[0],soft.inputs[0]);nt.links.new(soft.outputs[0],scale.inputs[0]);nt.links.new(scale.outputs[0],mult.inputs[0]);nt.links.new(strength.outputs[0],mult.inputs[1]);nt.links.new(mult.outputs[0],bs.inputs['Emission Strength'])
bs.inputs['Emission Color'].default_value=(.8,.88,1,1)
lower=box('Whole heavily frosted lower shell',(0,0,7),(W,D,14),frostbase,4)
bpy.context.view_layer.objects.active=lower
for mod in list(lower.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
cutter=box('Temporary cavity',(0,0,10),(W-5,D-5,15),rubber,2.5)
bpy.context.view_layer.objects.active=cutter
for mod in list(cutter.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.context.view_layer.objects.active=lower
mod=lower.modifiers.new('Open top cavity','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
box('Glossy black upper panel',(0,0,16),(W-1,D-1,4),deck,3.5)

rows=[['Esc','1','2','3','4'],['Tab','Q','W','E','R','T'],['Caps','A','S','D','F','G'],['Shift','Z','X','C','V','B']]
keys=[]
for r,row in enumerate(rows):
    for c,label in enumerate(row):keys.append((label,r,c,1))
keys += [('Ctrl',4,0,1),('Alt',4,1,1),('Space',4,2,2),('Fn',4,4,1),('5',4,5,1)]
for label,r,c,units in keys:
    x=MARGIN+(c+units/2)*PITCH;y=MARGIN+(r+.5)*PITCH
    cx,cy=xy(x,y);width=units*PITCH-2.05
    box('Switch placeholder · '+label,(cx,cy,19.8),(13,13,3.6),rubber,1.4,'Switch placeholders — 28')
    cap=box('Keycap · '+label,(cx,cy,24),(width,17,7),navy,2.1,'Keycaps — 28')
    cap['grid']=[r+1,c+1,units];cap['center_layout_mm']=[x,y];cap['width_mm']=width
    cap['optics']='Visual white legend only; MX stems/inlays absent'
    bpy.ops.object.text_add(location=(cx,cy,27.54));t=bpy.context.object;t.name='Illuminated legend · '+label
    t.data.body='—' if label=='Space' else label;t.data.align_x='CENTER';t.data.align_y='CENTER';t.data.size=3 if len(label)>3 else 3.6;t.data.extrude=.02;t.data.materials.append(legend);put(t,'Shine-through legends — 28')
# Knob occupies row1,column6 at the same pitch as the keys.
kx,ky=xy(MARGIN+5.5*PITCH,MARGIN+.5*PITCH)
cylinder('Encoder visual seat',(kx,ky,19),8.6,2,rubber)
cylinder('Top row rotary knob · magnetic riser separate',(kx,ky,25),8,10,metal)
cylinder('Knob black inset',(kx,ky,30.08),6.8,.45,deck)
box('White knob index',(kx,ky+4.9,30.4),(.8,2.5,.18),legend,.3,'Rotary control')
for i in range(40):
    a=i*2*math.pi/40;cylinder('Knob rib '+str(i),(kx+7.88*math.cos(a),ky+7.88*math.sin(a),25),.18,7,metal,vertices=10)

box('PCB placeholder · underside lights attach here',(0,0,12),(W-10,D-10,1.6),body,2,'Hidden electronics')
for x,y,w,d in [(0,-D/2+12,W-24,5),(-W/2+12,0,5,D-24),(W/2-12,0,5,D-24)]:
    box('Underside PCB LED strip placeholder',(x,y,10.7),(w,d,1),frost,.3,'Hidden electronics')
collections['Hidden electronics'].hide_render=True;collections['Hidden electronics'].hide_viewport=True
# Rear USB placeholder leaves the exact controller and opening unselected.
box('Rear USB-C surround',(W/2-19,D/2-.3,9),(12.5,1.4,5),steel,1.5,'Hardware details')
box('Rear USB-C cavity',(W/2-19,D/2+.5,9),(10.2,.5,3.2),rubber,1.2,'Hardware details')

# Parent the complete keypad, with all keys, before supporting its tilted bottom.
assembly=bpy.data.objects.new('Complete keypad · 4 degree default',None);scene.collection.objects.link(assembly);assembly.location=(0,PIVOT_Y,0)
for name in ['Enclosure','Keycaps — 28','Switch placeholders — 28','Shine-through legends — 28','Rotary control','Hardware details','Hidden electronics']:
    for o in collections[name].objects:o.parent=assembly;o.location.y-=PIVOT_Y
assembly.rotation_euler.x=ANGLE
# Two front rubber pads, low enough to keep the hand-facing diffuser open.
for x in [-W/2+9,W/2-9]:
    cylinder('Front rubber contact pad '+str(x),(x,PIVOT_Y+2,-1.25),4.7,2.5,rubber,'Hardware details')

def riser_bar(name,degrees,coll):
    a=math.radians(degrees);xf=W/2-5;front=D/2-22;rear=D/2-5
    top=lambda y:math.tan(a)*(y-PIVOT_Y)
    # True triangular Y/Z section: long top seat and rear desk-contact edge.
    verts=[(-xf,front,top(front)),(-xf,rear,top(rear)),(-xf,rear,-1.3),(xf,front,top(front)),(xf,rear,top(rear)),(xf,rear,-1.3)]
    bar=mesh_object(name,verts,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],body,coll)
    bar['angle_degrees']=degrees;bar['attachment']='Paired magnets, no mounting screws; holding force/polarity unverified'
    box('Rear rubber contact strip · '+str(degrees)+' degrees',(0,rear,-1.9),(W-12,3,1.2),rubber,.5,coll)
    for x in [-W/2+22,W/2-22]:
        y=rear-6;z=top(y)
        # Disks and surrounding shallow seats are visual placeholders, not a bore specification.
        seat=cylinder('Bar magnet seat · '+str(degrees)+' degrees '+str(x),(x,y,z-.5),4.3,1.1,rubber,coll)
        mag=cylinder('Bar magnet placeholder · '+str(degrees)+' degrees '+str(x),(x,y,z+.08),3.2,.7,steel,coll)
        seat.rotation_euler.x=a;mag.rotation_euler.x=a
    return bar
riser_bar('Full-width triangular magnetic rear bar · 4 degrees',4,'Magnetic rear bar · 4 degrees')
riser_bar('Alternative triangular magnetic rear bar · 7 degrees',7,'Alternative rear bar · 7 degrees')
collections['Alternative rear bar · 7 degrees'].hide_render=True;collections['Alternative rear bar · 7 degrees'].hide_viewport=True
for x in [-W/2+22,W/2-22]:
    y=D/2-11
    for name,rad,z,mat in [('Shell magnet recess placeholder',4.4,.2,rubber),('Shell magnet placeholder',3.2,-.2,steel)]:
        o=cylinder(name+' '+str(x),(x,y,z),rad,.75,mat,'Magnetic seat placeholders');o.parent=assembly;o.location.y-=PIVOT_Y
        o['warning']='Magnet polarity, material thickness and retention force must be engineered'
for x in [-W/2+9,W/2-9]:
    for y in [-D/2+7,D/2-7]:cylinder('Flat-only rubber pad '+str((x,y)),(x,y,-1.25),4.7,2.5,rubber,'Flat pads')
collections['Flat pads'].hide_render=True;collections['Flat pads'].hide_viewport=True

floor=box('Studio receiving desk',(0,0,-4),(2000,2000,3),backdrop,0,'Scene setup')
world=bpy.data.worlds.new('Calm navy studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.08,.1,.15,1);world.node_tree.nodes['Background'].inputs[1].default_value=.22;scene.world=world

def area(name,loc,power,size,color,target):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
area('Large softbox',(-100,-100,260),520000,220,(.86,.91,1),(0,0,10))
area('Soft edge reflection',(130,140,210),650000,180,(.65,.76,1),(0,0,10))
area('Front fill',(30,-220,100),100000,180,(1,.94,.85),(0,0,10))
# An outside-front soft source stands in for light emerging from the diffuser.
# This intentionally illustrates the desired desk spill; it is not optical validation.
spill=area('Illustrative diffuser spill onto hand-facing desk',(0,-D/2-2,2.2),6000,90,(.9,.95,1),(0,-D/2-26,-2.5));spill.data.shape='RECTANGLE';spill.data.size=100;spill.data.size_y=7
put(spill,'Diffused lighting')
scene.frame_start=1;scene.frame_end=72;scene.render.fps=12
for f,intensity,power,level in [(1,.22,4500,1.1),(12,.22,4500,1.1),(20,.7,15000,1.1),(30,.7,15000,1.1),(31,.7,15000,.18),(40,.7,15000,.45),(50,.7,15000,.72),(54,.7,15000,.72),(62,.22,4500,1.1),(72,.22,4500,1.1)]:
    strength.outputs[0].default_value=intensity;strength.outputs[0].keyframe_insert('default_value',frame=f)
    threshold.outputs[0].default_value=level;threshold.outputs[0].keyframe_insert('default_value',frame=f)
    spill.data.energy=power;spill.data.keyframe_insert('energy',frame=f)
for f,value in [(1,.5),(12,.5),(20,5.5),(30,5.5),(31,2.4),(54,2.4),(62,.5),(72,.5)]:
    legend.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=value
    legend.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].keyframe_insert('default_value',frame=f)
for f,name in [(1,'Ambient white'),(13,'Brightness adjustment'),(31,'Host volume feedback · illustrative'),(55,'Return to ambient')]:scene.timeline_markers.new(name,frame=f)

bpy.ops.object.camera_add(location=(230,-275,190));cam=bpy.context.object;cam.name='Beauty camera'
cam.rotation_euler=(Vector((0,0,13))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=222;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG'
scene.frame_set(1)
scene.render.filepath=str(OUT/'navy-lighting-v4.png')
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.shading.color_type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT');bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'navy-lighting-v4.blend'))
bpy.ops.render.render(write_still=True)
# Exploded underside view separates the magnetic bar from its paired shell seats.
for o in collections['Magnetic rear bar · 4 degrees'].objects:o.location.z-=23
floor.hide_render=True;spill.hide_render=True
cam.location=(200,210,-150);cam.rotation_euler=(Vector((0,5,-2))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=222
scene.render.filepath=str(OUT/'navy-lighting-v4-underside.png');bpy.ops.render.render(write_still=True)
# Restore the assembled camera and save native animation with readable phase labels.
for o in collections['Magnetic rear bar · 4 degrees'].objects:o.location.z+=23
floor.hide_render=False;spill.hide_render=False
cam.location=(230,-275,190);cam.rotation_euler=(Vector((0,0,13))-cam.location).to_track_quat('-Z','Y').to_euler()
for text,intervals in [('AMBIENT WHITE',[(1,12),(55,72)]),('BRIGHTNESS ADJUSTMENT',[(13,30)]),('HOST VOLUME FEEDBACK / ILLUSTRATIVE',[(31,54)])]:
    bpy.ops.object.text_add();t=bpy.context.object;t.name='Phase label · '+text;t.parent=cam;t.location=(0,-75,-180);t.rotation_euler=(0,0,0);t.data.body=text;t.data.align_x='CENTER';t.data.size=3.3;t.data.materials.append(legend);put(t,'Animation labels')
    for f in range(1,73):t.hide_render=not any(a<=f<=b for a,b in intervals);t.keyframe_insert('hide_render',frame=f)
scene.render.resolution_x=960;scene.render.resolution_y=720;scene.cycles.samples=12
scene.frame_set(1);scene.render.filepath=str(OUT/'frames'/'frame_')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'navy-lighting-v4.blend'))
(OUT/'frames').mkdir(exist_ok=True)
bpy.ops.render.render(animation=True)
print('CONCEPT_V4_COMPLETE',len(keys),'keys',W,D)
