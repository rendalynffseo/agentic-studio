using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Web.Script.Serialization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;

namespace AgenticStudio {
    public static class Data {
        public static readonly string Root=AppDomain.CurrentDomain.BaseDirectory;
        static readonly JavaScriptSerializer Json=new JavaScriptSerializer{MaxJsonLength=4000000};
        public static Dictionary<string,object> Read(string file){return Json.Deserialize<Dictionary<string,object>>(File.ReadAllText(file));}
        public static string Get(Dictionary<string,object> d,string key){return d.ContainsKey(key)&&d[key]!=null?Convert.ToString(d[key]):"";}
        public static List<Dictionary<string,object>> Rows(Dictionary<string,object> d,string key){return ((IEnumerable)d[key]).Cast<object>().Select(x=>(Dictionary<string,object>)x).ToList();}
        public static void Save(string file,Dictionary<string,object> data){File.WriteAllText(file+".tmp",Json.Serialize(data),new UTF8Encoding(false));if(File.Exists(file))File.Replace(file+".tmp",file,null);else File.Move(file+".tmp",file);}
        public static string Queue(params string[] args){
            var info=new ProcessStartInfo("node.exe",Quote(Path.Combine(Root,"workflow.mjs"))+" "+String.Join(" ",args.Select(Quote))){WorkingDirectory=Root,UseShellExecute=false,CreateNoWindow=true,RedirectStandardOutput=true,RedirectStandardError=true};
            using(var process=Process.Start(info)){string output=process.StandardOutput.ReadToEnd();string error=process.StandardError.ReadToEnd();if(!process.WaitForExit(15000)){process.Kill();throw new Exception("Queue operation timed out.");}if(process.ExitCode!=0)throw new Exception(error.Trim());return output;}
        }
        // Arguments are passed directly to Node, never through a command shell.
        static string Quote(string value){var result=new StringBuilder("\"");int slashes=0;foreach(char c in value){if(c=='\\'){slashes++;continue;}if(c=='\"'){result.Append('\\',slashes*2+1);result.Append(c);slashes=0;continue;}result.Append('\\',slashes);slashes=0;result.Append(c);}result.Append('\\',slashes*2);result.Append('"');return result.ToString();}
        public static string Group(string id){int n=Int32.Parse(id);if(n==1)return "dock";if(n<=3)return "planning";if(n<=5)return "research";if(n<=8)return "work";if(n==9)return "review";return "complete";}
        public static readonly string[] Titles={"Queue & intake","Planning","Project setup","SERP research","Site architecture","Content & snippets","Design & development","Technical SEO","Quality review","Release","Measurement"};
        public static readonly string[] Descriptions={"Understand the brief and collect the details needed to begin.","Define the scope, priorities, and acceptance checks.","Prepare the technology, workspace, and preview.","Research search intent and the current search landscape.","Map pages, primary queries, and internal links.","Write useful page content and accurate search snippets.","Build the responsive website and its interactions.","Verify crawlability, metadata, and structured data.","Review the actual site and verify the supporting evidence.","Prepare the release or verify an authorized deployment.","Measure actual search performance and plan improvements."};
    }
    public class Studio : Window {
        readonly Brush Bg=B("#0b1013"),Panel=B("#141a1d"),Line=B("#2a3234"),Muted=B("#89938f"),Ink=B("#e4e7de"),Gold=B("#dfbd7e");
        readonly StackPanel inspector=new StackPanel(),activity=new StackPanel();
        readonly OperationsScene scene=new OperationsScene();
        readonly ComboBox projects=new ComboBox();
        readonly TextBlock doneText=new TextBlock(),runText=new TextBlock(),attentionText=new TextBlock(),syncText=new TextBlock();
        readonly TextBlock notice=new TextBlock();
        readonly Dictionary<string,Button> tabs=new Dictionary<string,Button>();
        readonly DispatcherTimer timer=new DispatcherTimer();
        readonly Slider zoomSlider=new Slider{Minimum=55,Maximum=190,Value=100,Width=110,VerticalAlignment=VerticalAlignment.Center,Margin=new Thickness(10,0,10,0),SmallChange=5,LargeChange=10};
        readonly TextBlock sceneStatus=new TextBlock();
        bool updatingSceneControls;
        List<Dictionary<string,object>> tasks=new List<Dictionary<string,object>>();
        Dictionary<string,object> state,brief;
        string job="",fingerprint="",filter="all";
        bool loading=false;
        public Studio(){
            Title="Agentic Studio";Background=Bg;Foreground=Ink;FontFamily=new FontFamily("Segoe UI");FontSize=12;
            Width=Math.Min(1540,SystemParameters.WorkArea.Width-50);Height=Math.Min(960,SystemParameters.WorkArea.Height-45);MinWidth=1080;MinHeight=700;WindowStartupLocation=WindowStartupLocation.CenterScreen;WindowStyle=WindowStyle.None;ResizeMode=ResizeMode.CanResizeWithGrip;
            var outer=new Border{BorderBrush=Line,BorderThickness=new Thickness(1),Background=Bg};Content=outer;
            var layout=new Grid();layout.RowDefinitions.Add(new RowDefinition{Height=new GridLength(43)});layout.RowDefinitions.Add(new RowDefinition{Height=new GridLength(1,GridUnitType.Star)});layout.RowDefinitions.Add(new RowDefinition{Height=new GridLength(30)});outer.Child=layout;
            var title=new Grid{Background=B("#181e21")};title.ColumnDefinitions.Add(new ColumnDefinition{Width=new GridLength(1,GridUnitType.Star)});title.ColumnDefinitions.Add(new ColumnDefinition{Width=GridLength.Auto});
            title.MouseLeftButtonDown+=delegate(object sender,MouseButtonEventArgs e){if(e.ClickCount==2)WindowState=WindowState==WindowState.Maximized?WindowState.Normal:WindowState.Maximized;else if(e.LeftButton==MouseButtonState.Pressed)DragMove();};
            var titleText=T("◈   AGENTIC STUDIO",11,Ink);titleText.FontWeight=FontWeights.SemiBold;titleText.Margin=new Thickness(20,0,0,0);titleText.VerticalAlignment=VerticalAlignment.Center;title.Children.Add(titleText);
            var controls=new StackPanel{Orientation=Orientation.Horizontal};var min=Button("—",delegate{WindowState=WindowState.Minimized;});var max=Button("□",delegate{WindowState=WindowState==WindowState.Maximized?WindowState.Normal:WindowState.Maximized;});var close=Button("×",delegate{Close();});foreach(var b in new[]{min,max,close}){b.Width=43;b.Padding=new Thickness(0);b.Background=Brushes.Transparent;b.BorderThickness=new Thickness(0);controls.Children.Add(b);}Grid.SetColumn(controls,1);title.Children.Add(controls);layout.Children.Add(title);
            var body=new Grid();body.ColumnDefinitions.Add(new ColumnDefinition{Width=new GridLength(70)});body.ColumnDefinitions.Add(new ColumnDefinition{Width=new GridLength(1,GridUnitType.Star)});body.ColumnDefinitions.Add(new ColumnDefinition{Width=new GridLength(382)});Grid.SetRow(body,1);layout.Children.Add(body);
            var rail=new StackPanel{Margin=new Thickness(10,24,10,0)};var railBorder=new Border{BorderBrush=Line,BorderThickness=new Thickness(0,0,1,0),Background=B("#101619"),Child=rail};body.Children.Add(railBorder);
            var logo=T("a.",28,Gold);logo.HorizontalAlignment=HorizontalAlignment.Center;logo.FontWeight=FontWeights.Bold;logo.Margin=new Thickness(0,0,0,30);rail.Children.Add(logo);
            Rail(rail,"◈","Operations room",delegate{filter="all";Render();});Rail(rail,"▤","Edit website brief",delegate{EditBrief(false);});Rail(rail,"＋","Create a new task",delegate{EditBrief(true);});Rail(rail,"✎","Content writer",EditContent);Rail(rail,"▱","Open project folder",OpenFolder);Rail(rail,"↻","Refresh live queue",delegate{Refresh(true);});
            var center=new Grid();Grid.SetColumn(center,1);body.Children.Add(center);center.Children.Add(scene);
            scene.StationSelected+=delegate(string group){filter=group;Render();};
            var top=new Grid{VerticalAlignment=VerticalAlignment.Top,Margin=new Thickness(30,26,30,0)};top.ColumnDefinitions.Add(new ColumnDefinition{Width=new GridLength(1,GridUnitType.Star)});top.ColumnDefinitions.Add(new ColumnDefinition{Width=GridLength.Auto});center.Children.Add(top);
            var caption=new StackPanel();caption.Children.Add(Eyebrow("YOUR AGENT OPERATIONS ROOM"));var headline=T("Build something worth finding.",25,Ink);headline.FontWeight=FontWeights.SemiBold;headline.Margin=new Thickness(0,10,0,8);caption.Children.Add(headline);caption.Children.Add(T("A live workspace for your next search-ready website.",11,Muted));top.Children.Add(caption);
            var metrics=new StackPanel{Orientation=Orientation.Horizontal,HorizontalAlignment=HorizontalAlignment.Left,Margin=new Thickness(0,28,0,0)};
            Metric(metrics,"STAGES COMPLETE",doneText);Metric(metrics,"AGENTS WORKING",runText);Metric(metrics,"NEEDS ATTENTION",attentionText);caption.Children.Add(metrics);
            var newTask=Button("＋  New task",delegate{EditBrief(true);});newTask.Background=B("#e5e6da");newTask.Foreground=B("#1d2829");newTask.Margin=new Thickness(15,0,0,0);newTask.VerticalAlignment=VerticalAlignment.Top;newTask.Padding=new Thickness(16,11,16,11);Grid.SetColumn(newTask,1);top.Children.Add(newTask);
            var bottom=new StackPanel{VerticalAlignment=VerticalAlignment.Bottom,HorizontalAlignment=HorizontalAlignment.Center,Margin=new Thickness(20,0,20,25)};center.Children.Add(bottom);
            var stationHint=T("DRAG TO ROTATE  /  RIGHT-DRAG TO MOVE  /  SCROLL TO ZOOM",9,B("#8b9b93"));stationHint.HorizontalAlignment=HorizontalAlignment.Center;stationHint.Margin=new Thickness(0,0,0,10);bottom.Children.Add(stationHint);
            var viewTools=new StackPanel{Orientation=Orientation.Horizontal,HorizontalAlignment=HorizontalAlignment.Center};var toolsBorder=new Border{Background=B("#171e22"),BorderBrush=Line,BorderThickness=new Thickness(1),CornerRadius=new CornerRadius(7),Padding=new Thickness(5),Margin=new Thickness(0,0,0,9),Child=viewTools};bottom.Children.Add(toolsBorder);
            var rotateMode=Button("Rotate",delegate{scene.SetMoveMode(false);});var moveMode=Button("Move",delegate{scene.SetMoveMode(true);});
            viewTools.Children.Add(rotateMode);viewTools.Children.Add(moveMode);
            var zoomOut=Button("−",delegate{scene.SetZoom(scene.ZoomPercent/100/1.12);});zoomOut.ToolTip="Zoom out";System.Windows.Automation.AutomationProperties.SetName(zoomOut,"Zoom out");viewTools.Children.Add(zoomOut);
            System.Windows.Automation.AutomationProperties.SetName(zoomSlider,"Scene zoom percent");zoomSlider.ValueChanged+=delegate{if(!updatingSceneControls)scene.SetZoom(zoomSlider.Value/100);};viewTools.Children.Add(zoomSlider);
            var zoomIn=Button("＋",delegate{scene.SetZoom(scene.ZoomPercent/100*1.12);});zoomIn.ToolTip="Zoom in";System.Windows.Automation.AutomationProperties.SetName(zoomIn,"Zoom in");viewTools.Children.Add(zoomIn);
            var reset=Button("Reset view",delegate{scene.ResetView();});reset.ToolTip="Reset the camera (R or double-click empty space)";viewTools.Children.Add(reset);
            Button motion=null;motion=Button("Motion: on",delegate{scene.ToggleMotion();});viewTools.Children.Add(motion);
            foreach(var control in new[]{rotateMode,moveMode,zoomOut,zoomIn,reset,motion}){control.Padding=new Thickness(10,8,10,8);control.Margin=new Thickness(1,0,1,0);control.BorderThickness=new Thickness(0);control.FontSize=10;}
            sceneStatus.FontSize=8;sceneStatus.Foreground=B("#7d9187");sceneStatus.HorizontalAlignment=HorizontalAlignment.Center;sceneStatus.Margin=new Thickness(0,9,0,0);System.Windows.Automation.AutomationProperties.SetAutomationId(sceneStatus,"SceneViewStatus");
            scene.ViewChanged+=delegate{updatingSceneControls=true;zoomSlider.Value=scene.ZoomPercent;updatingSceneControls=false;sceneStatus.Text=scene.ViewDescription;motion.Content=scene.MotionEnabled?"Motion: on":"Motion: off";rotateMode.Foreground=!scene.MoveMode?Gold:Muted;moveMode.Foreground=scene.MoveMode?Gold:Muted;};sceneStatus.Text=scene.ViewDescription;
            var tabRow=new StackPanel{Orientation=Orientation.Horizontal};var tabBorder=new Border{Background=B("#171e22"),BorderBrush=Line,BorderThickness=new Thickness(1),CornerRadius=new CornerRadius(8),Padding=new Thickness(5),Child=tabRow};bottom.Children.Add(tabBorder);
            foreach(string name in new[]{"all","dock","planning","research","review","work","complete"}){string key=name;var b=Button(name=="all"?"All tasks":Char.ToUpper(name[0])+name.Substring(1),delegate{filter=key;Render();});b.FontSize=10;b.Padding=new Thickness(10,9,10,9);b.BorderThickness=new Thickness(0);b.Background=Brushes.Transparent;tabs[name]=b;tabRow.Children.Add(b);}
            bottom.Children.Add(sceneStatus);
            var right=new Border{Background=Panel,BorderBrush=Line,BorderThickness=new Thickness(1,0,0,0)};Grid.SetColumn(right,2);body.Children.Add(right);
            var rightGrid=new Grid();rightGrid.RowDefinitions.Add(new RowDefinition{Height=GridLength.Auto});rightGrid.RowDefinitions.Add(new RowDefinition{Height=new GridLength(1,GridUnitType.Star)});right.Child=rightGrid;
            var selector=new StackPanel{Margin=new Thickness(23,23,23,17)};selector.Children.Add(Eyebrow("TASK CONTROL"));projects.Margin=new Thickness(0,12,0,0);projects.Padding=new Thickness(10,8,10,8);projects.Background=B("#222b2e");projects.Foreground=Ink;projects.BorderBrush=Line;projects.FontSize=12;projects.SelectionChanged+=delegate{if(!loading&&projects.SelectedItem!=null){job=((ComboBoxItem)projects.SelectedItem).Tag.ToString();fingerprint="";Refresh(true);}};selector.Children.Add(projects);rightGrid.Children.Add(selector);
            var scroll=new ScrollViewer{VerticalScrollBarVisibility=ScrollBarVisibility.Auto,HorizontalScrollBarVisibility=ScrollBarVisibility.Disabled,Content=inspector};Grid.SetRow(scroll,1);rightGrid.Children.Add(scroll);inspector.Margin=new Thickness(23,0,23,25);
            var status=new Grid{Background=B("#12191c")};status.ColumnDefinitions.Add(new ColumnDefinition{Width=new GridLength(1,GridUnitType.Star)});status.ColumnDefinitions.Add(new ColumnDefinition{Width=GridLength.Auto});Grid.SetRow(status,2);layout.Children.Add(status);var statusText=T("●  LOCAL WORKSPACE     /     NATIVE DESKTOP     /     AUTO-SYNC 2s",9,B("#7d9187"));statusText.VerticalAlignment=VerticalAlignment.Center;statusText.Margin=new Thickness(18,0,0,0);status.Children.Add(statusText);syncText.Foreground=Muted;syncText.FontSize=9;syncText.VerticalAlignment=VerticalAlignment.Center;syncText.Margin=new Thickness(0,0,17,0);Grid.SetColumn(syncText,1);status.Children.Add(syncText);
            timer.Interval=TimeSpan.FromSeconds(2);timer.Tick+=delegate{Refresh(false);};Loaded+=delegate{Refresh(true);timer.Start();};Closed+=delegate{timer.Stop();};
        }
        static SolidColorBrush B(string value){return new SolidColorBrush((Color)ColorConverter.ConvertFromString(value));}
        TextBlock T(string value,double size,Brush color){return new TextBlock{Text=value,FontSize=size,Foreground=color,TextWrapping=TextWrapping.Wrap};}
        TextBlock Eyebrow(string value){return T(value,9,B("#8b968d"));}
        Button Button(string title,Action action){
            var b=new Button{Content=title,Foreground=Ink,Background=B("#252d2f"),BorderBrush=Line,BorderThickness=new Thickness(1),Padding=new Thickness(13,9,13,9),Cursor=Cursors.Hand,FontSize=11};
            var template=new ControlTemplate(typeof(Button));var border=new FrameworkElementFactory(typeof(Border));border.SetValue(Border.CornerRadiusProperty,new CornerRadius(5));border.SetBinding(Border.BackgroundProperty,new System.Windows.Data.Binding("Background"){RelativeSource=new System.Windows.Data.RelativeSource(System.Windows.Data.RelativeSourceMode.TemplatedParent)});border.SetBinding(Border.BorderBrushProperty,new System.Windows.Data.Binding("BorderBrush"){RelativeSource=new System.Windows.Data.RelativeSource(System.Windows.Data.RelativeSourceMode.TemplatedParent)});border.SetBinding(Border.BorderThicknessProperty,new System.Windows.Data.Binding("BorderThickness"){RelativeSource=new System.Windows.Data.RelativeSource(System.Windows.Data.RelativeSourceMode.TemplatedParent)});var content=new FrameworkElementFactory(typeof(ContentPresenter));content.SetValue(ContentPresenter.HorizontalAlignmentProperty,HorizontalAlignment.Center);content.SetValue(ContentPresenter.VerticalAlignmentProperty,VerticalAlignment.Center);content.SetBinding(ContentPresenter.MarginProperty,new System.Windows.Data.Binding("Padding"){RelativeSource=new System.Windows.Data.RelativeSource(System.Windows.Data.RelativeSourceMode.TemplatedParent)});border.AppendChild(content);template.VisualTree=border;b.Template=template;
            b.MouseEnter+=delegate{b.Opacity=.8;};b.MouseLeave+=delegate{b.Opacity=b.IsEnabled?1:.4;};b.IsEnabledChanged+=delegate{b.Opacity=b.IsEnabled?1:.4;};b.Click+=delegate{try{action();}catch(Exception error){MessageBox.Show(this,error.Message,"Agentic Studio",MessageBoxButton.OK,MessageBoxImage.Warning);}};return b;
        }
        void Rail(StackPanel parent,string icon,string tooltip,Action action){var b=Button(icon,action);b.ToolTip=tooltip;b.Background=Brushes.Transparent;b.BorderThickness=new Thickness(0);b.FontSize=21;b.Height=47;b.Margin=new Thickness(0,0,0,8);parent.Children.Add(b);}
        void Metric(StackPanel parent,string label,TextBlock value){var stack=new StackPanel();stack.Children.Add(Eyebrow(label));value.FontSize=24;value.Foreground=Ink;value.FontWeight=FontWeights.SemiBold;value.Margin=new Thickness(0,8,0,0);stack.Children.Add(value);parent.Children.Add(new Border{Background=B("#151d20"),BorderBrush=Line,BorderThickness=new Thickness(1),CornerRadius=new CornerRadius(7),Padding=new Thickness(16,12,22,12),Margin=new Thickness(0,0,9,0),Child=stack});}
        string JobDirectory {get {return Path.Combine(Data.Root,"jobs",job);}}
        string ProjectName(Dictionary<string,object> d){string n=Data.Get(d,"project_name");return n=="Replace with your website name"?"Your first website":n;}
        void Refresh(bool force){
            try{
                string directory=Path.Combine(Data.Root,"jobs");if(!Directory.Exists(directory))Directory.CreateDirectory(directory);
                var folders=Directory.GetDirectories(directory).Where(p=>File.Exists(Path.Combine(p,"state.json"))).OrderByDescending(p=>Directory.GetCreationTimeUtc(p)).ToArray();
                var valid=new List<KeyValuePair<string,Dictionary<string,object>>>();foreach(string folder in folders){try{valid.Add(new KeyValuePair<string,Dictionary<string,object>>(Path.GetFileName(folder),Data.Read(Path.Combine(folder,"state.json"))));}catch{}}
                string ids=String.Join("|",valid.Select(v=>v.Key));string oldIds=String.Join("|",projects.Items.Cast<ComboBoxItem>().Select(v=>v.Tag.ToString()));
                if(force||ids!=oldIds){loading=true;projects.Items.Clear();foreach(var item in valid){projects.Items.Add(new ComboBoxItem{Content=ProjectName(item.Value),Tag=item.Key,Foreground=Ink});}if(!valid.Any(x=>x.Key==job))job=valid.Count>0?valid[0].Key:"";foreach(ComboBoxItem item in projects.Items)if(item.Tag.ToString()==job)projects.SelectedItem=item;loading=false;}
                if(String.IsNullOrEmpty(job)){inspector.Children.Clear();inspector.Children.Add(T("No tasks yet.",22,Ink));inspector.Children.Add(T("Create a task to begin your website workflow.",12,Muted));inspector.Children.Add(Button("＋  New task",delegate{EditBrief(true);}));doneText.Text="0 / 11";runText.Text="0";attentionText.Text="0";return;}
                string stateFile=Path.Combine(JobDirectory,"state.json"),briefFile=Path.Combine(JobDirectory,"brief.json");string signature=File.ReadAllText(stateFile)+File.ReadAllText(briefFile)+String.Join("|",Directory.GetFiles(Path.Combine(JobDirectory,"artifacts")).Select(p=>p+File.GetLastWriteTimeUtc(p).Ticks));
                if(force||signature!=fingerprint){state=Data.Read(stateFile);brief=Data.Read(briefFile);tasks=Data.Rows(state,"tasks");fingerprint=signature;Render();}
                syncText.Text="SYNCED "+DateTime.Now.ToString("HH:mm:ss");
            }catch(Exception error){loading=false;syncText.Text="SYNC ERROR · "+error.Message;}
        }
        void Rule(StackPanel parent){parent.Children.Add(new Border{Height=1,Background=Line,Margin=new Thickness(0,18,0,18)});}
        Border Card(UIElement content,Brush border){return new Border{Background=B("#1b2225"),BorderBrush=border,BorderThickness=new Thickness(1),CornerRadius=new CornerRadius(7),Padding=new Thickness(14),Margin=new Thickness(0,0,0,12),Child=content};}
        void Render(){
            if(state==null)return;
            int done=tasks.Count(t=>Data.Get(t,"status")=="done"),running=tasks.Count(t=>Data.Get(t,"status")=="running"),failed=tasks.Count(t=>Data.Get(t,"status")=="failed");doneText.Text=done+" / 11";runText.Text=running.ToString();attentionText.Text=failed.ToString();attentionText.Foreground=failed>0?Gold:Ink;
            var counts=tasks.GroupBy(t=>Data.Group(Data.Get(t,"id"))).ToDictionary(g=>g.Key,g=>g.Count(t=>Data.Get(t,"status")!="done"));
            var stationStates=tasks.GroupBy(t=>Data.Group(Data.Get(t,"id"))).ToDictionary(g=>g.Key,g=>g.Any(t=>Data.Get(t,"status")=="running")?"running":g.Any(t=>Data.Get(t,"status")=="failed")?"failed":g.All(t=>Data.Get(t,"status")=="done")?"done":"pending");scene.UpdateAgentStates(stationStates);scene.UpdateCounts(counts,filter);
            foreach(var tab in tabs){tab.Value.Background=tab.Key==filter?B("#343b36"):Brushes.Transparent;tab.Value.Foreground=tab.Key==filter?Gold:Muted;}
            inspector.Children.Clear();var current=tasks.FirstOrDefault(t=>Data.Get(t,"status")!="done");string status=current==null?"Complete":Data.Get(current,"status")=="failed"?"Needs input":Data.Get(current,"status")=="running"?"Running":"Queued";
            var badge=T("●  "+status.ToUpperInvariant(),9,status=="Needs input"?Gold:B("#a0bba9"));inspector.Children.Add(badge);var heading=T(ProjectName(state),23,Ink);heading.FontWeight=FontWeights.SemiBold;heading.Margin=new Thickness(0,13,0,12);inspector.Children.Add(heading);
            var summary=T(String.IsNullOrWhiteSpace(Data.Get(brief,"offer"))?"Add your business, audience, and offer to begin a useful website brief.":Data.Get(brief,"offer"),12,Muted);summary.LineHeight=20;inspector.Children.Add(summary);
            var actions=new WrapPanel{Margin=new Thickness(0,17,0,17)};var edit=Button("Edit brief",delegate{EditBrief(false);});edit.Margin=new Thickness(0,0,7,0);actions.Children.Add(edit);var contentButton=Button("Content writer",EditContent);contentButton.Margin=new Thickness(0,0,7,0);actions.Children.Add(contentButton);var blogButton=Button("Add blog task",delegate{EditBrief(true,true);});blogButton.Margin=new Thickness(0,0,7,0);actions.Children.Add(blogButton);actions.Children.Add(Button("Open folder ↗",OpenFolder));inspector.Children.Add(actions);
            if(brief.ContainsKey("blog_enabled")&&Convert.ToBoolean(brief["blog_enabled"]))inspector.Children.Add(T("BLOG AGENT: "+Data.Get(brief,"blog_post_count")+" posts at "+Data.Get(brief,"blog_path"),10,Gold));
            string contentMode=Data.Get(brief,"content_mode");if(contentMode!=""&&contentMode!="agent"){var contentNote=T(contentMode=="provided"?"CONTENT: Your exact copy":"CONTENT: Your copy + agent fills gaps",10,Gold);contentNote.Margin=new Thickness(0,0,0,15);inspector.Children.Add(contentNote);}
            inspector.Children.Add(Eyebrow("WORKFLOW PROGRESS"));var progress=new ProgressBar{Minimum=0,Maximum=11,Value=done,Height=4,Foreground=Gold,Background=B("#303937"),BorderThickness=new Thickness(0),Margin=new Thickness(0,10,0,8)};inspector.Children.Add(progress);inspector.Children.Add(T(done+" of 11 stages complete · "+running+" currently working",10,Muted));
            var runner=new StackPanel();runner.Children.Add(T(running>0?"Agent stage active":current==null?"Workflow complete":"Ready to start / continue",11,Ink));var hint=T("1. Click Start / continue below. 2. Copy the task instructions into your coding agent. 3. Watch real stage progress here.",10,Muted);hint.LineHeight=17;hint.Margin=new Thickness(0,7,0,0);runner.Children.Add(hint);if(current!=null){var start=Button(running>0?"View continuation instructions":"Start / continue task",StartWork);start.Margin=new Thickness(0,12,0,0);runner.Children.Add(start);}var runnerCard=Card(runner,Line);runnerCard.Margin=new Thickness(0,18,0,16);inspector.Children.Add(runnerCard);
            if(current!=null&&Data.Get(current,"status")=="failed"){
                var issue=new StackPanel();issue.Children.Add(Eyebrow("ACTION NEEDED"));var reason=T(Data.Get(current,"failure"),11,Gold);reason.LineHeight=18;reason.Margin=new Thickness(0,9,0,14);issue.Children.Add(reason);var retry=Button("Retry current task ↗",Retry);retry.HorizontalAlignment=HorizontalAlignment.Left;issue.Children.Add(retry);inspector.Children.Add(Card(issue,B("#655438")));
            }
            inspector.Children.Add(Eyebrow(filter=="all"?"AGENT HANDOFFS":"STATION / "+filter.ToUpperInvariant()));
            foreach(var task in tasks.Where(t=>filter=="all"||Data.Group(Data.Get(t,"id"))==filter)){
                int index=Int32.Parse(Data.Get(task,"id"))-1;string stageStatus=Data.Get(task,"status");var stack=new StackPanel();var row=new DockPanel();var st=T(stageStatus=="failed"?"Needs input":stageStatus=="done"?"Complete":stageStatus=="running"?"Running":"Queued",9,stageStatus=="failed"?Gold:stageStatus=="done"?B("#99c2a8"):Muted);DockPanel.SetDock(st,Dock.Right);row.Children.Add(st);row.Children.Add(T(Data.Get(task,"id")+"   "+Data.Titles[index],12,Ink));stack.Children.Add(row);var desc=T(Data.Descriptions[index],10,Muted);desc.LineHeight=17;desc.Margin=new Thickness(0,9,0,8);stack.Children.Add(desc);stack.Children.Add(T(Data.Get(task,"agent")+" · "+Data.Get(task,"attempts")+" attempts",9,B("#73837b")));
                string artifact=Path.Combine(JobDirectory,Data.Get(task,"artifact").Replace('/',Path.DirectorySeparatorChar));if(File.Exists(artifact)){string capture=artifact;var view=Button("View handoff ↗",delegate{ReadFile(capture);});view.Margin=new Thickness(0,12,0,0);view.HorizontalAlignment=HorizontalAlignment.Left;stack.Children.Add(view);}var card=Card(stack,stageStatus=="failed"?B("#655438"):Line);card.Margin=new Thickness(0,12,0,0);inspector.Children.Add(card);
            }
            Rule(inspector);inspector.Children.Add(Eyebrow("DELIVERABLES"));
            var files=Directory.GetFiles(Path.Combine(JobDirectory,"artifacts"));if(files.Length==0){var empty=T("Agent outputs will appear here when saved.",11,Muted);empty.Margin=new Thickness(0,12,0,0);inspector.Children.Add(empty);}foreach(string file in files.OrderBy(p=>p)){string capture=file;var b=Button("▤  "+Path.GetFileName(file),delegate{ReadFile(capture);});b.Margin=new Thickness(0,10,0,0);b.HorizontalContentAlignment=HorizontalAlignment.Left;inspector.Children.Add(b);}
            Rule(inspector);inspector.Children.Add(Eyebrow("ACTIVITY LOG"));
            foreach(var evt in Data.Rows(state,"events").AsEnumerable().Reverse().Take(12)){
                var e=T(Data.Get(evt,"action").Replace('_',' ').ToUpperInvariant()+"  ·  STAGE "+Data.Get(evt,"stage"),10,Ink);e.Margin=new Thickness(0,15,0,5);inspector.Children.Add(e);string reason=Data.Get(evt,"reason");if(reason!="")inspector.Children.Add(T(reason,10,Muted));DateTime at;if(DateTime.TryParse(Data.Get(evt,"at"),out at)){var date=T(at.ToLocalTime().ToString("MMM d · HH:mm:ss"),9,B("#67776f"));date.Margin=new Thickness(0,5,0,0);inspector.Children.Add(date);}
            }
        }
        void StartWork(){
            if(String.IsNullOrEmpty(job))return;
            string prompt="Work in this workspace: "+Data.Root+"\r\nContinue the task at "+JobDirectory+" using ORCHESTRATOR.md and agents/roles.md. Read brief.json and state.json first. Execute the next unfinished role and continue sequentially, saving real deliverables and updating the queue. Respect affiliate_links, blog_enabled / blog_topics / blog_post_count / blog_path, and exact supplied content. Read templates/BLOG-WORKFLOW.md for blog tasks. If a stage is already running, inspect it before resuming; never launch a duplicate worker. Stop only for a real blocker or when all authorized work is done. Do not deploy unless the brief authorizes it.";
            var window=new Window{Title="Start / continue task - Agentic Studio",Owner=this,Width=720,Height=540,WindowStartupLocation=WindowStartupLocation.CenterOwner,Background=Panel,Foreground=Ink};
            var wrap=new StackPanel{Margin=new Thickness(26)};window.Content=new ScrollViewer{Content=wrap,VerticalScrollBarVisibility=ScrollBarVisibility.Auto};wrap.Children.Add(T("Start your task",24,Ink));
            var help=T("1. Copy the instructions below.\n2. Paste them into your coding agent with this workspace open, then send.\n3. Keep this app open to watch saved work and stage progress.\n\nCopying instructions does not start an AI worker. Your agent must receive and run them.",12,Muted);help.LineHeight=21;help.Margin=new Thickness(0,16,0,16);wrap.Children.Add(help);
            wrap.Children.Add(new TextBox{Text=prompt,IsReadOnly=true,TextWrapping=TextWrapping.Wrap,Height=155,VerticalScrollBarVisibility=ScrollBarVisibility.Auto,Background=Bg,Foreground=Ink,Padding=new Thickness(12)});
            var copied=T("",11,Gold);wrap.Children.Add(copied);var buttons=new WrapPanel{Margin=new Thickness(0,16,0,0)};buttons.Children.Add(Button("Copy task instructions",delegate{Clipboard.SetText(prompt);copied.Text="Copied. Paste into your coding agent and send to begin.";}));buttons.Children.Add(Button("Open workspace",delegate{Process.Start(new ProcessStartInfo("explorer.exe","\""+Data.Root+"\""){UseShellExecute=true});}));buttons.Children.Add(Button("Close",delegate{window.Close();}));wrap.Children.Add(buttons);window.ShowDialog();
        }
        void OpenFolder(){if(String.IsNullOrEmpty(job))return;Process.Start(new ProcessStartInfo("explorer.exe","\""+JobDirectory+"\""){UseShellExecute=true});}
        void EditContent(){
            if(brief==null){MessageBox.Show(this,"Create a website task first, then open Content writer.","Content writer");return;}
            if(tasks.Any(t=>Data.Get(t,"status")=="running")){MessageBox.Show(this,"Wait for the active agent to finish before changing content.","Content in use");return;}
            var window=new Window{Title="Content writer - Agentic Studio",Owner=this,Width=750,Height=800,MaxHeight=SystemParameters.WorkArea.Height-40,WindowStartupLocation=WindowStartupLocation.CenterOwner,Background=Panel,Foreground=Ink};
            var wrap=new StackPanel{Margin=new Thickness(28)};window.Content=new ScrollViewer{Content=wrap,VerticalScrollBarVisibility=ScrollBarVisibility.Auto};var heading=T("Your words. The right place.",25,Ink);heading.FontWeight=FontWeights.SemiBold;wrap.Children.Add(heading);var explanation=T("Paste your copy in separate blocks. The agent maps each block to a page and section while keeping its wording exact.",12,Muted);explanation.LineHeight=20;explanation.Margin=new Thickness(0,10,0,0);wrap.Children.Add(explanation);
            var editor=new ContentEditor(brief,Button);wrap.Children.Add(editor);var effect=T("Saving queues the content stage and later checks again. It does not launch workers or deploy a website by itself.",11,Muted);effect.LineHeight=18;effect.Margin=new Thickness(0,22,0,0);wrap.Children.Add(effect);var errorText=T("",11,Gold);errorText.Margin=new Thickness(0,12,0,0);wrap.Children.Add(errorText);
            var buttons=new StackPanel{Orientation=Orientation.Horizontal,Margin=new Thickness(0,18,0,0)};var save=Button("Save & queue content",delegate{
                string file=Path.Combine(Data.Root,"desktop","content-"+Guid.NewGuid().ToString("N")+".json");try{var supplied=editor.Collect();Data.Save(file,supplied);Data.Queue("set-content","--job",JobDirectory,"--input",file);fingerprint="";Refresh(true);window.Close();MessageBox.Show(this,"Content saved. The agent will create a placement map and verify your wording in the built pages when you continue this task.","Content writer",MessageBoxButton.OK,MessageBoxImage.Information);}catch(Exception error){errorText.Text=error.Message;}finally{if(File.Exists(file))File.Delete(file);}
            });save.Background=Gold;save.Foreground=B("#202723");buttons.Children.Add(save);var cancel=Button("Cancel",delegate{window.Close();});cancel.Margin=new Thickness(10,0,0,0);buttons.Children.Add(cancel);wrap.Children.Add(buttons);window.ShowDialog();
        }
        void Retry(){
            if(String.IsNullOrWhiteSpace(Data.Get(brief,"business"))||String.IsNullOrWhiteSpace(Data.Get(brief,"offer"))||Data.Get(brief,"project_name")=="Replace with your website name"){EditBrief(false);return;}
            Data.Queue("retry","--job",JobDirectory);Refresh(true);MessageBox.Show(this,"Task returned to the queue. Ask your coding agent to continue jobs/"+job+".\n\nThe desktop app tracks execution; it does not launch AI workers.","Task queued",MessageBoxButton.OK,MessageBoxImage.Information);
        }
        void ReadFile(string file){
            var window=new Window{Title=Path.GetFileName(file)+" — Agentic Studio",Owner=this,Width=850,Height=650,WindowStartupLocation=WindowStartupLocation.CenterOwner,Background=Panel,Foreground=Ink};var grid=new Grid{Margin=new Thickness(22)};grid.RowDefinitions.Add(new RowDefinition{Height=GridLength.Auto});grid.RowDefinitions.Add(new RowDefinition{Height=new GridLength(1,GridUnitType.Star)});var title=T(Path.GetFileName(file),20,Ink);title.Margin=new Thickness(0,0,0,18);grid.Children.Add(title);var text=new TextBox{Text=File.ReadAllText(file),IsReadOnly=true,TextWrapping=TextWrapping.Wrap,VerticalScrollBarVisibility=ScrollBarVisibility.Auto,FontFamily=new FontFamily("Consolas"),FontSize=12,Foreground=Ink,Background=Bg,BorderBrush=Line,Padding=new Thickness(16)};Grid.SetRow(text,1);grid.Children.Add(text);window.Content=grid;window.ShowDialog();
        }
        void EditBrief(bool create,bool blogOnly=false){
            if(!create&&brief==null){EditBrief(true);return;}
            if(!create&&tasks.Any(t=>Data.Get(t,"status")=="running"||Data.Get(t,"status")=="done")){MessageBox.Show(this,"The brief is locked once execution starts. Ask the orchestrator to reopen intake before changing active work.","Brief in use");return;}
            var input=create?Data.Read(Path.Combine(Data.Root,"templates","brief.json")):new Dictionary<string,object>(brief);
            if(blogOnly&&brief!=null){input=new Dictionary<string,object>(brief);input["project_name"]=Data.Get(brief,"project_name")+" - Blog update";input["request"]="Add blog posts to the existing website. Preserve existing pages and design; inspect the project before editing.";input["existing_site"]=Data.Get(brief,"domain")==""?Data.Get(brief,"existing_site"):Data.Get(brief,"domain");input["blog_enabled"]=true;input["deployment_authorized"]=false;input["content_mode"]="agent";input["content_blocks"]=new object[0];}
            var window=new Window{Title=create?"New website task — Agentic Studio":"Edit website brief — Agentic Studio",Owner=this,Width=640,Height=790,MaxHeight=SystemParameters.WorkArea.Height-40,WindowStartupLocation=WindowStartupLocation.CenterOwner,Background=Panel,Foreground=Ink};
            var wrap=new StackPanel{Margin=new Thickness(30)};window.Content=new ScrollViewer{Content=wrap,VerticalScrollBarVisibility=ScrollBarVisibility.Auto};wrap.Children.Add(Eyebrow("TASK INTAKE"));var title=T(create?"What are we building?":"Give your agents a direction.",25,Ink);title.FontWeight=FontWeights.SemiBold;title.Margin=new Thickness(0,12,0,10);wrap.Children.Add(title);wrap.Children.Add(T("Your brief is passed from one agent to the next. Start with the essentials.",12,Muted));
            var inputs=new Dictionary<string,TextBox>();string[] keys={"project_name","business","offer","audience","conversion_goal","target_country","language","domain","existing_site","project_path","additional_instructions"};string[] captions={"Website / business name *","Business or topic *","Your offer *","Target audience","Desired visitor action","Target country","Language","Production domain","Existing site URL (for updates)","Local website project path (for updates)","Additional instructions"};
            for(int i=0;i<keys.Length;i++){string key=keys[i];var label=T(captions[i],11,Muted);label.Margin=new Thickness(0,17,0,7);wrap.Children.Add(label);string value=Data.Get(input,key);if(key=="project_name"&&value=="Replace with your website name")value="";var tb=new TextBox{Text=value,Background=B("#0e1418"),Foreground=Ink,BorderBrush=Line,Padding=new Thickness(11),FontSize=12,CaretBrush=Gold};if(key=="additional_instructions"){tb.AcceptsReturn=true;tb.Height=75;tb.TextWrapping=TextWrapping.Wrap;}System.Windows.Automation.AutomationProperties.SetName(tb,captions[i]);inputs[key]=tb;wrap.Children.Add(tb);}
            var publishingEditor=new PublishingEditor(input,Button);wrap.Children.Add(publishingEditor);
            var contentEditor=new ContentEditor(input,Button);wrap.Children.Add(contentEditor);
            var errorText=T("",11,Gold);errorText.Margin=new Thickness(0,16,0,0);wrap.Children.Add(errorText);
            var buttons=new StackPanel{Orientation=Orientation.Horizontal,Margin=new Thickness(0,20,0,0)};var submit=Button(create?"Create task ↗":"Save brief & queue ↗",delegate{
                try{
                    foreach(string key in keys)input[key]=inputs[key].Text.Trim();if(String.IsNullOrWhiteSpace(Data.Get(input,"project_name"))||String.IsNullOrWhiteSpace(Data.Get(input,"business"))||String.IsNullOrWhiteSpace(Data.Get(input,"offer"))){errorText.Text="Enter a website name, business or topic, and offer.";return;}foreach(var setting in publishingEditor.Collect())input[setting.Key]=setting.Value;foreach(var supplied in contentEditor.Collect())input[supplied.Key]=supplied.Value;
                    if(create){
                        string id="site-"+DateTime.Now.ToString("yyyyMMdd-HHmmss")+"-"+Guid.NewGuid().ToString("N").Substring(0,4);string temp=Path.Combine(Data.Root,"desktop","brief-"+Guid.NewGuid().ToString("N")+".json");Data.Save(temp,input);try{Data.Queue("init","--brief",temp,"--job",Path.Combine(Data.Root,"jobs",id));}finally{File.Delete(temp);}job=id;
                    }else{
                        var latest=Data.Read(Path.Combine(JobDirectory,"state.json"));var rows=Data.Rows(latest,"tasks");if(rows.Any(t=>Data.Get(t,"status")=="running"||Data.Get(t,"status")=="done"))throw new Exception("An agent has started this job. Reopen intake before revising the brief.");Data.Save(Path.Combine(JobDirectory,"brief.json"),input);latest["project_name"]=Data.Get(input,"project_name");var events=Data.Rows(latest,"events");events.Add(new Dictionary<string,object>{{"at",DateTime.UtcNow.ToString("o")},{"action","brief_updated"},{"stage","01"},{"reason","Website brief saved in Agentic Studio desktop"}});latest["events"]=events;Data.Save(Path.Combine(JobDirectory,"state.json"),latest);if(rows.First(t=>Data.Get(t,"status")!="done")["status"].ToString()=="failed")Data.Queue("retry","--job",JobDirectory);
                    }
                    filter="all";fingerprint="";Refresh(true);window.Close();StartWork();
                }catch(Exception error){errorText.Text=error.Message;}
            });submit.Background=Gold;submit.Foreground=B("#202723");buttons.Children.Add(submit);var cancel=Button("Cancel",delegate{window.Close();});cancel.Margin=new Thickness(10,0,0,0);buttons.Children.Add(cancel);wrap.Children.Add(buttons);window.ShowDialog();
        }
        public void Snapshot(string file){var bitmap=new RenderTargetBitmap((int)ActualWidth,(int)ActualHeight,96,96,PixelFormats.Pbgra32);bitmap.Render((Visual)Content);var encoder=new PngBitmapEncoder();encoder.Frames.Add(BitmapFrame.Create(bitmap));using(var stream=File.Create(file))encoder.Save(stream);}
    }
    public static class Program {
        [STAThread]public static void Main(string[] args){
            try{
                if(args.Length>0&&args[0]=="--publishing-test"){File.WriteAllText(Path.Combine(Data.Root,"desktop","publishing-test-result.txt"),PublishingEditor.SelfCheck());return;}
                if(args.Length>0&&args[0]=="--scene-test"){File.WriteAllText(Path.Combine(Data.Root,"desktop","scene-test-result.txt"),OperationsScene.SelfCheck());return;}
                if(args.Length>0&&args[0]=="--self-test"){
                    var state=Data.Read(Path.Combine(Data.Root,"jobs","first-site","state.json"));var tasks=Data.Rows(state,"tasks");if(tasks.Count!=11)throw new Exception("Expected 11 stages");if(tasks.Select(t=>Data.Group(Data.Get(t,"id"))).Distinct().Count()!=6)throw new Exception("Expected six stations");Data.Queue("status","--job",Path.Combine(Data.Root,"jobs","first-site"));File.WriteAllText(Path.Combine(Data.Root,"desktop","self-test-result.txt"),"PASS: native JSON loading, 11 stages, six station groups, and Node queue interoperability.");return;
                }
                var app=new Application();using(var theme=File.OpenRead(Path.Combine(Data.Root,"desktop","Theme.xaml")))app.Resources.MergedDictionaries.Add((ResourceDictionary)System.Windows.Markup.XamlReader.Load(theme));app.DispatcherUnhandledException+=delegate(object sender,DispatcherUnhandledExceptionEventArgs e){File.WriteAllText(Path.Combine(Data.Root,"desktop","error.log"),e.Exception.ToString());MessageBox.Show(e.Exception.Message,"Agentic Studio");e.Handled=true;};var window=new Studio();
                if(args.Length==2&&args[0]=="--snapshot"){var timer=new DispatcherTimer{Interval=TimeSpan.FromSeconds(3)};timer.Tick+=delegate{timer.Stop();window.Snapshot(args[1]);};window.Loaded+=delegate{timer.Start();};}
                app.Run(window);
            }catch(Exception error){File.WriteAllText(Path.Combine(Data.Root,"desktop","error.log"),error.ToString());Environment.ExitCode=1;if(args.Length==0||!args[0].EndsWith("test"))MessageBox.Show(error.Message,"Agentic Studio could not start");}
        }
    }
}
