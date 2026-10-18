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
scene['envelope'] = '174 x 118 mm concept; wider than original 148 x 118 mm to reserve knob clearance'
scene['lighting'] = 'White legend emission illustrates 28 independently controlled LEDs; side volume preview is illustrative'

collections = {}
for name in ['Enclosure', 'Keycaps — 28', 'Switch placeholders — 28', 'Shine-through legends — 28', 'Rotary control', 'Diffused lighting', 'Hardware details']:
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

navy=material('Navy blue / opaque keycap shell',(.014,.032,.075),.08,.28)
body=material('Deep graphite / enclosure',(.021,.026,.034),.25,.3)
deck=material('Satin slate / switch deck',(.04,.05,.065),.35,.32)
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

def xy(x,y):return x-87,59-y

box('Lower shell · 174 × 118 mm concept', (0,0,7),(174,118,14),body,6)
box('Deck · separate editable appearance solid', (0,0,16),(172,116,4),deck,5)
# Front frosted band wraps the visible edge; no LED packages or optical internals are specified.
box('Front continuous frosted lens', (0,-58.9,9.5),(158,1.4,2.8),frost,.65,'Diffused lighting')
box('Left frosted return',(-86.8,-21,9.5),(1.4,58,2.8),frost,.65,'Diffused lighting')
# A single smooth exterior lens uses a soft material transition for volume.
volume_mat=material('Continuous diffuser / illustrative volume mask',(.76,.86,.97),0,.58,1.1)
nt=volume_mat.node_tree
tex=nt.nodes.new('ShaderNodeTexCoord')
sep=nt.nodes.new('ShaderNodeSeparateXYZ')
ramp=nt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position=.64
ramp.color_ramp.elements[0].color=(.76,.86,.97,1)
ramp.color_ramp.elements[1].position=.69
ramp.color_ramp.elements[1].color=(.065,.09,.12,1)
nt.links.new(tex.outputs['Generated'],sep.inputs[0])
nt.links.new(sep.outputs['Y'],ramp.inputs[0])
bs=nt.nodes.get('Principled BSDF')
nt.links.new(ramp.outputs['Color'],bs.inputs['Base Color'])
nt.links.new(ramp.outputs['Color'],bs.inputs['Emission Color'])
lens=box('Right continuous frosted lens',(86.8,0,9.5),(1.4,100,3),volume_mat,.65,'Diffused lighting')
lens['preview_only']='Approximately two thirds lit; host-volume helper synchronisation not implemented'

rows=[['Esc','1','2','3','4','5'],['Tab','Q','W','E','R','T'],['Caps','A','S','D','F','G'],['Shift','Z','X','C','V','B']]
offsets=[0,4.76,7.14,11.9]
keys=[(label,8+offsets[r]+c*19.05,9+r*19.05,17,17) for r,row in enumerate(rows) for c,label in enumerate(row)]
keys += [('Ctrl',8,86,21,17),('Alt',32,86,17,17),('Space',57,86,36.05,17),('Fn',101,86,17,17)]
for label,x,y,w,d in keys:
    cx,cy=xy(x+w/2,y+d/2)
    box('Switch placeholder · '+label,(cx,cy,19.8),(w-4,d-4,3.6),rubber,1.5,'Switch placeholders — 28')
    cap=box('Keycap · '+label,(cx,cy,24),(w,d,7),navy,2.1,'Keycaps — 28')
    cap['layout_mm']=[x,y,w,d]
    cap['optics']='Opaque navy cap with white translucent legend concept; no stem or printable cutouts yet'
    bpy.ops.object.text_add(location=(cx,cy,27.54))
    text=bpy.context.object;text.name='Illuminated legend · '+label
    text.data.body='—' if label=='Space' else label
    text.data.align_x='CENTER';text.data.align_y='CENTER'
    text.data.size=3.0 if len(label)>3 else 3.6
    text.data.extrude=.025;text.data.bevel_depth=.01
    text.data.materials.append(legend)
    put(text,'Shine-through legends — 28')

kx,ky=xy(155,29)
cylinder('Rotary encoder clearance placeholder',(kx,ky,19),12.1,2,rubber)
cylinder('Volume knob · assignable push action',(kx,ky,26),10.6,12,metal)
cylinder('Knob top inset',(kx,ky,32.08),9.2,.45,body)
box('White knob index',(kx,ky+6.6,32.4),(1,3.1,.18),legend,.4,'Rotary control')
for i in range(48):
    a=i*2*math.pi/48
    cylinder(f'Knurl rib {i+1:02d}',(kx+10.45*math.cos(a),ky+10.45*math.sin(a),26),.25,9,metal,vertices=12)
# Recessed USB socket approximation at rear; geometry is a placeholder.
ux,uy=xy(153,2)
box('USB-C surround placeholder',(ux,58.3,8),(12.5,1.5,5),steel,1.8,'Hardware details')
box('USB-C dark opening',(ux,59.15,8),(10.2,.6,3.2),rubber,1.3,'Hardware details')
box('USB-C tongue',(ux,59.5,8),(6.8,.3,.65),deck,.25,'Hardware details')
for i,(x,y) in enumerate([(5,5),(169,5),(5,113),(169,113)]):
    sx,sy=xy(x,y)
    cylinder('Deck screw '+str(i+1),(sx,sy,18.18),1.25,.5,steel,'Hardware details',32)
    box('Screw slot '+str(i+1),(sx,sy,18.47),(1.35,.3,.08),rubber,.08,'Hardware details')
    box('Rubber foot '+str(i+1),(sx,sy,-1.2),(10,10,2.4),rubber,2.7,'Hardware details')
# Restrained recessed labels in the control gutter.
def label_text(name,body_text,loc,size,mat):
    bpy.ops.object.text_add(location=loc)
    o=bpy.context.object;o.name=name;o.data.body=body_text;o.data.size=size
    o.data.align_x='CENTER';o.data.align_y='CENTER';o.data.extrude=.005;o.data.materials.append(mat)
    put(o,'Hardware details')
label_text('Volume control label','VOL',(kx,ky-17,18.06),2,steel)
label_text('Revision mark','28 / 01',(kx,-41,18.06),1.8,steel)
box('Studio floor',(0,0,-4),(2000,2000,3),backdrop,0,'Scene setup')

world=bpy.data.worlds.new('Soft slate studio')
world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.10,.13,.19,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.35
scene.world=world

def area(name,loc,power,size,color):
    bpy.ops.object.light_add(type='AREA',location=loc)
    o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color
    o.rotation_euler=(Vector((0,0,10))-o.location).to_track_quat('-Z','Y').to_euler()
area('Large neutral softbox',(-100,-100,260),800000,220,(.86,.91,1))
area('Soft rim',(130,140,210),1000000,180,(.65,.76,1))
area('Front fill',(30,-220,100),240000,180,(1,.94,.85))

bpy.ops.object.camera_add(location=(245,-300,310))
cam=bpy.context.object;cam.name='Studio camera · three quarter'
cam.rotation_euler=(Vector((0,0,12))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=272;scene.camera=cam
scene.render.engine='CYCLES'
scene.cycles.samples=48
scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(OUT/'navy-lighting-v1.png')
# Leave the native file in the intended camera view with material colors visible.
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':
            ar.spaces.active.region_3d.view_perspective='CAMERA'
            ar.spaces.active.shading.color_type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'navy-lighting-v1.blend'))
bpy.ops.render.render(write_still=True)
print('CONCEPT_COMPLETE',len(keys),'keys',str(OUT))

# Alternative steady ambient mode, with the same continuous frosted side lens.
collections['Diffused lighting'].objects['Right continuous frosted lens'].data.materials[0]=frost
scene.render.filepath=str(OUT/'navy-lighting-v1-ambient.png')
bpy.ops.render.render(write_still=True)
