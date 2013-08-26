#! /usr/bin/env python
# encoding: utf-8
# File Name: test_jeopardy.py
# Author: Sun Zhichuang
# Date  : 2013/8/25
# Task  : test the jeopardy_prototype.py

TestGroup = 0
TestGroupPad = 0
TestQuestion = 0
TestQuestionDatabase = 0
TestQuestionSquare = 0
TestQuestionType = 0
TestQuestionBoard = 1

if TestQuestionBoard == 1:
    from jeopardy_prototype import QuestionBoard
    qb = QuestionBoard()
    qt_CS = qb.getQuestionTypeByType('Common Sense')
    qt_PE = qb.getQuestionTypeByType('Programmer Expertise')
    qt_HL = qb.getQuestionTypeByType('History Literature')
    qt_ES = qb.getQuestionTypeByType('Economic Sociology')
    qt_list = [qt_CS,qt_PE,qt_HL,qt_ES]
    questionTypeList = qb.getQuestionTypeList()
    index = 0
    for qt in qt_list:
        qs = qt.getQuestionSquareByScore(100)
        ques = qs.fetchQuestion()
        print("[in %s]Get Question Info: body = %s, answer = %s, type = %s, score = %d" \
        %(questionTypeList[index],ques.getBody(), ques.getAnswer(),ques.getType(),ques.getScore()))
        print("questions left : %d" % qs.getQuestionNum())
        index += 1
     

if TestQuestionType == 1:
    from jeopardy_prototype import QuestionType
    qt = QuestionType('Common Sense')
    qs = qt.getQuestionSquareByScore(100)
    ques = qs.fetchQuestion()
    print("[in TestQuestionType]Get Question Info: body = %s, answer = %s, type = %s, score = %d" \
    %(ques.getBody(), ques.getAnswer(),ques.getType(),ques.getScore()))
    print("questions left : %d" % qs.getQuestionNum())

     

if TestQuestionSquare == 1:
    from jeopardy_prototype import QuestionSquare, Jeopardy
    qs = QuestionSquare("Common Sense",100,10)
    ques = qs.fetchQuestion()
    print("Get Question Info: body = %s, answer = %s, type = %s, score = %d" \
    %(ques.getBody(), ques.getAnswer(),ques.getType(),ques.getScore()))
    print("questions left : %d" % qs.getQuestionNum())

if TestQuestionDatabase == 1:
    from jeopardy_prototype import QuestionDatabase, Jeopardy
    jp = Jeopardy()
    dbname = jp.getDatabase()
    inputFile = "questions.xml"
    qd = QuestionDatabase(inputFile,dbname)
    conn = qd.connectDatabase()
    qd.createTable(conn)
    qd.handleXML(conn)
    curs = conn.cursor()
    curs.execute('select * from questiontable')
    for (q_id, q_body, q_answer, q_type, q_score) in curs.fetchall():
        print("q_id = %d, q_body = %s, q_answer = %s, q_type = %d, q_score = %d"%(q_id,q_body,q_answer,q_type,q_score))
    conn.close()

if TestGroup == 1:
    from jeopardy_prototype import Group
    gp = Group('C','TA_happy_ending','Sun Zhichuang\nZhang Mengchi\nGuan Xuetao')
    gp.addScore(100)
    print("Group info: key = %s, nick = %s, members = %s, score = %d"%(gp.getKey(),\
            gp.getNick(),gp.getMembers(),gp.getScore()))

if TestGroupPad == 1:
    from jeopardy_prototype import Group,GroupPad
    gp = Group('C','TA_happy_ending','Sun Zhichuang\nZhang Mengchi\nGuan Xuetao')
    gp.addScore(100)
    gppad = GroupPad()
    gppad.addGroup(gp)
    newgp = gppad.getGroupByKey('C')
    print("Get Group Info By Key: key = %s, nick = %s, members = %s, score = %d" \
    %(newgp.getKey(), newgp.getNick(),newgp.getMembers(),newgp.getScore()))
    
if TestQuestion == 1:
    from jeopardy_prototype import Question
    ques = Question("who invent bulb?","Edison","Common Sense",100)
    print("Get Question Info: body = %s, answer = %s, type = %s, score = %d" \
    %(ques.getBody(), ques.getAnswer(),ques.getType(),ques.getScore()))

