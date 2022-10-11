import ply.lex as lex
from ply import yacc
import turtle
from turtle import *
from tkinter import *

form = Tk()
form.title('ÇİZEN ROBOT')
form.geometry('1070x550')
form.minsize(960, 550)
# form.maxsize(960,550)
form.config(bg="#008080")
canvas = Canvas(form, height=500, width=500)
canvas.place(relx=0.47, rely=0.005, relwidth=0.525, relheight=0.925)
screen = TurtleScreen(canvas)

frame_input = Frame(form, bg='white')
frame_input.place(relx=0.005, rely=0.01, relwidth=0.46, relheight=0.04)
input_title = Label(frame_input, bg='white', text="Giriş Verisi", font="Verdana 11 bold")
input_title.pack(side=TOP)

my_text= Text(form, width=40, height=10, font=16, bg='White')
my_text.place(relx=0.005, rely=0.06, relwidth=0.46, relheight=0.46)

frame_error = Frame(form, bg='white')
frame_error.place(relx=0.005, rely=0.53, relwidth=0.46, relheight=0.04)
error_title = Label(frame_error, bg='white', text="Hata Bilgisi", font="Verdana 11 bold")
error_title.pack(side=TOP)

frame_hata = Frame(form, bg='white')
frame_hata.place(relx=0.005, rely=0.58, relwidth=0.46, relheight=0.35)
l = Label(frame_hata, bg='white', font='times 15 bold')

def opentxt():
    text_file = open("deneme.txt", 'r')
    stuff = text_file.read()
    my_text.insert(END, stuff)
    text_file.close()

def save():
    text_file = open('deneme.txt', 'w')
    text_file.write(my_text.get(1.0, END))

"""def clear_drawing():
    k.reset()

def clear_entry():
    my_text.delete(1.0, END)
"""
def restart():
    k.reset()
    my_text.delete(1.0, END)
    l['text'] = 'The program is restarted'
    l['fg'] = 'blue'

# open butonu
open_buton = Button(form, text='open txt', font='Verdana 8 italic', bg='light grey', command=opentxt)
open_buton.place(relx=0.005, rely=0.94, relwidth=0.07, relheight=0.05)

# save butonu
save_buton = Button(form, text='save', font='Verdana 8 italic', bg='light grey', command=save)
save_buton.place(relx=0.08, rely=0.94, relwidth=0.07, relheight=0.05)

#restart butonu
restart_buton = Button(form, text='restart', font='Verdana 8 italic', bg='light grey', command=restart)
restart_buton.place(relx=0.155, rely=0.94, relwidth=0.1, relheight=0.05)

#çizim temizleme butonu
#clear_drawing_buton = Button(form, text='clear drawing',font='Verdana 8 italic',bg='light grey', command=clear_drawing)
#clear_drawing_buton.place(relx=0.845,rely=0.94, relwidth=0.15,relheight=0.05)

#girdi ekranı temizleme butonu
#clear_entry_buton = Button(form, text='clear entry',font='Verdana 8 italic',bg='light grey', command=clear_entry)
#clear_entry_buton.place(relx=0.37, rely=0.94, relwidth=0.1, relheight=0.05)

k = turtle.RawTurtle(screen)

tokens = (
    'FORWARD',
    'RIGHT',
    'LOOP',
    'NUMBER',
    'COLOR',
    'PEN',
    'LPAREN',
    'RPAREN',
    'LINECOLOR',
)

t_FORWARD = r'F'
t_RIGHT = r'R'
t_LOOP = r'L'
t_COLOR = r'COLOR'
t_PEN = r'PEN'
t_LPAREN = r'\['
t_RPAREN = r'\]'
t_ignore = ' \t'
t_LINECOLOR = r'["K","Y","M","S"]'

def t_NUMBER(t):
    r'\d+'  #r'[0-9]+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'

def t_error(t):
    l['text']=' '+t.value[0]+' is an illegal character'
    l['fg']='red'
    l.pack(side='left')
    t.lexer.skip(1)
    raise ValueError

lexer=lex.lex()

# Parsing rules
def p_statement_expr(p):
    '''statement : expression
                  '''

    l['text'] = " The operation completed successfully"
    l['fg'] = 'green'
    l.pack(side='left')

def p_expression(p):
    '''expression : LOOP NUMBER LPAREN stmnt RPAREN term expression
                  | term LOOP NUMBER LPAREN stmnt RPAREN expression
                  | stmnt
                  | empty '''

def p_stmnt(p):
    '''stmnt : stmnt FORWARD NUMBER term expression
             | stmnt RIGHT NUMBER term expression
             | term RIGHT NUMBER term expression
             | term FORWARD NUMBER term expression
             | expression
             | empty '''

def p_term(p):
    '''term : PEN NUMBER COLOR LINECOLOR
            | COLOR LINECOLOR PEN NUMBER
            | PEN NUMBER
            | COLOR LINECOLOR
            | empty
    '''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    l['text'] = ' Syntax error!'
    l['fg'] = 'red'
    l.pack(side='left')
    raise SyntaxError

parser = yacc.yacc()

def buton():
    while True:
        data = my_text.get(1.0, END)
        try:
            parser.parse(data)
            ciz(k, data)
            break
        except ValueError:
            break
        except SyntaxError:
            break

#çizme butonu
buton=Button(form, text='Draw', command=buton, bg='red', fg='white', font='Verdana 8 italic')
buton.place(relx=0.260, rely=0.94, relwidth=0.1, relheight=0.05)

def drawfunc(k, i, dongusayisi, tokenlist):
    while (i < dongusayisi):
        if (not (tokenlist)):
            break
        if (tokenlist[i][0] == 'LOOP'):
            newlist = []
            tokenlist.pop(i)
            sayi = tokenlist[i][1]
            tokenlist.pop(i)
            copylist = tokenlist.copy()
            for l in range(sayi):
                newlist = loopfunc(k, tokenlist)
                tokenlist = copylist.copy()
            tokenlist = newlist.copy()
        elif (tokenlist[i][0] == 'FORWARD'):
            tokenlist.pop(i)
            k.forward(tokenlist[i][1])
            tokenlist.pop(i)
        elif (tokenlist[i][0] == 'RIGHT'):
            tokenlist.pop(i)
            k.right(tokenlist[i][1])
            tokenlist.pop(i)
        else:
            tokenlist.pop(i)

def colorpenfunc(k, j, dongusayisi2, renktokenlist):
    while (j < dongusayisi2):
        if (not (renktokenlist)):
            break
        if (renktokenlist[j][0] == 'COLOR'):
            renktokenlist.pop(j)
            if (renktokenlist[j][1] == 'K'):
                k.color("red")
            elif (renktokenlist[j][1] == 'S'):
                k.color("black")
            elif (renktokenlist[j][1] == 'M'):
                k.color("blue")
            elif (renktokenlist[j][1] == 'Y'):
                k.color("green")
            else:
                k.color('black')

        elif (renktokenlist[j][0] == 'PEN'):
            renktokenlist.pop(j)
            if (renktokenlist[j][1] == 1):
                k.pensize(1)
            elif (renktokenlist[j][1] == 2):
                k.pensize(3)
            elif (renktokenlist[j][1] == 3):
                k.pensize(5)
            else:
                k.pensize(3)
        else:
            renktokenlist.pop(j)

def loopfunc(k, tokenlist):
    p = 0
    looptime = len(tokenlist)
    newlist = []
    while (p < looptime):
        if (tokenlist[p][0] == 'LOOP'):
            tokenlist.pop(p)
            sayi = tokenlist[p][1]
            tokenlist.pop(p)
            copylist = tokenlist.copy()
            for l in range(sayi):
                newlist = loopfunc(k, tokenlist)
                tokenlist = copylist.copy()
            tokenlist = newlist.copy()
        elif (tokenlist[p][0] == 'FORWARD'):
            tokenlist.pop(p)
            k.forward(tokenlist[p][1])
            tokenlist.pop(p)
        elif (tokenlist[p][0] == 'RIGHT'):
            tokenlist.pop(p)
            k.right(tokenlist[p][1])
            tokenlist.pop(p)
        elif (tokenlist[p][0] == 'RPAREN'):
            tokenlist.pop(p)
            break
        else:
            tokenlist.pop(p)
    return tokenlist

def ciz(k, data):
    k.speed(5)
    lexer.input(data)
    token = lexer.token()  # NEXT TOKEN
    tokenlist = []
    renktokenlist = []

    while True:
        if not token:
            break
        temptoken = [token.type, token.value]
        tokenlist.append(temptoken)
        renktokenlist.append(temptoken)
        token = lexer.token()

    i = 0
    dongusayisi = len(tokenlist)
    colorpenfunc(k, i, dongusayisi, renktokenlist)
    drawfunc(k, i, dongusayisi, tokenlist)

form.mainloop()