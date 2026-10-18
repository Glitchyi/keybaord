"""Shared cap-shell construction and a closed, robust custom Q stencil."""
import bpy,math
def rounded(w,d,r,segments=8):
    pts=[]
    for x,y,a in [(w/2-r,d/2-r,0),(-w/2+r,d/2-r,90),(-w/2+r,-d/2+r,180),(w/2-r,-d/2+r,270)]:
        for i in range(segments):
            t=math.radians(a+i*90/(segments-1));pts.append((x+r*math.cos(t),y+r*math.sin(t)))
    return pts

def cap_shell_geometry(key):
    d=key['capDimensions'];n=32; rings=[];vs=[]
    outline=rounded(d['width'],d['depth'],d['cornerRadius'])
    crown=rounded(d['crownWidth'],d['crownDepth'],d['cornerRadius'])
    innerbot=rounded(d['width']-2*d['wall'],d['depth']-2*d['wall'],max(.2,d['cornerRadius']-d['wall']))
    innertop=rounded(d['crownWidth']-2*d['wall'],d['crownDepth']-2*d['wall'],max(.2,d['cornerRadius']-d['wall']))
    def ring(points,z):
        ids=[]
        for x,y in points:ids.append(len(vs));vs.append((x,y,z(x,y) if callable(z) else z))
        rings.append(ids);return ids
    a=ring(outline,d['bottomZ']);b=ring(crown,d['crownTopZ']);c=ring(innerbot,d['bottomZ']);e=ring(innertop,d['crownTopZ']-1)
    fs=[]
    def bridge(a,b,rev=False):
        for i in range(n):
            j=(i+1)%n;f=(a[i],a[j],b[j],b[i]);fs.append(tuple(reversed(f)) if rev else f)
    bridge(a,b);bridge(c,a);bridge(e,c)
    for outer,base,reverse in [(b,crown,False),(e,innertop,True)]:
        prev=outer
        for fraction in [.8,.6,.4,.2]:
            z=d['crownTopZ']-d['dishDepth']*(1-fraction*fraction)-(1 if reverse else 0)
            nxt=ring([(x*fraction,y*fraction) for x,y in base],z);bridge(prev,nxt,reverse);prev=nxt
        idx=len(vs);vs.append((0,0,d['crownTopZ']-d['dishDepth']-(1 if reverse else 0)))
        for i in range(n):
            f=(prev[i],prev[(i+1)%n],idx);fs.append(tuple(reversed(f)) if reverse else f)
    return vs,fs

def _object(name,vertices,faces,parent,material):
    me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o);o.parent=parent;o.data.materials.append(material);return o

def _bool(obj,other,operation):
    bpy.context.view_layer.objects.active=obj;m=obj.modifiers.new('Closed glyph operation','BOOLEAN');m.operation=operation;m.solver='EXACT';m.object=other;bpy.ops.object.modifier_apply(modifier=m.name)

def repair_q(spec):
    key=next(k for k in spec['layout']['keys'] if k['id']=='q');cap=bpy.data.objects['cap.q'];insert=bpy.data.objects['insert.q'];navy=bpy.data.materials['Deep navy custom shells'];white=bpy.data.materials['White translucent inlays']
    vertices,faces=cap_shell_geometry(key);fresh=bpy.data.meshes.new('Pristine Q cap shell');fresh.from_pydata(vertices,[],faces);fresh.update();fresh.materials.append(navy);cap.data=fresh
    n=64;verts=[]
    for z,rx,ry in [(10,.92,1.16),(10,.60,.84),(13,.92,1.16),(13,.60,.84)]:
        verts.extend((-.12+rx*math.cos(i*math.tau/n),.1+ry*math.sin(i*math.tau/n),z) for i in range(n))
    fs=[]
    for i in range(n):
        j=(i+1)%n;fs.extend([(i,j,2*n+j,2*n+i),(n+i,3*n+i,3*n+j,n+j),(j,i,n+i,n+j),(2*n+i,2*n+j,3*n+j,3*n+i)])
    cutter=_object('Closed Q oval cutter',verts,fs,cap.parent,white)
    bpy.ops.mesh.primitive_cube_add(size=1,location=(.62,-.80,11.5));tail=bpy.context.object;tail.name='Closed Q tail cutter';tail.dimensions=(1.4,.28,3);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);tail.parent=cap.parent;tail.rotation_euler.z=-math.pi/4
    _bool(cutter,tail,'UNION');bpy.data.objects.remove(tail,do_unlink=True)
    insert.data=cutter.data.copy();insert.location=(0,0,0);insert.rotation_euler=(0,0,0);insert.scale=(1,1,1)
    shellcopy=cap.copy();shellcopy.data=cap.data.copy();bpy.context.scene.collection.objects.link(shellcopy);_bool(insert,shellcopy,'INTERSECT');bpy.data.objects.remove(shellcopy,do_unlink=True)
    _bool(cap,cutter,'DIFFERENCE');bpy.data.objects.remove(cutter,do_unlink=True)
    insert.data.materials.clear();insert.data.materials.append(white)
    for face in insert.data.polygons:face.material_index=0
    cap['legendConstruction']='Closed custom oval Q with tail; original text Boolean lacked roof faces'
    bpy.context.view_layer.update()
