using System;
using System.Collections;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace AgenticStudio {
    public class PublishingEditor : StackPanel {
        class LinkRow { public TextBox Url,Label,Placement; public Border Card; }
        readonly List<LinkRow> links=new List<LinkRow>();
        readonly StackPanel linkCards=new StackPanel(),blogFields=new StackPanel();
        readonly CheckBox blogs=new CheckBox();
        readonly TextBox topics,count,path;
        readonly Func<string,Action,Button> button;
        readonly Button add;
        static Brush B(string color){return new SolidColorBrush((Color)ColorConverter.ConvertFromString(color));}
        public PublishingEditor(Dictionary<string,object> input,Func<string,Action,Button> makeButton){
            button=makeButton;Margin=new Thickness(0,22,0,0);
            Label(this,"AFFILIATE LINKS",true);Label(this,"Add destinations and choose auto placement or specify a page / section. Blank URLs are ignored.",false);Children.Add(linkCards);
            add=button("Add affiliate link",delegate{AddLink(null);});Children.Add(add);
            if(input.ContainsKey("affiliate_links")&&input["affiliate_links"] is IEnumerable){foreach(object item in (IEnumerable)input["affiliate_links"]){var link=item as Dictionary<string,object>;if(link!=null)AddLink(link);}}
            if(links.Count==0&&!String.IsNullOrWhiteSpace(Data.Get(input,"affiliate_url")))AddLink(new Dictionary<string,object>{{"url",Data.Get(input,"affiliate_url")},{"label",Data.Get(input,"affiliate_label")},{"placement",Data.Get(input,"affiliate_placement")}});
            if(links.Count==0)AddLink(null);
            Label(this,"BLOG AGENT",true);blogs.Content="Create blog posts for this task";blogs.Foreground=B("#e4e7de");blogs.Margin=new Thickness(0,8,0,12);blogs.IsChecked=input.ContainsKey("blog_enabled")&&Convert.ToBoolean(input["blog_enabled"]);System.Windows.Automation.AutomationProperties.SetName(blogs,"Create blog posts");Children.Add(blogs);Children.Add(blogFields);
            Label(blogFields,"Topics or titles: one per line. Leave empty for the agent to research topics.",false);topics=Input(Data.Get(input,"blog_topics"),"Blog topics",true);blogFields.Children.Add(topics);
            Label(blogFields,"Number of posts (1–20). Topic lines must not exceed this count.",false);count=Input(Data.Get(input,"blog_post_count")==""?"3":Data.Get(input,"blog_post_count"),"Blog post count",false);blogFields.Children.Add(count);
            Label(blogFields,"Blog section path",false);path=Input(Data.Get(input,"blog_path")==""?"/blog/":Data.Get(input,"blog_path"),"Blog path",false);blogFields.Children.Add(path);
            Label(blogFields,"The agent researches topics, writes posts, builds a blog index, adds internal links and metadata, and checks the output. Use Content writer below for your own exact text. Publishing requires separate authorization.",false);
            blogs.Checked+=delegate{blogFields.Visibility=Visibility.Visible;};blogs.Unchecked+=delegate{blogFields.Visibility=Visibility.Collapsed;};blogFields.Visibility=blogs.IsChecked==true?Visibility.Visible:Visibility.Collapsed;
        }
        void Label(StackPanel panel,string text,bool heading){panel.Children.Add(new TextBlock{Text=text,TextWrapping=TextWrapping.Wrap,FontSize=heading?10:11,Foreground=B(heading?"#dfbd7e":"#a1afa3"),Margin=new Thickness(0,heading?18:8,0,7)});}
        TextBox Input(string text,string name,bool multiline){var box=new TextBox{Text=text,Background=B("#0e1418"),Foreground=B("#e4e7de"),BorderBrush=B("#34413a"),Padding=new Thickness(10),Margin=new Thickness(0,0,0,8),FontSize=12};if(multiline){box.AcceptsReturn=true;box.Height=100;box.TextWrapping=TextWrapping.Wrap;box.VerticalScrollBarVisibility=ScrollBarVisibility.Auto;}System.Windows.Automation.AutomationProperties.SetName(box,name);return box;}
        void AddLink(Dictionary<string,object> input){
            if(links.Count>=20)return;var row=new LinkRow();var body=new StackPanel();row.Card=new Border{Child=body,BorderBrush=B("#34413a"),BorderThickness=new Thickness(1),Padding=new Thickness(14),Margin=new Thickness(0,5,0,10)};
            Label(body,"Destination URL (http:// or https://)",false);row.Url=Input(input==null?"":Data.Get(input,"url"),"Affiliate URL",false);body.Children.Add(row.Url);
            Label(body,"Button / link text",false);row.Label=Input(input==null?"":Data.Get(input,"label"),"Affiliate label",false);body.Children.Add(row.Label);
            Label(body,"Placement: auto or page / section",false);row.Placement=Input(input==null||Data.Get(input,"placement")==""?"auto":Data.Get(input,"placement"),"Affiliate placement",false);body.Children.Add(row.Placement);
            body.Children.Add(button("Remove link",delegate{linkCards.Children.Remove(row.Card);links.Remove(row);add.IsEnabled=links.Count<20;}));links.Add(row);linkCards.Children.Add(row.Card);if(add!=null)add.IsEnabled=links.Count<20;
        }
        public Dictionary<string,object> Collect(){
            var result=new List<Dictionary<string,object>>();
            foreach(var row in links){string url=row.Url.Text.Trim();if(url=="")continue;Uri parsed;if(!Uri.TryCreate(url,UriKind.Absolute,out parsed)||(parsed.Scheme!="https"&&parsed.Scheme!="http")||!String.IsNullOrEmpty(parsed.UserInfo))throw new Exception("Each affiliate link must be an absolute HTTP(S) URL without embedded credentials.");result.Add(new Dictionary<string,object>{{"url",url},{"label",row.Label.Text.Trim()},{"placement",String.IsNullOrWhiteSpace(row.Placement.Text)?"auto":row.Placement.Text.Trim()}});}
            bool enabled=blogs.IsChecked==true;int number;if(!Int32.TryParse(count.Text,out number)||number<1||number>20){if(enabled)throw new Exception("Choose a blog post count from 1 to 20.");number=3;}
            string destination=path.Text.Trim();if(enabled&&(!destination.StartsWith("/")||destination.StartsWith("//")||destination.Contains("..")||destination.IndexOfAny(new[]{'?', '#', '\\', ':'})>=0))throw new Exception("Use a local blog path such as /blog/, without query strings or parent paths.");
            string topicText=topics.Text.Trim();if(enabled&&topicText.Split(new[]{'\r','\n'},StringSplitOptions.RemoveEmptyEntries).Length>number)throw new Exception("Increase the post count to cover all topic lines, or remove extra topics.");
            var first=result.Count==0?new Dictionary<string,object>{{"url",""},{"label",""},{"placement","auto"}}:result[0];
            return new Dictionary<string,object>{{"affiliate_links",result},{"affiliate_url",first["url"]},{"affiliate_label",first["label"]},{"affiliate_placement",first["placement"]},{"blog_enabled",enabled},{"blog_topics",topicText},{"blog_post_count",number},{"blog_path",destination==""?"/blog/":destination}};
        }
        public static string SelfCheck(){
            Func<string,Action,Button> factory=(label,action)=>new Button{Content=label};
            string url="https://example.com/offer?ref=owner&campaign=blog%20one";
            var editor=new PublishingEditor(new Dictionary<string,object>{{"affiliate_url",url},{"affiliate_label","Read offer"},{"affiliate_placement","/blog/example/ end"}},factory);
            var saved=editor.Collect();var list=(List<Dictionary<string,object>>)saved["affiliate_links"];
            if(list.Count!=1||Data.Get(list[0],"url")!=url)throw new Exception("Legacy URL migration changed tracking parameters.");
            editor.AddLink(new Dictionary<string,object>{{"url","https://example.org/second"},{"label","Second"},{"placement","auto"}});
            editor.blogs.IsChecked=true;editor.count.Text="2";editor.topics.Text="First topic\r\nSecond topic";
            var serialized=new JavaScriptSerializerForPublishing().RoundTrip(editor.Collect());
            var restored=new PublishingEditor(serialized,factory);var roundTrip=restored.Collect();
            if(((List<Dictionary<string,object>>)roundTrip["affiliate_links"]).Count!=2||!Convert.ToBoolean(roundTrip["blog_enabled"])||Convert.ToInt32(roundTrip["blog_post_count"])!=2||Data.Get(roundTrip,"blog_topics")!="First topic\r\nSecond topic")throw new Exception("Publishing settings did not survive a JSON round trip.");
            editor.links[0].Url.Text="javascript:alert(1)";bool rejected=false;try{editor.Collect();}catch{rejected=true;}if(!rejected)throw new Exception("Unsafe URL accepted.");editor.links[0].Url.Text=url;
            editor.count.Text="1";rejected=false;try{editor.Collect();}catch{rejected=true;}if(!rejected)throw new Exception("Excess topic lines silently dropped.");editor.count.Text="2";
            editor.path.Text="/../";rejected=false;try{editor.Collect();}catch{rejected=true;}if(!rejected)throw new Exception("Parent blog path accepted.");editor.path.Text="/blog/";
            editor.links.Clear();if(Data.Get(editor.Collect(),"affiliate_url")!="")throw new Exception("Removing links retained a stale destination.");
            return "PASS: legacy migration, multiple links, exact tracking URL, blog settings JSON round trip, unsafe URL rejection, topic/count conflict, path validation, and removing links.";
        }
        class JavaScriptSerializerForPublishing {
            public Dictionary<string,object> RoundTrip(Dictionary<string,object> value){var json=new System.Web.Script.Serialization.JavaScriptSerializer();return json.Deserialize<Dictionary<string,object>>(json.Serialize(value));}
        }
    }
}
