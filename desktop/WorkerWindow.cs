using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Web.Script.Serialization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Threading;
using System.Text.RegularExpressions;
using Microsoft.Win32;

namespace AgenticStudio {
    public class WorkerWindow : Window {
        readonly TextBox log=new TextBox(),enginePath=new TextBox();
        readonly StackPanel signInCard=new StackPanel();
        readonly TextBox deviceCode=new TextBox();
        readonly TextBlock connection=new TextBlock(),status=new TextBlock();
        readonly Button start=new Button(),pause=new Button(),stop=new Button(),login=new Button(),check=new Button(),browse=new Button(),recover=new Button();
        readonly DispatcherTimer monitor=new DispatcherTimer{Interval=TimeSpan.FromSeconds(1)};
        readonly string jobDirectory;
        Process process;
        bool checking,loginMode,ready,attached;
        string previousLog="";
        public bool Busy {get{return process!=null||attached;}}
        public string JobDirectory {get{return jobDirectory;}}
        static Brush B(string hex){return new SolidColorBrush((Color)ColorConverter.ConvertFromString(hex));}
        public WorkerWindow(string job){
            jobDirectory=job;Title="AI worker - Agentic Studio";Width=860;Height=780;MinWidth=650;MinHeight=560;Background=B("#141a1d");Foreground=B("#e4e7de");WindowStartupLocation=WindowStartupLocation.CenterOwner;
            MaxHeight=SystemParameters.WorkArea.Height-35;MaxWidth=SystemParameters.WorkArea.Width-35;
            var top=new StackPanel{Margin=new Thickness(28)};Content=new ScrollViewer{Content=top,VerticalScrollBarVisibility=ScrollBarVisibility.Auto};
            top.Children.Add(new TextBlock{Text="YOUR AI WORKSPACE",FontSize=10,Foreground=B("#dfbd7e"),Margin=new Thickness(0,0,0,10)});
            top.Children.Add(new TextBlock{Text="Let your agents take it from here.",FontSize=27,FontWeight=FontWeights.SemiBold,TextWrapping=TextWrapping.Wrap});
            top.Children.Add(new TextBlock{Text="Connect your account, start your task, and follow the work here.",Foreground=B("#a8b5ae"),TextWrapping=TextWrapping.Wrap,Margin=new Thickness(0,10,0,22)});
            connection.Text="Checking your account...";connection.TextWrapping=TextWrapping.Wrap;connection.Foreground=B("#dfbd7e");top.Children.Add(connection);
            signInCard.Margin=new Thickness(0,18,0,18);signInCard.Children.Add(new TextBlock{Text="1  Connect your account",FontSize=17,FontWeight=FontWeights.SemiBold});
            signInCard.Children.Add(new TextBlock{Text="Sign in once with ChatGPT. When a code appears, open the sign-in page and enter it. Keep this window open while you finish.",TextWrapping=TextWrapping.Wrap,Foreground=B("#a8b5ae"),Margin=new Thickness(0,8,0,12)});
            var authButtons=new WrapPanel();Configure(login,"Connect account",SignIn);System.Windows.Automation.AutomationProperties.SetName(login,"Sign in");authButtons.Children.Add(login);var browser=new Button();Configure(browser,"Open sign-in page",delegate{Process.Start(new ProcessStartInfo("https://auth.openai.com/codex/device"){UseShellExecute=true});});authButtons.Children.Add(browser);signInCard.Children.Add(authButtons);
            deviceCode.IsReadOnly=true;deviceCode.Background=B("#0b1013");deviceCode.Foreground=B("#dfbd7e");deviceCode.FontSize=22;deviceCode.FontFamily=new FontFamily("Consolas");deviceCode.Padding=new Thickness(12);deviceCode.Text="Your code will appear here";deviceCode.Margin=new Thickness(0,10,0,8);signInCard.Children.Add(deviceCode);
            var copyCode=new Button();Configure(copyCode,"Copy sign-in code",delegate{if(deviceCode.Tag!=null)Clipboard.SetText(deviceCode.Tag.ToString());});signInCard.Children.Add(copyCode);top.Children.Add(new Border{Child=signInCard,Background=B("#192326"),CornerRadius=new CornerRadius(10),Padding=new Thickness(18),Margin=new Thickness(0,16,0,16)});
            top.Children.Add(new TextBlock{Text="2  Start your task",FontSize=17,FontWeight=FontWeights.SemiBold,Margin=new Thickness(0,14,0,12)});
            top.Children.Add(new TextBlock{Text=String.IsNullOrEmpty(job)?"No task selected. Create or select one in the main window.":"Task: "+Path.GetFileName(job),TextWrapping=TextWrapping.Wrap,Foreground=B("#a8b5ae"),Margin=new Thickness(0,0,0,10)});
            status.Text="Ready when you are.";status.TextWrapping=TextWrapping.Wrap;top.Children.Add(status);
            var controls=new WrapPanel{Margin=new Thickness(0,14,0,8)};top.Children.Add(controls);Configure(start,"Start / continue",Start);start.Background=B("#dfbd7e");start.Foreground=B("#0b1013");start.FontSize=14;start.FontWeight=FontWeights.SemiBold;controls.Children.Add(start);Configure(pause,"Pause after current agent",delegate{Send("pause");status.Text="Pausing after the current agent finishes.";pause.IsEnabled=false;});controls.Children.Add(pause);Configure(stop,"Stop worker",Stop);controls.Children.Add(stop);
            top.Children.Add(new TextBlock{Text="Pause lets the current agent finish. Stop preserves partial work so you can review it later.",TextWrapping=TextWrapping.Wrap,Foreground=B("#a8b5ae"),FontSize=11,Margin=new Thickness(0,0,0,20)});
            top.Children.Add(new TextBlock{Text="3  Follow the progress",FontSize=17,FontWeight=FontWeights.SemiBold,Margin=new Thickness(0,0,0,12)});
            log.IsReadOnly=true;log.AcceptsReturn=true;log.TextWrapping=TextWrapping.Wrap;log.VerticalScrollBarVisibility=ScrollBarVisibility.Auto;log.FontFamily=new FontFamily("Consolas");log.FontSize=12;log.Background=B("#0b1013");log.Foreground=B("#d3d8e1");log.Padding=new Thickness(14);log.Height=240;log.Text="Your agents' updates will appear here after you start.";System.Windows.Automation.AutomationProperties.SetName(log,"AI worker live log");top.Children.Add(log);
            var advanced=new StackPanel();advanced.Children.Add(new TextBlock{Text="Engine location (usually detected automatically)",Margin=new Thickness(0,10,0,8),Foreground=B("#a8b5ae")});enginePath.IsReadOnly=true;enginePath.Background=B("#0b1013");enginePath.Foreground=Foreground;enginePath.Padding=new Thickness(10);System.Windows.Automation.AutomationProperties.SetName(enginePath,"Codex engine path");advanced.Children.Add(enginePath);
            string settings=Path.Combine(Data.Root,"desktop","worker-settings.json");if(File.Exists(settings)){try{enginePath.Text=Data.Get(Data.Read(settings),"engine_path");}catch{}}
            var options=new WrapPanel{Margin=new Thickness(0,12,0,8)};advanced.Children.Add(options);Configure(browse,"Choose engine",delegate{var picker=new OpenFileDialog{Title="Select Codex engine",Filter="Codex executable|codex.exe|Executable files|*.exe",CheckFileExists=true};if(picker.ShowDialog(this)==true){enginePath.Text=picker.FileName;SaveSettings();CheckConnection();}});options.Children.Add(browse);Configure(check,"Check connection",CheckConnection);options.Children.Add(check);
            Configure(recover,"Recover interrupted stage",delegate{if(MessageBox.Show(this,"Only recover if no other agent is working on this task. All partial files will be kept. Continue?","Recover interrupted stage",MessageBoxButton.YesNo)==MessageBoxResult.Yes)RunControl("recover","--job",jobDirectory);});advanced.Children.Add(recover);
            top.Children.Add(new Expander{Header="Advanced settings & recovery",Content=advanced,Foreground=B("#a8b5ae"),Margin=new Thickness(0,22,0,8)});
            monitor.Tick+=delegate{PollExistingWorker();};Loaded+=delegate{PollExistingWorker();CheckConnection();monitor.Start();};Closed+=delegate{monitor.Stop();};Closing+=delegate(object sender,System.ComponentModel.CancelEventArgs e){if(Busy){e.Cancel=true;Hide();}};UpdateButtons();
        }
        void Configure(Button button,string title,Action action){
            button.Content=title;button.Padding=new Thickness(16,11,16,11);button.Margin=new Thickness(0,0,10,8);button.Background=B("#2a3638");button.Foreground=B("#eef2ed");button.BorderBrush=B("#485654");button.BorderThickness=new Thickness(1);button.Cursor=System.Windows.Input.Cursors.Hand;
            var template=new ControlTemplate(typeof(Button));var border=new FrameworkElementFactory(typeof(Border));border.SetValue(Border.CornerRadiusProperty,new CornerRadius(7));foreach(var property in new[]{"Background","BorderBrush","BorderThickness","Padding"})border.SetBinding(property=="Background"?Border.BackgroundProperty:property=="BorderBrush"?Border.BorderBrushProperty:property=="Padding"?Border.PaddingProperty:Border.BorderThicknessProperty,new System.Windows.Data.Binding(property){RelativeSource=new System.Windows.Data.RelativeSource(System.Windows.Data.RelativeSourceMode.TemplatedParent)});var content=new FrameworkElementFactory(typeof(ContentPresenter));content.SetValue(ContentPresenter.HorizontalAlignmentProperty,HorizontalAlignment.Center);border.AppendChild(content);template.VisualTree=border;button.Template=template;
            Brush background=null,foreground=null;button.IsEnabledChanged+=delegate{if(!button.IsEnabled){background=button.Background;foreground=button.Foreground;button.Background=B("#20292b");button.Foreground=B("#9daaa5");}else if(background!=null){button.Background=background;button.Foreground=foreground;}};
            button.Click+=delegate{try{action();}catch(Exception error){Append(error.Message);}};
        }
        void UpdateButtons(){start.IsEnabled=ready&&!checking&&!Busy&&!String.IsNullOrEmpty(jobDirectory);pause.IsEnabled=Busy&&!loginMode;stop.IsEnabled=Busy;check.IsEnabled=!Busy&&!checking;login.IsEnabled=!Busy&&!checking;browse.IsEnabled=!Busy&&!checking;((FrameworkElement)signInCard.Parent).Visibility=ready&&!loginMode?Visibility.Collapsed:Visibility.Visible;recover.IsEnabled=!Busy&&!checking&&!String.IsNullOrEmpty(jobDirectory);}
        void PollExistingWorker(){
            if(process!=null||String.IsNullOrEmpty(jobDirectory))return;attached=false;
            try{string file=Path.Combine(jobDirectory,"worker-status.json"),lockFile=Path.Combine(Data.Root,"desktop","worker-runtime.lock");if(File.Exists(file)){var saved=Data.Read(file);status.Text=Data.Get(saved,"message");if(File.Exists(lockFile)){var owner=Data.Read(lockFile);if(String.Equals(Data.Get(owner,"job"),jobDirectory,StringComparison.OrdinalIgnoreCase)){int pid;if(Int32.TryParse(Data.Get(owner,"pid"),out pid)){try{using(var existing=Process.GetProcessById(pid))attached=!existing.HasExited;}catch{}}}}}string events=Path.Combine(jobDirectory,"worker-events.jsonl");if(File.Exists(events)){string text=File.ReadAllText(events);if(text!=previousLog){previousLog=text;log.Text=text.Length>100000?text.Substring(text.Length-100000):text;log.ScrollToEnd();}}}catch{}UpdateButtons();
        }
        void RunControl(params string[] arguments){ThreadPool.QueueUserWorkItem(delegate{try{using(var child=Process.Start(Info(arguments))){string output=child.StandardOutput.ReadToEnd();child.WaitForExit();Append(output);}}catch(Exception error){Append(error.Message);}});}
        void Append(string message){if(!Dispatcher.CheckAccess()){Dispatcher.BeginInvoke(new Action<string>(Append),message);return;}if(loginMode){var code=Regex.Match(message,@"\b[A-Z0-9]{4,6}-[A-Z0-9]{4,6}\b");if(code.Success){deviceCode.Text=code.Value;deviceCode.Tag=code.Value;}}log.AppendText(message.TrimEnd()+Environment.NewLine);if(log.Text.Length>160000)log.Text=log.Text.Substring(log.Text.Length-100000);log.ScrollToEnd();}
        void SaveSettings(){Data.Save(Path.Combine(Data.Root,"desktop","worker-settings.json"),new Dictionary<string,object>{{"engine_path",enginePath.Text.Trim()}});ready=false;}
        ProcessStartInfo Info(params string[] arguments){return new ProcessStartInfo("node.exe",Data.Quote(Path.Combine(Data.Root,"scripts","desktop-worker.mjs"))+" "+String.Join(" ",Array.ConvertAll(arguments,Data.Quote))){WorkingDirectory=Data.Root,UseShellExecute=false,CreateNoWindow=true,RedirectStandardOutput=true,RedirectStandardError=true,RedirectStandardInput=true,StandardOutputEncoding=Encoding.UTF8,StandardErrorEncoding=Encoding.UTF8};}
        public void CheckConnection(){
            if(Busy||checking)return;checking=true;ready=false;connection.Text="Checking engine and account...";UpdateButtons();
            ThreadPool.QueueUserWorkItem(delegate{
                string output="",error="";int exit=-1;
                try{using(var child=Process.Start(Info("doctor"))){var stderr=new StringBuilder();child.ErrorDataReceived+=delegate(object sender,DataReceivedEventArgs e){if(e.Data!=null)stderr.AppendLine(e.Data);};child.BeginErrorReadLine();output=child.StandardOutput.ReadToEnd();child.WaitForExit();exit=child.ExitCode;error=stderr.ToString();}}
                catch(Exception exception){error=exception.Message;}
                Dispatcher.BeginInvoke(new Action(delegate{checking=false;try{var result=new JavaScriptSerializer().Deserialize<Dictionary<string,object>>(output.Trim());if(exit==0){ready=result.ContainsKey("signed_in")&&Convert.ToBoolean(result["signed_in"]);connection.Text=ready?"Connected - your account is ready.":"Connect your ChatGPT account to start.";if(enginePath.Text=="")enginePath.ToolTip=Data.Get(result,"engine");}else connection.Text=Data.Get(result,"message");}catch{connection.Text=error==""?"Could not check engine. Choose codex.exe and try again.":error;}UpdateButtons();}));
            });
        }
        void Start(){if(!ready||Busy||String.IsNullOrEmpty(jobDirectory))return;Begin(false,"run","--job",jobDirectory);}
        void SignIn(){if(Busy)return;Append("Follow the device sign-in instructions below. Sign-in codes are not saved to task logs.");Begin(true,"login");}
        void Begin(bool auth,params string[] arguments){
            if(Busy)return;loginMode=auth;process=new Process{StartInfo=Info(arguments),EnableRaisingEvents=true};var active=process;
            active.OutputDataReceived+=delegate(object sender,DataReceivedEventArgs e){if(e.Data==null)return;try{var item=new JavaScriptSerializer().Deserialize<Dictionary<string,object>>(e.Data);string message=Data.Get(item,"message");if(message!="")Append(message);if(Data.Get(item,"type")=="status")Dispatcher.BeginInvoke(new Action(delegate{status.Text=message;}));}catch{Append(e.Data);}};
            active.ErrorDataReceived+=delegate(object sender,DataReceivedEventArgs e){if(e.Data!=null)Append(e.Data);};
            active.Exited+=delegate{int code;try{active.WaitForExit();code=active.ExitCode;}catch{code=-1;}Dispatcher.BeginInvoke(new Action(delegate{if(process!=active)return;process=null;active.Dispose();Append("Worker process ended (exit "+code+").");if(loginMode){loginMode=false;CheckConnection();}else{if(status.Text.StartsWith("Selected task:")||status.Text=="Starting worker...")status.Text=code==0?"Worker finished. Check the task progress.":"Worker needs attention. Review the log and task status.";UpdateButtons();}}));};
            try{active.Start();active.BeginOutputReadLine();active.BeginErrorReadLine();status.Text=auth?"Waiting for sign-in...":"Starting worker...";UpdateButtons();}catch{process=null;active.Dispose();UpdateButtons();throw;}
        }
        void Send(string command){if(process==null){if(attached)RunControl("control","--job",jobDirectory,"--action",command);return;}if(process.HasExited)return;process.StandardInput.WriteLine("{\"command\":\""+command+"\"}");process.StandardInput.Flush();}
        void Stop(){if(process==null&&!attached)return;if(loginMode){process.Kill();return;}Send("stop");stop.IsEnabled=false;pause.IsEnabled=false;status.Text="Stopping worker and preserving partial work...";}
    }
}
