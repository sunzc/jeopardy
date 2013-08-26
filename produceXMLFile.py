#! /usr/bin/env python
# encoding:utf-8
# File Name: produceXML.py
# Author: Sun Zhichuang
# Date  : 2013/8/26
# Task  : produce test data for question.xml

questionTypeList = ["Common Sense","Programmer Expertise","History & Literature",\
    "Economic & Sociology"]
scoreList = [100, 200, 300, 400, 500]
body = "what the nearest planet to the Sun ? \n \
       A. Mars B. Venus C.Mercury D. Earth "
answer = "C"
"""
		<?xml version="1.0"?>
		<question>
            <body></body>
			<answer>C</answer>
			<type>Common Sense</type>
			<score>100</score>
        </question>
"""
print("<?xml version=\"1.0\"?>")
print("<questionList>")
print("\t<typeList>")

id = 0 
for typeName in questionTypeList:
    id +=1
    print("\t\t<type>")
    print("\t\t\t<t_id>%d</t_id>"%id)
    print("\t\t\t<t_name>%s</t_name>"%typeName)
    print("\t\t</type>")

print("\t</typeList>")

for t_id in range(id):
    for score in scoreList:
        for i in range(10):
            print("\t<question>")
            print("\t\t<body>%s</body>"% body )
            print("\t\t<answer>%s</answer>"% answer)
            print("\t\t<type>%s</type>"% str(t_id+1))
            print("\t\t<score>%d</score>" % score)
            print("\t</question>")

print("</questionList>")
