from tkinter import *

rt = Tk()
rt.title('calculator')

#init special widgets
t = Label(rt,relief='sunken',justify='left')
t.grid(row=0,column=0,columnspan=3,sticky='nesw')
b = Button(rt,
           text='<-',
           command=lambda:t.configure(text=t.cget('text')[:len(t.cget('text'))-1]))
b.grid(row=0,column=3)

#2d-list of button chars
bts = [['1','2','3','+'],
       ['4','5','6','-'],
       ['7','8','9','*'],
       ['0','.','=','/']]

#just pressed equals?
eq = False

#takes a string and returns a func that will append that string to the output,
#or replace the output with that number if the equals buttons was just pressed
def app_func(s):
    def handle():
        global eq
        x = s if eq else t.cget('text')+s
        eq = False
        t.configure(text=x)
    return handle

#computes the answer (uses eval - could implement own handler)
#note that eval can be dangerous but is fine here as input is limited to set chars
def calculate():
    global eq
    eq = True
    try:
        x = str(eval(t.cget('text')))
    except ValueError:
        x = 'syntax error'
    t.configure(text=x)


#init the remaining buttons
for i,row in enumerate(bts):
    for j,s in enumerate(row):
        b = Button(rt, text=s)
        if s == '=':
            b.configure(command=calculate)
        else:
            b.configure(command=app_func(s))
        b.grid(row=i+1,column=j)

#enter mainloop
rt.mainloop()
