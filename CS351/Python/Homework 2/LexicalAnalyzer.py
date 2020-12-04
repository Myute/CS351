########################################
# Assignment: Homework 5 - Parse Tree  #
# Names: Kevyn Higbee, Preston Roberts #
# Date Due: 10/18/19                   #
# Course: CS351                        #
########################################
 
from tkinter import *
import tkinter.scrolledtext as tkst
from tkinter import font
import re
 
class LexicalAnalyzer:  # gui and tokenizer for lexical analyzer
    def __init__(self, master):
        # initialize variables
        self.master = master
        self.parseTree = ParseTree()
        self.tokenList = []     # for token map
        self.parseTokens = []   # for tokenslistf or parsing
        self.lineVal = []
        self.clines = 0
        self.itlines = 0
        self.currentLineCounter = 0
        # initial function calls
        self.initGUI()
        self.createTokenList()
    def initGUI(self):                                      # add gui widgets and change properties for formatting
        # variables
        self.lineDisp = StringVar(self.master,"No Current Line")
 
        # top menu
        self.topMenu = Menu(self.master)
        self.topMenu.add_command(label="Quit",command=self.master.quit)
        self.topMenu.add_command(label="New",command=self.__newGUI__)
 
        # master
        self.master["background"]="gray21"
        self.master.title("Lexical Analyzer")
        self.master.bind("<Escape>", self.quitFunc)
        self.master.bind("<Return>", self.checkInputLines)
        self.master.bind("<BackSpace>", self.DelCheckInput)
        self.master.bind("<Control-v>", self.DelCheckInput)
        self.master.geometry("1000x500")
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=2)
        self.master.rowconfigure(1, minsize=70)
        self.master.configure(menu=self.topMenu) 
 
        # top frame
        self.topFrame = Frame(self.master,background="gray18")
        self.topFrame.grid_propagate(False)
        self.topFrame.grid(row=0, sticky=N+E+W+S)
        self.topFrame.rowconfigure(1,weight=1)
        self.topFrame.columnconfigure(0,weight=1)
 
        # top label
        self.topLabel = Label(self.topFrame,text="Procode DE",font=font.Font(self.master,family="Georgia",size=14),foreground="white",background="gray18")
        self.topLabel.grid(sticky=N+E+W+S,pady=8)
 
        # mid frame
        self.midFrame = Frame(self.topFrame,background="gray18")
        self.midFrame.grid_propagate(False)
        self.midFrame.grid(row=1,sticky=N+E+W+S)
        self.midFrame.columnconfigure(0,weight=4)
        self.midFrame.columnconfigure(1,weight=3)
        self.midFrame.columnconfigure(2,weight=3)
        self.midFrame.rowconfigure(0,weight=1)
 
        # next button
        self.nextButton = Button(self.master,background="gray20",command=self.nextLineFunc,foreground="white",font=font.Font(self.master,family="Georgia",size=12),padx=3,text="Next Line")
        self.nextButton.grid(row=1,column=0,sticky=W,padx=50)
 
        # line label
        self.lineLabel = Label(self.master,textvariable=self.lineDisp, font=font.Font(self.master,family="Georgia",size=12), foreground="white",  background="gray21")
        self.lineLabel.grid(row=1,column=0,sticky=E,padx=50)
 
        # left frame
        self.leftFrame = Frame(self.midFrame, background="gray10")
        self.leftFrame.grid_propagate(False)
        self.leftFrame.grid(row=0, column=0, sticky=N+E+S+W)
        self.leftFrame.columnconfigure(1,weight=1)
        self.leftFrame.rowconfigure(1,weight=1)
        self.leftFrame.columnconfigure(0,minsize=30)
 
        # right frame
        self.rightFrame = Frame(self.midFrame, background="gray10")
        self.rightFrame.grid_propagate(False)
        self.rightFrame.grid(row=0, column=2, sticky=N+E+S+W)
        self.rightFrame.columnconfigure(1,weight=1)
        self.rightFrame.rowconfigure(1,weight=1)
 
        # center frame
        self.centerFrame = Frame(self.midFrame, background="gray10")
        self.centerFrame.grid_propagate(False)
        self.centerFrame.grid(row=0, column=1, sticky=N+E+S+W)
        self.centerFrame.columnconfigure(1,weight=1)
        self.centerFrame.rowconfigure(1,weight=1)
 
        # input label
        self.inputLabel = Label(self.leftFrame, text="Code Input", font=font.Font(self.master,family="Georgia",size=12), foreground="white",  background="gray10")
        self.inputLabel.grid(row=0, column=1, sticky=S, pady=(5,0))
 
        # output label
        self.outputLabel = Label(self.centerFrame, text="Token Output", font=font.Font(self.master,family="Georgia",size=12), foreground="white",  background="gray10")
        self.outputLabel.grid(row=0, column=1, sticky=S, pady=(5,0))
 
        # tree label
        self.treeLabel = Label(self.rightFrame, text="Parse Tree", font=font.Font(self.master,family="Georgia",size=12), foreground="white",  background="gray10")
        self.treeLabel.grid(row=0, column=1, sticky=S, pady=(5,0))
 
        # input text box
        self.inpuText = Text(self.leftFrame, undo=True, maxundo=-1, state="normal", wrap="none", background="gray10", borderwidth="1", foreground="white",highlightcolor="white", insertbackground="white", font=font.Font(self.master,family="Courier",size=12))
        self.inpuText.grid(row=1,column=1,sticky=N+E+S+W, padx="16", pady=(5,12))
        self.inpuText.tag_configure("High", background="coral")
        self.inpuText.config(yscrollcommand=self.updateScroll)
 
        #input line box
        self.inputLine = Text(self.leftFrame, background="gray11", state="disabled", foreground="white", width="4", font=font.Font(self.master,family="Courier",size=12), borderwidth=0)
        self.inputLine.grid(row=1,column=0,sticky=N+E+S+W, pady=(5,12))
        self.inputLine.tag_configure("Right",justify='right')
        self.inputLine.config(state="normal")
        self.inputLine.insert(INSERT,"0", "Right")
        self.inputLine.config(state="disabled")
        self.inputLine.config(yscrollcommand=self.updateScroll)
 
        # output text box (tokens)
        self.outpuText = Text(self.centerFrame, undo=True, state="disabled", wrap="none", background="gray10", borderwidth="1", foreground="white",highlightcolor="white", insertbackground="white", font=font.Font(self.master,family="Courier",size=12))
        self.outpuText.grid(row=1,column=1,sticky=N+E+S+W, padx="12", pady=(5,12))
        self.outpuText.config(yscrollcommand=self.updateScrollResult)
 
        # tree text box
        self.treeOut = Text(self.rightFrame, state="disabled", wrap="none", background="gray10", borderwidth="1", foreground="white",highlightcolor="white", insertbackground="white", font=font.Font(self.master,family="Courier",size=12))
        self.treeOut.grid(row=1, column=1, sticky=N+E+S+W, padx=(5,20), pady=(5,12))
        
        # scrollbar
        self.uniscrollbar = Scrollbar(self.leftFrame, activerelief=None)
        self.uniscrollbar.grid(row=1, column=2, sticky=NS, pady=(5,12))
        self.uniscrollbar.config(command=self.scrollBoth)
 
        # scrollbar
        self.resultscrollbar = Scrollbar(self.centerFrame, activerelief=None)
        self.resultscrollbar.grid(row=1, column=2, sticky=NS, pady=(5,12), padx=(0,12))
        self.resultscrollbar.config(command=self.scrollResult)
 
        return
    def scrollBoth(self,action,position,type=None):         # for scrollbar synchronization
        self.inpuText.yview_moveto(position)
        return
    def updateScroll(self,first,last,type=None):            # for updating the scrollbar
        self.inpuText.yview_moveto(first)
        self.inputLine.yview_moveto(first)
        self.uniscrollbar.set(first, last)
        return
    def scrollResult(self, action, position, type=None):    # for scrolling
        self.outpuText.yview_moveto(position)
        return    
    def updateScrollResult(self, first, last, type=None):   # updating scrollbar
        self.outpuText.yview_moveto(first)
        self.resultscrollbar.set(first,last)
        return  
    def __newGUI__(self):                                   # launching another instance of gui without exiting current one
        LexicalAnalyzer(Tk())
        self.quitFunc()
        return
    def checkInputLines(self, event=None):                  # checks vaildity of input lines
        self.clines+=1
        self.gotLines = int(self.inpuText.index('end').split('.')[0]) - 1
        if(self.gotLines != self.clines):
            self.clines = self.gotLines
            self.inputLine.config(state="normal")
            self.inputLine.delete('2.0', END)
            for line in range(1,(self.gotLines)):
                self.inputLine.insert(INSERT,"\n"+str(line), "Right")
            self.inputLine.config(state="disabled")
        else:
            #print("iterated");
            self.inputLine.config(state="normal")
            self.inputLine.insert(INSERT,"\n"+(str(self.clines - 1)), "Right")
            self.inputLine.config(state="disabled")
        return
    def DelCheckInput(self,event=None):                     # checking line number on deletion of a character or pasting code
        self.delLines = int(self.inpuText.index('end').split('.')[0]) - 2
        if(self.clines != self.delLines):
            self.checkInputLines()
        return
    def nextLineFunc(self, Event=None):                     # perform logic on current line
        if (self.clines == 0 and self.itlines == 0) or (self.clines != 0 and self.clines > self.itlines):
            self.inpuText.tag_remove("High","1.0",END)
            self.lineVal.insert(self.itlines, str(self.inpuText.get(str(self.itlines+1)+".0",str(self.itlines+2)+".0")))
            self.inpuText.tag_add("High",str(self.itlines + 1)+".0",str(self.itlines + 2)+".0")
            self.lineDisp.set("Current Line: "+str(self.itlines))
            self.outStr = self.tokenize(self.lineVal[self.itlines])
            self.itlines+=1
        elif self.itlines >= self.clines:
            self.inpuText.tag_remove("High","1.0",END)
            self.itlines = 0
            self.outpuText.config(state="normal")
            self.outpuText.delete("1.0",END)
            self.outpuText.config(state="disabled")
            self.lineDisp.set("No Current Line")
 
        self.tokenOutput(self.outStr)
        self.parseTreeOutput(self.parseTree.parse(self.parseTokens))
        self.checkInputLines()
        return
    def parseTreeOutput(self, stringthing):                 # outputs parse tree to parse tree output box
        self.treeOut.config(state="normal")
        self.treeOut.insert("end", "Line " + str(self.itlines-1) + ":\n" + str(stringthing))
        self.treeOut.config(state="disabled")
        return
    def tokenOutput(self, stringlist):                      # outputs list of tokens to token output box
        self.outpuText.config(state="normal")
        self.outpuText.insert("end", "Line " + str(self.itlines-1) + ":\n")
        for string in stringlist:
            self.outpuText.insert("end", string+"\n")
        self.outpuText.config(state="disabled")
        self.currentLineCounter+=1
        return
    def quitFunc(self, Event=None):                         # exits program
        self.master.destroy()
        return
    def tokenize(self, stringthing):                        # tokenize passed string based on items in tokenView
        self.tokenList = []
        
        for token in self.tokenView.items():
            for match in re.finditer(token[1], stringthing):
                self.tokenList.append((token[0][0], match))
 
        self.tokenList.sort(key=lambda x: x[1].start())
        self.retStrList = []
        for item in self.tokenList:
            self.parseTokens.append((item[0],stringthing[item[1].start():item[1].end()]))
        for item in self.tokenList:
            self.retStrList.append("<" + item[0] + ", " + stringthing[item[1].start():item[1].end()] + ">")
 
        return self.retStrList
    def createTokenList(self):                              # creates tokenView for tokenizing string using regex
        self.tokenView = {}     # everything is separated for organization purposes
        self.keywords = {
            ("keyword", "if") : re.compile(r'((?<=[\s])|^|\b\?)if(?=[\(,:,\s,=\)])'),
            ("keyword", "else") : re.compile(r'((?<=[\s])|^|\b\?)else(?=[\(,:,\s,=\)])'),
            ("keyword", "int") : re.compile(r'((?<=[\s])|^|\b\?)int(?=[\(,:,\s,=\)])'),
            ("keyword", "float") : re.compile(r'((?<=[\s])|^|\b\?)float(?=[\(,:,\s,=\)])')
        }
        self.tokenView.update(self.keywords)
        
        self.operators = {
            ("operator", "=") : re.compile(r'='),
            ("operator", "+") : re.compile(r'\+'),
            ("operator", ">") : re.compile(r'>'),
            ("operator", "*") : re.compile(r'\*')
        }
        self.tokenView.update(self.operators)
        
        self.separators = {
            ("separator", "(") : re.compile(r'\('),
            ("separator", ")") : re.compile(r'\)'),
            ("separator", ":") : re.compile(r':'),
            ("separator", "\"") : re.compile(r'\"'),
            ("separator", ";") : re.compile(r';')
        }
        self.tokenView.update(self.separators)
        
        identifierCompilationString = r""
        for word in self.keywords:
            identifierCompilationString = identifierCompilationString + "(?!" + word[1] + " )"
        identifierCompilationString = identifierCompilationString + "(?<![A-Z\?a-z\"])[A-Za-z]+\d*(?=[\b$\s\(\)\"=])(?!\")"
        
        self.tokens = { 
            ("identifier", "var") : re.compile(identifierCompilationString),
            ("int_literal", "int") : re.compile(r'(?<![A-Za-z\.\d\"])\d+(?![A-Za-z\.\d\"])'),
            ("string_literal", "string") : re.compile(r'".*?"'),
            ("float_literal", "float") : re.compile(r'(?<![A-Za-z\d\"])\d*\.\d+(?![A-Za-z\d\"])')
        }
        self.tokenView.update(self.tokens)
        return=
class ParseTree:        # class for parsing expressions
    def __init__(self):                 # constructor
        self.expression = []
        self.parsedExpression = []
        self.outStr = ""
        return
    def parse(self, expression):        # parses expression, returns a string specifying nodes and their values ( this is the only one that should be called by anything outside the class )
        self.expression = expression
        self.outStr = ""
        while(len(self.expression) > 0):
            self.acceptToken(self.expression.pop(0))
        return self.outStr
    def acceptToken(self, new_token):   # grabs token and sends it to appropriate function based on type
        typeT, token = new_token
        if(typeT == "keyword"):
            return6
        elif(typeT == "operator"):
            return
        elif(typeT == "separator"):
            return
        elif(typeT == "identifier"):
            return
        elif(typeT == "int_literal"):
            return
        elif(typeT == "string_literal"):
            return
        elif(typeT == "float_literal"):
            return
        return
    def math(self, new_token):          # performs BNF logic on math related nodes
        return
 
def __main__():         # main function definition
    root = Tk()
    analyzer = LexicalAnalyzer(root)
    root.mainloop()
    return
__main__()
 
 
 
 

