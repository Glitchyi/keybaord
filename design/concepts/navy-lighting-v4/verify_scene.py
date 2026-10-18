"""Verify native concept structure and distinct illustrative timeline settings."""
import bpy, math, json
scene=bpy.context.scene
expected=[('Esc',1,1,1),('1',1,2,1),('2',1,3,1),('3',1,4,1),('4',1,5,1)]
for r,labels in [(2,['Tab','Q','W','E','R','T']),(3,['Caps','A','S','D','F','G']),(4,['Shift','Z','X','C','V','B'])]:
    expected.extend((label,r,c,1) for c,label in enumerate(labels,1))
expected += [('Ctrl',5,1,1),('Alt',5,2,1),('Space',5,3,2),('Fn',5,5,1),('5',5,6,1)]
assert len(bpy.data.collections['Keycaps — 28'].objects)==len(expected)==28
assert len(bpy.data.collections['Shine-through legends — 28'].objects)==28
w,d=128.3,109.25;pitch=19.05;pivot=-d/2+5
for label,r,c,units in expected:
    cap=bpy.data.objects['Keycap · '+label]
    assert list(cap['grid'])==[r,c,units],(label,'grid')
    x=7+((c-1)+units/2)*pitch;y=7+(r-.5)*pitch
    assert abs(cap.location.x-(x-w/2))<.001,(label,'x')
    assert abs(cap.location.y-(d/2-y-pivot))<.001,(label,'y')
    assert abs(cap['width_mm']-(units*pitch-2.05))<.001,(label,'width')
knob=bpy.data.objects['Top row rotary knob · magnetic riser separate']
assert abs(knob.location.x-(7+5.5*pitch-w/2))<.001
assert abs(knob.location.y-(d/2-(7+.5*pitch)-pivot))<.001
assert abs(math.degrees(bpy.data.objects['Complete keypad · 4 degree default'].rotation_euler.x)-4)<.001
assert not bpy.data.libraries
assert not [i for i in bpy.data.images if i.source=='FILE' and not i.packed_file]
assert not [o.name for o in scene.objects if 'screw' in o.name.lower()]
frames={}
for f in [1,20,31,50,72]:
    scene.frame_set(f)
    nodes=bpy.data.materials['Heavy frost / whole translucent lower shell'].node_tree.nodes
    frames[f]={'base_intensity':nodes['Ambient / adjustment intensity'].outputs[0].default_value,'volume_fraction':nodes['Host volume fraction · illustrative'].outputs[0].default_value,'legend_intensity':bpy.data.materials['White translucent legend / illumination preview'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value,'desk_spill':bpy.data.objects['Illustrative diffuser spill onto hand-facing desk'].data.energy}
assert frames[20]['legend_intensity']>frames[1]['legend_intensity']
assert frames[20]['desk_spill']>frames[1]['desk_spill']
assert frames[50]['volume_fraction']>frames[31]['volume_fraction']
assert abs(frames[1]['base_intensity']-frames[72]['base_intensity'])<.001
scene.frame_set(1)
print('NATIVE_V4_VERIFIED',json.dumps({'keys':28,'layout_exact':True,'space_width_mm':bpy.data.objects['Keycap · Space']['width_mm'],'envelope_mm':[w,d],'animation':frames}))
