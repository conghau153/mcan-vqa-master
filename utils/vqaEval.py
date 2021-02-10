# coding=utf-8

__author__='aagrawal'

import sys
import re

class VQAEval:
	def __init__(self, vqa, vqaRes, n=2):
		self.n 			  = n
		self.accuracy     = {}
		self.evalQA       = {}
		self.evalQuesType = {}
		self.evalAnsType  = {}
		self.vqa 		  = vqa
		self.vqaRes       = vqaRes
		self.params		  = {'question_id': vqa.getQuesIds()}
		self.manualMap    = { 'none': '0',
							  'không': '0',
							  'một': '1',
							  'hai': '2',
							  'ba': '3',
							  'bốn': '4',
							  'năm': '5',
							  'sáu': '6',
							  'bảy': '7',
							  'tám': '8',
							  'chín': '9',
							  'mười': '10'
							}
		self.articles     = ['a',
							 'an',
							 'the'
							]
 
		self.periodStrip  = re.compile("(?!<=\d)(\.)(?!\d)")
		self.commaStrip   = re.compile("(\d)(,)(\d)")
		self.punct        = [';', r"/", '[', ']', '"', '{', '}',
							 '(', ')', '=', '+', '\\', '_', '-',
							 '>', '<', '@', '`', ',', '?', '!']

	
	def evaluate(self, quesIds=None):
		if quesIds == None:
			quesIds = [quesId for quesId in self.params['question_id']]
		gts = {}
		res = {}
		for quesId in quesIds:
			gts[quesId] = self.vqa.qa[quesId]
			res[quesId] = self.vqaRes.qa[quesId]
		
		# =================================================
		# Compute accuracy
		# =================================================
		accQA       = []
		accQuesType = {}
		accAnsType  = {}
		print ("computing accuracy")
		step = 0
		for quesId in quesIds:
			resAns      = res[quesId]['answer']
			resAns      = resAns.replace('\n', ' ')
			resAns      = resAns.replace('\t', ' ')
			resAns      = resAns.strip()
			resAns      = self.processPunctuation(resAns)
			resAns      = self.processDigitArticle(resAns)
			gtAcc  = []
			gtAnswers = [ans['answer'] for ans in gts[quesId]['answers']]
			if len(set(gtAnswers)) > 1: 
				for ansDic in gts[quesId]['answers']:
					ansDic['answer'] = self.processPunctuation(ansDic['answer'])
			for gtAnsDatum in gts[quesId]['answers']:
				otherGTAns = [item for item in gts[quesId]['answers'] if item!=gtAnsDatum]
				matchingAns = [item for item in otherGTAns if item['answer']==resAns]
				acc = min(1, float(len(matchingAns))/3)
				gtAcc.append(acc)
			quesType    = gts[quesId]['question_type']
			ansType     = gts[quesId]['answer_type']
			avgGTAcc = float(sum(gtAcc))/len(gtAcc)
			accQA.append(avgGTAcc)
			if quesType not in accQuesType:
				accQuesType[quesType] = []
			accQuesType[quesType].append(avgGTAcc)
			if ansType not in accAnsType:
				accAnsType[ansType] = []
			accAnsType[ansType].append(avgGTAcc)
			self.setEvalQA(quesId, avgGTAcc)
			self.setEvalQuesType(quesId, quesType, avgGTAcc)
			self.setEvalAnsType(quesId, ansType, avgGTAcc)
			if step%100 == 0:
				self.updateProgress(step/float(len(quesIds)))
			step = step + 1

		self.setAccuracy(accQA, accQuesType, accAnsType)
		print ("Done computing accuracy")
	
	def processPunctuation(self, inText):
		outText = inText
		for p in self.punct:
			if (p + ' ' in inText or ' ' + p in inText) or (re.search(self.commaStrip, inText) != None):
				outText = outText.replace(p, '')
			else:
				outText = outText.replace(p, ' ')	
		outText = self.periodStrip.sub("",
									  outText,
									  re.UNICODE)
		return outText
	
	def processDigitArticle(self, inText):
		outText = []
		tempText = inText.lower().split()
		# for word in tempText:
		# 	word = self.manualMap.setdefault(word, word)
		# 	if word not in self.articles:
		# 		outText.append(word)
		# 	else:
		# 		pass
		# for wordId, word in enumerate(outText):
		# 	if word in self.contractions:
		# 		outText[wordId] = self.contractions[word]
		outText = ' '.join(outText)
		return outText

	def setAccuracy(self, accQA, accQuesType, accAnsType):
		self.accuracy['overall']         = round(100*float(sum(accQA))/len(accQA), self.n)
		self.accuracy['perQuestionType'] = {quesType: round(100*float(sum(accQuesType[quesType]))/len(accQuesType[quesType]), self.n) for quesType in accQuesType}
		self.accuracy['perAnswerType']   = {ansType:  round(100*float(sum(accAnsType[ansType]))/len(accAnsType[ansType]), self.n) for ansType in accAnsType}
			
	def setEvalQA(self, quesId, acc):
		self.evalQA[quesId] = round(100*acc, self.n)

	def setEvalQuesType(self, quesId, quesType, acc):
		if quesType not in self.evalQuesType:
			self.evalQuesType[quesType] = {}
		self.evalQuesType[quesType][quesId] = round(100*acc, self.n)
	
	def setEvalAnsType(self, quesId, ansType, acc):
		if ansType not in self.evalAnsType:
			self.evalAnsType[ansType] = {}
		self.evalAnsType[ansType][quesId] = round(100*acc, self.n)

	def updateProgress(self, progress):
		barLength = 20
		status = ""
		if isinstance(progress, int):
			progress = float(progress)
		if not isinstance(progress, float):
			progress = 0
			status = "error: progress var must be float\r\n"
		if progress < 0:
			progress = 0
			status = "Halt...\r\n"
		if progress >= 1:
			progress = 1
			status = "Done...\r\n"
		block = int(round(barLength*progress))
		text = "\rFinshed Percent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), int(progress*100), status)
		sys.stdout.write(text)
		sys.stdout.flush()

