from tkinter import *
import tkinter as tk
import random
from functools import partial
import mysql.connector as sqltor
mycon=sqltor.connect(host="localhost",user="root",passwd="SyVf#469",database="vishal")
mycursor=mycon.cursor()

Home=tk.Tk()
game=tk.Tk()

game.title('Game')
game.geometry('700x700+400+50')
game.configure(bg='dimgray')
Home.title('Home Screen')
Home.geometry('+600+350')

P1=tk.StringVar()
A1=tk.StringVar()
p=[0,0]
text1=['P1','P2']
c=[0,0]
posi=[]
activ=[]

def selection():
    global posi
    global activ
    
    query='select position from ACTIVITY'
    data=mycursor.execute(query)
    posi=mycursor.fetchall()
    print(posi)

    query='select activities from ACTIVITY'
    data=mycursor.execute(query)
    activ=mycursor.fetchall()
    print(activ)


def activity(pos,j):
##    if pos==36 or pos==79:
##        acti=tk.Label(game,text="Sing a Song",bg='light sea green').grid(row=7,column=15)
##    elif pos==93 or pos==6:
##        acti=tk.Label(game,text="Do a Dance",bg='light sea green').grid(row=7,column=15)
##    elif pos==51 or pos==37:
##        acti=tk.Label(game,text="Roll Again",bg='light sea green').grid(row=7,column=15)
    global c
    for i in range (0,len(posi)):
        if pos==posi[i][0]:
            if activ[i][0]=='Roll Again':
                c[j]-=1
            acti=tk.Label(game,text=activ[i][0],bg='light sea green').grid(row=7,column=15)
            break
                
def move(i):
    global p,c
    global text1
    global posi
    color=['blue','red']
    s=random.randrange(0,6)+1
    label=tk.Label(game,text=".                                            .",bg='dimgray',fg='dimgray').grid(row=9,column=15)
    acti=tk.Label(game,text=".                   .",bg='dimgray',fg='dimgray').grid(row=7,column=15)
    if (p[i],) not in posi:
        if p[i]!=0:
            if p[0]!=p[1]:
                if p[i]%10!=0:
                    p1=tk.Label(game,text=p[i],bg="chocolate1",padx=5).grid(row=(p[i]//10)+2,column=(p[i]%10)+1)
                else:
                    p1=tk.Label(game,text=p[i],bg="chocolate1",padx=5).grid(row=(p[i]//10)+1,column=11)
    else:
        if p[i]!=0:
            if p[0]!=p[1]:
                if p[i]%10!=0:
                    p1=tk.Label(game,text=p[i],bg="mediumpurple3",padx=5).grid(row=(p[i]//10)+2,column=(p[i]%10)+1)
                else:
                    p1=tk.Label(game,text=p[i],bg="mediumpurple3",padx=5).grid(row=(p[i]//10)+1,column=11)

    roll=''    
    if c[0]==c[1]:
        if i==0:
            p[i]+=s
            c[i]+=1
            roll=text1[i]+' has rolled a '+str(s)
        else:
            roll='It is not your turn yet'
            label=tk.Label(game,text=roll).grid(row=9, column=15)
            if p[i]%10!=0:
                p1=tk.Label(game,text=text1[i],fg=color[i]).grid(row=(p[i]//10)+2,column=(p[i]%10)+1)
            else:
                p1=tk.Label(game,text=text1[i],fg=color[i]).grid(row=(p[i]//10)+1,column=11)
            return
    else:
        if i==1:
            p[i]+=s
            c[i]+=1
            roll=text1[i]+' has rolled a '+str(s)
        else:
            roll='It is not your turn yet'
            label=tk.Label(game,text=roll).grid(row=9, column=15)
            if p[i]%10!=0:
                p1=tk.Label(game,text=text1[i],fg=color[i]).grid(row=(p[i]//10)+2,column=(p[i]%10)+1)
            else:
                p1=tk.Label(game,text=text1[i],fg=color[i]).grid(row=(p[i]//10)+1,column=11)
            return
    label=tk.Label(game,text=roll).grid(row=9, column=15)
    
    if p[i]<100:
        if p[i]%10!=0:
            p1=tk.Label(game,text=text1[i],fg=color[i]).grid(row=(p[i]//10)+2,column=(p[i]%10)+1)
        else:
            p1=tk.Label(game,text=text1[i],fg=color[i]).grid(row=(p[i]//10)+1,column=11)
    elif p[i]==100:
        win=text1[i]+' HAS WON!!'
        p1=tk.Label(game,text=text1[i],bg=color[i],fg='white').grid(row=11,column=11)
        label=tk.Label(game,text=win,bg='medium sea green').grid(row=6,column=15)
    else:
        p[i]-=s
        p1=tk.Label(game,text=text1[i],fg=color[i]).grid(row=(p[i]//10)+2,column=(p[i]%10)+1)
        label=tk.Label(game,text="ROLL AGAIN",bg='MediumOrchid',fg='white').grid(row=6,column=15)

    if (p[i],) in posi:
        activity(p[i],i)

def actimake():
    mycursor.execute("insert into ACTIVITY(position,activities)values({},'{}')".format(P1.get(),A1.get()))
    mycon.commit()
    
def initialize():
    selection()
    a=1
    global posi
    for i in range(0,10):
        for j in range(0,10):
            t=(a,)
            if (a,) not in posi:
                board=tk.Label(game,text=a,bd=1,relief="solid",bg='chocolate1',padx=20,pady=20).grid(row=(i+2),column=(j+2))
            else:
                board=tk.Label(game,text=a,bd=1,relief="solid",bg='mediumpurple3',padx=20,pady=20).grid(row=(i+2),column=(j+2))
            a+=1
    Home.destroy()
    
def Close():
    game.destroy()

##Buttons
initialize=partial(initialize)
buttonCal=tk.Button(Home,text="Create",command=partial(initialize),font=30,padx=10,pady=10).grid(row=4,column=2)

move=partial(move)

player1=tk.Label(game,text="P1",bg="blue",fg='white').grid(row=3,column=15)
buttonCal=tk.Button(game,text="Roll P1",command=partial(move,0),padx=10,pady=10,relief='raised',bg='azure3').grid(row=10,column=15)

player2=tk.Label(game,text="P2",bg='red',fg='white').grid(row=4,column=15)
buttonCal=tk.Button(game,text="Roll P2",command=partial(move,1),padx=10,pady=10,relief='raised',bg='azure3').grid(row=12,column=15)

exit_button = tk.Button(game,text="EXIT",command=Close,padx=10,pady=10,relief='raised',bg='azure3').grid(row=2,column=15)


label1=tk.Label(Home,text='Position',font=30,padx=10,pady=10).grid(row=2,column=1)
entry1 = tk.Entry(Home, textvariable=P1,font=30).grid(row=2,column=2)
label2=tk.Label(Home,text='Activity',font=30,padx=10,pady=10).grid(row=3,column=1)
entry2=tk.Entry(Home,textvariable=A1,font=30).grid(row=3,column=2)

actimake=partial(actimake)
buttonCal=tk.Button(Home,text='Add Activity',command=partial(actimake),font=30,padx=10,pady=10).grid(row=4,column=1)

Home.mainloop()
