#! /usr/bin/env python
# File Name: jeopardy_view.py
# Task : create a GUI for the jeopardy system
# Author: Sun Zhichuang
# Date  : 2013/8/31

"""
Define the Jeopardy GUI:
# Here explain the work flows:
1.  The system starts with a main control board, which contains two control button, one for 
    starting the Register Groups , the other for starting Answering Questions;

2.  First we press the Register Groups button to activate registering process, during which
    key press is perceived and blocked for filling register infomation dialog in order.
    
    Information collected will be displayed in the GroupPad, which maintains all the register-
    ed group's information, including ID, members, nick, and Score.

3.  After register, we press the Answering Questions button to stop register and start answer-
    ing questions, it initiate a Question Board, which maintains question information.

4.  We click on the Question Board to fetch a certain kind of question in the form of question
    window, this window is sensible for key press too, it judges who first press a key to race 
    for the chance for answering the question.

5.  After answering a question, the teacher is responsible for grade a group by judging right 
    or wrong.

# Tree-relationships between all the kinds of windows:

                                 ControlBoard
                                       |
                                       |
                  +-----------------------------------------+
                  |                                         |
             GroupBoard                               QuestionBoard
                  |                                         |
                  |                                         |
          +-------+-------+                              TypePad(s)    
          |               |                                 |
          |               |                      +----------+----------+
   GroupRegister     GroupFrame(s)               |                     |
                          |                  TypeLabel              ScorePad(s)
                          |                                            |
                          |                                            |
                       GroupInfo(s)                                ScoreSquare(s)
                                                                       |
                                                                       |
                                                                  QuestionWindow  
"""

from Tkinter import *
from jeopardy_prototype import *

class JeopardyControlBoard(Frame):
    """
main control board
contains two button: one for start register, the other for start answer question
always exists as the other window's root, maybe.
    """
    def __init__(self, parent=None,**options):
        Frame.__init__(self, parent)
        self.pack()
        self.config(height=80,width=50)
        self.row = Frame(self)
        self.row.pack(side=TOP)
        self.lbl = Label(self.row,text="Jeopardy Control Board")
        self.lbl.pack(side=TOP,fill=BOTH)
        self.lbl.config(height=5, width=30)
        self.btn1 = Button(self.row,text="Start Register",command=self.startRegister)
        self.btn1.pack(side=LEFT)
        self.btn1.config(height=3,width=15)
        self.btn2 = Button(self.row,text="Start Jeopardy",command=self.startJeopardy)
        self.btn2.pack(side=RIGHT)
        self.btn2.config(height=3,width=15)
        self.groupBoardFlag=False
        self.questionDisplayBoardFlag=False
        self.groupBoard=None
        self.questionDisplayBoard=None
    def startRegister(self):
        if(self.groupBoardFlag is False):
            self.groupBoardFlag=True
            self.groupBoard=GroupBoard(parent=self,side=TOP)
    def startJeopardy(self):
        if(self.questionDisplayBoardFlag is False):
            self.questionDisplayBoardFlag=True
            self.groupBoard.unbindKeyEvent()
            self.questionDisplayBoard=QuestionDisplayBoard(parent=self,side=TOP)

class GroupBoard(Frame):
    """
maintain group information here
made up of GroupFrame(s), each handles a Group
GroupFrames add gradually after being registered
pop up group register window on key press event!
    """
    def __init__(self, parent=None, **options):
        Frame.__init__(self,parent)
        self.pack()
        self.grouppad = GroupPad()
        self.groupframes={}
        self.lbl = Label(self,text='Group Information Board') 
        self.lbl.pack(side=TOP,expand=YES,fill=X)
        self.lbl.bind('<KeyPress>', self.popUpRegisterWindow)
        self.lbl.focus()
    def popUpRegisterWindow(self,event):
        # bind this function on key press of registering request
        RegisterWindow(event.char, parent=self)
    def addNewGroup(self,group):
        self.groupframes[group.getKey()]=GroupFrame(group,self,side=LEFT)
        self.grouppad.addGroup(group)
       
    def unbindKeyEvent(self):
        # called when we start answering questions
        self.lbl.unbind('<KeyPress>')

class GroupFrame(Frame):
    """
maintain a single group's information
includes nick, pressed Key, members, score
    """
    def __init__(self, group, parent=None, **options):
        Frame.__init__(self, parent)
        self.pack(side=LEFT)
        self.group = group
        self.NickVar = StringVar()
        self.KeyVar = StringVar()
        self.MembersVar = StringVar()
        self.ScoreVar = IntVar()
        self.NickVar.set(group.getNick())
        self.KeyVar.set(group.getKey())
        self.MembersVar.set(group.getMembers())
        self.ScoreVar.set(group.getScore())
        self.makeForm()

    def makeForm(self):
        row1 = Frame(self)
        labKey = Label(row1, width=10,text='Pressed Key')
        labKeyVar = Label(row1, width=10,textvariable=self.KeyVar)
        row1.pack(side=TOP,fill=X)
        labKey.pack(side=LEFT)
        labKeyVar.pack(side=RIGHT)
        row2 = Frame(self)
        labNick = Label(row2, width=10,text='Nick Name')
        labNickVar = Label(row2, width=10,textvariable=self.NickVar)
        row2.pack(side=TOP,fill=X)
        labNick.pack(side=LEFT)
        labNickVar.pack(side=RIGHT)
        row3 = Frame(self)
        labMembers = Label(row3, width=10,text='Members')
        labMembersVar = Label(row3, width=10,textvariable=self.MembersVar)
        row3.pack(side=TOP,fill=X)
        labMembers.pack(side=LEFT)
        labMembersVar.pack(side=RIGHT)
        row4 = Frame(self)
        labScore = Label(row4, width=10,text='Score')
        labScoreVar = Label(row4, width=10,textvariable=self.ScoreVar)
        row4.pack(side=TOP,fill=X)
        labScore.pack(side=LEFT)
        labScoreVar.pack(side=RIGHT)

    def updateScore(self):
        self.ScoreVar.set(self.group.getScore()) 

from tkMessageBox import askokcancel
class Quitter(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.parent=parent
        widget = Button(self, text='Cancel', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)

    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans: self.parent.destroy()

fields=['Nickname','Members']
class RegisterWindow():
    """
a window popuped by GroupBoard on key press event
collect group register information
includes nick, pressed Key, members
    """
    def __init__(self,key, parent=None, fields=fields):
        self.popup = Toplevel(parent)
        self.fields=fields
        self.parent=parent
        self.group=None
        self.entries=[]
        self.key=key
        self.makeForm(key)

    def makeForm(self,key):
        row = Frame(self.popup)
        labKeyText = 'Key \''+key+'\''+' is Pressed'
        lab = Label(row,  text=labKeyText)
        row.pack(side=TOP,fill=X)
        lab.pack(side=TOP,fill=X)
        for field in self.fields:
            row = Frame(self.popup)
            lab = Label(row, width=15,text=field)
            ent = Entry(row)
            row.pack(side=TOP, fill=X)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            self.entries.append(ent)
        btn_OK = Button(self.popup, width=8,text='submit',command=self.finishRegisterForm)
        btn_OK.pack(side=LEFT)
        Quitter(self.popup).pack(side=RIGHT)
        row.pack(side=TOP,fill=X)
        self.popup.grab_set()
        self.popup.focus_set()
        self.popup.wait_window()

    def finishRegisterForm(self):
        # called when OK button is pressed to finish a registeration
        # may return a Group object 
        (nick,members) = (ent.get() for ent in self.entries)
        group = Group(self.key,nick,members)
        self.group = group
        self.parent.addNewGroup(group)
        self.popup.destroy()

questionTypeList = ["Common Sense","Programmer Expertise","History Literature","Economic Sociology"]
class QuestionDisplayBoard(Frame):
    """
maintains questions information here
made up of question TypeBoard(s), which handles a certain type of questions
pop up QuestionWindows on request
    """
    def __init__(self,questionTypeList=questionTypeList, parent=None, **options):
        Frame.__init__(self, parent)
        self.pack()
        self.parent=parent
        self.lbl = Label(self, text='Question Board')
        self.lbl.pack(side=TOP)
        self.questionBoard=QuestionBoard(questionTypeList)
        self.questionTypeList=questionTypeList
        for questionType in questionTypeList:
            TypeDisplayBoard(questionType,parent=self,side=TOP)

scoreList=[100,200,300,400,500]
class TypeDisplayBoard(Frame):
    # --_?_-- forgive my laziness to define so many class! It's a bad habit, though,
    # showing the hierarchical relationship explicitly, for the sake of making thinking easier!
    """
maintains questions info of a certain type
made up of a frame with a TypeLabel and several QuestionSquare Buttons embeded
    """
    def __init__(self, questionType,scoreList = scoreList,parent=None, **options):
        Frame.__init__(self, parent)
        self.pack(side=TOP)
        self.parent = parent
        self.scoreList = scoreList
        self.questionType=questionType
        typeLabelText=questionType
        Label(self, text=questionType ,width=18).pack(side=LEFT)
        for score in scoreList:
            QuestionDisplaySquare(score,questionType, parent=self)

class QuestionDisplaySquare(Frame):
    """
maintains questions of a certain type and score
made up of a button, which shows the info of  score and questions left
pop up a QuestionWindow on click
    """
    def __init__(self, score, questionType, parent=None, **options):
        Frame.__init__(self, parent)
        self.pack(side=LEFT)
        self.parent=parent
        self.score = score
        self.questionSquare = QuestionSquare(questionType, score, num=10)
        self.qsButtonText=StringVar()
        self.qsButtonText.set('Score: '+ str(self.score)+'\n'+'('+str(self.questionSquare.getQuestionNum())+')')
        self.btn = Button(self, textvariable=self.qsButtonText,command=self.popUpQuestionWindow)
        self.btn.pack(side=TOP)
    def popUpQuestionWindow(self):
        question=self.questionSquare.fetchQuestion()
        self.qsButtonText.set('Score: '+ str(self.score)+'\n'+'('+str(self.questionSquare.getQuestionNum())+')')
        QuestionWindow(question,parent=self)

class QuestionWindow():
    """
poped up by QuestionSquare, show the question information
as well as catching which group first press a key to answer this question
it also offeres a judge key for grading and a show key for showing answer 
    """
    def __init__(self,question, parent=None):
        self.popup = Toplevel(parent)
        self.parent=parent
        self.question=question
        self.group=None
        self.flag=False
        self.key=''
        self.keyVar = StringVar()
        self.keyVar.set('')
        self.groupVar = StringVar()
        self.groupVar.set('')
        self.answerVar = StringVar()
        self.answerVar.set('')
        self.judgeVar = IntVar(0)
        self.makeForm()
        self.popup.bind('<KeyPress>', self.whoGetTheChance)
        self.popup.focus()
    def makeForm(self):
        row1 = Frame(self.popup)
        labQuestionText = self.question.getBody()
        lab1 = Label(row1,  text=labQuestionText)
        row1.pack(side=TOP,fill=X)
        lab1.pack(side=TOP,fill=X)

        row2 = Frame(self.popup)
        lab2 = Button(row2,width=13, text='Key-Pressed')
        labKey = Label(row2,width=15,textvariable=self.keyVar)
        labKey.config(relief=SUNKEN)
        row2.pack(side=TOP,fill=X,expand=YES)
        lab2.pack(side=LEFT)
        labKey.pack(side=LEFT,fill=X)

        row3 = Frame(self.popup)
        lab3 = Button(row3,width=13, text='Group-granted')
        labGroup = Label(row3,width=15,textvariable=self.groupVar)
        labGroup.config(relief=SUNKEN)
        row3.pack(side=TOP,fill=X,expand=YES)
        lab3.pack(side=LEFT)
        labGroup.pack(side=LEFT,fill=X)

        row4 = Frame(self.popup)
        lab4 = Button(row4,width=13, text='Show-Answer',command=self.showAnswer)
        labAnswer = Label(row4,width=15, textvariable=self.answerVar)
        labAnswer.config(relief=SUNKEN)
        row4.pack(side=TOP,fill=X, expand=YES)
        lab4.pack(side=LEFT)
        labAnswer.pack(side=LEFT,fill=X)

        row5 = Frame(self.popup)
        row5.pack(side=TOP)
        Radiobutton(row5, text='Right',value=0,variable=self.judgeVar).pack(side=LEFT)
        Radiobutton(row5, text='Wrong',value=1,variable=self.judgeVar).pack(side=RIGHT)

        row6 = Frame(self.popup)
        btn1 = Button(row6, text='OK', command=self.gradeGroup)
        btn2 = Button(row6, text='Cancel', command=self.cancel)
        row6.pack(side=TOP)
        btn1.pack(side=RIGHT)
        btn2.pack(side=LEFT)

    def showAnswer(self):
        self.answerVar.set(self.question.getAnswer()) 
    def whoGetTheChance(self, event):
        # catch the first one who press the key ,and prevent the others
        self.keyVar.set(str(event.char)) 
        group = self.parent.parent.parent.parent.groupBoard.grouppad.getGroupByKey(event.char)
        if(self.flag is False and group is not None):
            self.groupVar.set(group.getNick())
            self.flag=True
            self.key=event.char
            self.group=group
        
    def gradeGroup(self):
        # associated with the judge button
        if(self.judgeVar.get() is 0 and self.group is not None):
            self.group.addScore(self.parent.questionSquare.getScore())
            self.parent.parent.parent.parent.groupBoard.groupframes[self.key].updateScore()
            self.group=None # avoid add two times
        elif (self.judgeVar.get() is 1 and self.group is not None):
            self.group.addScore(-self.parent.questionSquare.getScore())
            self.parent.parent.parent.parent.groupBoard.groupframes[self.key].updateScore()
            self.group=None
        else:
            print('No effect group is get!')
        self.popup.destroy()

    def cancel(self):
        self.popup.destroy()

if __name__=='__main__':
    JeopardyControlBoard().mainloop()
