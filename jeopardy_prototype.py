# File Name: jeopardy_prototype.py
# Project Name: Jeopardy System
# Task: realize a off line Jeopardy System
# Author: Sun Zhichuang
# Date:   2013/8/25

# define an off line jeopardy system :
#
#	The Jeopardy System we are going to realize is mimicry of the famous American 
#   TV show “Jeopardy”.
#
#	Generally, the system contains three parts, the jeopardy software system, the 
#   students groups, and the teacher.
#
#	The software system is deployed on a computer with several keyboards connected
#   to it,  the keyboards will be used by the students groups . the software 
#   interface keeps showing the questions states, groups information which includes
#   membership, nickname and scores. It will also accept the teacher’s grading 
#   command.
#
#	For the students, in each round , a group will be chosen to select a certain type
#   of questions. After the question is ready, all the groups are ready to race 
#   answering questions by press the allocated key on their keyboard. The group who
#   win the race will be granted to answer the question.
#
#	The teacher is responsible for grading each group using the software system.

import sqlite3

class Jeopardy:
	"""
	maintains some static and global information of this Jeopardy system
	"""
	def __init__(self):
		self.dbname = "dbname"
	def getDatabase(self):
		return self.dbname


class Group:
	"""
	keeps the basic information of a Group,like Allocated Key, Group's Nickname, 
	Group's ID, Group's members and Group's Score.
	A group is created at the register stage, when a registering key is received, we collect useful information
	and create a group.
	the group id is allocated by the group pad class, who is in charge of the groups
	"""
	def __init__(self, key, nick, members):
		self.key = key
		self.nick = nick
		self.members = members
		self.score = 0
	def addScore(self, addAmount):
		# addAmount may be minus, that turns out to be subtract score
		self.score += addAmount
	def getKey(self):
		return self.key
	
class GroupPad:
	"""
	groupPad keeps all the groups information and shows them, group info will be added to a group pad after registered,
	the initial state of groupPad is empty.
	we use the key to locate the group
	"""
	def __init__(self, group_num = 6):
	# group_num defines the default max groups
		self.group_num = group_num
		self.groups = {}
	def addGroup(self,newGroup):
		self.groups[newGroup.getKey()] = newGroup
	def getGroupByKey(self,key):
		return self.groups[key]
		
		
class Question:
	"""
	describe a question object ,includes body, answer, type, score
	"""
	def __init__(self,body,answer,typeName,score):
		self.body = body
		self.answer = answer
		self.typeName = typeName
		self.score = score
	def getScore(self):
		return self.score
	def getType(self):
		return self.typeName
	def getBody(self):
		return self.body
	def getAnswer(self):
		return self.answer

class QuestionBoard:
	"""
	a question board keeps the information of all types of questions of different score
	a certain type of question is stored in a QuestionType object
	"""
	def __init__(self,questionTypeList["Common Sense","Programmer Expertise","History & Literature","Economic & Sociology"]):
		self.questionTypeList = questionTypeList
		self.typeList = {}
		for typeName in questionTypeList:
			self.typeList[typeName] = QuestionType(typeName)			
	def getQuestionTypeByType(self,typeName):
		return self.typeList[typeName]
		
class QuestionType:
	"""
	a question type keeps a list of questionSquare, 
	we names a certain type list of questions of the score : QuestionSquare
	scoreTypeList =[100,200,300,400,500]
	"""
	def __init__(self,typeName,scoreTypeList=[100,200,300,400,500]):
		self.typeName = typeName
		self.scoreTypeList = scoreTypeList
		self.squareList = {}
		for score in range(self.scoreTypeList):
			# default numbers of questions of the same score and type is 10
			self.squareList[score]=QuestionSquare(typeName,score,num=10)
			
	def getQuestionSquareByScore(self,score):
		return self.squareList[score]

class QuestionSquare:
	"""
	a questionSquare contains question of the same type and score, it also represent a square in the question board
	it is in charge of maintain the question display and numbers of questions left
	"""
	def __init__(self, typeName, score, num):
		dbname = Jeopardy.getDbName()
		conn = self.connectDatabase(dbname)
		self.questionList = self.fetchQuestionList(conn,typeName,score,num)
		self.num = num
	def connectDatabase(self,dbname):
		conn = sqlite3.connect(dbname)
        return conn
	def fetchQuestionList(self,conn,typeName,score,num):
        curs = conn.cursor()
        # get type id
        curs.execute('select * from typetable')
        typeDic = {}
        for (t_id,t_name) in curs.fetchall():
            typeDic[t_name]=t_id
        q_type = typeDic[typeName]
        curs.execute('select * from question where q_type=? and q_score = ?',(q_type,score))
        int i = 0;
        questionList = []
        for(q_id,q_body,q_answer,q_type,q_score) in curs.fetchall():
            if i < num :
                question = Question(q_body,q_answer,q_type,q_score)
                questionList.append(question)
                i += 1
            else:
                break
		return questionList

	def fetchQuestion(self):
		self.num -= 1
		if self.num>=0:
			return self.questionList[self.num]
		else:
			return None
	
class QuestionWindow:
	"""
	represent a question being showed, includes the question body, answer, scores, types
	and the key it get in the race round,as well as the Right or Wrong judge button
	"""
	def __init__(self, question):
		self.question = question
		self.keyPressed = None
		self.judge = None
	def getKeyPressed(self):
		return self.keyPressed
	def setKeyPressed(self, key):
		self.keyPressed = key
	def getJudge(self):
		return self.judge
	def setJudge(self,value):
		self.judge = value
	def getQuestion(self):
		return self.question
	def getAnswer(self):
		return self.question.getAnswer()

from xml.etree import ElementTree
class QuestionDatabase:
	"""
	handle input question file, cook them into formatted database file
	Suppose the input file is in the format of follows:
		questionFile.xml:
		<?xml version="1.0"?>
		<question>
			<body>what the nearest planet to the Sun ?
				A. Mars B. Venus C.Mercury D. Earth</body>
			<answer>C</answer>
			<type>Common Sense</type>
			<score>100</score>
		</question>
	"""
	def __init__(self,inputFile,dbname):
		self.inputFile = inputFile
		self.dbname = dbname
	def connectDatabase(self):
		conn = sqlite3.connect(self.dbname)
        return conn
	def createTable(self,conn):
		curs = conn.cursor()
        typetablecmd = 'create table typetable (t_id int(4),t_name char(100))'
        questiontablecmd = 'create table questiontable (q_id int(4), q_body char(200),\
                        q_answer char(200),q_type int(4), q_score int(4))'
        curs.execute(typetablecmd)
        curs.execute(questiontablecmd)
        conn.commit()
	def handleXML(self,conn):
        curs = conn.cursor()
        root = ElementTree.parse(r"./questions.xml")
        typeList = root.find('typeList')
        typeListNode = typeList.getiterator("type")
        for node in typeListNode:
            typeIdNode = node.find('t_id')
            typeNameNode = node.find('t_name')
            t_id = typeIdNode.text
            t_name = typeNameNode.text
            curs.execute('insert into typetable values(?,?)',(t_id,t_name))
            
        questionListNode = root.getiterator("question")
        q_id = 0
        for node in questionListNode:
            bodyNode = node.find('body')
            answerNode = node.find('answer')
            scoreNode = node.find('score')
            typeNode = node.find('type')  
            q_id += 1
            q_body = bodyNode.text
            q_answer = answerNode.text
            q_type = typeNode.text 
            q_score = scoreNode.text
            curs.execute('insert into questiontable values(?,?,?,?,?)',\
                    (q_id,q_body,q_answer,q_type,q_score))
        conn.commit()
