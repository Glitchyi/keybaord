"""Reproducible drawing-based assembly. No manufacturing or physical-fit claim.
Blender --background --python design/fit-v1/build_scene.py -- [--render]
"""
from pathlib import Path
import bpy, math, json, hashlib, sys
from mathutils import Vector, Matrix, Quaternion

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
SPEC=ROOT/'spec'/'resolved.json'
S=json.loads(SPEC.read_text()); C=S['custom']; P=S['parts']; D=S['datums']
sys.path.insert(0,str(OUT))
from cap_geometry import cap_shell_geometry,repair_q
RENDER='--render' in sys.argv
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection': bpy.data.collections.remove(c)
bpy.data.collections['Collection'].name='Studio'
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=.001
scene['sourceSpecHash']=S['sourceSpecHash']; scene['geometryHash']=S['geometryHash']
scene['status']='Drawing-based assembly; physical fit, fabrication and optics unvalidated'
colls={}
for name in ['Case','Soldered assembly','Caps and inserts','Rotary control','Riser 4','Riser 7','Overlay concept','Reference only']:
    co=bpy.data.collections.new(name); scene.collection.children.link(co); colls[name]=co
objects=[]; groups={}; stemgroups={}; instances=[]; assumptions=[]

def empty(name,parent=None,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None); scene.collection.objects.link(o); o.parent=parent; o.location=loc; return o
assembly=empty('Assembly | common frozen datum')
board=empty('Soldered PCB + plate + switches | never desoldered',assembly)
casegroup=empty('Case subassembly',assembly)
caproot=empty('Removable caps and inserts',assembly)
knobroot=empty('Removable push knob',assembly)
risers={a:empty('Magnetic riser '+str(a),assembly) for a in [4,7]}

def mat(name,rgb,rough=.4,metal=0,emit=0,trans=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgb,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*rgb,1); bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    bs.inputs['Emission Color'].default_value=(*rgb,1);bs.inputs['Emission Strength'].default_value=emit
    bs.inputs['Transmission Weight'].default_value=trans
    return m
navy=mat('Deep navy custom shells',S['materials']['keycaps']['rgb'],.25,.04)
black=mat('Mirror black support plate',S['materials']['top']['rgb'],.06,.65)
frost=mat('Frosted full lower enclosure',(.52,.59,.68),.72,0,.04,.35)
white=mat('White translucent inlays',(.9,.95,1),.3,0,1.2,.2)
metal=mat('Brushed metal',(.33,.37,.43),.25,.8)
rubber=mat('Dark rubber contacts',(.012,.016,.022),.8)
pcbmat=mat('Unrouted dark PCB',(.025,.065,.055),.5)
basewhite=mat('RGB strip diffused light',(.85,.94,1),.6,0,3)
clear=mat('Approximate clear switch upper housing',(.55,.66,.7),.3,0,0,.45)
jade=mat('Jade stem',(.10,.36,.25),.35)
copper=mat('Solder and pads',(.5,.36,.12),.3,.7)
flexmat=mat('FPC amber polyimide',(.45,.21,.04),.5)
labelmat=mat('Studio annotation',(.65,.73,.84),.6,0,.2)

def place(o,name,part,parent=assembly,coll='Soldered assembly',status=None):
    o.name=name
    for co in list(o.users_collection):co.objects.unlink(o)
    colls.get(coll,bpy.data.collections['Studio']).objects.link(o)
    o.parent=parent
    o['partId']=part; o['sourceIds']=json.dumps(P.get(part,{}).get('sourceIds',[]));o['dimensionStatus']=status or P.get(part,{}).get('dimensionStatus','custom-nominal')
    objects.append(o);return o

def mesh(name,vs,fs,material,part,parent=assembly,coll='Soldered assembly'):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
    if material:o.data.materials.append(material)
    return place(o,name,part,parent,coll)

def box(name,loc,size,material,part,parent=assembly,coll='Soldered assembly',bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if material:o.data.materials.append(material)
    place(o,name,part,parent,coll)
    if bevel:
        md=o.modifiers.new('Nominal corner radius','BEVEL');md.width=bevel;md.segments=3
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=md.name)
    return o

def cyl(name,loc,r,dep,material,part,parent=assembly,coll='Soldered assembly',verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=dep,location=loc);o=bpy.context.object
    if material:o.data.materials.append(material)
    return place(o,name,part,parent,coll)

def cut(o,cutter,op='DIFFERENCE'):
    bpy.context.view_layer.objects.active=o
    md=o.modifiers.new('Actual opening','BOOLEAN');md.solver='EXACT';md.operation=op;md.object=cutter
    bpy.ops.object.modifier_apply(modifier=md.name)
    if cutter in objects:objects.remove(cutter)
    bpy.data.objects.remove(cutter,do_unlink=True)

def rounded(w,d,r,segments=8):
    pts=[]
    for x,y,a in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
        for i in range(segments):
            t=math.radians(a+i*90/(segments-1));pts.append((x+r*math.cos(t),y+r*math.sin(t)))
    return pts

def prism(name,w,d,r,z0,z1,material,part,parent,coll):
    outline=rounded(w,d,r); n=len(outline)
    vs=[(x,y,z) for z in [z0,z1] for x,y in outline]
    fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name,vs,fs,material,part,parent,coll)

def hole(o,loc,w,d,z0,z1,r=.2):
    cutter=prism('cutter',w,d,r,z0,z1,None,'cutter',o.parent,'Reference only');cutter.location.x=loc[0];cutter.location.y=loc[1];cut(o,cutter)

def bore(o,loc,r,depth):
    cut(o,cyl('cutter',loc,r,depth,None,'cutter',o.parent,'Reference only'))

def text(name,body,loc,size,material,parent,coll='Caps and inserts',extrude=0):
    bpy.ops.object.text_add(location=loc);o=bpy.context.object;o.data.body=body;o.data.align_x='CENTER';o.data.align_y='CENTER';o.data.size=size;o.data.extrude=extrude
    o.data.materials.append(material);return place(o,name,'legend',parent,coll)

# True hollow lower shell and real cut switch plate.
cc=C['case']; W=cc['width']; DEP=cc['depth']; zbot=cc['bottomZ']
lower=prism('case.lower',W,DEP,cc['cornerRadius'],zbot,cc['topZ'],frost,'case',casegroup,'Case')
cavity=prism('cavity',W-2*cc['wall'],DEP-2*cc['wall'],cc['cornerRadius']-cc['wall'],zbot+cc['floor'],2,None,'cutter',casegroup,'Reference only');cut(lower,cavity)
pl=C['plate'];plate=prism('plate',pl['width'],pl['depth'],pl['cornerRadius'],-pl['thickness'],0,black,'plate',board,'Soldered assembly')
cp=C['pcb'];pcb=prism('pcb.unrouted',cp['width'],cp['depth'],2,D['pcbBottom'],D['pcbTop'],pcbmat,'pcb',board,'Soldered assembly')
for key in S['layout']['keys']:
    x,y,_=key['center'];hole(plate,(x,y),14,14,-2,1,.25)
    # Sourced center bore plus the drawing-based contact positions.
    bore(pcb,(x,y,-5.75),3.99/2,3)
    for dx,dy in [(-3.81,-2.54),(2.54,-5.08)]:
        bore(pcb,(x+dx,y+dy,-5.75),.75,3)
        cyl('Pad '+key['id'],(x+dx,y+dy,-6.53),1.05,.06,copper,'switch',board)
        cyl('Soldered terminal '+key['id'],(x+dx,y+dy,-7.3),.42,2.3,metal,'switch',board)
    capparent=empty('Cap motion '+key['id'],caproot,(x,y,0));groups[key['id']]=capparent
    holeparent=empty('Stem motion '+key['id'],board,(x,y,0));stemgroups[key['id']]=holeparent
    # Exact envelope; undimensioned upper BOX opening is explicitly provisional.
    box('switch.lower.'+key['id'],(x,y,-2.5),(13.95,13.95,5),rubber,'switch',board,bevel=.18)
    up=box('switch.upper.'+key['id'],(x,y,3.1),(15.6,13.9,6.2),clear,'switch',board,bevel=.3)
    bore(up,(x,y,4),3.0,7)
    sd=P['switch']['dimensions']
    cyl('switch.center-post.'+key['id'],(x,y,D['pcbTop']-sd['centerPostProjection']/2),sd['centerPostDiameter']/2,sd['centerPostProjection'],rubber,'switch',board)
    latchdepth=(sd['widthOverLatches']-sd['mountBodyDepth'])/2
    for side in [-1,1]:box('switch.latch.'+key['id']+'.'+str(side),(x,y+side*(sd['mountBodyDepth']/2+latchdepth/2),-1.9),(4,latchdepth,.8),rubber,'switch',board,bevel=.06)
    stem=box('switch.stem.'+key['id'],(0,0,8.1),(3.8,1.15,3.8),jade,'switch',holeparent,bevel=.1)
    box('switch.stem.cross.'+key['id'],(0,0,8.1),(1.15,3.8,3.8),jade,'switch',holeparent,bevel=.1)
    # Per-key source-sized LED external to filled switch-envelope region.
    kd=P['key_led']['dimensions'];ko=C['components']['key_led']['offset'];box('led.key.'+key['id'],(x+ko[0],y+ko[1],ko[2]+kd['height']/2),(kd['width'],kd['depth'],kd['height']),white,'key_led',board,bevel=.05)
    dd=P['diode']['dimensions'];do=C['components']['diode']['offset'];box('diode.'+key['id'],(x+do[0],y+do[1],do[2]),(dd.get('bodyLength',2.7),dd.get('bodyWidth',1.55),dd.get('bodyHeight',1.175)),rubber,'diode',board,bevel=.12)

# Hollow custom shallow-dish caps with physical roof, skirt and three Space sockets.
def makecap(key):
    d=key['capDimensions'];vs,fs=cap_shell_geometry(key)
    parent=groups[key['id']]
    cap=mesh('cap.'+key['id'],vs,fs,navy,key['partId'],parent,'Caps and inserts')
    for dx in ([0,-11.9,11.9] if key['units']==2 else [0]):
        st=d['stemSocket'];mouth=st['ceilingZ']-st['depth']
        boss=cyl('Socket boss '+key['id']+' '+str(dx),(dx,0,(mouth+10.8)/2),st['bossOuter']/2,10.8-mouth,navy,key['partId'],parent,'Caps and inserts')
        for sz in [(st['crossLength'],st['crossWidth']),(st['crossWidth'],st['crossLength'])]:
            cut(boss,box('cross cutter',(dx,0,(mouth+st['ceilingZ'])/2-.05),(*sz,st['depth']+.1),None,'cutter',parent,'Reference only'))
    # Source-free custom legend, cut and insert follow the actual roof volume.
    body='—' if key['id']=='space' else key['label']
    t=text('legend cutter',body,(0,0,11.5),2.7 if len(body)>3 else 3.2,white,parent,extrude=1.6)
    bpy.context.view_layer.objects.active=t;t.select_set(True);bpy.ops.object.convert(target='MESH');t=bpy.context.object
    inlay=t.copy();inlay.data=t.data.copy();scene.collection.objects.link(inlay);place(inlay,'insert.'+key['id'],'legend',parent,'Caps and inserts')
    shellcopy=cap.copy();shellcopy.data=cap.data.copy();scene.collection.objects.link(shellcopy);cut(inlay,shellcopy,'INTERSECT')
    cut(cap,t)
    return cap
caps=[makecap(k) for k in S['layout']['keys']]
repair_q(S)

# Source-based Cherry 2u axes and drill pair. Exterior housing/wire shape approximate.
sp=next(k for k in S['layout']['keys'] if k['id']=='space');sy=sp['center'][1];st=P['stabilizer']['dimensions']
for dx in [-st['supportOffsetX'],st['supportOffsetX']]:
    for dy,rad in [(st['smallHoleOffsetY'],st['smallHoleDiameter']/2),(st['largeHoleOffsetY'],st['largeHoleDiameter']/2)]:bore(pcb,(dx,sy+dy,-5.75),rad,3)
    hole(plate,(dx,sy),6.8,16,-2,1,.5)
    br=box('stabilizer bracket '+str(dx),(dx,sy,-1.9),(6.2,14.5,6.2),rubber,'stabilizer',board,bevel=.5)
    bore(br,(dx,sy,0),2.8,10)
    box('stabilizer plunger '+str(dx),(dx,0,8),(3.8,1.15,4),jade,'stabilizer',stemgroups['space'])
    box('stabilizer plunger cross '+str(dx),(dx,0,8),(1.15,3.8,4),jade,'stabilizer',stemgroups['space'])
    cyl('stabilizer moving lower guide '+str(dx),(dx,0,2),1.6,8,jade,'stabilizer',stemgroups['space'])

def tube(name,pts,r,material,part,parent,coll='Soldered assembly'):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3
    spl=cu.splines.new('POLY');spl.points.add(len(pts)-1)
    for p,co in zip(spl.points,pts):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);scene.collection.objects.link(o);o.data.materials.append(material);return place(o,name,part,parent,coll)
wire=tube('stabilizer approximate equalizing wire',[(-11.9,sy,-3),(-11.9,sy+6,-3),(11.9,sy+6,-3),(11.9,sy,-3)],.6,metal,'stabilizer',board)

# Bourns body clears a full body-sized opening, not a shaft-only hole.
enc=S['layout']['encoder'];kx,ky,_=enc['center'];ed=P['encoder']['dimensions']
hole(plate,(kx,ky),*pl['encoderOpening'],-2,3,.5)
box('encoder body',(kx,ky,-5+ed['bodyHeight']/2),(ed['bodyWidth'],ed['bodyDepth'],ed['bodyHeight']),metal,'encoder',board,bevel=.35)
cyl('encoder bushing',(kx,ky,1.5+ed['bushingLength']/2),3.5,ed['bushingLength'],metal,'encoder',board)
shaft=cyl('encoder shaft',(kx,ky,9),3,15,metal,'encoder',board)
cut(shaft,box('D shaft flat',(kx,ky+4.75,13.5),(10,5,8),None,'cutter',board,'Reference only'))
for dx in [-5,5]:
    for dy in [-5,5]:cyl('encoder solder tab',(kx+dx,ky+dy,-6.85),.5,3.7,metal,'encoder',board)
kn=C['knob'];knob=cyl('knob',(kx,ky,(kn['bottomZ']+kn['topZ'])/2),kn['diameter']/2,kn['height'],navy,'knob',knobroot,'Rotary control',96)
bore(knob,(kx,ky,(kn['bottomZ']+16.5)/2-.1),kn['shaftBore']/2,16.5-kn['bottomZ']+.2)
# D-flat wall remains inside the cylindrical seat; source fit still provisional.
box('knob D-flat seat',(kx,ky+2.65,12.5),(4.1,.65,8),navy,'knob',knobroot,'Rotary control',.1)
box('knob white index',(kx,ky+5.2,18.52),(.65,2.5,.08),white,'knob',knobroot,'Rotary control',.15)
for i in range(48):
    a=i*math.tau/48
    cyl('knob grip '+str(i),(kx+7.9*math.cos(a),ky+7.9*math.sin(a),13.5),.12,8,navy,'knob',knobroot,'Rotary control',8)

# Official CAD-derived controller and adapter, preserving original tessellation.
def source_mesh(part,placement,normalize,parent,coll):
    data=json.loads((ROOT/C['components'][part]['sourceMesh']).read_text());result=[]
    for solid in data['solids']:
        vs=[tuple(v[i]+normalize[i] for i in range(3)) for v in solid['vertices']]
        material=pcbmat if solid['index']==0 else (metal if part=='usb_adapter' and solid['index']==32 else rubber)
        o=mesh(part+'.CADsolid.'+str(solid['index']),vs,solid['faces'],material,part,parent,coll);o.location=placement;o['sourceStepHash']=data.get('sourceStepSHA256','');result.append(o)
    return result
co=C['components']['controller'];dm=P['controller']['dimensions']
controller_data=json.loads((ROOT/'spec/references/waveshare/controller-datums.json').read_text())
controller_objects=source_mesh('controller',co['center'],controller_data['normalization']['translate'],board,'Soldered assembly')
controller=controller_objects[0]
for part,dimensions in [('led_driver',(5,5,C['components']['led_driver']['height'])),('logic_buffer',(C['components']['logic_buffer']['width'],C['components']['logic_buffer']['depth'],C['components']['logic_buffer']['height']))]:
    box(part,C['components'][part]['center'],dimensions,rubber,part,board,bevel=.12)
rg=C['components']['rgb_strip'];rd=P['rgb_strip']['dimensions'];length=rg['pixels']*rd['pixelPitch']
strip=box('RGB covered strip',(0,rg['centerY'],rg['topZ']-rd['height']/2),(length,rd['width'],rd['height']),basewhite,'rgb_strip',board,bevel=.8)
for i in range(rg['pixels']):box('RGB pixel '+str(i),(-length/2+(i+.5)*rd['pixelPitch'],rg['centerY'],rg['topZ']-.4),(3.5,3.5,.8),white,'rgb_strip',board,bevel=.3)

usbgroup=empty('USB adapter retained in case',casegroup)
usbdata=json.loads((ROOT/C['components']['usb_adapter']['sourceDatums']).read_text())
usb=C['components']['usb_adapter'];usbX=usb['centerX'];rear=DEP/2
usb_objects=source_mesh('usb_adapter',usb['boardOrigin'],usbdata['normalization']['translate'],usbgroup,'Case')
# True rear aperture from exact sourced mouth, with .3 mm custom clearance.
mc=usb['mouthCenter'];ow,oh,orr=usb['mouthOuter'];aperture=prism('USB aperture',ow+.6,oh+.6,orr+.3,-4,4,None,'cutter',casegroup,'Reference only')
aperture.rotation_euler.x=math.pi/2;aperture.location=mc;cut(lower,aperture)
# Board edge is 0.0269 mm in front of mouth plane in official CAD: preserve, never crop source.
pcbEndY=usbdata['pcb']['bounds'][3]+usbdata['normalization']['translate'][1]+usb['boardOrigin'][1]
pcbPocketEnd=pcbEndY+usb['pcbEdgeClearance'];pcbPocketStart=rear-6
hole(lower,(usb['boardOrigin'][0],(pcbPocketStart+pcbPocketEnd)/2),18.62,pcbPocketEnd-pcbPocketStart,usb['pcbTopZ']-1.3,usb['pcbTopZ']+.3,.3)
# Nominal cradle and clamps outside manufacturer PCB (no board screw holes).
ucx,ucy,ucz=usb['boardOrigin']
cradle=box('USB cradle',(ucx,ucy,ucz-2.25),(21,20,2.5),frost,'case',casegroup,'Case',.8)
cut(cradle,box('cradle trim',(ucx,rear-cc['wall']+25,ucz-2),(50,50,20),None,'cutter',casegroup,'Reference only'))
for dx in C['mounting']['usbClampScrewOffsetsX']:
    sx=ucx+dx;sy=ucy+C['mounting']['usbClampScrewOffsetY']
    post=cyl('USB clamp post '+str(dx),(sx,sy,-17.25),2.5,6.5,frost,'case',casegroup,'Case');bore(post,(sx,sy,-17),1.15,9)
    clamp=box('USB clamp '+str(dx),(sx-dx/abs(dx)*1.7,sy,-12.5),(5.2,3,1),navy,'case',casegroup,'Case',.4);bore(clamp,(sx,sy,-12.5),1.15,3)
    nutcut=cyl('USB nut pocket',(sx,sy,-16.5),C['mounting']['nutTrapAcrossFlats']/math.sqrt(3),C['mounting']['nutTrapHeight'],None,'cutter',casegroup,'Reference only',6);cut(post,nutcut)
    cyl('USB clamp screw '+str(dx),(sx,sy,-15),1,6,metal,'fastener',casegroup,'Case')
    head=cyl('USB clamp head '+str(dx),(sx,sy,-11),1.9,2,metal,'fastener',casegroup,'Case');bore(head,(sx,sy,-10.25),.85,.6)
    nut=cyl('USB clamp nut '+str(dx),(sx,sy,-16.5),4/math.sqrt(3),1.6,metal,'fastener_nut',casegroup,'Case',6);bore(nut,(sx,sy,-16.5),1,3)

# Flat ribbon on nominal source-contract route; rounded corners are an explicit assumption.
fpcparams=C['components']['fpc_cable'];route=[Vector(v) for v in fpcparams['route']]
def fillet_route(points,radius):
    out=[points[0]];exact=sum((b-a).length for a,b in zip(points,points[1:]))
    for prev,p,nxt in zip(points,points[1:],points[2:]):
        u=(p-prev).normalized();v=(nxt-p).normalized();theta=u.angle(v);dist=radius*math.tan(theta/2)
        assert dist<(p-prev).length*.49 and dist<(nxt-p).length*.49,'Route segment too short for nominal circular bend'
        start=p-u*dist;end=p+v*dist;normal=(v-u*math.cos(theta))/math.sin(theta);center=start+normal*radius;rad=start-center;axis=u.cross(v).normalized();out.append(start)
        for j in range(1,25):out.append(center+Quaternion(axis,theta*j/24)@rad)
        exact-=2*dist-radius*theta
    out.append(points[-1]);return out,exact
route_smooth,fpc_exact_length=fillet_route(route,fpcparams['minimumBendRadius']);fpc_vs=[];width=fpcparams['width'];th=fpcparams['thickness']
for i,pnt in enumerate(route_smooth):
    tangent=(route_smooth[min(i+1,len(route_smooth)-1)]-route_smooth[max(i-1,0)]).normalized();side=tangent.cross(Vector((0,0,1))).normalized()*width/2
    for zadd,sgn in [(-th/2,-1),(-th/2,1),(th/2,1),(th/2,-1)]:fpc_vs.append(tuple(pnt+side*sgn+Vector((0,0,zadd))))
fpc_faces=[]
for i in range(len(route_smooth)-1):
    for j in range(4):fpc_faces.append((i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j))
fpc_faces+=[(3,2,1,0),tuple(range(len(fpc_vs)-4,len(fpc_vs)))]
fpc=mesh('FPC | provisional ribbon envelope',fpc_vs,fpc_faces,flexmat,'fpc_cable',board)
fpc_length=sum((b-a).length for a,b in zip(route_smooth,route_smooth[1:]))
fpc['routeLength']=fpc_length;fpc['status']='Nominal route only; flat-flex folding and contact side unverified'

# Fixed case feet: source envelope, analytic spherical-cap contact approximation.
ft=C['rubberFoot'];fr=ft['diameter']/2;fh=ft['height'];R=(fr*fr+fh*fh)/(2*fh)
def foot(name,x,y,z,parent,coll,rotation=0):
    # z is adhesive/mating plane; rotationally symmetric spherical segment, closed top.
    n=48;vs=[(0,0,-fh)];fs=[];rings=12
    theta=math.acos((R-fh)/R)
    for j in range(1,rings+1):
        a=theta*j/rings;rr=R*math.sin(a);zz=R-fh-R*math.cos(a)
        for i in range(n):vs.append((rr*math.cos(i*math.tau/n),rr*math.sin(i*math.tau/n),zz))
    for i in range(n):fs.append((0,1+(i+1)%n,1+i))
    for j in range(rings-1):
        for i in range(n):a=1+j*n+i;b=1+j*n+(i+1)%n;fs.append((a,b,b+n,a+n))
    fs.append(tuple(range(1+(rings-1)*n,1+rings*n)))
    o=mesh(name,vs,fs,rubber,'rubber_foot',parent,coll);o.location=(x,y,z);o.rotation_euler.x=rotation;return o
for x,y in ft['centers']:foot('case foot '+str((x,y)),x,y,zbot,casegroup,'Case')
# Captive case magnets: local bosses preserve 1 mm floor web.
mag=P['magnet']['dimensions'];rp=C['riser'];my=rp['magnetY']
for x in rp['magnetX']:
    boss=cyl('case magnet boss '+str(x),(x,my,zbot+cc['floor']+cc['magnetBossHeight']/2),4.8,cc['magnetBossHeight'],frost,'case',casegroup,'Case')
    pocket=cyl('pocket',(x,my,zbot+rp['magnetPocketDepth']/2-.01),rp['magnetPocketDiameter']/2,rp['magnetPocketDepth']+.02,None,'cutter',casegroup,'Reference only')
    cut(lower,pocket)
    bore(boss,(x,my,zbot+rp['magnetPocketDepth']/2),rp['magnetPocketDiameter']/2,rp['magnetPocketDepth'])
    cyl('case magnet '+str(x),(x,my,zbot+.15+mag['thickness']/2),mag['diameter']/2,mag['thickness'],metal,'magnet',casegroup,'Case')
    ring=cyl('case captive magnet cover '+str(x),(x,my,zbot+.075),rp['magnetPocketDiameter']/2,.15,frost,'case',casegroup,'Case');bore(ring,(x,my,zbot),3.05,1)

# Alternative rear bars share the exact case interface; flat mode removes both.
for angle in [4,7]:
    a=math.radians(angle);pose=S['poses'][str(angle)];root=risers[angle]
    front=rp['frontY'];back=rp['rearY'];fy=rp['footY']
    bottom=(fh-pose['translation'][2]-fy*math.sin(a))/math.cos(a)
    outline=rounded(rp['width'],rp['depth'],rp['endRadius'])
    pts=[(x,y+(front+back)/2) for x,y in outline];n=len(pts)
    def zb(y):return (fh-pose['translation'][2]-y*math.sin(a))/math.cos(a)
    vs=[(x,y,zbot) for x,y in pts]+[(x,y,zb(y)) for x,y in pts]
    fs=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
    bar=mesh('riser.'+str(angle),vs,fs,navy,'riser_'+str(angle),root,'Riser '+str(angle))
    md=bar.modifiers.new('Blunt rounded edges','BEVEL');md.width=rp['edgeRadius'];md.segments=4
    bpy.context.view_layer.objects.active=bar;bpy.ops.object.modifier_apply(modifier=md.name)
    # Rear case feet remain attached; actual reliefs prevent intersecting the bar.
    for x,y in ft['centers']:
        if y>0:bore(bar,(x,y,zbot-rp['rearFootReliefDepth']/2),rp['rearFootReliefDiameter']/2,rp['rearFootReliefDepth']+.05)
    for x in rp['magnetX']:
        bore(bar,(x,my,zbot-rp['magnetPocketDepth']/2+.01),rp['magnetPocketDiameter']/2,rp['magnetPocketDepth']+.02)
        cyl('riser magnet '+str((angle,x)),(x,my,zbot-.15-mag['thickness']/2),mag['diameter']/2,mag['thickness'],metal,'magnet',root,'Riser '+str(angle))
        ring=cyl('riser captive magnet cover '+str((angle,x)),(x,my,zbot-.075),rp['magnetPocketDiameter']/2,.15,navy,'case',root,'Riser '+str(angle));bore(ring,(x,my,zbot),3.05,1)
    for x in rp['footX']:foot('riser foot '+str((angle,x)),x,fy,bottom,root,'Riser '+str(angle),-a)
    sk=rp['shearKeys']
    for x,y in sk['centers']:
        cyl('riser shear key '+str((angle,x)),(x,y,zbot+sk['height']/2),sk['diameter']/2,sk['height'],navy,'case',root,'Riser '+str(angle))
    for o in colls['Riser '+str(angle)].objects:o['modeAngle']=angle

for x,y in rp['shearKeys']['centers']:bore(lower,(x,y,zbot+rp['shearKeys']['pocketDepth']/2),rp['shearKeys']['pocketDiameter']/2,rp['shearKeys']['pocketDepth']+.05)

# Nominal support/fastener map. Holes and captive nut pockets are drawn, no threads invented.
caseScrewRoot=empty('Removable case screws',assembly)
for x,y in C['mounting']['caseScrewPositions']:
    bore(plate,(x,y,-.75),C['mounting']['panelScrewClearanceDiameter']/2,4)
    bore(pcb,(x,y,-5.75),C['mounting']['pcbPostClearanceDiameter']/2,3)
    post=cyl('case plate support '+str((x,y)),(x,y,-4.75),C['mounting']['postDiameter']/2,6.5,frost,'case',casegroup,'Case')
    bore(post,(x,y,-4.75),1.15,8)
    nutcut=cyl('nut pocket',(x,y,-5.2),C['mounting']['nutTrapAcrossFlats']/math.sqrt(3),C['mounting']['nutTrapHeight'],None,'cutter',casegroup,'Reference only',6);cut(post,nutcut)
    screw=cyl('case screw shank '+str((x,y)),(x,y,-3),1,6,metal,'fastener',caseScrewRoot,'Case')
    head=cyl('case screw head '+str((x,y)),(x,y,1),1.9,2,metal,'fastener',caseScrewRoot,'Case');bore(head,(x,y,1.7),.85,.7)
    nut=cyl('captive nut '+str((x,y)),(x,y,-5.2),4/math.sqrt(3),1.6,metal,'fastener_nut',casegroup,'Case',6);bore(nut,(x,y,-5.2),1,3)

# Separate hidden overlay concept; no sensor or fit mechanics are asserted.
overlay=prism('overlay | concept with dial notch',C['overlay']['width'],C['overlay']['depth'],3,C['overlay']['bottomZ'],C['overlay']['bottomZ']+C['overlay']['thickness'],mat('Overlay concept',(.14,.18,.25),.6),'overlay',assembly,'Overlay concept')
hole(overlay,(kx,ky),24,30,12,15,3)
colls['Overlay concept'].hide_render=True;colls['Overlay concept'].hide_viewport=True

# Studio and cameras.
floor=box('Desk',(0,0,-1.5),(2000,2000,3),mat('Desk',(.035,.045,.062),.7),'studio',None,'Studio')
world=bpy.data.worlds.new('Studio world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.13,.17,.23,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35;scene.world=world

def area(name,loc,power,size,target,color):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
area('Key light',(-130,-120,250),400000,190,(0,0,20),(.84,.91,1))
area('Reflection strip',(80,140,180),500000,160,(0,0,15),(.65,.77,1))
area('Fill',(100,-160,80),120000,140,(0,0,20),(1,.91,.82))
spill=area('Illustrative base glow',(0,-58,5),4000,90,(0,-85,0),(.8,.92,1));spill.data.shape='RECTANGLE';spill.data.size_y=5

def camera(name,loc,target,scale):
    bpy.ops.object.camera_add(location=loc);o=bpy.context.object;o.name=name;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=scale;return o
beauty=camera('CAM assembled and glow',(220,-260,190),(0,0,24),218)
under=camera('CAM underside',(190,180,-130),(0,0,24),270)
sectioncam=camera('CAM section',(0,-220,80),(0,-7,20),180)
switchcam=camera('CAM switch travel',(100,-180,125),(-10,-15,32),165)
scene.camera=beauty
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.view_settings.view_transform='AgX';scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.fps=S['animations']['fps']
scene.render.film_transparent=False

def pose(angle):
    p=S['poses'][str(angle)];assembly.rotation_euler=(p['rotationX'],0,0);assembly.location=p['translation']
    for a in [4,7]:
        colls['Riser '+str(a)].hide_render=(a!=angle);colls['Riser '+str(a)].hide_viewport=(a!=angle)
pose(C['riser']['defaultAngle'])
scene.frame_start=1;scene.frame_end=576
for f,name in [(1,'ASSEMBLY | 12 seconds'),(289,'SWITCH TRAVEL | 4 seconds'),(385,'GLOW | 8 seconds')]:scene.timeline_markers.new(name,frame=f)
# One source scene, explicit clip frame ranges. Soldered parts always share board parent.
for root,offset in [(caproot,Vector((0,0,42))),(knobroot,Vector((0,0,42))),(board,Vector((0,0,22))),(risers[4],Vector((0,0,-24)))]:
    for f,t in [(1,0),(48 if root==board else 24,0),(96,1),(144,1),(240,0),(288,0),(289,0),(576,0)]:
        root.location=offset*t;root.keyframe_insert('location',frame=f)
for f,t in [(1,0),(24,0),(48,1),(216,1),(240,0),(576,0)]:
    caseScrewRoot.location=(0,0,50*t);caseScrewRoot.keyframe_insert('location',frame=f)
for kid,frames in [('a',[(289,0),(300,0),(312,1.8),(324,3.6),(336,0),(384,0)]),('space',[(289,0),(336,0),(348,1.8),(360,3.6),(372,3.6),(384,0)])]:
    for g in [groups[kid],stemgroups[kid]]:
        base=g.location.copy()
        for f,travel in frames:g.location=base-Vector((0,0,travel));g.keyframe_insert('location',frame=f)
basepose=Vector(S['poses']['4']['translation'])
for f,lift in [(1,0),(24,0),(96,24),(144,24),(240,0),(288,0),(576,0)]:
    assembly.location=basepose+Vector((0,0,lift));assembly.keyframe_insert('location',frame=f)
# RGB base animation remains illustrative; white key LEDs never turn RGB.
bs=frost.node_tree.nodes.get('Principled BSDF')
for f,color,emit,power in [(1,(.8,.9,1,1),.06,4000),(385,(.8,.9,1,1),.06,4000),(432,(.8,.9,1,1),.06,4000),(456,(.8,.9,1,1),.5,10000),(480,(.8,.9,1,1),.5,10000),(504,(.15,.65,1,1),.55,10000),(528,(.3,.15,1,1),.5,9000),(552,(.8,.9,1,1),.06,4000),(576,(.8,.9,1,1),.06,4000)]:
    bs.inputs['Emission Color'].default_value=color;bs.inputs['Emission Color'].keyframe_insert('default_value',frame=f)
    bs.inputs['Emission Strength'].default_value=emit;bs.inputs['Emission Strength'].keyframe_insert('default_value',frame=f)
    spill.data.color=color[:3];spill.data.keyframe_insert('color',frame=f);spill.data.energy=power;spill.data.keyframe_insert('energy',frame=f)
wb=white.node_tree.nodes.get('Principled BSDF')
for f,e in [(1,1.2),(385,1.2),(432,1.2),(456,4),(480,4),(504,1.2),(576,1.2)]:wb.inputs['Emission Strength'].default_value=e;wb.inputs['Emission Strength'].keyframe_insert('default_value',frame=f)
scene.frame_set(1)

# Verification distinguishes measured nominal geometry from unsupported interfaces.
checks=[]
def check(name,ok,details):checks.append({'id':name,'status':'PASS' if ok else 'FAIL','details':details})
def unknown(name,details):checks.append({'id':name,'status':'UNKNOWN','details':details})
check('key_count',len(caps)==28,{'actual':len(caps),'expected':28})
check('single_space_switch',sum(k['id']=='space' for k in S['layout']['keys'])==1,{'spaceCenter':sp['center'],'stabilizerAxes':[-11.9,11.9]})
worst=S['fitPolicy']['switchWorstCaseTravel'];roof=C['keycap_1u']['minInnerRoofZ']-worst-(D['pcbTop']+P['switch']['dimensions']['housingRoofAbovePCB']);skirt=C['keycap_1u']['bottomZ']-worst
check('cap_roof_clearance_at_max_travel',roof>=.3,{'mm':roof,'travel':worst,'excludesStemBoss':True})
check('cap_skirt_plate_clearance_at_max_travel',skirt>=.3,{'mm':skirt,'travel':worst})
check('adjacent_caps',S['layout']['pitch']-C['keycap_1u']['width']>=.3,{'minimumGap':S['layout']['pitch']-C['keycap_1u']['width']})
check('knob_to_adjacent_cap',S['layout']['pitch']-kn['diameter']/2-C['keycap_1u']['width']/2>=.3,{'gap':S['layout']['pitch']-kn['diameter']/2-C['keycap_1u']['width']/2})
check('encoder_body_plate_opening',min(pl['encoderOpening'][0]-ed['bodyWidth'],pl['encoderOpening'][1]-ed['bodyDepth'])/2>=.3,{'nominalMinimumPerSide':min(pl['encoderOpening'][0]-ed['bodyWidth'],pl['encoderOpening'][1]-ed['bodyDepth'])/2})
check('knob_push_bushing_clearance',kn['bottomZ']-ed['pushTravel']-(D['pcbTop']+ed['bodyHeight']+ed['bushingLength'])>=.3,{'gap':kn['bottomZ']-ed['pushTravel']-(D['pcbTop']+ed['bodyHeight']+ed['bushingLength'])})
check('magnet_floor_web',cc['floor']+cc['magnetBossHeight']-rp['magnetPocketDepth']>=.99,{'mm':cc['floor']+cc['magnetBossHeight']-rp['magnetPocketDepth']})
check('FPC_length_fits_selected_cable',fpc_exact_length<=fpcparams['maximumRouteLength'],{'measuredArcLength':fpc_exact_length,'cableLength':P['fpc_cable']['dimensions']['length'],'remainingAllowance':P['fpc_cable']['dimensions']['length']-fpc_exact_length})
check('usb_blind_pocket_outer_wall',rear-pcbPocketEnd>=usb['minimumOuterWallSkin'],{'remainingWall':rear-pcbPocketEnd,'sourcePCBFrontClearance':pcbPocketEnd-pcbEndY})
check('controller_floor_clearance',co['center'][2]-1.000003-(zbot+cc['floor'])>=.3,{'mm':co['center'][2]-1.000003-(zbot+cc['floor'])})
check('soldered_subassembly_rigid',all(o.parent==board for o in objects if o.name.startswith(('switch.upper','switch.lower','Soldered terminal','encoder body'))),{'ordinaryDisassemblyDoesNotDesolder':True})
for angle in [0,4,7]:
    pp=S['poses'][str(angle)];a=pp['rotationX'];zc=zbot+R-fh;yf=-DEP/2+9
    contact=pp['translation'][2]+yf*math.sin(a)+zc*math.cos(a)-R
    check('front_contact_'+str(angle),abs(contact)<1e-6,{'analyticDeskGap':contact,'profile':'spherical-cap approximation'})
unknown('stem_socket_BOX_guide','Manufacturer source does not dimension cross or BOX guide. Provisional socket and stem mesh; no claim of physical cap retention or boss sweep fit.')
unknown('stabilizer_housing_motion','Axes and PCB drill pattern are sourced; housing exterior, plunger fit and equalizing-wire dynamics approximate.')
check('usb_flush_source_datum',abs((rear-mc[1])-usb.get('nominalMouthRecess',.05))<1e-6,{'mouthCenter':mc,'outerDimensions':usb['mouthOuter'],'sourceStepSHA256':usbdata['sourceStepSHA256'],'PCBEdgeProjection':.026905-usb.get('nominalMouthRecess',.05),'nominalMouthRecess':usb.get('nominalMouthRecess',.05)})
for angle in [4,7]:
    a=math.radians(angle);pp=S['poses'][str(angle)];frontbottom=(fh-pp['translation'][2]-rp['frontY']*math.sin(a))/math.cos(a)
    check('riser_minimum_nose_'+str(angle),zbot-frontbottom>=rp['minimumNoseHeight'],{'actualNoseHeight':zbot-frontbottom,'minimum':rp['minimumNoseHeight'],'underside':'parallel to world desk'})
check('riser_magnet_pocket_contained',rp['rearY']-(my+rp['magnetPocketDiameter']/2)>=.3,{'rearWeb':rp['rearY']-(my+rp['magnetPocketDiameter']/2)})
check('riser_rear_foot_support',rp['rearY']-(rp['footY']+fr)>=.3,{'rearWeb':rp['rearY']-(rp['footY']+fr)})
unknown('usb_cable_sample','Mouth CAD plane is flush. Plug overmould envelope is an unselected reference; actual cable not tested.')
unknown('FPC_interface_and_bend',{'routeLengthMm':fpc_length,'analyticArcLengthMm':fpc_exact_length,'nominalCableLength':P['fpc_cable']['dimensions']['length'],'note':'Source outlets inferred; exact neutral axis, contact side and flat-flex folding/bend radius unverified. Ribbon route is a planning envelope.'})
unknown('optical_diffusion','Emission and external spill are illustrative, not optical validation. Per-key LED passage is provisional.')
unknown('manufacturing_and_retention','Printed fit, rubber deformation/adhesive, magnet force, screw access and inserts require physical validation. PCB unrouted.')

# Native geometry manifest: actual mesh bbox/vertex hashes tied to the frozen source.
bpy.context.view_layer.update()
manifest={'revision':S['revision'],'sourceSpecHash':S['sourceSpecHash'],'geometryHash':S['geometryHash'],'units':'mm','coordinateSystem':S['coordinateSystem'],'poses':S['poses'],'instances':[]}
mesh_digest=hashlib.sha256()
for o in objects:
    if o.type!='MESH':continue
    me=o.data
    coords=[tuple(round(v,6) for v in p.co) for p in me.vertices]
    digest=hashlib.sha256(json.dumps({'vertices':coords,'faces':[tuple(p.vertices) for p in me.polygons]},sort_keys=True).encode()).hexdigest()
    mesh_digest.update((o.name+digest).encode())
    vs=[Vector(v) for v in o.bound_box];bmin=[min(v[i] for v in vs) for i in range(3)];bmax=[max(v[i] for v in vs) for i in range(3)]
    manifest['instances'].append({'id':o.name,'partId':o.get('partId'),'sourceIds':json.loads(o.get('sourceIds','[]')),'dimensionStatus':o.get('dimensionStatus'),'parent':o.parent.name if o.parent else None,'location':list(o.location),'rotation':list(o.rotation_euler),'bboxLocal':{'min':bmin,'max':bmax},'vertices':len(me.vertices),'faces':len(me.polygons),'meshHash':digest})
manifest['builtMeshHash']=mesh_digest.hexdigest()
(OUT/'geometry-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
report={'revision':S['revision'],'sourceSpecHash':S['sourceSpecHash'],'geometryHash':S['geometryHash'],'builtMeshHash':manifest['builtMeshHash'],'keys':len(caps),'physicalFitValidated':False,'pcbRouted':False,'checks':checks,'failures':[c['id'] for c in checks if c['status']=='FAIL'],'limitations':[c['id'] for c in checks if c['status']=='UNKNOWN'],'clips':[{'file':'assembly.mp4','frames':[1,288],'seconds':12},{'file':'switch-motion.mp4','frames':[289,384],'seconds':4},{'file':'glow.mp4','frames':[385,576],'seconds':8}],'blenderVersion':bpy.app.version_string}
(OUT/'model-report.json').write_text(json.dumps(report,indent=2)+'\n')
assert not report['failures'],report['failures']
scene.camera=beauty;scene.frame_set(1);scene.render.resolution_x=960;scene.render.resolution_y=720
bpy.ops.object.select_all(action='DESELECT');bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'keypad-fit-v1.blend'))
print('FIT_V1_MODEL_CHECKPOINT',json.dumps({'objects':len(objects),'keys':len(caps),'hash':S['sourceSpecHash'],'failures':report['failures'],'unknown':len(report['limitations'])}))
if RENDER:
    scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1600;scene.render.resolution_y=1200
    for cam,path in [(beauty,'assembled.png'),(under,'underside.png')]:
        scene.camera=cam;floor.hide_render=cam==under;scene.render.filepath=str(OUT/path);bpy.ops.render.render(write_still=True)
    floor.hide_render=False
    # Section the custom enclosure and caps using true mesh cut modifiers. Purchased switch internals are omitted, not invented.
    sectioncut=box('Section plane cutter',(0,-107,10),(400,200,200),None,'cutter',None,'Reference only')
    sectioned=[]
    for o in objects.copy():
        if o.type=='MESH' and o.get('partId') in ['case','plate','pcb','keycap_1u','keycap_2u','legend'] and o!=sectioncut:
            md=o.modifiers.new('Display section only','BOOLEAN');md.object=sectioncut;md.operation='DIFFERENCE';md.solver='EXACT';sectioned.append((o,md))
    sectioncut.hide_render=True
    scene.camera=sectioncam;scene.render.filepath=str(OUT/'section.png');bpy.ops.render.render(write_still=True)
    for o,m in sectioned:o.modifiers.remove(m)
    bpy.data.objects.remove(sectioncut,do_unlink=True)
    scene.render.engine='CYCLES';scene.cycles.samples=4;scene.render.resolution_x=960;scene.render.resolution_y=720
    for start,end,name,cam in [(1,288,'assembly',beauty),(289,384,'switch-motion',switchcam),(385,576,'glow',beauty)]:
        folder=OUT/'frames'/name;folder.mkdir(parents=True,exist_ok=True);scene.camera=cam;scene.frame_start=start;scene.frame_end=end;scene.render.filepath=str(folder/'frame_');bpy.ops.render.render(animation=True)
    scene.camera=beauty;scene.frame_start=1;scene.frame_end=576;scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'keypad-fit-v1.blend'))
