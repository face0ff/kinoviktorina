
# -*- coding: utf-8 -*-
import kivy
import os
import sys
import random
import re
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.progressbar import ProgressBar
from kivmob import KivMob
import shutil
from kivy.utils import platform

Builder.load_file(os.path.join ("my.kv"))

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
# Builder.load_file(os.path.join ("my1(2).kv"))
Window.fullScreen = True




# Declare both scsreens
class MenuScreen(Screen):
	
	def setSett(self):
		sm.get_screen('settings').ids.textL.text = str(score)
		sm.get_screen('settings').ids.textLose.text = str(lose)
		sm.get_screen('settings').ids.textW.text = str(winScore)
		sm.get_screen('vopros').ids.ostalos.value = ostalos



		

class ScoreScreenW(Screen):
	pass
class ScoreScreenL(Screen):

	def proverkaLose(self):
		with open('dataS.txt', 'r', encoding='utf-8') as f:
			listScoreStart = f.read()
		num_list = [int(num) for num in filter(lambda num: num.isnumeric(), listScoreStart)]
		lose = int(num_list[2])
		if lose >= 3:
			self.manager.current = 'endGame'
		else:
			self.manager.current = 'vopros'

class EndGameScreen(Screen):
	pass
	

	


		
# app: всегда относится к экземпляру вашего приложения.
# root: относится к базовому виджету / шаблону в текущем правиле
# self: всегда обращаться к текущему виджету		
		
		



class VoprosScreen(Screen):

	# достает прогресс из фаила
	with open('dataS.txt', 'r', encoding='utf-8') as f:
		listScoreStart = f.read()
	
	print(listScoreStart)
	# достает цифры из списка
	nums = re.findall(r'\d+', listScoreStart)
	num_list = [int(i) for i in nums]

	global score
	global winScore
	global lose
	global ostalos
	ostalos = 0
	global xStart
	xStart = 0

	# срез списка на циферы 
	score = int(num_list[0])
	
	winScore = int(num_list[1])
	
	lose = int(num_list[2])
	#  загружает циферы до загрузки экрана
	def on_pre_enter(self):

		self.poiskPerem()
		self.soundLoad()


	
	def scorePlus(self):
		global score
		global lose
		if score >=0:
			score=int(score) + 1
			sm.get_screen('settings').ids.textL.text = str(score)

		if lose >= 3:
			sm.get_screen('settings').ids.textLose.text = str(lose)
			sm.get_screen('settings').ids.textW.text = str(winScore)
			self.manager.current = 'endGame'

		



	def soundLoad(self):
		self.sound = SoundLoader.load(question)

	def btn_first(self):
		global xStart
		
		if xStart == 0:
			self.sound = SoundLoader.load(question)
			self.sound.play()
			self.sound.loop = True
			self.ids['button_one'].background_normal = 'downPlay.png'
			xStart = xStart + 1

		else:
			self.ids['button_one'].background_normal = 'normPlay.png'
			self.sound.stop()
			xStart = 0
	



	def poiskPerem(self ,*args):

		
		# quizFile = open('data.txt',"r", encoding='utf-8' )
		# quizData = quizFile.readlines()
		if os.stat('data.txt').st_size > 0:

			with open('data.txt', 'r', encoding='utf-8') as f:
				quizData = f.readlines()
			
			random.shuffle(quizData)
			# print(quizData[0])

			# print('[%s]' % ', '.join(map(str, quizData)))

			for i in range(1):
				x = quizData[i].strip()
				data = x.split(",")
				global question
				question = str(data[0])
				global correctAnswer

				correctAnswer = str(data[1])
				incorectAnswer = data[1:]
				random.shuffle(incorectAnswer)
				# self.ids.quest.text = question
				
				global score
				score=int(score)
				sm.get_screen('settings').ids.textL.text = str(score)
				

				global lose
				
				sm.get_screen('settings').ids.textLose.text = str(lose)

				global ostalos
				ostalos = 3 - lose
				sm.get_screen('vopros').ids.ostalos.value = ostalos


				# pereig = quizData[0]
				with open('data.txt', 'w', encoding='utf-8') as f:
					f.writelines(quizData[1:])

				

				# print(question)
				# print(correctAnswer)
				# print('[%s]' % ', '.join(map(str, incorectAnswer)))

				for i in range(4):
					# oneAnswer = incorectAnswer[i]
					self.ids.ansveR.text = incorectAnswer[0]
					self.ids.ansveR1.text = incorectAnswer[1]
					self.ids.ansveR2.text = incorectAnswer[2]
					self.ids.ansveR3.text = incorectAnswer[3]

				listScore =[score, winScore, lose]
				

				with open('dataS.txt', 'w', encoding='utf-8') as f:
					f.writelines(str(listScore))
				# print(f)
				
		else:
			self.manager.current = 'settings'
				
	def callback(self):
		global xStart
		xStart = 0
		self.ids['button_one'].background_normal = 'normPlay.png'
		if self.ids.ansveR.text == correctAnswer:
			self.manager.current = 'scoreW'
			global winScore
			winScore=int(winScore)+1
			self.poiskPerem()
			sm.get_screen('settings').ids.textW.text = str(winScore)
		else:
			global lose
			lose=int(lose)+1
			self.manager.current = 'scoreL'
		
	def callback1(self):
		global xStart
		xStart = 0
		self.ids['button_one'].background_normal = 'normPlay.png'

		if self.ids.ansveR1.text == correctAnswer:
			print(correctAnswer)
			self.manager.current = 'scoreW'
			global winScore
			winScore=winScore+1
			self.poiskPerem()
			sm.get_screen('settings').ids.textW.text = str(winScore)
		else:
			global lose
			lose=int(lose)+1
			self.manager.current = 'scoreL'

	def callback2(self):
		global xStart
		xStart = 0
		self.ids['button_one'].background_normal = 'normPlay.png'

		if self.ids.ansveR2.text == correctAnswer:
			print(correctAnswer)
			self.manager.current = 'scoreW'
			global winScore
			winScore=winScore+1
			self.poiskPerem()
			sm.get_screen('settings').ids.textW.text = str(winScore)
		else:
			global lose
			lose=int(lose)+1
			self.manager.current = 'scoreL'

	def callback3(self):
		global xStart
		xStart = 0
		self.ids['button_one'].background_normal = 'normPlay.png'

		if self.ids.ansveR3.text == correctAnswer:
			print(correctAnswer)
			self.manager.current = 'scoreW'
			global winScore
			winScore=winScore+1
			self.poiskPerem()
			sm.get_screen('settings').ids.textW.text = str(winScore)
		else:
			global lose
			lose=int(lose)+1
			self.manager.current = 'scoreL'


class SettingsScreen(Screen):
	
	def copyData(self):
		shutil.copy2("dataBack.txt", "data.txt")
		shutil.copy2("dataBackS.txt", "dataS.txt")
		global score
		global winScore
		global lose
		global ostalos
		ostalos = 3
		score = 0
		winScore = 0
		lose = 0
		sm.get_screen('settings').ids.textL.text = str(score)
		sm.get_screen('settings').ids.textLose.text = str(lose)
		sm.get_screen('settings').ids.textW.text = str(winScore)
		sm.get_screen('vopros').ids.ostalos.value = ostalos
		self.manager.current = 'menu'



		

	
	
sm = ScreenManager(transition=FadeTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(ScoreScreenW(name='scoreW'))
sm.add_widget(ScoreScreenL(name='scoreL'))
sm.add_widget(EndGameScreen(name='endGame'))
sm.add_widget(VoprosScreen(name='vopros'))


class TestApp(App):
	def __init__(self, **kwargs):

		
		self.title = "KinoViktorina"
		if platform not in ("android", "ios"):
			 Window.size = (400, 750)
		super().__init__(**kwargs)
	def build(self):
		self.ads = KivMob('ca-app-pub-1222043780390154~2212404600')
		self.ads.new_interstitial('ca-app-pub-1222043780390154/3142342897')
		self.ads.request_interstitial()

		return sm
	def on_resume(self):
		self.ads.request_interstitial()
		

		

if __name__ == '__main__':
	TestApp().run()


# root.silkaPop.poiskPerem() 
# class SimplePopup(Popup):
#     silkaPop = VoprosScreen()
# <SimplePopup>:
#     id:pop
#     size_hint: .4, .4
#     auto_dismiss: False
#     title: 'Hello world!!'
#     Button:
#         text: 'Click here to dismiss'
#         on_press: pop.dismiss() ; root.silkaPop.poiskPerem() 
# root.fire_popup() ;
# text = "Fire Popup !"
# 	def fire_popup(self):
# 		pops=SimplePopup()
# 		pops.open()
# self.ads = KivMob("ca-app-pub-1222043780390154~2212404600")
# 		self.ads.new_interstitial("ca-app-pub-1222043780390154/3142342897")

# background_color: 0, 0, 0, 0
