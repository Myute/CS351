#by Preston Roberts

import re;
from tkinter import *;
from tkinter import font; #for some reason importing the whold Tkinter modules with '*' doesn't autoinclude some submodules like font... *shrugs*
keywordCount = {
    "if" : 0,
    "else" : 0,
    "int" : 0,
};

searchMap = {
    ("if","keyword"): re.compile(r'((?<=[\s])|^|\b)if((?=[$,\:,\(])|\b)'),
    ("else","keyword"): re.compile(r'((?<=[\s,\b])|^|\b)else((?=[$,\:,\(])|\b)'),
    ("int","keyword"): re.compile(r'((?<=[\s,\b,\(,\)])|^|\b)int((?=[$,\(,\),\s,\t])|\b)'),
    ("=","operator"): re.compile(r'='),
    ("+","operator"): re.compile(r'\+'),
    (">","operator"): re.compile(r'>'),
    ("(","separator"): re.compile(r'\('),
    (")","separator"): re.compile(r'\)'),
    (":","separator"): re.compile(r':'),
    #("\"...\"","sp"): re.compile(r'\"[\s\S]*[\w\W]*[\d\D]*\"'),
    ("string","literal"): re.compile(r'([\"\'])(?:(?=(\\?))\2.)*?\1'), #made by expanding on a few findings from Google
    ("\"","separator"): re.compile(r'\"'),
    ("var","identifier"): re.compile(r'(?<=[\s,^,=,\b,\+,\-,\/,\%,\*,\),\(,<,>])[a-zA-z]+\d*(?=\s+|$|\b|=|[\+,\-,\/,\%,\*,\),\(,<,>])'), #this got a tad long, but I think this is all cases. It was easier to work inclusively than exclusively here.
    ("integer","literal"): re.compile(r'(?<=[\s,^,=,\+,\-,\/,\%,\*,\),\(,<,>)])\d+(?=\s+|$|\b|=|[\+,\-,\/,\%,\*,\),\(,<,>])'),
    #("str","literat"): re.compile(r'\b[a-zA-z]+\b'), #I'm slightly confused on whether string literal would be parsed with/without quotation marks
}
searchView = searchMap.items();

class PrestonGUI:
    
    def __init__(self, TKmaster):
        self.kymod = dict(keywordCount);
        self.lineVal = [];
        self.outVal = [];
        self.master = TKmaster;
        self.itLine = 0; self.clines = 0;
        self.lineDisp = StringVar(self.master,"No Current Line"); 
        self.master.title("Preston's Code Analysis System"); #title
        self.master.geometry("800x450"); #resize the canvas so I don't have to manually
        self.master["background"]="gray21";

        #top header
        self.topFrame = Frame(self.master, background="gray18");
        self.topFrame.grid_propagate(False);
        self.topFrame.grid(row=0, sticky=N+E+W+S);
        self.topLabel = Label(self.topFrame,text="Procode DE", font=font.Font(self.master,family="Georgia",size=14), foreground="white",  background="gray18");
        self.topLabel.grid(sticky=N+E+S+W, pady=8); #make toplabel stick to top of row, and give it some y-padding.
        self.topFrame.columnconfigure(0,weight=1);
        self.midFrame = Frame(self.topFrame, background="gray18"); #this way I'm taking one large auto-resizing column, and makign a grid inside of it.
        self.midFrame.grid_propagate(False); #don't need grid propagation for midframe so that scaling can be easier/more-precise.
        self.midFrame.grid(row=1, sticky=N+E+S+W);
        self.midFrame.columnconfigure(0,weight=1);#, minsize=300); #set up for the left/right frames
        self.midFrame.columnconfigure(1,weight=1);#, minsize=300);
        self.topFrame.rowconfigure(1, weight=1);

        self.master.columnconfigure(0,weight=1);
        self.master.rowconfigure(0, weight=2);
        self.master.rowconfigure(1, minsize=70);#row 1 is where I'll be putting the buttons and counter.
        self.midFrame.rowconfigure(0, weight=1);#this is the primary row of the midframe, so let's stretch it. 

        #bottom row initilization
        self.nextButton = Button(self.master,background="gray20",command=self.next_line ,foreground="white",font=font.Font(self.master,family="Georgia",size=12),padx=3,text="Next Line"); self.nextButton.grid(row=1,column=0,sticky=W,padx=50);
        self.lineLabel = Label(self.master,textvariable=self.lineDisp, font=font.Font(self.master,family="Georgia",size=12), foreground="white",  background="gray21"); self.lineLabel.grid(row=1,column=0,sticky=E,padx=50);
        #self.lineDisp = "Current Line: 0";
        #self.master.bind('<>', self.next_line);#this was going to be for proceeding to next line... I just could never think of a good key to bind it to since we're also using text

        self.leftFrame = Frame(self.midFrame, background="gray10");  self.leftFrame.grid_propagate(False); self.leftFrame.grid(row=0, column=0, sticky=N+E+S+W);
        self.rightFrame = Frame(self.midFrame, background="gray10"); self.rightFrame.grid_propagate(False); self.rightFrame.grid(row=0, column=1, sticky=N+E+S+W); 
        self.leftFrame.columnconfigure(1,weight=1);
        self.leftFrame.rowconfigure(1,weight=1);
        self.rightFrame.columnconfigure(1,weight=1);
        self.rightFrame.rowconfigure(1,weight=1);
        #breaks up the envorinment body into topFrame and midFrame that can scale individually.

        #the labels that I alomst forgot to add to the input and output boxes.
        self.inputLabel = Label(self.leftFrame, text="Code Input", font=font.Font(self.master,family="Georgia",size=12), foreground="white",  background="gray10"); self.inputLabel.grid(row=0, column=1, sticky=S, pady=(5,0));
        self.outputLabel = Label(self.rightFrame, text="Parsed Output", font=font.Font(self.master,family="Georgia",size=12), foreground="white",  background="gray10"); self.outputLabel.grid(row=0, column=1, sticky=S, pady=(5,0));

        #input, output, and line number boxes....
        self.intpuText = Text(self.leftFrame, undo=True, maxundo=-1, state="normal", wrap="none", background="gray10", borderwidth="1", foreground="white",highlightcolor="white", insertbackground="white", font=font.Font(self.master,family="Courier",size=12));self.intpuText.grid(row=1,column=1,sticky=N+E+S+W, padx="16", pady=(5,12));
        self.inputLine = Text(self.leftFrame, background="gray11", state="disabled", foreground="white", width="4", font=font.Font(self.master,family="Courier",size=12), borderwidth=0); self.inputLine.grid(row=1,column=0,sticky=N+E+S+W, pady=(5,12)); self.leftFrame.columnconfigure(0,minsize=30);
        self.inputLine.tag_configure("Right",justify='right'); #need to add this tag to all line numbering text because it's the only way to justify right with the text widget.
        self.outpuText = Text(self.rightFrame, undo=True, state="disabled", wrap="none", background="gray10", borderwidth="1", foreground="white",highlightcolor="white", insertbackground="white", font=font.Font(self.master,family="Courier",size=12));self.outpuText.grid(row=1,column=1,sticky=N+E+S+W, padx="12", pady=(5,12));
        #I wanted to make the inputLine (count) a label instead of a text box, but unfortunately you can't scroll a label like I would want.
        self.intpuText.tag_configure("High", background="coral");
        self.inputLine.config(state="normal");
        self.inputLine.insert(INSERT,"0", "Right"); #adding zero (which will never be deleted so we dont' have leading new lines) and justifying right.
        self.inputLine.config(state="disabled");

        #scrollbar
        self.uniscrollbar= Scrollbar(self.leftFrame, activerelief=None);self.uniscrollbar.grid(row=1, column=2, sticky=NS, pady=(5,12));
        self.uniscrollbar.config(command=self.scrollBoth);
        self.intpuText.config(yscrollcommand=self.updateScroll);
        self.inputLine.config(yscrollcommand=self.updateScroll);

        self.resultscrollbar= Scrollbar(self.rightFrame, activerelief=None);self.resultscrollbar.grid(row=1, column=2, sticky=NS, pady=(5,12), padx=(0,12));
        self.resultscrollbar.config(command=self.scrollResult);
        self.outpuText.config(yscrollcommand=self.updateScrollResult);

        #menu creation
        self.topMenu = Menu(self.master);
        self.topMenu.add_command(label="Quit",command=self.master.quit);
        self.topMenu.add_command(label="New",command=self.__newGUI__);
        self.master.configure(menu=self.topMenu);
        
        #ease of access
        self.master.bind("<Escape>", quit); #hitting escape will end the run
        self.master.bind("<Return>", self.checkInputLines);
        self.master.bind("<Control-v>", self.DelCheckInput); #added this to cover the "paste from clipboard" event which could add lines
        self.master.bind("<BackSpace>", self.DelCheckInput); #this could be commented out if more performance is required


    #next line iterator
    def next_line(self, event=None):
        if(self.clines != 0 and self.clines > self.itLine):
            self.intpuText.tag_remove("High","1.0",END);
            self.lineVal.insert( self.itLine, str(self.intpuText.get(str(self.itLine + 1)+".0", str(self.itLine + 2)+".0")) );
            self.intpuText.tag_add("High",str(self.itLine + 1)+".0",str(self.itLine + 2)+".0");
            self.lineDisp.set("Current Line: "+str(self.itLine));
            self.line_parse(self.lineVal,self.itLine,self.kymod);
            self.itLine+=1;
        elif(self.itLine >= self.clines):
            self.intpuText.tag_remove("High","1.0",END);
            self.itLine = 0;
            self.outpuText.config(state="normal");
            self.outpuText.delete("1.0",END);
            self.outpuText.config(state="disabled");
            self.lineDisp.set("No Current Line");
            self.kymod = dict(keywordCount);

        return;

    def sortNum(self,tup): #for sorting function below
        return tup[0];

    #separate parsing function
    def line_parse(self, incoming, idx, keywords):

        resultSet = [];

        work = "";
        for token in searchView:
            print(token[0][0]);
            res = token[1].finditer(incoming[idx]);
            for m in res:
                try: #avoid performance drops like the plague
                    strnky = m.string[m.start():m.end()];
                    #print(strnky);
                    work += keywords.get(token[0][0],"& ");
                    work += keywords.get(str(strnky),"| ");
                    resultSet.insert(m.start(),(m.start(), token[0][1], token[0][0], m.string[m.start():m.end()]));
                    print(strnky);
                    #I'll admit, this is probably an overly-complicated mess just to avoid an if statement, but it will be better for longer scripts, because the only tokens that will take longer will be keywords.
                    #and this way I'll be collecting keyword statistics to make sure that every else has an if, etc.
                except:
                    if token[0][1] == "keyword":
                        resultSet.insert(m.start(),(m.start(), token[0][1], token[0][0], m.string[m.start():m.end()]));
                        keywords[token[0][0]] += 1;
                        #print(keywords);
                        pass;
                    else:
                        pass;
                    #if this makes things ugly later on then I'll scrap it and just us an if statement comparing for every token.


        resultSet.sort(key=self.sortNum);
        
        self.outpuText.config(state="normal");
        self.outpuText.insert(INSERT,"\nline: "+str(idx)+"\n");
        self.outpuText.config(state="disabled");

        for res in resultSet:
            self.outpuText.config(state="normal");
            self.outpuText.insert(INSERT,"<"+res[1]+","+ res[3].replace('\n',' ').replace('\r',' ') +">\n");
            self.outpuText.config(state="disabled");
        
        #self.outpuText.insert(INSERT,incoming[idx]);
        


    #the event-based number updating
    def checkInputLines(self, event=None):
        self.clines+=1; #line count (total)
        self.gotLines = int(self.intpuText.index('end').split('.')[0]) - 1; #get number of existing lines
        #print(str(self.gotLines)+" : "+str(self.clines)+"\n");
        if(self.gotLines != self.clines): #if the lines number that we've just called is different from our count (someone deleted some lines) then redraw
            #print("redrawn");
            self.clines = self.gotLines; #set the line count to whatever the actual number has changed to.
            self.inputLine.config(state="normal");
            self.inputLine.delete('2.0', END);
            for line in range(1,(self.gotLines)):
                self.inputLine.insert(INSERT,"\n"+str(line), "Right");
            self.inputLine.config(state="disabled");
        else:
            #print("iterated");
            self.inputLine.config(state="normal");
            self.inputLine.insert(INSERT,"\n"+(str(self.clines - 1)), "Right");
            self.inputLine.config(state="disabled");
        return;

    #this was more of a vanity thing for me, but I didn't like how infrequently it was redrawing the line numbers, so I made a different event for backspace
    def DelCheckInput(self,event=None):
        self.delLines = int(self.intpuText.index('end').split('.')[0]) - 1;
        if(self.clines != self.delLines and self.clines != 0): #finally fixed this by having it not trigger when the linecoung is zero
            self.checkInputLines();
        return;

    #couldn't really find a better way to contol the scrolling
    def scrollResult(self, action, position, type=None):
        self.outpuText.yview_moveto(position);

    def scrollBoth(self, action, position, type=None):
        self.intpuText.yview_moveto(position);
        self.inputLine.yview_moveto(position);

    def updateScroll(self, first, last, type=None):
        self.intpuText.yview_moveto(first);
        self.inputLine.yview_moveto(first);
        self.uniscrollbar.set(first, last);

    def updateScrollResult(self, first, last, type=None):
        self.outpuText.yview_moveto(first);
        self.resultscrollbar.set(first,last);

    #for the "new" button
    def __newGUI__(self):
        PrestonGUI(Tk());
    

    
root = Tk();
my_gui = PrestonGUI(root);
root.mainloop();

#this exercise was quite fun, and got me more used to Tkinter. Granted, the documentation on the actual library is slighthly... sub-par...
#but since last time I used Tkinter, it seems to have actually gotten it's central documentation updated. And I also noticed they added ttk as part of the library now instead of it being a submodule
