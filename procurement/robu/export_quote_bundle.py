"""Export frozen fit-v1 custom geometry for local budgetary quoting only.
Run with Blender --background design/fit-v1/keypad-fit-v1.blend --python procurement/robu/export_quote_bundle.py
Never saves the native scene; source/native/media files are read-only inputs.
"""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,struct,csv,datetime
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree

OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent;STL=OUT/'stl';STL.mkdir(exist_ok=True)
SPEC=json.loads((ROOT/'spec/resolved.json').read_text());SRC=json.loads((ROOT/'design/fit-v1/geometry-manifest.json').read_text());MEDIA=json.loads((ROOT/'design/fit-v1/media-manifest.json').read_text())
NATIVE=ROOT/'design/fit-v1/keypad-fit-v1.blend';native_hash=hashlib.sha256(NATIVE.read_bytes()).hexdigest();media_hash=hashlib.sha256((ROOT/'design/fit-v1/media-manifest.json').read_bytes()).hexdigest()
assert native_hash==MEDIA['files']['keypad-fit-v1.blend']['sha256'];assert bpy.context.scene['sourceSpecHash']==SPEC['sourceSpecHash']==SRC['sourceSpecHash']
scene=bpy.context.scene;scene.frame_set(1);assembly=bpy.data.objects['Assembly | common frozen datum'];C=SPEC['custom'];objects=bpy.data.objects
export_coll=bpy.data.collections.new('Transient quote export');scene.collection.children.link(export_coll)
records=[];failures=[];pending={};normal_log=[]

def body_matrix(obj):
    """Use local hierarchy matrices, including hidden 7-degree objects, without assembly pose."""
    mat=Matrix.Identity(4);node=obj
    while node is not None and node!=assembly:
        mat=(node.matrix_parent_inverse@node.matrix_basis)@mat;node=node.parent
    if node!=assembly:raise RuntimeError('Part outside mechanical assembly: '+obj.name)
    return mat

def clone(name,target=Matrix.Identity(4)):
    src=objects[name];me=src.data.copy();me.transform(target@body_matrix(src));o=bpy.data.objects.new('QUOTE '+name,me);export_coll.objects.link(o)
    bm=bmesh.new();bm.from_mesh(me);before=sum(1 for e in bm.edges if not e.is_manifold);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
    o['sourceName']=name;o['sourceNonManifoldEdges']=before;return o

def boolean(obj,other,operation):
    bpy.context.view_layer.objects.active=obj;m=obj.modifiers.new('Transient exact '+operation,'BOOLEAN');m.operation=operation;m.solver='EXACT';m.object=other
    bpy.ops.object.modifier_apply(modifier=m.name)

def union(names,target):
    parts=[clone(name,target) for name in names];result=parts[0];steps=[]
    for other in parts[1:]:
        before=len(result.data.polygons)
        try:boolean(result,other,'UNION');steps.append({'other':other['sourceName'],'status':'applied','beforeFaces':before,'afterFaces':len(result.data.polygons)})
        except Exception as ex:steps.append({'other':other['sourceName'],'status':'failed','error':str(ex)})
        bpy.data.objects.remove(other,do_unlink=True)
    return result,steps

def component_stats(bm):
    unseen=set(bm.verts);components=[]
    while unseen:
        root=unseen.pop();stack=[root];verts={root};faces=set()
        while stack:
            v=stack.pop();faces.update(v.link_faces)
            for e in v.link_edges:
                w=e.other_vert(v)
                if w in unseen:unseen.remove(w);verts.add(w);stack.append(w)
        volume=sum(f.calc_area()*f.normal.dot(f.calc_center_median())/3 for f in faces)
        components.append({'vertices':len(verts),'faces':len(faces),'signedVolumeMm3':volume})
    return components

def inspect(obj):
    bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.normal_update()
    comps=component_stats(bm);boundary=sum(e.is_boundary for e in bm.edges);wire=sum(e.is_wire for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);noncontiguous=sum(e.is_manifold and not e.is_contiguous for e in bm.edges);deg=sum(f.calc_area()<1e-10 for f in bm.faces)
    volume=bm.calc_volume(signed=True);area=sum(f.calc_area() for f in bm.faces);verts=[v.co.copy() for v in bm.verts];bounds={'min':[min(v[i] for v in verts) for i in range(3)],'max':[max(v[i] for v in verts) for i in range(3)]};dims=[bounds['max'][i]-bounds['min'][i] for i in range(3)]
    info={'dimensionsMm':dims,'boundsMm':bounds,'signedVolumeMm3':volume,'absoluteVolumeMm3':abs(volume),'surfaceAreaMm2':area,'vertices':len(bm.verts),'triangles':len(bm.faces),'boundaryEdges':boundary,'nonManifoldEdges':nonmanifold,'wireEdges':wire,'inconsistentWindingEdges':noncontiguous,'degenerateTriangles':deg,'connectedComponents':comps,'closedManifold':nonmanifold==0 and noncontiguous==0 and deg==0 and abs(volume)>1e-7}
    return bm,info

def write_stl(path,bm):
    header=b'Quote only - fit-v1 nominal mm - not print ready'.ljust(80,b' ')
    with path.open('wb') as f:
        f.write(header);f.write(struct.pack('<I',len(bm.faces)))
        for face in bm.faces:
            a,b,c=[v.co for v in face.verts];normal=(b-a).cross(c-a)
            if normal.length:normal.normalize()
            f.write(struct.pack('<12fH',*normal,*a,*b,*c,0))

def ray_wall(obj,point,direction):
    vs=[v.co for v in obj.data.vertices];tree=BVHTree.FromPolygons(vs,[list(p.vertices) for p in obj.data.polygons]);v=Vector(point);d=Vector(direction).normalized();h1=tree.ray_cast(v,d)
    if h1[0] is None:return None
    h2=tree.ray_cast(h1[0]+d*.00001,d)
    return (h2[0]-h1[0]).length if h2[0] is not None else None

def feature(label,value,kind='wall',status='below-provider-minimum'):
    return {'feature':label,'mm':value,'kind':kind,'status':status}

def export(pid,names,quantity,material,finish,notes,thin,eligible=False,origin=(0,0,0),category='custom'):
    target=Matrix.Translation(Vector(origin)*-1);part,steps=union(names,target);bm,info=inspect(part)
    zmin=info['boundsMm']['min'][2];shift=Matrix.Translation((0,0,-zmin));bm.transform(shift);bm.normal_update();path=STL/(pid+'.stl');write_stl(path,bm);bm.free()
    valid=info['closedManifold'] and info['signedVolumeMm3']>0 and not any(s['status']=='failed' for s in steps)
    record={'id':pid,'file':str(path.relative_to(OUT)),'quantity':quantity,'category':category,'sourceObjects':names,'sourcePartIds':sorted({objects[n].get('partId') for n in names}),'neutralPose':True,'units':'mm','scaleApplied':1,'assemblyToSTL':{'subtractPartOriginMm':list(origin),'thenTranslateZMm':-zmin},'mesh':info,'exactUnionOperations':steps,'materialTarget':material,'finishTarget':finish,'thinFeatures':thin,'notes':notes,'validClosedPositiveMesh':valid,'budgetaryInstantQuoteCandidate':bool(eligible and valid),'printReady':False,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if not valid:record['blockingMeshDefects']=[k for k in ['boundaryEdges','nonManifoldEdges','wireEdges','inconsistentWindingEdges','degenerateTriangles'] if info[k]]
    records.append(record);pending[pid]=part;return record,part

# Main shell: geometric union of only the actual integral custom case pieces.
case_names=['case.lower','USB cradle','USB clamp post -11','USB clamp post 11']+[n for n in objects.keys() if n.startswith(('case magnet boss ','case plate support '))]
usb=C['components']['usb_adapter'];rear=C['case']['depth']/2
case_thin=[feature('rear USB blind-pocket outer skin',ray_wall(objects['case.lower'],(usb['centerX']+7.5,rear+1,-13.6),(0,-1,0))),feature('support-post hex nut trap minimum radial wall',ray_wall(objects['case plate support (57.65, 49.625)'],(6,0,0),(-1,0,0)))]
# The second targeted ray uses local source coordinates in this helper, recorded analytically if needed.
case_thin[1]['mm']=C['mounting']['postDiameter']/2-C['mounting']['nutTrapAcrossFlats']/math.sqrt(3)
export('lower-case',case_names,1,'translucent/frosted polymer not selected','heavy frost; optical result unvalidated',['Integral support/cradle geometry is unioned from source components; purchased magnets, nuts, screws and feet excluded.','Rear USB wall and nut trap walls are below provider limits.','Cradle/post load capacity, trapped-nut assembly access and optical diffusion unvalidated.'],case_thin)
export('plate',['plate'],1,'rigid black material not selected','mirror/gloss black finish not quoted',['1.5 mm plate is a nominal drawing decision; polymer stiffness and switch clip retention are unvalidated.','Manufacturer switch installation drawing references a 1.5 mm metal frame; a plastic quote is not a substitute manufacturing approval.'],[feature('plate thickness',1.5,'wall','below-size-based-2mm-wall-minimum')],False)
for angle in [4,7]:
    names=['riser.'+str(angle)]+[n for n in objects.keys() if n.startswith('riser shear key ('+str(angle)+',')]
    export('riser-'+str(angle)+'deg',names,1,'navy polymer not selected','deep navy; rounded edges',['Magnet covers are separate STL lines; magnets and rubber feet excluded.','Magnet retention, slip resistance and rubber adhesion unvalidated.'],[feature('locating key height',C['riser']['shearKeys']['height'],'raised feature','at-provider-thinnest-feature-limit')],True)
knames=['knob','knob D-flat seat']+[n for n in objects.keys() if n.startswith('knob grip ')]
knob_notes=['White index is a separate STL; encoder and shaft excluded.','D-bore retention/push fit and fine grip reproduction unvalidated.','Actual flat seat inner face is +2.325 mm from shaft axis; effective opposite-arc-to-flat size is about 5.4 mm, not the planned 4.65 mm parameter. Do not manufacture without reconciling this mismatch.']
knob_thin=[feature('grip cylinder diameter before union',.24,'surface detail','below-provider-thinnest-feature-limit'),feature('approximate grip proudness after union',.02,'surface detail','supplier-detail-review-required')]
export('knob',knames,1,'navy polymer not selected','deep navy; fine grip detail',knob_notes,knob_thin,False,origin=(SPEC['layout']['encoder']['center'][0],SPEC['layout']['encoder']['center'][1],0))

# Hollow cap shells plus their actual mating bosses, kept as separate variants because legends differ.
interferences=[]
for key in SPEC['layout']['keys']:
    kid=key['id'];origin=(key['center'][0],key['center'][1],0);names=['cap.'+kid]+[n for n in objects.keys() if n.startswith('Socket boss '+kid+' ')]
    caprec,cap=export('cap-'+('2u-' if key['units']==2 else '1u-')+kid,names,1,'opaque deep navy polymer not selected','uniform shallow dish',['Hollow custom shell, unvalidated stem/crosssocket and stabilizer fit.','Legend openings are not a validated two-shot or separate-insert manufacturing process.'],[feature('nominal side wall',key['capDimensions']['wall']),feature('nominal boss-to-cross-tip radial wall',key['capDimensions']['stemSocket']['bossOuter']/2-key['capDimensions']['stemSocket']['crossLength']/2)],False,origin,'cap shell')
    insrec,ins=export('legend-'+kid,['insert.'+kid],1,'white translucent polymer not selected','white light-transmitting inlay',['Separate glyph islands may need a sprue, support fixture or a different process; none is invented here.','Light transmission, bonding and two-material fit unvalidated.'],[{'feature':'glyph stroke minimum','mm':None,'kind':'surface detail','status':'not-fully-measured; sub-0.8mm nominal glyph strokes and disconnected islands require redesign or process review'}],False,origin,'legend inlay')
    # Measurable source overlap between distinct printing materials is a DFM defect, not silently repaired.
    overlap=cap.copy();overlap.data=cap.data.copy();export_coll.objects.link(overlap)
    try:
        boolean(overlap,ins,'INTERSECT');ibm,ii=inspect(overlap);ibm.free();iv=ii['absoluteVolumeMm3']
    except Exception as ex:iv=None;caprec['intersectionError']=str(ex)
    bpy.data.objects.remove(overlap,do_unlink=True)
    caprec['navyWhiteSourceIntersectionVolumeMm3']=iv;insrec['navyWhiteSourceIntersectionVolumeMm3']=iv;interferences.append({'key':kid,'volumeMm3':iv})

# Additional custom assembly pieces that would otherwise be missing from a quote.
export('usb-retaining-clamp',['USB clamp -11'],2,'navy polymer not selected','plain',['One geometry used twice, mirrored by 180-degree in-plane rotation.','Bore breaks out through the short end of the clamp; mechanical retention and screw-head support unvalidated.'],[feature('thickness',1.0)],False,origin=tuple(objects['USB clamp -11'].location))
export('magnet-capture-ring',['case captive magnet cover -42'],6,'2 frosted + 4 navy pieces','plain',['Identical nominal annulus used for two case and four alternative-riser covers.','Captive closure assembly/service method unvalidated.'],[feature('thickness',.15),feature('radial wall',.3)],False,origin=(-42,C['riser']['magnetY'],0))
export('knob-index-white',['knob white index'],1,'white polymer or alternate marking process undecided','white index',['Existing geometry has no engineered separate-part attachment or pocket; source overlaps knob by about 0.02 mm.','Paint/printing instead of a separate physical insert is a design decision, not assumed in this export.'],[feature('thickness',.08)],False,origin=(SPEC['layout']['encoder']['center'][0],SPEC['layout']['encoder']['center'][1],0))

# Dimensions/volume round trip of the actual binary STLs, with quantized vertex welding for topology.
def roundtrip(path):
    # Independently audit actual serialized float32 triangles without Blender dependency updates.
    data=path.read_bytes();count=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*count
    lookup={};vs=[];fs=[];edges={};volume=0.;area=0.;deg=0
    for i in range(count):
        row=struct.unpack_from('<12fH',data,84+50*i);face=[];points=[]
        for j in range(3):
            point=tuple(row[3+j*3:6+j*3]);points.append(point)
            if point not in lookup:lookup[point]=len(vs);vs.append(point)
            face.append(lookup[point])
        fs.append(face)
        a,b,c=map(Vector,points);ar=(b-a).cross(c-a).length/2;area+=ar;deg+=ar<1e-10;volume+=a.dot(b.cross(c))/6
        for u,v in zip(face,face[1:]+face[:1]):
            key=tuple(sorted((u,v)));edges.setdefault(key,[]).append(1 if u<v else -1)
    adj=[set() for v in vs]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    todo=set(range(len(vs)));components=[]
    while todo:
        root=todo.pop();stack=[root];component={root}
        while stack:
            for v in adj[stack.pop()]:
                if v in todo:todo.remove(v);component.add(v);stack.append(v)
        components.append({'vertices':len(component)})
    nonmanifold=sum(len(x)!=2 for x in edges.values());winding=sum(len(x)==2 and sum(x)!=0 for x in edges.values());bounds={'min':[min(v[i] for v in vs) for i in range(3)],'max':[max(v[i] for v in vs) for i in range(3)]}
    return {'dimensionsMm':[bounds['max'][i]-bounds['min'][i] for i in range(3)],'boundsMm':bounds,'absoluteVolumeMm3':abs(volume),'signedVolumeMm3':volume,'surfaceAreaMm2':area,'vertices':len(vs),'triangles':count,'boundaryEdges':sum(len(x)==1 for x in edges.values()),'nonManifoldEdges':nonmanifold,'inconsistentWindingEdges':winding,'degenerateTriangles':deg,'connectedComponents':components,'closedManifold':nonmanifold==0 and winding==0 and deg==0 and volume>0,'method':'Exact float32 vertex welding; each edge has two opposite incidences; no tolerance welding'}
for rec in records:
    rt=roundtrip(OUT/rec['file']);rec['stlRoundtrip']=rt
    same=all(abs(a-b)<.0001 for a,b in zip(rt['dimensionsMm'],rec['mesh']['dimensionsMm'])) and abs(rt['absoluteVolumeMm3']-rec['mesh']['absoluteVolumeMm3'])<max(.001,rec['mesh']['absoluteVolumeMm3']*.00001)
    rec['stlRoundtripDimensionVolumePass']=same
    if not same or not rt['closedManifold']:
        rec['budgetaryInstantQuoteCandidate']=False;rec['validClosedPositiveMesh']=False
        rec['blockingMeshDefects']={'source':{k:rec['mesh'][k] for k in ['boundaryEdges','nonManifoldEdges','inconsistentWindingEdges','degenerateTriangles']},'serializedSTL':{k:rt[k] for k in ['boundaryEdges','nonManifoldEdges','inconsistentWindingEdges','degenerateTriangles']},'dimensionVolumeMatch':same}

manifest={'scope':'Local budgetary quote geometry only. Not print ready; no upload, message or order performed.','units':'mm','sourceSpecHash':SPEC['sourceSpecHash'],'geometryHash':SPEC['geometryHash'],'builtMeshHash':SRC['builtMeshHash'],'sourceNativeSHA256':native_hash,'generatedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'providerRules':{'origin':'Robu current industrial service guidance supplied by parent audit','wallThicknessMustExceedMm':1.2,'thinnestPartAtLeastMm':.8,'sizeBasedMinimumWallsMm':[{'maximumPartSizeMm':50,'minimumWallMm':1.0},{'maximumPartSizeMm':100,'minimumWallMm':1.5},{'maximumPartSizeMm':200,'minimumWallMm':2.0}],'smallestDetailMm':.8,'minimumHoleMm':1.0,'staticClearanceMm':.2,'movingClearanceMm':.5,'notAutomaticallyValidated':True},'conditioning':['Neutral mechanical coordinates, excluding the assembly tilt and motion.','Integral source submeshes consolidated with exact Boolean union on transient copies.','Face normals recalculated on transient copies; no offsets, scaling, thickening, voxel remesh, supports or sprues.','Each output translated to Z-min=0; XY remains part-local as documented.'],'parts':records,'navyWhiteSourceInterferences':interferences,'sourceNativeUnchanged':hashlib.sha256(NATIVE.read_bytes()).hexdigest()==native_hash,'sourceMediaManifestUnchanged':hashlib.sha256((ROOT/'design/fit-v1/media-manifest.json').read_bytes()).hexdigest()==media_hash}
(OUT/'quote-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
with (OUT/'quote-parts.csv').open('w',newline='') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['id','file','quantity','width_mm','depth_mm','height_mm','volume_mm3','closed_manifold','components','instant_budgetary_candidate','print_ready','thin_features'])
    for r in records:w.writerow([r['id'],r['file'],r['quantity'],*r['mesh']['dimensionsMm'],r['mesh']['absoluteVolumeMm3'],r['validClosedPositiveMesh'],len(r['mesh']['connectedComponents']),r['budgetaryInstantQuoteCandidate'],False,json.dumps(r['thinFeatures'])])
assert manifest['sourceNativeUnchanged'] and manifest['sourceMediaManifestUnchanged']
print('QUOTE_EXPORT_COMPLETE',json.dumps({'files':len(records),'physicalPieceQuantity':sum(r['quantity'] for r in records),'closedMeshes':sum(r['validClosedPositiveMesh'] for r in records),'candidateIds':[r['id'] for r in records if r['budgetaryInstantQuoteCandidate']],'sourceUnchanged':True}))
