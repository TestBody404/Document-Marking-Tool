import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import os
from ltp import LTP
import json

filename = ''

window = Tk()
window.title('司法案例分析')
window.geometry('900x640')

def open_file():
    global filename
    filename = tkinter.filedialog.askopenfilename(defaultextension='.txt')
    if filename == '':
        filename = None
    else:
        window.title('Filename:'+os.path.basename(filename))
        input_text.delete(1.0, END)
        f = open(filename, 'r', encoding='utf-8')
        input_text.insert(1.0, f.read())
        f.close()
def save_txt():
    f = tkinter.filedialog.asksaveasfilename(initialfile='未命名.txt', defaultextension='.txt')
    global filename
    filename = f
    if f == None:
        return
    fh = open(f, 'w')
    msg = input_text.get(1.0, END)
    fh.write(msg)
    fh.close()
    window.title('Filename:'+os.path.basename(f))
def save_json():
    json_file = [{'当事人': people_text.get(1.0, END), '性别': gender_text.get(1.0, END), '民族': nation_text.get(1.0, END), '出生地': birthplace_text.get(1.0, END), '案由': case_text.get(1.0, END), '法院': court_text.get(1.0, END)}]
    f = tkinter.filedialog.asksaveasfilename(initialfile='未命名.json', defaultextension='.json')
    global filename
    filename = f
    if f == None:
        return
    fh = open(f, 'w')
    msg = json.dumps(json_file, indent=4)
    fh.write(msg)
    fh.close()


menu = tk.Menu(window, tearoff=False)
file_menu = Menu(menu, tearoff=False)
file_menu.add_command(label='导入案件', command=lambda: open_file())
file_menu.add_command(label='导出文本', command=lambda: save_txt())
file_menu.add_command(label='导出标注', command=lambda: save_json())
menu.add_cascade(label='文件', menu=file_menu)
window.config(menu=menu)

"""----------菜单栏，导入导出文件-------------"""

frame1 = Frame(window, width=10, height=15)
input_text = Text(frame1, width=10, height=15)
scroll1 = Scrollbar(frame1, orient=VERTICAL)
scroll1.pack(side=tk.RIGHT, fill=tk.Y)
input_text.pack(fill=tk.X)
scroll1.config(command=input_text.yview)
input_text.config(yscrollcommand=scroll1.set)
frame1.pack(fill=tk.X)
"""----------输入文本框---------------"""

button1 = Button(window, text='确定', bg='#C0C0C0', font=('Arial', 10), width=12, height=1)
button1.pack(anchor='e')
"""----------确定输入完成-------------"""

frame2 = Frame(window, width=10, height=5)
people_button = Button(frame2, text='当事人', bg='#C0C0C0', font=('Arial', 10), width=12, height=1, command=lambda: call_frame(people_frame))
gender_button = Button(frame2, text='性别', bg='#C0C0C0', font=('Arial', 10), width=12, height=1, command=lambda: call_frame(gender_frame))
nation_button = Button(frame2, text='民族', bg='#C0C0C0', font=('Arial', 10), width=12, height=1, command=lambda: call_frame(nation_frame))
birthplace_button = Button(frame2, text='出生地', bg='#C0C0C0', font=('Arial', 10), width=12, height=1, command=lambda: call_frame(birthplace_frame))
case_button = Button(frame2, text='案由', bg='#C0C0C0', font=('Arial', 10), width=12, height=1, command=lambda: call_frame(case_frame))
court_button = Button(frame2, text='法院', bg='#C0C0C0', font=('Arial', 10), width=12, height=1, command=lambda: call_frame(court_frame))
people_button.grid(row=0, column=0)
gender_button.grid(row=0, column=1)
nation_button.grid(row=0, column=2)
birthplace_button.grid(row=0, column=3)
case_button.grid(row=0, column=4)
court_button.grid(row=0, column=5)
frame2.pack(anchor='nw')
"""------------基本信息选项-------------"""

frame3 = Frame(window, width=10, height=5)
noun = Label(frame3, text="名词", font=('黑体', 20)).grid(row=0, column=0, padx=38)
verb = Label(frame3, text="动词", font=('黑体', 20)).grid(row=0, column=1, padx=38)
des = Label(frame3, text="形容词", font=('黑体', 20)).grid(row=0, column=2, padx=38)
res = Label(frame3, text="标注内容", font=('黑体', 20)).grid(row=0, column=3, padx=38)
frame3.pack(anchor='nw')

frame_noun = Frame(window).pack(anchor='nw')
frame_verb = Frame(window).pack(anchor='nw')
frame_des = Frame(window).pack(anchor='nw')
lb_noun = tkinter.Listbox(frame_noun, selectmode=tkinter.EXTENDED)
lb_verb = tkinter.Listbox(frame_verb, selectmode=tkinter.EXTENDED)
lb_des = tkinter.Listbox(frame_des, selectmode=tkinter.EXTENDED)
ltp = LTP()
ltp.init_dict(path="扩充词库.txt", max_window=20)
with open("扩充词库.txt", 'r', encoding='utf-8')as f:
    ltp.add_words(words=f.readlines(), max_window=20)

def useLTP():
    seg, hidden = ltp.seg(input_text.get(1.0, END).split( ))
    zipped = zip(sum(seg, []), sum(ltp.pos(hidden), []))
    diction = dict(zipped)
    lb_noun.delete(0, tk.END)
    lb_verb.delete(0, tk.END)
    lb_des.delete(0, tk.END)
    t1 = 0
    t2 = 0
    t3 = 0
    zu = "族"
    cha = "×"
    kuo1 = "("
    kuo2 = ")"
    j = 0
    for key in list(diction.keys()):
        flag = cha in key or kuo2 in key or kuo1 in key
        if ("犯" in key and len(key) >= 8):
            flag = True
        if not flag:
            if t1 == 1 and diction[key] == "nh":
                lb_noun.insert(tkinter.END, key)
                del diction[key]
                del key
                continue
            if key == "当事人" or key == "被告人" or key == "上诉人":
                t1 = 1

            if "户籍" in key or "生于" in key:
                t2 = 1

            if "犯" in key or "指控" in key or "涉嫌" in key:
                t3 = 1

            if diction[key] == "b" and key == "男" or key == "女" or key == "男性" or key == "女性":
                lb_des.insert(tkinter.END, key)
                del diction[key]
                del key
                continue
            if diction[key] == "nz" and zu in key:
                lb_noun.insert(tkinter.END, key)
                del diction[key]
                del key
                continue
            if "法院" in key:
                lb_noun.insert(tkinter.END, key)
                del diction[key]
                del key
                continue
            if t1 > 0 and t1 < 5:
                t1 += 1
                if diction[key] == 'nh':
                    lb_noun.insert(tkinter.END, key)
                    del diction[key]
                    del key
                    continue
            if t2 > 0 and t2 < 5:
                t2 += 1
                if diction[key] == 'ns':
                    lb_noun.insert(tkinter.END, key)
                    del diction[key]
                    del key
                    continue
            if t3 > 0 and t3 < 5:
                t3 += 1
                flag3 = "犯罪" in key
                if "罪" in key and not flag3:
                    lb_noun.insert(tkinter.END, key)
                    del diction[key]
                    del key
                    continue
    """提高部分结果的优先级，将可能性较大的放在列表前面"""
    for key in diction.keys():
        flag = cha in key or kuo2 in key or kuo1 in key
        if("犯" in key and len(key) >= 6):
            flag = True
        if not flag:
            if diction[key] == "ni" or diction[key] == "nl" or diction[key] == "ns" or diction[key] == "nt" or diction[
                key] == "nz" or diction[key] == "nh" or diction[key] == "nd" or diction[key] == "n":
                lb_noun.insert(tkinter.END, key)
            if not flag and diction[key] == "v":
                lb_verb.insert(tkinter.END, key)
            if not flag and diction[key] == "a" or diction[key] == "b" or diction[key] == "z":
                lb_des.insert(tkinter.END, key)

lb_noun.pack(side=LEFT, anchor='nw')
lb_verb.pack(side=LEFT, anchor='nw')
lb_des.pack(side=LEFT, anchor='nw')
button1.config(command=lambda: useLTP())

"""------------分词结果-------------"""
people_frame = Frame(window)
gender_frame = Frame(window)
nation_frame = Frame(window)
birthplace_frame = Frame(window)
case_frame = Frame(window)
court_frame = Frame(window)
people_text = Text(people_frame, height=14)
gender_text = Text(gender_frame, height=14)
nation_text = Text(nation_frame, height=14)
birthplace_text = Text(birthplace_frame, height=14)
case_text = Text(case_frame, height=14)
court_text = Text(court_frame, height=14)
people_text.pack()
gender_text.pack()
nation_text.pack()
birthplace_text.pack()
case_text.pack()
court_text.pack()

current_text = people_text

def show(event):
    object = event.widget
    indexs = object.curselection()
    global current_text
    for index in indexs:
         current_text.insert(END, object.get(index)+" ")

lb_noun.bind("<<ListboxSelect>>", show)
lb_verb.bind("<<ListboxSelect>>", show)
lb_des.bind("<<ListboxSelect>>", show)

def call_frame(chosen_frame):
    global current_text
    if(chosen_frame == people_frame):
        current_text = people_text
    if (chosen_frame == gender_frame):
        current_text = gender_text
    if (chosen_frame == nation_frame):
        current_text = nation_text
    if (chosen_frame == case_frame):
        current_text = case_text
    if (chosen_frame == court_frame):
        current_text = court_text
    if (chosen_frame == birthplace_frame):
        current_text = birthplace_text
    people_frame.forget()
    gender_frame.forget()
    nation_frame.forget()
    birthplace_frame.forget()
    case_frame.forget()
    court_frame.forget()
    chosen_frame.pack()


"""-----------选择结果--------------"""
window.mainloop()