"""Render saved native assembly without changing its source geometry."""
import bpy, json, sys, subprocess, hashlib, struct, shutil
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parent
scene=bpy.context.scene
# Stills choose their own cameras; the animation bindings are restored after them.
for marker in scene.timeline_markers:marker.camera=None
media_path=OUT/'media-manifest.json'
if '--preview' not in sys.argv and media_path.exists():media_path.unlink()
PREVIEW='--preview' in sys.argv
scene.render.engine='CYCLES' if '--cycles' in sys.argv else 'CYCLES'
scene.cycles.samples=4 if PREVIEW else 12
scene.cycles.use_denoising=True
scene.render.resolution_x=960 if PREVIEW else 1600;scene.render.resolution_y=720 if PREVIEW else 1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
# Add an illustrative source-free volume mask, preserving white key-light color.
frost=bpy.data.materials['Frosted full lower enclosure'];nt=frost.node_tree;bs=nt.nodes.get('Principled BSDF')
tex=nt.nodes.new('ShaderNodeTexCoord');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(tex.outputs['Generated'],sep.inputs[0])
level=nt.nodes.new('ShaderNodeValue');level.name='Illustrative volume fraction'
sub=nt.nodes.new('ShaderNodeMath');sub.operation='SUBTRACT';nt.links.new(level.outputs[0],sub.inputs[0]);nt.links.new(sep.outputs['X'],sub.inputs[1])
soft=nt.nodes.new('ShaderNodeMath');soft.operation='MULTIPLY_ADD';soft.inputs[1].default_value=15;soft.inputs[2].default_value=.5;soft.use_clamp=True;nt.links.new(sub.outputs[0],soft.inputs[0])
scale=nt.nodes.new('ShaderNodeMath');scale.operation='MULTIPLY_ADD';scale.inputs[1].default_value=.8;scale.inputs[2].default_value=.2;nt.links.new(soft.outputs[0],scale.inputs[0])
intensity=nt.nodes.new('ShaderNodeValue');intensity.name='Illustrative base intensity';mult=nt.nodes.new('ShaderNodeMath');mult.operation='MULTIPLY';nt.links.new(scale.outputs[0],mult.inputs[0]);nt.links.new(intensity.outputs[0],mult.inputs[1]);nt.links.new(mult.outputs[0],bs.inputs['Emission Strength'])
for f,v in [(1,1),(385,1),(480,1),(481,.15),(504,.45),(528,.8),(552,1),(576,1)]:level.outputs[0].default_value=v;level.outputs[0].keyframe_insert('default_value',frame=f)
for f,v in [(1,.06),(385,.06),(432,.06),(456,.5),(480,.5),(504,.55),(528,.5),(552,.06),(576,.06)]:intensity.outputs[0].default_value=v;intensity.outputs[0].keyframe_insert('default_value',frame=f)
base=bpy.data.materials['RGB strip diffused light'].node_tree.nodes.get('Principled BSDF')
for f,color in [(1,(.85,.94,1,1)),(480,(.85,.94,1,1)),(504,(.15,.65,1,1)),(528,(.3,.15,1,1)),(552,(.85,.94,1,1)),(576,(.85,.94,1,1))]:
    base.inputs['Emission Color'].default_value=color;base.inputs['Emission Color'].keyframe_insert('default_value',frame=f)
for o in scene.objects:
    if o.name.startswith('RGB pixel'):o.data.materials.clear();o.data.materials.append(bpy.data.materials['RGB strip diffused light'])
scene.frame_set(1);scene.camera=bpy.data.objects['CAM assembled and glow']
scene.render.filepath=str(OUT/('preview.png' if PREVIEW else 'assembled.png'))
bpy.ops.render.render(write_still=True)
if PREVIEW:quit()
# An exploded underside without a floor exposes actual source CAD and captive interfaces.
floor=bpy.data.objects['Desk'];floor.hide_render=True
scene.camera=bpy.data.objects['CAM underside'];scene.frame_set(120)
sys.path.insert(0,str(OUT));from camera_framing import fit_still_camera
fit_still_camera(scene,scene.camera,120)
scene.render.filepath=str(OUT/'underside.png');bpy.ops.render.render(write_still=True)
scene.frame_set(1);floor.hide_render=False
# Cross section of custom geometry; purchased internals are exterior reference envelopes.
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,-100,20));cutter=bpy.context.object;cutter.name='Temporary display section';cutter.dimensions=(400,200,200);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);cutter.hide_render=True
mods=[];hidden=[]
wire=bpy.data.objects.get('stabilizer approximate equalizing wire')
if wire:wire.hide_render=True;hidden.append(wire)
assembly=bpy.data.objects['Assembly | common frozen datum'];bpy.context.view_layer.update()
for o in list(scene.objects):
    if o.type=='MESH' and o.get('partId') in ['switch','stabilizer','key_led','diode','fastener','fastener_nut','rubber_foot','rgb_strip'] and (assembly.matrix_world.inverted()@o.matrix_world.translation).y<0:
        o.hide_render=True;hidden.append(o)
for o in list(scene.objects):
    if o.type=='MESH' and o.get('partId') in ['case','plate','pcb','keycap_1u','keycap_2u','legend']:
        md=o.modifiers.new('Display-only section','BOOLEAN');md.operation='DIFFERENCE';md.solver='EXACT';md.object=cutter;mods.append((o,md))
scene.camera=bpy.data.objects['CAM section'];scene.render.filepath=str(OUT/'section.png');bpy.ops.render.render(write_still=True)
for o,m in mods:o.modifiers.remove(m)
for o in hidden:o.hide_render=False
bpy.data.objects.remove(cutter,do_unlink=True)
scene.camera=bpy.data.objects['CAM assembled and glow'];scene.frame_set(1)
# Rear still explicitly displays sourced mouth and .05 mm nominal recess.
assembly=bpy.data.objects['Assembly | common frozen datum'];spec=json.loads((OUT.parent.parent/'spec/resolved.json').read_text());mc=assembly.matrix_world@Vector(spec['custom']['components']['usb_adapter']['mouthCenter'])
bpy.ops.object.camera_add(location=mc+Vector((30,60,17)));rear=bpy.context.object;rear.name='CAM rear USB';rear.rotation_euler=(mc-rear.location).to_track_quat('-Z','Y').to_euler();rear.data.type='ORTHO';rear.data.ortho_scale=60
scene.camera=rear;scene.render.filepath=str(OUT/'rear-usb.png');bpy.ops.render.render(write_still=True)
# Fit all animation frames and bind the native timeline to the actual clip cameras.
sys.path.insert(0,str(OUT))
from camera_framing import prepare_cameras
prepare_cameras(scene,OUT)
# Save native with named clip cameras before rendering clips.
scene.camera=bpy.data.objects['CAM assembled and glow'];scene.frame_set(1)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'keypad-fit-v1.blend'))
if '--stills-only' in sys.argv:quit()
scene.render.resolution_x=960;scene.render.resolution_y=720
scene.render.engine='BLENDER_EEVEE'
scene.eevee.taa_render_samples=16
for start,end,name,cam in [(1,288,'assembly','CAM assembly full frame'),(289,384,'switch-motion','CAM switch full frame'),(385,576,'glow','CAM assembled and glow')]:
    folder=OUT/'frames'/name;folder.mkdir(parents=True,exist_ok=True);scene.camera=bpy.data.objects[cam];scene.frame_start=start;scene.frame_end=end
    scene.render.filepath=str(folder/'frame_');bpy.ops.render.render(animation=True)
    subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-framerate','24','-start_number',str(start),'-i',str(folder/'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-movflags','+faststart',str(OUT/(name+'.mp4'))],check=True)
scene.frame_start=1;scene.frame_end=576;scene.frame_set(1);scene.camera=bpy.data.objects['CAM assembled and glow']

current=json.loads((OUT.parent.parent/'spec/resolved.json').read_text())
assert scene['sourceSpecHash']==current['sourceSpecHash'],'Source changed while rendering'
files=['assembled.png','underside.png','section.png','rear-usb.png','assembly.mp4','switch-motion.mp4','glow.mp4','keypad-fit-v1.blend']
media={'sourceSpecHash':scene['sourceSpecHash'],'geometryHash':scene['geometryHash'],'builtMeshHash':json.loads((OUT/'model-report.json').read_text())['builtMeshHash'],'complete':True,'files':[{'name':name,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest(),'bytes':(OUT/name).stat().st_size} for name in files]}
for item in media['files']:
    path=OUT/item['name']
    if path.suffix=='.png':
        item['width'],item['height']=struct.unpack('>II',path.read_bytes()[16:24])
    if path.suffix=='.mp4':
        probe=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_frames','-show_entries','format=duration','-of','json',str(path)]))
        st=probe['streams'][0];item.update(st);item['duration']=float(probe['format']['duration']);assert st['codec_name']=='h264' and st['r_frame_rate']=='24/1' and st['width']==960 and st['height']==720
assert sum(i.get('duration',0) for i in media['files'])==24
media['outputSHA256']={i['name']:i['sha256'] for i in media['files'] if i['name'].endswith(('.png','.mp4'))}
media['files']={i['name']:{k:v for k,v in i.items() if k!='name'} for i in media['files']}
media_path.write_text(json.dumps(media,indent=2)+'\n')
# Disposable outputs belong only to this generator. Keep compact checked reports and deliverables.
if (OUT/'frames').exists():shutil.rmtree(OUT/'frames')
for path in OUT.glob('*.blend1'):path.unlink()

print('MEDIA_COMPLETE',json.dumps({'sourceSpecHash':scene['sourceSpecHash'],'files':len(files)}))
