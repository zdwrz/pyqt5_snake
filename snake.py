#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, threading, random

from PyQt5 import QtCore, uic, QtWidgets  
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QPoint

Ui_game_screen, QtBaseClass = uic.loadUiType("snake_main.ui" )
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT =4
PEN_SIZE = 20
GAME_AREA = 50
SCREEN_WIDTH = 640
SCREEN_HIGHT = 480
SPEED = 800
class GameCore:
	def __init__(self):
		self.generateDot()
		self.snake_shape = [QPoint(20,20)]
		self.snake_direction = random.randint(1,4)
		self.snake_head = self.snake_shape[-1]
		# print(self.snake_head)
	def generateDot(self):
		self.dotPosition = QPoint(random.randint(1,SCREEN_WIDTH / PEN_SIZE - 1),random.randint(1,SCREEN_HIGHT / PEN_SIZE - 1))

	def moveSnake(self):
		if self.snake_direction == DIRECTION_UP:
			self.snake_shape.append(QPoint(self.snake_head.x(), self.snake_head.y() - 1))
		elif self.snake_direction == DIRECTION_DOWN:
			self.snake_shape.append(QPoint(self.snake_head.x(), self.snake_head.y() + 1))
		elif self.snake_direction == DIRECTION_LEFT:
			self.snake_shape.append(QPoint(self.snake_head.x() - 1, self.snake_head.y()))
		elif self.snake_direction == DIRECTION_RIGHT:
			self.snake_shape.append(QPoint(self.snake_head.x() + 1, self.snake_head.y()))
		self.snake_head = self.snake_shape[-1]
		if not self.checkCollision():
			return False #Game Over
		self.snake_shape.pop(0)
		if self.snake_head == self.dotPosition:
			self.snake_shape.append(self.dotPosition)
			self.snake_shape.append(self.dotPosition)
			self.snake_shape.append(self.dotPosition)
			self.snake_head = self.snake_shape[-1]
			self.generateDot()
		return True

	def checkCollision(self):
		count = 0
		for body in self.snake_shape:
			if body == self.snake_head:
				count += 1
		if count > 1:
			return False
		if self.snake_head.x() <= 0 or self.snake_head.x() >= SCREEN_WIDTH / PEN_SIZE \
			or self.snake_head.y() <= 0 or self.snake_head.y() >= SCREEN_HIGHT / PEN_SIZE :
			# print(self.snake_head)
			return False
		return True

	def changeDirection(self, direction):
		self.snake_direction = direction

class GameWindow(QtWidgets.QMainWindow, Ui_game_screen):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)	
		# Ui_game_screen.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("Snake eat dots")
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.gameRun)
		self.timer.start(SPEED)
		self.game = GameCore()
		self.pen_snake = QPen()
		self.pen_snake.setWidth(PEN_SIZE)
		self.pen_dot = QPen()
		self.pen_dot.setWidth(PEN_SIZE)
		self.pen_dot.setColor(QColor(255, 0, 0, 127))
		self.pen_board = QPen()
		self.pen_board.setWidth(PEN_SIZE)
		self.pen_board.setColor(QColor(127, 0, 0, 127))
		
	def gameRun(self):
		if not self.game.moveSnake():
			self.timer.stop()
		self.update()

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		qp.setPen(self.pen_snake)
		# size = self.size()
		#Paint Border
		qp.setPen(self.pen_board)
		qp.drawRect(0,0,SCREEN_WIDTH,SCREEN_HIGHT)
		#Paint snake
		for i in range(len(self.game.snake_shape)):
			qp.drawPoint(self.game.snake_shape[i].x() * PEN_SIZE, self.game.snake_shape[i].y() * PEN_SIZE)   
		#Paint Dot
		qp.setPen(self.pen_dot)
		qp.drawPoint(self.game.dotPosition.x() * PEN_SIZE, self.game.dotPosition.y() * PEN_SIZE)
		qp.end()

	def on_playButton_released(self):
		print("maya")
		# self.update()
		self.playButton.hide()

	def keyPressEvent(self, event):
		key_press = event.key()
		# print(key_press)
		# don't need autorepeat, while haven't released, just run once
		if not event.isAutoRepeat():
			if (key_press == Qt.Key_W or key_press == Qt.Key_Up ) and self.game.snake_direction != DIRECTION_DOWN:			# W 
				# print('up')
				self.game.changeDirection(DIRECTION_UP)
			elif (key_press == Qt.Key_S or key_press == Qt.Key_Down ) and self.game.snake_direction != DIRECTION_UP:			# S 
				# print('down')	
				self.game.changeDirection(DIRECTION_DOWN)
			elif (key_press == Qt.Key_A or key_press == Qt.Key_Left ) and self.game.snake_direction != DIRECTION_RIGHT:			# A 
				# print('left')
				self.game.changeDirection(DIRECTION_LEFT)
			elif (key_press == Qt.Key_D or key_press == Qt.Key_Right ) and self.game.snake_direction != DIRECTION_LEFT:			# D
				# print('right')
				self.game.changeDirection(DIRECTION_RIGHT)
			elif key_press == Qt.Key_Space:			# SPACE 
				if self.timer.isActive():
					self.timer.stop()
				else: 
					self.timer.start()
		self.update()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	gameWindow = GameWindow()
	gameWindow.show()
	sys.exit(app.exec_())