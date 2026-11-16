using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using System.Windows.Media.Animation;
using System.Windows.Threading;

namespace AgenticStudio {
    public class OperationsScene : Grid {
        readonly Viewport3D viewport = new Viewport3D();
        readonly Canvas labels = new Canvas();
        readonly Model3DGroup world = new Model3DGroup();
        Model3DGroup meshTarget;
        readonly Dictionary<string, Button> stations = new Dictionary<string, Button>();
        readonly Dictionary<string, Point3D> positions = new Dictionary<string, Point3D>();
        readonly OrthographicCamera camera = new OrthographicCamera(new Point3D(19,24,30), new Vector3D(-19,-23,-28), new Vector3D(0,1,0), 25);
        readonly List<AgentActor> actors = new List<AgentActor>();
        readonly DispatcherTimer animation = new DispatcherTimer(DispatcherPriority.Background);
        readonly Stopwatch clock = new Stopwatch();
        readonly Dictionary<string,string> agentStates = new Dictionary<string,string>();
        AxisAngleRotation3D crystalRotation;
        Point lastPointer;
        Vector3D pan;
        double yaw=34, pitch=38, zoom=1, previousFrame,sceneTime;
        bool dragging, panning;
        public bool MotionEnabled {get;private set;}
        public bool MoveMode {get;private set;}
        public double ZoomPercent {get{return zoom*100;}}
        public string ViewDescription {get{return String.Format("VIEW {0:0}%  /  ORBIT {1:0}°  /  TILT {2:0}°  /  PAN {5:0.0}  /  MOTION {3}  /  DRAG {4}",zoom*100,(yaw%360+360)%360,pitch,MotionEnabled?"ON":"OFF",MoveMode?"MOVE":"ROTATE",pan.Length);}}
        public event Action ViewChanged;
        public event Action<string> StationSelected;
        sealed class AgentActor {
            public string Station,Agent,State="pending";
            public readonly ScaleTransform3D VisibilityScale=new ScaleTransform3D(1.2,1.2,1.2);
            public double HomeX,HomeZ,WorkX,WorkZ,BaseY,X,Z,Phase,Heading;
            public TranslateTransform3D Position=new TranslateTransform3D(),Bob=new TranslateTransform3D();
            public AxisAngleRotation3D Facing=new AxisAngleRotation3D(new Vector3D(0,1,0),0),Head=new AxisAngleRotation3D(new Vector3D(0,1,0),0),LeftArm=new AxisAngleRotation3D(new Vector3D(1,0,0),0),RightArm=new AxisAngleRotation3D(new Vector3D(1,0,0),0),LeftLeg=new AxisAngleRotation3D(new Vector3D(1,0,0),0),RightLeg=new AxisAngleRotation3D(new Vector3D(1,0,0),0);
            public SolidColorBrush Indicator=new SolidColorBrush();
            public List<TranslateTransform3D> Packets=new List<TranslateTransform3D>();
            public List<ScaleTransform3D> PacketScales=new List<ScaleTransform3D>();
        }
        static readonly Color Ivory = C("#c8c4b7"), White = C("#e5e0d3"), Steel = C("#555d5c"), Dark = C("#272f30"), Gold = C("#e5bc6c"), Mint = C("#92c4b2");
        public OperationsScene() {
            Focusable=true;FocusVisualStyle=null;IsManipulationEnabled=true;MotionEnabled=true;
            System.Windows.Automation.AutomationProperties.SetAutomationId(this,"OperationsScene");
            System.Windows.Automation.AutomationProperties.SetName(this,"Interactive 3D operations room");
            ClipToBounds = true;
            Background = new RadialGradientBrush(C("#1b2324"), C("#090d10"));
            viewport.Camera = camera;
            world.Children.Add(new AmbientLight(C("#7e8584")));
            world.Children.Add(new DirectionalLight(C("#ffedcf"), new Vector3D(-3,-6,-4)));
            world.Children.Add(new DirectionalLight(C("#778d9d"), new Vector3D(3,-2,1)));
            var visual = new ModelVisual3D(); visual.Content = world; viewport.Children.Add(visual);
            Children.Add(viewport); Children.Add(labels);
            // The floor, corridors, furniture, robots and hub are native WPF 3D meshes.
            Cylinder(0,-0.9,1,13.5,.18,64,C("#0c1215"));
            Corridor(-6,0,0,0); Corridor(0,-6,0,0); Corridor(6,0,0,0); Corridor(4.5,6.2,0,0); Corridor(-4.5,6.2,0,0);
            Room(-6,0,0); Room(0,-6,1); Room(6,0,2); Room(4.5,6.2,3); Room(-4.5,6.2,4);
            Hub();
            Robots("dock",-6,1.35,-6.95,-.55,0);
            Robots("planning",1.5,1.2,1.15,1.25,.55);
            Robots("research",1.25,-5.3,.8,-6.55,0);
            Robots("review",7.45,.85,6.8,-.55,0);
            Robots("work",4.15,7.75,4.2,7.4,0);
            Robots("complete",-4.7,7.7,-4.5,7.55,0);
            AddLabel("dock", "01", "Dock", new Point3D(-6,1.2,1.4));
            AddLabel("planning", "02", "Planning", new Point3D(0,4.5,0));
            AddLabel("research", "03", "Research", new Point3D(0,1.5,-6));
            AddLabel("review", "04", "Review", new Point3D(6,1.1,1.4));
            AddLabel("work", "05", "Work", new Point3D(4.5,3,6.2));
            AddLabel("complete", "06", "Complete", new Point3D(-4.5,.9,7.7));
            SizeChanged += delegate { UpdateCamera(); };
            Loaded += delegate {UpdateCamera();clock.Start();previousFrame=clock.Elapsed.TotalSeconds;animation.Start();};
            Unloaded += delegate {animation.Stop();clock.Stop();};
            animation.Interval=TimeSpan.FromMilliseconds(33);animation.Tick+=Animate;
            LostMouseCapture+=delegate{dragging=false;Cursor=Cursors.Arrow;};
            UpdateCamera();
        }
        static Color C(string hex) { return (Color)ColorConverter.ConvertFromString(hex); }
        Material Mat(Color color, bool glow) {
            var group = new MaterialGroup();
            group.Children.Add(new DiffuseMaterial(new SolidColorBrush(color)));
            group.Children.Add(new SpecularMaterial(new SolidColorBrush(Color.FromArgb(65,255,255,255)), 35));
            if(glow) group.Children.Add(new EmissiveMaterial(new SolidColorBrush(Color.FromArgb(160,color.R,color.G,color.B))));
            return group;
        }
        void Mesh(Point3D[] points, int[] indices, Color color, bool glow) {
            var mesh = new MeshGeometry3D(); foreach(var p in points) mesh.Positions.Add(p); foreach(var i in indices) mesh.TriangleIndices.Add(i);mesh.Freeze();
            var material = Mat(color, glow); var model = new GeometryModel3D(mesh, material); model.BackMaterial = material; (meshTarget??world).Children.Add(model);
        }
        void Box(double x,double y,double z,double w,double h,double d,Color color) { Box(x,y,z,w,h,d,color,0,false); }
        void Box(double x,double y,double z,double w,double h,double d,Color color,double angle,bool glow) {
            Point3D[] points = new Point3D[8]; double a=angle*Math.PI/180; int i=0;
            for(int yy=0;yy<2;yy++) for(int zz=0;zz<2;zz++) for(int xx=0;xx<2;xx++) {
                double px=(xx-.5)*w, pz=(zz-.5)*d;
                points[i++]=new Point3D(x+px*Math.Cos(a)+pz*Math.Sin(a),y+(yy-.5)*h,z-px*Math.Sin(a)+pz*Math.Cos(a));
            }
            Mesh(points,new[]{0,2,3,0,3,1,4,5,7,4,7,6,0,1,5,0,5,4,2,6,7,2,7,3,0,4,6,0,6,2,1,3,7,1,7,5},color,glow);
        }
        void Cylinder(double x,double y,double z,double radius,double h,int segments,Color color) {Cylinder(x,y,z,radius,h,segments,color,false);}
        void Cylinder(double x,double y,double z,double radius,double h,int segments,Color color,bool glow) {
            var ps=new List<Point3D>(); var ix=new List<int>();
            ps.Add(new Point3D(x,y-h/2,z));ps.Add(new Point3D(x,y+h/2,z));
            for(int i=0;i<segments;i++) {double a=i*Math.PI*2/segments;ps.Add(new Point3D(x+radius*Math.Cos(a),y-h/2,z+radius*Math.Sin(a)));ps.Add(new Point3D(x+radius*Math.Cos(a),y+h/2,z+radius*Math.Sin(a)));}
            for(int i=0;i<segments;i++){int p=2+i*2,n=2+(i+1)%segments*2;ix.AddRange(new[]{0,n,p,1,p+1,n+1,p,n,n+1,p,n+1,p+1});}
            Mesh(ps.ToArray(),ix.ToArray(),color,glow);
        }
        void Bar(double x1,double z1,double x2,double z2,double y,double w,double h,Color color) {
            double dx=x2-x1,dz=z2-z1; Box((x1+x2)/2,y,(z1+z2)/2,Math.Sqrt(dx*dx+dz*dz),h,w,color,-Math.Atan2(dz,dx)*180/Math.PI,false);
        }
        void Corridor(double x1,double z1,double x2,double z2) {
            Bar(x1,z1,x2,z2,-.1,1.65,.32,Steel);Bar(x1,z1,x2,z2,.08,1.45,.1,Ivory);
            double dx=x2-x1,dz=z2-z1,l=Math.Sqrt(dx*dx+dz*dz),nx=-dz/l*.66,nz=dx/l*.66;
            Bar(x1+nx,z1+nz,x2+nx,z2+nz,.55,.08,.08,White);Bar(x1-nx,z1-nz,x2-nx,z2-nz,.55,.08,.08,White);
            for(int i=1;i<5;i++){double t=i/5.0;Box(x1+dx*t+nx,.3,z1+dz*t+nz,.12,.65,.12,Steel);Box(x1+dx*t-nx,.3,z1+dz*t-nz,.12,.65,.12,Steel);}
        }
        void Room(double x,double z,int type) {
            Cylinder(x,-.34,z,3.22,.54,10,Dark); Cylinder(x,-.04,z,3.28,.13,10,Ivory); Cylinder(x,.06,z,3.08,.1,10,C("#666960"));
            // Tile grid and layered exterior trim.
            for(int i=-3;i<=3;i++){
                double p=i*.7, half=Math.Sqrt(Math.Max(0,8.1-p*p));
                Box(x+p,.122,z,.018,.012,half*2,C("#454b45"));Box(x,.123,z+p,half*2,.012,.018,C("#454b45"));
            }
            for(int i=0;i<10;i++){
                double a=(i+.5)*Math.PI*2/10, a1=i*Math.PI*2/10,a2=(i+1)*Math.PI*2/10;
                double x1=x+3.02*Math.Cos(a1),z1=z+3.02*Math.Sin(a1),x2=x+3.02*Math.Cos(a2),z2=z+3.02*Math.Sin(a2);
                bool back=Math.Sin(a)<-.15 || Math.Cos(a)<-.8;
                double height=back?2.55:.55;
                Bar(x1,z1,x2,z2,.18+height/2,.16,height,Ivory);
                Bar(x1,z1,x2,z2,.19+height,.22,.1,White);
                Bar(x1,z1,x2,z2,-.22,.12,.13,Steel);
                Box(x1,.2+height/2,z1,.16,height+.14,.19,White);
                if(back){
                    double px=x+2.84*Math.Cos(a),pz=z+2.84*Math.Sin(a),angle=-a*180/Math.PI+90;
                    Box(px,1.6,pz,.5,.92,.1,Dark,angle,false);
                    for(int row=0;row<4;row++) Box(px,1.4+row*.14,pz+.06,.32,.026,.13,row==1?Mint:Steel,angle,row==1);
                }
            }
            // Modular desks and terminal displays.
            Workstation(x-.95,z-1.35,0); Workstation(x+.8,z-1.35,0);
            ServerRack(x-2.1,z-.55); Plant(x+2.05,z-.8);
            if(type==0){ Workstation(x,z+.65,0); }
            if(type==1){ Cylinder(x,.55,z+.3,.85,.8,16,Dark);Cylinder(x,1,z+.3,.97,.12,24,Gold,true);Cylinder(x,1.12,z+.3,.68,.12,24,Ivory); Hologram(x,2,z+.3); }
            if(type==2){ Cylinder(x,.43,z+.6,.92,.48,16,Ivory);Cylinder(x,.72,z+.6,.85,.1,24,Gold,true);Cylinder(x,1.05,z+.6,.48,.55,8,Dark); }
            if(type==3){ Box(x,.85,z+.4,1.8,.14,1.1,White);Box(x,.47,z+.4,.25,.7,.55,Steel);Box(x+1.65,.85,z+.1,.24,1.4,.25,Gold);Box(x+1.4,1.5,z+.1,.8,.2,.25,Steel); }
            if(type==4){ Workstation(x,z+.6,0);Plant(x+1.7,z+1.1); }
            // Front edge light bars.
            for(int i=0;i<3;i++)Box(x-1.3+i*1.2,-.23,z+2.65,.5,.055,.08,White,0,true);
        }
        void Workstation(double x,double z,double a) {
            Box(x,.88,z,1.25,.13,.74,White);Box(x-.43,.49,z,.11,.7,.6,Steel);Box(x+.43,.49,z,.11,.7,.6,Steel);
            Box(x,1.19,z-.13,.1,.44,.1,Steel);Box(x,1.43,z-.16,.77,.47,.09,Dark);
            Box(x,1.43,z-.1,.65,.34,.018,C("#263f40"),0,true);
            for(int i=0;i<3;i++) Box(x-.15,1.34+i*.08,z-.083,.28+i*.06,.017,.012,Mint,0,true);
            Box(x,.967,z+.16,.43,.03,.19,C("#777e73"));Cylinder(x,.44,z+.65,.25,.08,10,Steel);Box(x,.71,z+.8,.43,.47,.09,Dark);Cylinder(x,.23,z+.65,.05,.4,8,Steel);
        }
        void ServerRack(double x,double z) {
            Box(x,.96,z,.55,1.65,.53,Steel);Box(x,.96,z+.28,.44,1.5,.03,Dark);
            for(int i=0;i<6;i++){Box(x, .36+i*.22,z+.31,.34,.11,.03,C("#68736e"));Box(x-.11,.36+i*.22,z+.34,.035,.035,.02,Mint,0,true);}
        }
        void Plant(double x,double z) {
            Cylinder(x,.35,z,.24,.4,7,Ivory);
            for(int i=0;i<7;i++){double a=i*2.4;Box(x+Math.Cos(a)*.12,.74+i*.035,z+Math.Sin(a)*.13,.12,.6,.19,C("#6a825d"),i*37,false);}
        }
        void Part(Model3DGroup parent,Transform3D transform,Action geometry) {
            var previous=meshTarget;var group=new Model3DGroup{Transform=transform};parent.Children.Add(group);meshTarget=group;geometry();meshTarget=previous;
        }
        void Robots(string station,double x,double z,double workX,double workZ,double baseY){
            var profiles=Data.Rows(Data.Read(Path.Combine(Data.Root,"config","agent-team.json")),"agents").Where(a=>Data.Get(a,"station")==station).ToList();
            for(int i=0;i<profiles.Count;i++){double offset=(i-(profiles.Count-1)/2.0)*.72;Robot(Data.Get(profiles[i],"agent"),station,x+offset,z+(i%2==0?-.18:.18),workX,workZ,baseY);}
        }
        void Robot(string assigned,string station,double x,double z,double workX,double workZ,double baseY) {
            var actor=new AgentActor{Agent=assigned,Station=station,HomeX=x,HomeZ=z,WorkX=workX,WorkZ=workZ,BaseY=baseY,X=x,Z=z,Phase=actors.Count*1.37};actors.Add(actor);
            var root=new Model3DGroup();var transform=new Transform3DGroup();transform.Children.Add(actor.VisibilityScale);transform.Children.Add(new RotateTransform3D(actor.Facing));transform.Children.Add(actor.Position);root.Transform=transform;world.Children.Add(root);
            var body=new Model3DGroup{Transform=actor.Bob};root.Children.Add(body);var previous=meshTarget;meshTarget=body;
            Box(0,.7,0,.42,.49,.33,Ivory);Box(0,.71,.18,.25,.2,.03,Dark);Box(0,.66,.202,.17,.025,.014,Gold,0,true);
            Part(body,new RotateTransform3D(actor.Head,new Point3D(0,1.04,0)),delegate{
                Box(0,1.12,0,.5,.36,.4,White);Box(0,1.12,.215,.41,.21,.025,Dark);
                foreach(double eye in new[]{-.105,.105}){
                    Box(eye,1.14,.238,.07,.065,.018,Mint,0,true);var model=(GeometryModel3D)meshTarget.Children[meshTarget.Children.Count-1];var material=new MaterialGroup();material.Children.Add(new DiffuseMaterial(actor.Indicator));material.Children.Add(new EmissiveMaterial(actor.Indicator));model.Material=material;model.BackMaterial=material;
                }
                Cylinder(0,1.36,0,.035,.16,8,Steel);Cylinder(0,1.46,0,.055,.06,8,Gold,true);
            });
            Part(body,new RotateTransform3D(actor.LeftArm,new Point3D(-.3,.89,0)),delegate{Box(-.3,.7,0,.13,.42,.16,Steel);Box(-.3,.46,0,.15,.13,.18,Ivory);});
            Part(body,new RotateTransform3D(actor.RightArm,new Point3D(.3,.89,0)),delegate{Box(.3,.7,0,.13,.42,.16,Steel);Box(.3,.46,0,.15,.13,.18,Ivory);});
            Part(root,new RotateTransform3D(actor.LeftLeg,new Point3D(-.13,.47,0)),delegate{Box(-.13,.3,0,.14,.32,.17,Steel);Box(-.13,.105,.05,.2,.12,.3,Ivory);});
            Part(root,new RotateTransform3D(actor.RightLeg,new Point3D(.13,.47,0)),delegate{Box(.13,.3,0,.14,.32,.17,Steel);Box(.13,.105,.05,.2,.12,.3,Ivory);});
            meshTarget=previous;actor.Position.OffsetX=x;actor.Position.OffsetZ=z;actor.Position.OffsetY=baseY;
            for(int i=0;i<3;i++){
                var scale=new ScaleTransform3D(0,0,0);var packet=new TranslateTransform3D();var packetTransform=new Transform3DGroup();packetTransform.Children.Add(scale);packetTransform.Children.Add(packet);Part(world,packetTransform,delegate{Box(0,0,0,.11,.11,.11,Mint,0,true);});actor.Packets.Add(packet);actor.PacketScales.Add(scale);
            }
        }
        void Hologram(double x,double y,double z){
            for(int i=0;i<3;i++) Cylinder(x,y+i*.24,z,.46-i*.08,.018,12,Gold,true);
            Box(x,y+.25,z,.02,.8,.02,Gold,0,true);Box(x,y+.25,z,.55,.02,.02,Gold,0,true);
        }
        void Hub() {
            Cylinder(0,.06,0,2.35,.62,12,Dark);Cylinder(0,.4,0,2.4,.14,12,Ivory);Cylinder(0,.53,0,2.03,.13,32,Gold,true);Cylinder(0,.65,0,1.8,.15,32,Dark);Cylinder(0,.75,0,1.45,.12,32,Ivory);Cylinder(0,.83,0,1.22,.05,32,Gold,true);
            for(int i=0;i<5;i++) {double a=(i*72+15)*Math.PI/180;if(Math.Sin(a)>.4)continue;double x=2*Math.Cos(a),z=2*Math.Sin(a);Box(x,2.3,z,.27,3.8,.3,Ivory);Box(x+.02,2.3,z+.17,.08,3.4,.05,Gold,0,true);}
            // Open crown around the rotating crystal.
            for(int i=0;i<16;i++){double a=i*Math.PI*2/16,b=(i+1)*Math.PI*2/16;Bar(2.1*Math.Cos(a),2.1*Math.Sin(a),2.1*Math.Cos(b),2.1*Math.Sin(b),4.1,.24,.24,Steel);}
            double y=2.15;
            var crystal=new MeshGeometry3D();
            crystal.Positions=new Point3DCollection(new[]{new Point3D(0,y+1.15,0),new Point3D(-.72,y,0),new Point3D(0,y,-.72),new Point3D(.72,y,0),new Point3D(0,y,.72),new Point3D(0,y-.95,0)});
            crystal.TriangleIndices=new Int32Collection(new[]{0,1,2,0,2,3,0,3,4,0,4,1,5,2,1,5,3,2,5,4,3,5,1,4});
            var material=Mat(Gold,true);var model=new GeometryModel3D(crystal,material);model.BackMaterial=material;
            crystalRotation=new AxisAngleRotation3D(new Vector3D(0,1,0),0);model.Transform=new RotateTransform3D(crystalRotation);world.Children.Add(model);
        }
        void AddLabel(string id,string number,string title,Point3D position) {
            var text=new StackPanel();text.Children.Add(new TextBlock{Text=number+"   "+title,Foreground=new SolidColorBrush(C("#ddd9ca")),FontSize=11,FontWeight=FontWeights.SemiBold});text.Children.Add(new TextBlock{Text="0 tasks",Foreground=new SolidColorBrush(C("#8e978f")),FontSize=9,Margin=new Thickness(20,4,0,0)});
            var b=new Button{Content=text,Background=new SolidColorBrush(C("#161d20")),Foreground=Brushes.White,BorderBrush=new SolidColorBrush(C("#424842")),BorderThickness=new Thickness(1),Padding=new Thickness(11,8,13,8),Cursor=System.Windows.Input.Cursors.Hand,Tag=id};
            b.Click+=delegate {if(StationSelected!=null)StationSelected(id);};stations[id]=b;positions[id]=position;labels.Children.Add(b);
        }
        public void UpdateCounts(Dictionary<string,int> counts,string selected) {
            foreach(var pair in stations){var content=(StackPanel)pair.Value.Content;var subtitle=(TextBlock)content.Children[1];string status=agentStates.ContainsKey(pair.Key)?agentStates[pair.Key]:"pending";subtitle.Text=(counts.ContainsKey(pair.Key)?counts[pair.Key]:0)+" left · "+(status=="running"?"Working":status=="failed"?"Needs input":status=="done"?"Complete":"Standby");subtitle.Foreground=new SolidColorBrush(status=="running"?Mint:status=="failed"?Gold:C("#8e978f"));pair.Value.BorderBrush=new SolidColorBrush(C(pair.Key==selected?"#c2a36c":status=="running"?"#71a99c":"#424842"));pair.Value.Background=new SolidColorBrush(C(pair.Key==selected?"#322b20":"#161d20"));}
        }
        public void UpdateAgentStates(Dictionary<string,string> states) {
            agentStates.Clear();foreach(var pair in states)agentStates[pair.Key]=pair.Value;
            foreach(var actor in actors){actor.State=states.ContainsKey(actor.Station)?states[actor.Station]:"pending";actor.Indicator.Color=actor.State=="failed"?Gold:actor.State=="done"?Color.FromRgb(137,187,143):Mint;if(actor.State!="running")foreach(var scale in actor.PacketScales){scale.ScaleX=0;scale.ScaleY=0;scale.ScaleZ=0;}}
        }
        public void UpdateRoleStates(Dictionary<string,string> states){
            foreach(var actor in actors){bool included=states.ContainsKey(actor.Agent);actor.VisibilityScale.ScaleX=actor.VisibilityScale.ScaleY=actor.VisibilityScale.ScaleZ=included?1.2:0;actor.State=included?states[actor.Agent]:"inactive";actor.Indicator.Color=actor.State=="failed"?Gold:actor.State=="done"?Color.FromRgb(137,187,143):Mint;if(actor.State!="running")foreach(var scale in actor.PacketScales){scale.ScaleX=scale.ScaleY=scale.ScaleZ=0;}}
        }
        void Animate(object sender,EventArgs args) {
            double time=clock.Elapsed.TotalSeconds,dt=Math.Min(.1,Math.Max(0,time-previousFrame));previousFrame=time;
            var window=Window.GetWindow(this);if(!MotionEnabled||!IsVisible||(window!=null&&window.WindowState==WindowState.Minimized))return;
            sceneTime+=dt;AnimateActors(sceneTime,dt);
        }
        void AnimateActors(double time,double dt) {
            if(crystalRotation!=null)crystalRotation.Angle=time*13%360;
            foreach(var a in actors){
                if(a.State=="inactive")continue;
                double t=time+a.Phase;bool work=a.State=="running",blocked=a.State=="failed",done=a.State=="done";
                double targetX=work?a.WorkX:blocked||done?a.HomeX:a.HomeX+Math.Sin(t*.55)*.48;
                double targetZ=work?a.WorkZ:blocked||done?a.HomeZ:a.HomeZ+Math.Sin(t*.55)*Math.Cos(t*.55)*.46;
                double dx=targetX-a.X,dz=targetZ-a.Z,distance=Math.Sqrt(dx*dx+dz*dz);bool walking=distance>.035;
                double step=Math.Min(1,dt*(work?2.4:3));a.X+=dx*step;a.Z+=dz*step;
                double heading=walking?Math.Atan2(dx,dz)*180/Math.PI:work?180:blocked?15:Math.Sin(t*.5)*20;
                double turn=(heading-a.Heading+540)%360-180;a.Heading+=turn*Math.Min(1,dt*5);a.Facing.Angle=a.Heading;
                a.Position.OffsetX=a.X;a.Position.OffsetZ=a.Z;a.Position.OffsetY=a.BaseY;
                bool typing=work&&distance<.18;
                double gait=Math.Sin(t*8);a.LeftLeg.Angle=walking?gait*23:0;a.RightLeg.Angle=walking?-gait*23:0;
                a.Bob.OffsetY=walking?Math.Abs(Math.Sin(t*8))*.055:Math.Sin(t*2)*.018;
                a.LeftArm.Angle=typing?-62+Math.Sin(t*11)*13:walking?-gait*25:blocked?-18+Math.Sin(t)*8:Math.Sin(t*1.7)*7;
                a.RightArm.Angle=typing?-62+Math.Sin(t*11+Math.PI)*13:walking?gait*25:Math.Sin(t*1.7+1)*7;
                a.Head.Angle=typing?Math.Sin(t*1.6)*9:Math.Sin(t*.9)*28;
                bool blink=t%4.4<.12;a.Indicator.Color=blink?Color.FromRgb(40,60,58):blocked?Gold:done?Color.FromRgb(137,187,143):Mint;
                for(int i=0;i<a.Packets.Count;i++){
                    var scale=a.PacketScales[i];double visible=work?1:0;scale.ScaleX=visible;scale.ScaleY=visible;scale.ScaleZ=visible;
                    if(work){double f=(t*.22+i/3.0)%1;a.Packets[i].OffsetX=a.HomeX*f;a.Packets[i].OffsetZ=a.HomeZ*f;a.Packets[i].OffsetY=.52+Math.Sin(f*Math.PI)*.18;}
                }
            }
        }
        public void SetZoom(double value){zoom=Math.Max(.55,Math.Min(1.9,value));UpdateCamera();}
        public void Rotate(double horizontal,double vertical){yaw=(yaw+horizontal)%360;pitch=Math.Max(20,Math.Min(72,pitch+vertical));UpdateCamera();}
        public void Move(double horizontal,double vertical){
            var f=camera.LookDirection;f.Normalize();var r=Vector3D.CrossProduct(f,camera.UpDirection);r.Normalize();var u=Vector3D.CrossProduct(r,f);u.Normalize();double scale=camera.Width/Math.Max(1,ActualWidth);pan+=(-r*horizontal+u*vertical)*scale;
            if(pan.Length>15){pan.Normalize();pan*=15;}UpdateCamera();
        }
        public void ResetView(){yaw=34;pitch=38;zoom=1;pan=new Vector3D();UpdateCamera();}
        public void ToggleMotion(){MotionEnabled=!MotionEnabled;if(ViewChanged!=null)ViewChanged();}
        public void SetMoveMode(bool value){MoveMode=value;if(ViewChanged!=null)ViewChanged();}
        void UpdateCamera(){
            double y=yaw*Math.PI/180,p=pitch*Math.PI/180;var target=new Point3D(0,1,1.5)+pan;
            camera.Position=target+new Vector3D(42*Math.Sin(y)*Math.Cos(p),42*Math.Sin(p),42*Math.Cos(y)*Math.Cos(p));camera.LookDirection=target-camera.Position;
            double width=Math.Max(25,17*ActualWidth/Math.Max(1,ActualHeight));camera.Width=width/zoom;PositionLabels();if(ViewChanged!=null)ViewChanged();
        }
        bool IsButton(object source){var item=source as DependencyObject;while(item!=null){if(item is ButtonBase)return true;if(!(item is Visual)&&!(item is Visual3D))return false;item=VisualTreeHelper.GetParent(item);}return false;}
        protected override void OnMouseDown(MouseButtonEventArgs e){
            base.OnMouseDown(e);if(IsButton(e.OriginalSource))return;
            if(e.ChangedButton==MouseButton.Left&&e.ClickCount==2){ResetView();e.Handled=true;return;}
            if(e.ChangedButton!=MouseButton.Left&&e.ChangedButton!=MouseButton.Right&&e.ChangedButton!=MouseButton.Middle)return;
            Focus();dragging=true;panning=MoveMode||e.ChangedButton!=MouseButton.Left||(Keyboard.Modifiers&ModifierKeys.Shift)!=0;lastPointer=e.GetPosition(this);CaptureMouse();Cursor=panning?Cursors.SizeAll:Cursors.Hand;e.Handled=true;
        }
        protected override void OnMouseMove(MouseEventArgs e){base.OnMouseMove(e);if(!dragging)return;var point=e.GetPosition(this);var delta=point-lastPointer;lastPointer=point;if(panning)Move(delta.X,delta.Y);else Rotate(delta.X*.38,delta.Y*.24);e.Handled=true;}
        protected override void OnMouseUp(MouseButtonEventArgs e){base.OnMouseUp(e);if(!dragging)return;dragging=false;ReleaseMouseCapture();Cursor=Cursors.Arrow;e.Handled=true;}
        protected override void OnMouseWheel(MouseWheelEventArgs e){base.OnMouseWheel(e);Focus();SetZoom(zoom*Math.Pow(1.12,e.Delta/120.0));e.Handled=true;}
        protected override void OnKeyDown(KeyEventArgs e){
            base.OnKeyDown(e);bool shift=(Keyboard.Modifiers&ModifierKeys.Shift)!=0;
            switch(e.Key){case Key.Left:if(shift)Move(35,0);else Rotate(-8,0);break;case Key.Right:if(shift)Move(-35,0);else Rotate(8,0);break;case Key.Up:if(shift)Move(0,35);else Rotate(0,-5);break;case Key.Down:if(shift)Move(0,-35);else Rotate(0,5);break;case Key.Add:case Key.OemPlus:SetZoom(zoom*1.12);break;case Key.Subtract:case Key.OemMinus:SetZoom(zoom/1.12);break;case Key.R:ResetView();break;case Key.Space:ToggleMotion();break;case Key.Escape:if(dragging){dragging=false;ReleaseMouseCapture();Cursor=Cursors.Arrow;}break;default:return;}e.Handled=true;
        }
        protected override void OnManipulationStarting(ManipulationStartingEventArgs e){base.OnManipulationStarting(e);e.ManipulationContainer=this;e.Mode=ManipulationModes.Translate|ManipulationModes.Scale|ManipulationModes.Rotate;e.Handled=true;}
        protected override void OnManipulationDelta(ManipulationDeltaEventArgs e){base.OnManipulationDelta(e);Move(e.DeltaManipulation.Translation.X,e.DeltaManipulation.Translation.Y);Rotate(e.DeltaManipulation.Rotation,0);SetZoom(zoom*e.DeltaManipulation.Scale.X);e.Handled=true;}
        public static string SelfCheck(){
            var scene=new OperationsScene();scene.Measure(new Size(1000,700));scene.Arrange(new Rect(0,0,1000,700));scene.ResetView();var initial=scene.camera.Position;double labelX=Canvas.GetLeft(scene.stations["dock"]);
            scene.Rotate(55,10);if((scene.camera.Position-initial).Length<1||Math.Abs(Canvas.GetLeft(scene.stations["dock"])-labelX)<1)throw new Exception("Orbit or projected station labels did not move.");
            var beforePan=scene.camera.Position;scene.Move(120,70);if((scene.camera.Position-beforePan).Length<1)throw new Exception("Camera pan did not move.");scene.SetZoom(100);if(Math.Abs(scene.ZoomPercent-190)>.001)throw new Exception("Upper zoom limit failed.");scene.SetZoom(.01);if(Math.Abs(scene.ZoomPercent-55)>.001)throw new Exception("Lower zoom limit failed.");scene.ResetView();if((scene.camera.Position-initial).Length>.001||scene.ZoomPercent!=100)throw new Exception("Reset did not restore the initial view.");
            scene.AnimateActors(1,.1);double actorX=scene.actors[0].X;scene.AnimateActors(2,.1);if(Math.Abs(actorX-scene.actors[0].X)<.001)throw new Exception("Idle robot did not move.");
            scene.UpdateAgentStates(new Dictionary<string,string>{{"work","running"},{"dock","failed"}});
            for(int i=0;i<200;i++)scene.AnimateActors(3+i/30.0,1/30.0);
            var worker=scene.actors.Find(a=>a.Station=="work");if(Math.Abs(worker.X-worker.WorkX)>.02||Math.Abs(worker.Z-worker.WorkZ)>.02||worker.LeftArm.Angle>-40||worker.PacketScales[0].ScaleX!=1)throw new Exception("Running robot did not arrive, type, and send activity packets.");
            if(scene.actors.Find(a=>a.Station=="dock").Indicator.Color!=Gold)throw new Exception("Blocked status did not reach the robot indicator.");
            foreach(var actor in scene.actors)if(actor.Station!="work"&&actor.PacketScales[0].ScaleX!=0)throw new Exception("Idle station displayed work packets.");
            scene.UpdateAgentStates(new Dictionary<string,string>{{"work","done"}});if(worker.PacketScales[0].ScaleX!=0)throw new Exception("Work packets persisted after completion.");
            if(scene.actors.Count!=18||scene.actors.Select(a=>a.Agent).Distinct().Count()!=18)throw new Exception("Expected one robot per assigned role.");
            scene.UpdateRoleStates(new Dictionary<string,string>{{"blog-writing-agent","running"},{"affiliate-agent","pending"}});
            if(scene.actors.Count(a=>a.State=="running")!=1||scene.actors.Find(a=>a.Agent=="content-agent").VisibilityScale.ScaleX!=0||scene.actors.Find(a=>a.Agent=="affiliate-agent").State!="pending")throw new Exception("Role-specific motion or optional robot visibility failed.");
            scene.ToggleMotion();double angle=scene.crystalRotation.Angle;scene.Animate(null,EventArgs.Empty);if(scene.crystalRotation.Angle!=angle||scene.MotionEnabled)throw new Exception("Motion pause failed.");scene.ToggleMotion();if(!scene.MotionEnabled)throw new Exception("Motion resume failed.");
            return "PASS: 18 distinct role robots, per-role state/visibility, camera orbit/pan, projected station labels, zoom limits/reset, idle robot motion, running walk-to-desk/typing, blocked indicators, queue-bound work packets, completion transitions, and motion pause/resume. No job files were changed.";
        }
        void PositionLabels() {
            double w=ActualWidth,h=ActualHeight;if(w<1||h<1)return;
            var f=camera.LookDirection;f.Normalize();var r=Vector3D.CrossProduct(f,camera.UpDirection);r.Normalize();var u=Vector3D.CrossProduct(r,f);u.Normalize();
            foreach(var pair in stations){var delta=positions[pair.Key]-camera.Position;double xx=w/2+Vector3D.DotProduct(delta,r)/camera.Width*w,yy=h/2-Vector3D.DotProduct(delta,u)/camera.Width*w;Canvas.SetLeft(pair.Value,xx-60);Canvas.SetTop(pair.Value,yy-9);}
        }
    }
}
