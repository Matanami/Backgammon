import time
import tkinter as tk
from tkinter import *
import random
import functools
from PIL import Image, ImageTk



class Board(tk.Frame):

    def __init__(self, parent, length, width):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.length = length
        self.width = width
        self.config(height=self.length * 100, width=self.width * 100)
        self.pack()
        self.red_tri_up = ImageTk.PhotoImage(Image.open("Imgae/up_red.jpg").resize((60, 400)))
        self.black_tri_up = ImageTk.PhotoImage(Image.open("Imgae/up_black.jpg").resize((60, 400)))
        self.red_tri_down = ImageTk.PhotoImage(Image.open("Imgae/up_red.jpg").rotate(180).resize((60, 400)))
        self.black_tri_down = ImageTk.PhotoImage(Image.open("Imgae/up_black.jpg").rotate(180).resize((60, 400)))
        self.black_line = ImageTk.PhotoImage(Image.open("Imgae/black_line.png").resize((20, 800)))
        self.black_circul = ImageTk.PhotoImage(Image.open("Imgae/black_circul.jpg").resize((40, 40)))
        self.white_circul = ImageTk.PhotoImage(Image.open("Imgae/white_cir.jpg").resize((40, 40)))
        self.playing_color =None
        self.buttons = {}#dic of all the buttons
        self.play_fild = {}#dic of the high of the o=play fild
        self.black_solider = {}
        self.white_solider = {}
        self.black_fild = {}
        self.white_fild = {}
        self.dice = {}
        self.import_and_create_dice()
        self.x_coord = {0: 35, 1: 94, 2: 156, 3: 219, 4: 283, 5: 342, 6: 427, 7: 488, 8: 552, 9: 618, 10: 678, 11: 735,
                   23: 35, 22: 94, 21: 156, 20: 219, 19: 283, 18: 342, 17: 427, 16: 488, 15: 552, 14: 618, 13: 678,
                   12: 735}
        self.set_borad()
        self.turn = 0
        self.white_num = [0,0]
        self.black_num = [0,0]
        self.white_roll = [0,0]
        self.black_roll = [0,0]
        self.messege = Label(self)
        self.okVar = tk.StringVar()
        self.out_come = None
        self.white_roll_x_coord = 590
        self.white_roll_y_coord = 400
        self.black_roll_x_coord = 170
        self.black_roll_y_coord = 400
        self.curr_play = None
        self.valid_move = [] #list 0f valid move
        self.switch = 0 # switch between statos 0-pick solger to move,1-pick a place to move to , 2- when the curent player have eating solider
        self.white_eated = [] #list of the eating solider
        self.black_eated = []
        self.op_eat =[] #list of the options to  eating solider
        self.double = False
        self.double_dice = 0
        self.white_solider_eated = 0#the num of eating solider
        self.black_solider_eated = 0
        self.op_free = []#list of the options to free eating solider
        self.white_get_out = []
        self.black_get_out = []

    def free_the_eat(self):
        self.op_eat = []
        self.op_free = []
        if self.turn == 0:
            if self.white_solider_eated>0:
                self.switch = 2
                if self.white_num[0] > 0:
                    if 24-self.white_num[0] not in self.black_solider :
                        self.buttons[24-self.white_num[0]].config(bg="green")
                        self.op_free.append(24-self.white_num[0])
                    elif len(self.black_solider[24-self.white_num[0]]) == 1:
                        self.buttons[24 - self.white_num[0]].config(bg="green")
                        self.op_free.append(24 - self.white_num[0])
                        self.op_eat.append(24 - self.white_num[0])
                if self.white_num[1] > 0:
                    if 24-self.white_num[1] not in self.black_solider :
                        self.buttons[24-self.white_num[1]].config(bg="green")
                        self.op_free.append(24-self.white_num[1])
                    elif len(self.black_solider[24-self.white_num[1]]) == 1:
                        self.buttons[24 - self.white_num[1]].config(bg="green")
                        self.op_free.append(24 - self.white_num[1])
                        self.op_eat.append(24 - self.white_num[1])
                if len(self.op_free) == 0 :
                    self.switch = 0
                    self.turn = 1
                    self.the_game()
        if self.turn == 1:
            if self.black_solider_eated>0:
                self.switch = 2
                if self.black_num[0] > 0:
                    if self.black_num[0]-1 not in self.white_solider :
                        self.buttons[self.black_num[0]-1].config(bg="green")
                        self.op_free.append(self.black_num[0]-1)
                    elif len(self.white_solider[self.black_num[0]-1]) == 1:
                        self.buttons[-1+self.black_num[0]].config(bg="green")
                        self.op_free.append(-1+self.black_num[0])
                        self.op_eat.append(-1+self.black_num[0])
                if self.black_num[1] > 0:
                    if self.black_num[1]-1 not in self.white_solider:
                        self.buttons[-1+self.black_num[1]].config(bg="green")
                        self.op_free.append(-1+self.black_num[1])
                    elif len(self.white_solider[-1+self.black_num[1]]) == 1:
                        self.buttons[-1+self.black_num[1]].config(bg="green")
                        self.op_free.append(-1+self.black_num[1])
                        self.op_eat.append(-1+self.black_num[1])
                if len(self.op_free) == 0 :
                    self.switch = 0
                    self.turn = 0
                    self.the_game()

    def eat(self,num,color):
        '''
        :param num: the number of button where the eating solider in
        :param color: the color of the eating solider
        :return: null
        '''
        self.play_fild[num] -=1
        if color == "white":
            label = self.white_solider[num].pop()
            self.white_solider_eated += 1
            label.place(x=390, y=320 -self.white_solider_eated*40)
            self.white_eated.append(label)
            self.white_solider.pop(num)
        if color == "black":
            label = self.black_solider[num].pop()
            self.black_solider_eated += 1
            label.place(x=390, y=440+self.black_solider_eated*40)
            self.black_eated.append(label)
            self.black_solider.pop(num)


    def check_move(self,num,checker = False):
        '''
        check for giving button of place acording to which player know playing to where he can go
        :param num:
        :return:
        '''

        self.clear_path()
        self.buttons[num].config(bg="red")
        self.valid_move =[]
        self.op_eat = []
        self.curr_play = None
        self.switch = 1
        final_move = self.check_final_move()
        if self.turn == 0:
            self.white_get_out = []
            if self.white_num[0] > 0:
                if  num - self.white_num[0] >= 0 : #check if the move in the border and not the same spot
                    if num - self.white_num[0] not in self.black_solider:
                        self.buttons[num-self.white_num[0]].config(bg="green")
                        self.valid_move.append(num-self.white_num[0])
                    elif len(self.black_solider[num-self.white_num[0]]) == 1: #check if the move is opp for eating
                        self.buttons[num-self.white_num[0]].config(bg="red")
                        self.valid_move.append(num - self.white_num[0])
                        self.op_eat.append(num - self.white_num[0])
                if final_move:
                    if num - self.white_num[0] == -1 :
                        self.left_border.config(bg="green")
                        self.white_get_out.append([num,0])
                    elif num -self.white_num[0] < -1 and num == (functools.reduce(lambda a,b:a if a>b else b , self.white_solider.keys())):
                        self.left_border.config(bg="green")
                        self.white_get_out.append([num,0])
            if self.white_num[1] > 0:
                if num - self.white_num[1] >= 0 : #check if the move in the border and not the same spot
                    if num - self.white_num[1] not in self.black_solider:
                        self.buttons[num-self.white_num[1]].config(bg="green")
                        self.valid_move.append(num - self.white_num[1])
                    elif len(self.black_solider[num-self.white_num[1]]) == 1 :
                        self.buttons[num - self.white_num[1]].config(bg="green")
                        self.valid_move.append(num - self.white_num[1])
                        self.op_eat.append(num - self.white_num[1])
                if final_move:
                    if num - self.white_num[1] == -1 :
                        self.left_border.config(bg="green")
                        self.white_get_out.append([num,1])
                    elif num - self.white_num[1] < -1 and num == (functools.reduce(lambda a, b: a if a>b else b, self.white_solider.keys())):
                        self.white_get_out.append([num,1])
                        self.left_border.config(bg="green")
            if num - self.white_num[1] - self.white_num[0] >= 0 and self.white_num[1] > 0 and self.white_num[0] > 0:  #check if the move in the border and not the same spot
                if num - self.white_num[1] not in self.black_solider or num - self.white_num[0] not in self.black_solider:
                    if num - self.white_num[1] - self.white_num[0] not in self.black_solider :
                        self.buttons[num - self.white_num[1]-self.white_num[0]].config(bg="green")
                        self.valid_move.append(num - self.white_num[1]-self.white_num[0])
                    elif len(self.black_solider[num-self.white_num[1]-self.white_num[0]]) == 1 :
                        self.buttons[num - self.white_num[1]-self.white_num[0]].config(bg="green")
                        self.valid_move.append(num - self.white_num[1]-self.white_num[0])
                        self.op_eat.append(num - self.white_num[1]-self.white_num[0])
        elif self.turn == 1:
            if  self.black_num[0] > 0:
                if num + self.black_num[0]<24 :
                    if num + self.black_num[0] not in self.white_solider:
                        self.buttons[num+self.black_num[0]].config(bg="green")
                        self.valid_move.append(num+self.black_num[0])
                    elif len(self.white_solider[num+self.black_num[0]]) == 1 :
                        self.buttons[num + self.black_num[0]].config(bg="green")
                        self.valid_move.append(num+self.black_num[0])
                        self.op_eat.append(num+self.black_num[0])
                elif final_move:
                    if num + self.black_num[0] == 24 :
                        self.left_border.config(bg="green")
                        self.black_get_out.append([num,0])
                    elif num + self.black_num[0] > 24 and num == (functools.reduce(lambda a,b:a if a<b else b , self.black_solider.keys())):
                        self.black_get_out.append([num,0])
                        self.left_border.config(bg="green")
            if self.black_num[1] > 0:
                if num + self.black_num[1] < 24 :
                    if num + self.black_num[1] not in self.white_solider:
                        self.buttons[num+self.black_num[1]].config(bg="green")
                        self.valid_move.append(num+self.black_num[1])
                    elif len(self.white_solider[num+self.black_num[1]]) == 1 :
                        self.buttons[num + self.black_num[1]].config(bg="green")
                        self.valid_move.append(num+self.black_num[1])
                        self.op_eat.append(num + self.black_num[1])
                elif final_move:
                    if num + self.black_num[1] == 24 :
                        self.left_border.config(bg="green")
                        self.black_get_out.append([num,1])
                    elif num + self.black_num[1] >24 and num == (functools.reduce(lambda a,b:a if a<b else b , self.black_solider.keys())):
                        self.left_border.config(bg="green")
                        self.black_get_out.append([num,1])
            if num + self.black_num[1] + self.black_num[0] < 24 and self.black_num[0] > 0 and self.black_num[1] > 0:
                if num + self.black_num[1] not in self.white_solider or num + self.black_num[0] not in self.white_solider:
                    if (num + self.black_num[1] + self.black_num[0] not in self.white_solider):
                        self.buttons[num+self.black_num[1]+self.black_num[0]].config(bg="green")
                        self.valid_move.append(num+self.black_num[1]+self.black_num[0])
                    elif len(self.white_solider[num + self.black_num[1] + self.black_num[0]]) == 1 :
                        self.buttons[num+self.black_num[1]+self.black_num[0]].config(bg="green")
                        self.valid_move.append(num+self.black_num[1]+self.black_num[0])
                        self.op_eat.append((num+self.black_num[1]+self.black_num[0]))
        if checker:
            return len(self.valid_move)>0

    def side_border(self,side):
        if self.switch != 1:
            return
        else:
            if self.turn == 0 and len(self.white_get_out) > 0:
                num,dice = self.white_get_out.pop()
                self.white_num[dice] = 0
                self.white_solider[num].pop().place_forget()
                if len(self.white_solider[num]) == 0:
                    self.white_solider.pop(num)
                self.play_fild[num] -= 1
                if self.check_winner():
                    self.messege.config(text="the white winnnnnn")
                    return
                if self.white_num[0] == 0 and self.white_num[1] == 0:
                    self.turn = 1
                    self.clear_path()
                    self.the_game()
                else:
                    self.clear_path()
                    self.switch = 0

            if self.turn == 1 and len(self.black_get_out) > 0:
                num, dice = self.black_get_out.pop()
                self.black_num[dice] = 0
                self.black_solider[num].pop().place_forget()
                if len(self.black_solider[num]) == 0:
                    self.black_solider.pop(num)
                self.play_fild[num] -= 1
                if self.check_winner():
                    self.messege.config(text="the black winnnnnn")
                    return
                if self.black_num[0] == 0 and self.black_num[1] == 0:
                    self.turn = 0
                    self.clear_path()
                    self.the_game()
                else:
                    self.clear_path()
                    self.switch = 0


    def bord_button_prees(self,num):
        '''
        make the command when the buttom press
        :param num:
        :return: null
        '''
        if self.switch == 3:
            return
        elif self.switch == 2:#when the player have eating soilder
            if self.turn == 0:#check how tuen it is
                #check if there are valid move
                if len(self.op_free) == 0 :
                    self.switch = 0
                    self.turn = 1
                    self.the_game()
                elif num in self.op_free:# check if there are available step
                    #moving the eat solider back
                    print(self.white_eated)
                    label = self.white_eated.pop().place_forget()
                    self.white_solider_eated -= 1
                    #check if the move eat the other player
                    if num in self.op_eat:
                        self.eat(num,"black")
                    self.add_piece_to(num, "white", self.play_fild[num], "down")
                    self.switch = 0
                    dice = 24 - num
                    # delete the used dice
                    if self.white_num[0] == dice:
                        self.white_num[0] = 0
                    else:
                        self.white_num[1] = 0
                    if self.white_num[0] == 0 and self.white_num[1] == 0:
                        self.switch = 0
                        self.turn = 1
                        self.op_free = []
                        self.the_game()
            if self.turn == 1:
                #check if there are valid move
                if len(self.op_free) == 0:
                    self.switch = 0
                    self.turn = 0
                    self.the_game()
                elif num in self.op_free:
                    print(self.black_eated)
                    label = self.black_eated.pop().place_forget()
                    self.black_solider_eated -= 1
                    #check if the move eat the other player
                    if num in self.op_eat:
                        self.eat(num,"white")
                    self.add_piece_to(num, "black", self.play_fild[num], "up")
                    self.switch = 0
                    dice = 1 + num
                    # delete the used dice
                    if self.black_num[0] == dice:
                        self.black_num[0] = 0
                    else:
                        self.black_num[1] = 0
                    if self.black_num[0] == 0 and self.black_num[1] == 0:
                        self.switch = 0
                        self.turn = 0
                        self.op_free = []
                        self.the_game()

            self.clear_path()
            return

        elif self.switch == 0:
            if self.turn == 0:
                if self.white_solider_eated > 0:
                    return
                if not self.check_final_move():
                    flag = False
                    for solider in self.white_solider:
                        if self.check_move(solider, True):
                            flag = True
                            break
                    if not flag:
                        self.turn = 1
                        self.messege.config(text="the white don't have valid move")
                        time.sleep(2)
                        self.the_game()
                    else:
                        self.clear_path()
                if num in self.white_solider:
                    self.check_move(num)
                    self.curr_play = num
                    self.switch = 1
                else:
                    return
            if self.turn == 1:
                if self.black_solider_eated > 0:
                    return
                if not self.check_final_move():
                    flag = False
                    for solider in self.white_solider:
                        if self.check_move(solider, True):
                            flag = True
                            break
                    if not flag:
                        self.turn = 0
                        self.messege.config(text="the black don't have valid move")
                        time.sleep(2)
                        self.the_game()
                    else:
                        self.clear_path()
                if num in self.black_solider:
                    self.check_move(num)
                    self.switch = 1
                    self.curr_play = num
                else:
                    return
        elif self.switch == 1:
            if self.curr_play == num or len(self.valid_move) == 0:
                self.clear_path()
                self.switch = 0
            elif num in self.valid_move:
                if self.turn == 0:
                    # take out the solider how moving
                    label = self.white_solider[self.curr_play].pop().place_forget()
                    # if it's the last solider in the ceil delete the ciel
                    if len(self.white_solider[self.curr_play]) == 0:
                        self.white_solider.pop(self.curr_play)
                    self.play_fild[self.curr_play] -= 1
                    # put the solider in the new place
                    if num < 12:
                        place = "up"
                    else:
                        place = "down"
                    if num in self.op_eat:
                        self.eat(num,"black")
                    self.add_piece_to(num, "white", self.play_fild[num], place)
                    # find the with whice dice used and delete her
                    dice = self.curr_play-num
                    if self.white_num[0] == dice:
                        self.white_num[0] = 0
                    elif self.white_num[1] == dice:
                        self.white_num[1] = 0
                    else:
                        self.white_num[0] = 0
                        self.white_num[1] = 0
                else:
                    label = self.black_solider[self.curr_play].pop().place_forget()
                    self.play_fild[self.curr_play] -= 1
                    if len(self.black_solider[self.curr_play]) == 0:
                        self.black_solider.pop(self.curr_play)
                    if num < 12:
                        place = "up"
                    else:
                        place = "down"
                    if num in self.op_eat:
                        self.eat(num,"white")
                    self.add_piece_to(num, "black", self.play_fild[num], place)
                    dice = num-self.curr_play
                    if self.black_num[0] == dice:
                        self.black_num[0] = 0
                    elif self.black_num[1] == dice:
                        self.black_num[1] = 0
                    else:
                        self.black_num[0] = 0
                        self.black_num[1] = 0
            self.switch = 0
            self.clear_path()
        if self.turn == 1:
            # check if used the two dice and if it is a double the are 2 more
            if self.black_num[0] == 0 and self.black_num[1] == 0:
                if self.double :
                    self.black_num[1] = self.black_num[0] = self.double_dice
                    self.double = False
                else:
                    self.turn = 0
                    self.switch = 3
                    self.the_game()
        else:
            if self.white_num[0] == 0 and self.white_num[1] == 0:
                if self.double:
                    self.white_num[1] = self.white_num[0] = self.double_dice
                    self.double = False
                else:

                    self.turn = 1
                    self.switch = 3
                    self.the_game()

    def check_final_move(self):
        if self.turn == 0:
            for solider in self.white_solider:
                if solider > 5:
                    return False
            return True
        else:
            for solider in self.black_solider:
                if solider < 17:
                    return False
            return True

    def clear_path(self):
        #clear all the bg color
        for button in self.buttons:
            self.buttons[button].config(bg="white",state=NORMAL)
        self.curr_play = None
        self.valid_move = []
        self.left_border.config(bg="white")

    def check_winner(self):
        if self.turn == 0:
            return len(self.black_solider) == 0
        else:
            return len(self.white_solider) == 0

    def the_game(self,first_turn=False):
        self.black_roll[0].place_forget()
        self.white_roll[0].place_forget()
        if self.turn == 0:
            if not first_turn:
                self.black_roll[1].place_forget()
            if self.check_winner():
                self.messege.config(text="the black winnnnnn")
            else:
                self.messege.config(text="white turn")
                self.playing_color = "white"
                self.white_roll[0] = Button(self,text="roll",command=lambda: self.roll("white",2))
                self.white_roll[0].place(x=self.white_roll_x_coord, y= self.white_roll_y_coord)
        else:
            if not first_turn:
                self.white_roll[1].place_forget()
            if self.check_winner():
                self.messege.config(text="the white winnnnnn")
            else:
                self.messege.config(text="black turn")
                self.playing_color = "black"
                self.black_roll[0] = Button(self,text="roll",command=lambda: self.roll("black",2))
                self.black_roll[0].place(x=self.black_roll_x_coord, y=self.black_roll_y_coord)

        self.wait_variable(self.okVar)

        if self.turn == 0:
            if self.white_num[0] == self.white_num[1]:
                self.double = True
                self.double_dice = self.white_num[0]

        else:
            if self.black_num[0] == self.black_num[1]:
                self.double =True
                self.double_dice = self.black_num[0]
        self.switch = 0



    def set_borad(self):
        for i in range(24):

            self.play_fild.setdefault(i, 0)
        for x in range(12):
            if x == 0:
                self.left_border = Button(self, image=self.black_line, bd=0, command=lambda :self.side_border("left"))
                self.left_border.grid(row=1, column=0, rowspan=2)
                self.right_border = Button(self, image=self.black_line, bd=0 ,command=lambda :self.side_border("right"))
                self.right_border.grid(row=1, column=14, rowspan=2)
            if x == 7:
                self.border_button = Button(self, image=self.black_line, bd=0, command=self.free_the_eat)
                self.border_button.grid(row=1, column=x, rowspan=2)
            if x < 12:
                if x % 2 == 0:
                    image = self.red_tri_up
                else:
                    image = self.black_tri_up
                button = Button(self, image=image, bd=0,command=lambda spot=x: self.bord_button_prees(spot))
                if x < 6:
                    button.grid(row=1, column=x+1)
                else:
                    button.grid(row=1, column=x + 2)
                self.buttons.setdefault(x, button)
        for x in range(12):
                if x % 2 == 1:
                    image = self.red_tri_down
                else:
                    image = self.black_tri_down
                button = Button(self, image=image, bd=0, command=lambda spot=x: self.bord_button_prees(23-spot))
                if x < 6:
                    button.grid(row=2, column=x+1)
                else:
                    button.grid(row=2, column=x+2)
                self.buttons.setdefault(23-x, button)

        self.set_the_solider()
        self.start_button = Button(self, text="Start", command=self.start)
        self.start_button.place(x=385, y=400)


    def set_the_solider(self):

        for x in range(15):
            if x < 2:

                fild_up = 0
                color_up = "black"
                fild_down = 23
                color_down = "white"
            elif x < 7:
                fild_up = 5
                color_up = "white"
                fild_down = 18
                color_down = "black"
            elif x < 10:
                fild_up = 7
                color_up = "white"
                fild_down = 16
                color_down = "black"
            else:
                fild_up = 11
                color_up = "black"
                fild_down = 12
                color_down = "white"
            self.add_piece_to(fild_up, color_up, self.play_fild[fild_up], "up")
            self.add_piece_to(fild_down, color_down, self.play_fild[fild_down], "down")



    def add_piece_to(self, ground, color, fild_num, up_or_down):
        height = fild_num * 42
        if up_or_down == "down":
            height = 760 - height
        if color == "black":
            label = Label(self, image=self.black_circul, bd=0,borderwidth=0)
            if ground in self.black_solider:
                self.black_solider[ground].append(label)
            else:
                self.black_solider[ground] = [label]
            if ground in self.black_fild:
                self.black_fild[ground] += 1
            else:
                self.black_fild.setdefault(ground,1)
        else:
            label = Label(self, image=self.white_circul, bd=0,borderwidth=0)
            if ground in self.white_solider:
                self.white_solider[ground].append(label)
            else:
                self.white_solider[ground] = [label]
            if ground in self.white_fild:
                self.white_fild[ground] += 1
            else:
                self.white_fild.setdefault(ground,1)
        label.place(x=self.x_coord[ground], y=height)
        self.play_fild[ground] = fild_num + 1


    def import_and_create_dice(self):
        dice_1 = ImageTk.PhotoImage(Image.open("Imgae/dice_1.jpg").resize((40, 40)))
        dice_2 = ImageTk.PhotoImage(Image.open("Imgae/dice_2.jpg").resize((40, 40)))
        dice_3 = ImageTk.PhotoImage(Image.open("Imgae/dice_3.jpg").resize((40, 40)))
        dice_4 = ImageTk.PhotoImage(Image.open("Imgae/dice_4.jpg").resize((40, 40)))
        dice_5 = ImageTk.PhotoImage(Image.open("Imgae/dice_5.jpg").resize((40, 40)))
        dice_6 = ImageTk.PhotoImage(Image.open("Imgae/dice_6.jpg").resize((40, 40)))
        self.dice = {1: dice_1, 2: dice_2, 3: dice_3, 4: dice_4, 5: dice_5, 6: dice_6}

    def start(self,sec_try=False):
        self.start_button.place_forget()
        self.update()
        self.white_roll[0] = Button(self, text="white", command=lambda:self.roll("white",1))
        self.black_roll[0] = Button(self, text="black", command=lambda: self.roll("black",1))
        self.white_roll[0].place(x=self.white_roll_x_coord,y=self.white_roll_y_coord)
        self.black_roll[0].place(x=self.black_roll_x_coord,y=self.black_roll_y_coord)
        self.wait_variable(self.okVar)
        self.wait_variable(self.okVar)
        if self.white_num == self.black_num:
            self.messege = Label(self, text="it is a tie rool again",anchor=CENTER)
            self.messege.place(x=420, y=400)
            self.update()
            time.sleep(2)
            self.white_roll[0].place_forget()
            self.white_roll[0] = 0
            self.black_roll[0].place_forget()
            self.black_roll[0] = 0
            self.start(True)
        else:
            if self.white_num > self.black_num:
                self.messege.config(text="the white start",anchor=CENTER)
                self.messege.place(x=370, y=400)
                self.turn = 0
                time.sleep(2)
            elif self.white_num < self.black_num:
                self.messege.config(text="the black start",anchor=CENTER)
                #self.messege = Label(self, text="the black start")
                self.messege.place(x=370, y=400)
                self.turn = 1
                time.sleep(2)
            self.white_roll[0].place_forget()
            self.black_roll[0].place_forget()
            self.update()
            self.the_game(True)


    def roll(self,color,num):

        if color == "white":
            for i in range(num):
                if i == 0:
                    self.white_roll[0].place_forget()
                    self.white_roll[0] = 0
                self.white_num[i] = random.randint(1,6)
                image = self.dice[self.white_num[i]]
                label = Label(self,image=image)
                self.white_roll[i] = label
                self.white_roll[i].place(x=self.white_roll_x_coord+i*40 ,y=self.white_roll_y_coord)
        else:
            for i in range(num):
                if i == 0:
                    self.black_roll[0].place_forget()
                    self.black_roll[0] = 0
                self.black_num[i] = random.randint(1,6)
                image = self.dice[self.black_num[i]]
                self.black_roll[i] = Label(self,image=image)
                self.black_roll[i].place(x=self.black_roll_x_coord + i*40,y=self.black_roll_y_coord)
        self.update()
        self.okVar.set(1)

def main():
    window = tk.Tk()
    game = Board(window,8,8)
    window.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

