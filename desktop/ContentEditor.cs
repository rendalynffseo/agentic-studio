using System;
using System.Collections;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace AgenticStudio {
    public class ContentEditor : StackPanel {
        readonly ComboBox mode=new ComboBox();
        readonly StackPanel cards=new StackPanel();
        readonly TextBlock hint=new TextBlock();
        readonly List<ContentRow> rows=new List<ContentRow>();
        readonly Func<string,Action,Button> makeButton;
        readonly Button add;
        int nextNumber;
        class ContentRow { public string Id;public Border Card;public TextBox Label,Text,Page,Section; }
        static Brush B(string color){return new SolidColorBrush((Color)ColorConverter.ConvertFromString(color));}
        public ContentEditor(Dictionary<string,object> input,Func<string,Action,Button> buttonFactory){
            makeButton=buttonFactory;Margin=new Thickness(0,22,0,0);
            Children.Add(new TextBlock{Text="CONTENT WRITER",FontSize=10,Foreground=B("#dfbd7e"),Margin=new Thickness(0,0,0,10)});
            mode.Items.Add(new ComboBoxItem{Content="Agent writes content",Tag="agent"});mode.Items.Add(new ComboBoxItem{Content="Use my exact content",Tag="provided"});mode.Items.Add(new ComboBoxItem{Content="My content + agent fills gaps",Tag="hybrid"});
            mode.Foreground=B("#e4e7de");mode.Margin=new Thickness(0,0,0,10);System.Windows.Automation.AutomationProperties.SetName(mode,"Content source");Children.Add(mode);
            hint.Foreground=B("#a1afa3");hint.FontSize=11;hint.TextWrapping=TextWrapping.Wrap;hint.LineHeight=18;hint.Margin=new Thickness(0,0,0,14);Children.Add(hint);Children.Add(cards);
            add=makeButton("Add content block",delegate{AddRow(null);});add.HorizontalAlignment=HorizontalAlignment.Left;add.Margin=new Thickness(0,2,0,0);Children.Add(add);
            if(input.ContainsKey("content_blocks")&&input["content_blocks"] is IEnumerable){foreach(object item in (IEnumerable)input["content_blocks"]){var block=item as Dictionary<string,object>;if(block!=null)AddRow(block);}}
            if(rows.Count==0)AddRow(null);
            string value=Data.Get(input,"content_mode");mode.SelectedIndex=value=="provided"?1:value=="hybrid"?2:0;
            mode.SelectionChanged+=delegate{UpdateMode();};UpdateMode();
        }
        TextBox Input(string text,string name,bool multiline){
            var box=new TextBox{Text=text,Foreground=B("#e4e7de"),Background=B("#0e1418"),BorderBrush=B("#34413a"),Padding=new Thickness(10),FontSize=12,CaretBrush=B("#dfbd7e"),Margin=new Thickness(0,6,0,13)};
            if(multiline){box.AcceptsReturn=true;box.AcceptsTab=true;box.Height=165;box.MaxLength=200000;box.TextWrapping=TextWrapping.Wrap;box.VerticalScrollBarVisibility=ScrollBarVisibility.Auto;box.FontFamily=new FontFamily("Consolas");}
            System.Windows.Automation.AutomationProperties.SetName(box,name);return box;
        }
        void Label(StackPanel panel,string text){panel.Children.Add(new TextBlock{Text=text,Foreground=B("#a1afa3"),FontSize=11,TextWrapping=TextWrapping.Wrap});}
        void AddRow(Dictionary<string,object> block){
            if(rows.Count>=20)return;int number=++nextNumber;
            var row=new ContentRow();row.Id=block==null?"block-"+Guid.NewGuid().ToString("N"):Data.Get(block,"id");if(row.Id=="")row.Id="block-"+Guid.NewGuid().ToString("N");
            var placement=block!=null&&block.ContainsKey("placement")?block["placement"] as Dictionary<string,object>:null;
            var body=new StackPanel();row.Card=new Border{Background=B("#1a2326"),BorderBrush=B("#34413a"),BorderThickness=new Thickness(1),CornerRadius=new CornerRadius(7),Padding=new Thickness(17),Margin=new Thickness(0,0,0,14),Child=body};
            var header=new DockPanel{Margin=new Thickness(0,0,0,13)};var remove=makeButton("Remove block "+number,delegate{cards.Children.Remove(row.Card);rows.Remove(row);add.IsEnabled=rows.Count<20;});remove.FontSize=10;remove.Padding=new Thickness(8,5,8,5);DockPanel.SetDock(remove,Dock.Right);header.Children.Add(remove);header.Children.Add(new TextBlock{Text="CONTENT BLOCK "+number,FontSize=10,Foreground=B("#dfbd7e"),VerticalAlignment=VerticalAlignment.Center});body.Children.Add(header);
            Label(body,"Label (for example: Hero heading, About us, or FAQ answer)");row.Label=Input(block==null?"":Data.Get(block,"label"),"Content label "+number,false);body.Children.Add(row.Label);
            Label(body,"Your exact content");row.Text=Input(block==null?"":Data.Get(block,"text"),"Exact content "+number,true);body.Children.Add(row.Text);
            Label(body,"Target page: auto, /, /about/, or another page path");row.Page=Input(placement==null?"auto":Data.Get(placement,"page"),"Target page "+number,false);body.Children.Add(row.Page);
            Label(body,"Target section: auto, hero, about, FAQ, or a section name");row.Section=Input(placement==null?"auto":Data.Get(placement,"section"),"Target section "+number,false);body.Children.Add(row.Section);
            body.Children.Add(new TextBlock{Text="Wording is preserved exactly. Leave placement on auto for the agent to decide.",Foreground=B("#a1afa3"),FontSize=10,TextWrapping=TextWrapping.Wrap});rows.Add(row);cards.Children.Add(row.Card);add.IsEnabled=rows.Count<20;
        }
        void UpdateMode(){string selected=((ComboBoxItem)mode.SelectedItem).Tag.ToString();bool supplied=selected!="agent";cards.Visibility=supplied?Visibility.Visible:Visibility.Collapsed;add.Visibility=supplied?Visibility.Visible:Visibility.Collapsed;hint.Text=selected=="agent"?"The content agent writes the website copy from your brief.":selected=="provided"?"Use your supplied wording. The agent places each block and does not write additional body copy without your instruction.":"Your wording stays exact. The agent can write the remaining sections around your content.";}
        public Dictionary<string,object> Collect(){
            string selected=((ComboBoxItem)mode.SelectedItem).Tag.ToString();var blocks=new List<Dictionary<string,object>>();int characters=0;
            foreach(var row in rows){if(String.IsNullOrWhiteSpace(row.Text.Text))continue;characters+=row.Text.Text.Length;blocks.Add(new Dictionary<string,object>{{"id",row.Id},{"label",row.Label.Text.Trim()},{"text",row.Text.Text},{"preserve_exact",true},{"placement",new Dictionary<string,object>{{"page",String.IsNullOrWhiteSpace(row.Page.Text)?"auto":row.Page.Text.Trim()},{"section",String.IsNullOrWhiteSpace(row.Section.Text)?"auto":row.Section.Text.Trim()}}}});}
            if(selected!="agent"&&blocks.Count==0)throw new Exception("Paste your content into at least one content block.");if(characters>500000)throw new Exception("Supplied content exceeds 500,000 characters.");
            return new Dictionary<string,object>{{"content_mode",selected},{"content_blocks",blocks}};
        }
    }
}
