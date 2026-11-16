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
using Microsoft.Win32;

namespace AgenticStudio {
    public class WorkerWindow : Window {
        readonly TextBox log=new TextBox(),enginePath=new TextBox();
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
            var grid=new Grid{Margin=new Thickness(24)};Content=grid;grid.RowDefinitions.Add(new RowDefinition{Height=GridLength.Auto});grid.RowDefinitions.Add(new RowDefinition{Height=new GridLength(1,GridUnitType.Star)});
            var top=new StackPanel();grid.Children.Add(top);top.Children.Add(new TextBlock{Text="Run your agents here",FontSize=25,Margin=new Thickness(0,0,0,10)});
            top.Children.Add(new TextBlock{Text="No VS Code window is needed. The signed-in Codex engine runs each role separately and passes verified work to the next agent.",TextWrapping=TextWrapping.Wrap,Foreground=B("#a1afa3"),Margin=new Thickness(0,0,0,14)});
            connection.Text="Checking engine...";connection.TextWrapping=TextWrapping.Wrap;connection.Foreground=B("#dfbd7e");top.Children.Add(connection);
            top.Children.Add(new TextBlock{Text="Codex executable (leave empty to detect automatically)",Margin=new Thickness(0,14,0,6),FontSize=11});enginePath.Background=B("#0e1418");enginePath.Foreground=Foreground;enginePath.Padding=new Thickness(9);enginePath.IsReadOnly=true;System.Windows.Automation.AutomationProperties.SetName(enginePath,"Codex engine path");top.Children.Add(enginePath);
            string settings=Path.Combine(Data.Root,"desktop","worker-settings.json");if(File.Exists(settings)){try{enginePath.Text=Data.Get(Data.Read(settings),"engine_path");}catch{}}
            var options=new WrapPanel{Margin=new Thickness(0,9,0,12)};top.Children.Add(options);Configure(browse,"Choose engine",delegate{var picker=new OpenFileDialog{Title="Select Codex engine",Filter="Codex executable|codex.exe|Executable files|*.exe",CheckFileExists=true};if(picker.ShowDialog(this)==true){enginePath.Text=picker.FileName;SaveSettings();CheckConnection();}});options.Children.Add(browse);Configure(check,"Check connection",CheckConnection);options.Children.Add(check);Configure(login,"Sign in",SignIn);options.Children.Add(login);
            status.Text=String.IsNullOrEmpty(job)?"Create or select a task to start.":"Selected task: "+Path.GetFileName(job);status.TextWrapping=TextWrapping.Wrap;top.Children.Add(status);
            var controls=new WrapPanel{Margin=new Thickness(0,12,0,9)};top.Children.Add(controls);Configure(start,"Start / continue",Start);start.Background=B("#dfbd7e");start.Foreground=B("#0b1013");controls.Children.Add(start);Configure(pause,"Pause after current agent",delegate{Send("pause");status.Text="Pause requested. The current agent will finish first.";pause.IsEnabled=false;});controls.Children.Add(pause);Configure(stop,"Stop worker",Stop);controls.Children.Add(stop);
            Configure(recover,"Recover interrupted stage",delegate{if(MessageBox.Show(this,"Only recover if no other agent is working on this task. This marks the interrupted stage as failed for review and preserves all files. Continue?","Recover interrupted stage",MessageBoxButton.YesNo,MessageBoxImage.Question)==MessageBoxResult.Yes)RunControl("recover","--job",jobDirectory);});controls.Children.Add(recover);
            top.Children.Add(new TextBlock{Text="Pause finishes the active role. Stop interrupts it and preserves partial files. Failed stages require review and Retry in the task panel. Deployment still follows the task's authorization.",FontSize=11,TextWrapping=TextWrapping.Wrap,Foreground=B("#a1afa3"),Margin=new Thickness(0,0,0,12)});
            log.IsReadOnly=true;log.AcceptsReturn=true;log.TextWrapping=TextWrapping.Wrap;log.VerticalScrollBarVisibility=ScrollBarVisibility.Auto;log.FontFamily=new FontFamily("Consolas");log.FontSize=11;log.Background=B("#0b1013");log.Foreground=B("#d3d8e1");log.Padding=new Thickness(12);System.Windows.Automation.AutomationProperties.SetName(log,"AI worker live log");Grid.SetRow(log,1);grid.Children.Add(log);
            monitor.Tick+=delegate{PollExistingWorker();};Loaded+=delegate{PollExistingWorker();CheckConnection();monitor.Start();};Closed+=delegate{monitor.Stop();};Closing+=delegate(object sender,System.ComponentModel.CancelEventArgs e){if(Busy){e.Cancel=true;Hide();}};UpdateButtons();
        }
        void Configure(Button button,string title,Action action){button.Content=title;button.Padding=new Thickness(12,8,12,8);button.Margin=new Thickness(0,0,8,5);button.Background=B("#283234");button.Foreground=Foreground;button.Click+=delegate{try{action();}catch(Exception error){Append(error.Message);}};}
        void UpdateButtons(){start.IsEnabled=ready&&!checking&&!Busy&&!String.IsNullOrEmpty(jobDirectory);pause.IsEnabled=Busy&&!loginMode;stop.IsEnabled=Busy;check.IsEnabled=!Busy&&!checking;login.IsEnabled=!Busy&&!checking;browse.IsEnabled=!Busy&&!checking;recover.IsEnabled=!Busy&&!checking&&!String.IsNullOrEmpty(jobDirectory);}
        void PollExistingWorker(){
            if(process!=null||String.IsNullOrEmpty(jobDirectory))return;attached=false;
            try{string file=Path.Combine(jobDirectory,"worker-status.json"),lockFile=Path.Combine(Data.Root,"desktop","worker-runtime.lock");if(File.Exists(file)){var saved=Data.Read(file);status.Text=Data.Get(saved,"message");if(File.Exists(lockFile)){var owner=Data.Read(lockFile);if(String.Equals(Data.Get(owner,"job"),jobDirectory,StringComparison.OrdinalIgnoreCase)){int pid;if(Int32.TryParse(Data.Get(owner,"pid"),out pid)){try{using(var existing=Process.GetProcessById(pid))attached=!existing.HasExited;}catch{}}}}}string events=Path.Combine(jobDirectory,"worker-events.jsonl");if(File.Exists(events)){string text=File.ReadAllText(events);if(text!=previousLog){previousLog=text;log.Text=text.Length>100000?text.Substring(text.Length-100000):text;log.ScrollToEnd();}}}catch{}UpdateButtons();
        }
        void RunControl(params string[] arguments){ThreadPool.QueueUserWorkItem(delegate{try{using(var child=Process.Start(Info(arguments))){string output=child.StandardOutput.ReadToEnd();child.WaitForExit();Append(output);}}catch(Exception error){Append(error.Message);}});}
        void Append(string message){if(!Dispatcher.CheckAccess()){Dispatcher.BeginInvoke(new Action<string>(Append),message);return;}log.AppendText(message.TrimEnd()+Environment.NewLine);if(log.Text.Length>160000)log.Text=log.Text.Substring(log.Text.Length-100000);log.ScrollToEnd();}
        void SaveSettings(){Data.Save(Path.Combine(Data.Root,"desktop","worker-settings.json"),new Dictionary<string,object>{{"engine_path",enginePath.Text.Trim()}});ready=false;}
        ProcessStartInfo Info(params string[] arguments){return new ProcessStartInfo("node.exe",Data.Quote(Path.Combine(Data.Root,"scripts","desktop-worker.mjs"))+" "+String.Join(" ",Array.ConvertAll(arguments,Data.Quote))){WorkingDirectory=Data.Root,UseShellExecute=false,CreateNoWindow=true,RedirectStandardOutput=true,RedirectStandardError=true,RedirectStandardInput=true,StandardOutputEncoding=Encoding.UTF8,StandardErrorEncoding=Encoding.UTF8};}
        public void CheckConnection(){
            if(Busy||checking)return;checking=true;ready=false;connection.Text="Checking engine and account...";UpdateButtons();
            ThreadPool.QueueUserWorkItem(delegate{
                string output="",error="";int exit=-1;
                try{using(var child=Process.Start(Info("doctor"))){var stderr=new StringBuilder();child.ErrorDataReceived+=delegate(object sender,DataReceivedEventArgs e){if(e.Data!=null)stderr.AppendLine(e.Data);};child.BeginErrorReadLine();output=child.StandardOutput.ReadToEnd();child.WaitForExit();exit=child.ExitCode;error=stderr.ToString();}}
                catch(Exception exception){error=exception.Message;}
                Dispatcher.BeginInvoke(new Action(delegate{checking=false;try{var result=new JavaScriptSerializer().Deserialize<Dictionary<string,object>>(output.Trim());if(exit==0){ready=result.ContainsKey("signed_in")&&Convert.ToBoolean(result["signed_in"]);connection.Text=Data.Get(result,"message")+"  "+Data.Get(result,"version");if(enginePath.Text=="")enginePath.ToolTip=Data.Get(result,"engine");}else connection.Text=Data.Get(result,"message");}catch{connection.Text=error==""?"Could not check engine. Choose codex.exe and try again.":error;}UpdateButtons();}));
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
