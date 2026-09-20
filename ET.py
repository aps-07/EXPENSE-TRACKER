from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

import tkinter as aps
import tkcalendar as asr
import matplotlib.pyplot as mpl

next_row = 2

root = aps.Tk()
root.title("DAILY EXPENSE TRACKER")
root.geometry("850x790+400+100")
root["bg"] = "peach puff"

date_list = []
amount_list = []
category_list = []


def ask_ai():
    prompt = f"""
    Here is my expense data:

    Dates: {date_list}
    Amounts: {amount_list}
    Categories: {category_list}

    Analyze my expenses and tell me where I am spending the most.
    """

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    ai_output.delete("1.0", aps.END)
    ai_output.insert(aps.END, response.output_text)


def add_expense():
    global next_row
    
    try:
        amo = int(Amount_Value.get())
        amount_list.append(amo)
        dt = Date_entered.get()
        date_list.append(dt)
        cat = Category_text.get()
        category_list.append(cat)
        notes = Note_entered.get()


        note_show = aps.Label(root,text=notes,bg="peach puff",font=("Arial",11))
        note_show.grid(row=next_row,column=0,padx=12)

        date_show = aps.Label(root,text=dt,bg="peach puff",font=("Arial",11))
        date_show.grid(row=next_row,column=1,padx=13)

        amount_show = aps.Label(root,text=amo,bg="peach puff",font=("Arial",11))
        amount_show.grid(row=next_row,column=2,padx=13)

        category_show = aps.Label(root,text=cat,bg="peach puff",font=("Arial",11))
        category_show.grid(row=next_row,column=3,padx=13)

        Note_entered.delete(0,aps.END)
        Date_entered.delete(0,aps.END)
        Amount_Value.delete(0,aps.END)
        Category_text.delete(0,aps.END)
        next_row += 1
    except ValueError:
        Amount_Value.delete(0,aps.END)
        Amount_Value.insert(0,"!! INVALID INTEGER !!")
        root.after(3000,lambda:Amount_Value.delete(0,"end"))
        Note_entered.delete(0,aps.END)
        Date_entered.delete(0,aps.END)
        Category_text.delete(0,aps.END)


def show_graph():
    unique_date = []
    for i in date_list:
        if i not in unique_date:
            unique_date.append(i)
    unique_amount = []
    unique_cat = []
    for i in unique_date:
        amou = 0
        cate = []
        for j in range(len(date_list)):
            if i == date_list[j]:
                amou += amount_list[j]
                cate.append(category_list[j])
        unique_amount.append(amou)
        if len(cate) == 1:
            unique_cat.append(cate[0])
        else:
            unique_cat.append(list(dict.fromkeys(cate)))

    mpl.figure(figsize=(6,4))
    mpl.title("EXPENSE GRAPH")
    mpl.xlabel("DATE")
    mpl.ylabel("AMOUNT")
    bars = mpl.bar(unique_date,unique_amount)
    mpl.bar_label(bars,labels = unique_cat)
    print(unique_date)
    print(unique_amount)
    print(unique_cat)
    mpl.show()

def show_piechart():
    piedict = {}
    for i in range(len(category_list)):
        if category_list[i] in piedict:
            piedict[category_list[i]] += amount_list[i]
        else:
            piedict[category_list[i]] = amount_list[i]
    dictcat = piedict.keys()
    dictamount = piedict.values()

    mpl.pie(dictamount,labels=dictcat,autopct="%1.1f%%")
    mpl.figtext(0.5, 0.02,f"Total Expense = {sum(dictamount)}",ha="center",fontsize=12,color="red")
    mpl.show()

# CALENDAR WORK
def show_data(event):
    Date_entered.delete(0,aps.END) # delete entrybox text from start to end
    Date_entered.insert(0,cal.get_date()) # insert at index 0 in entrybox the given text, cal.get_date() returns the selected date as string.
cal = asr.Calendar(root,date_pattern="dd-mm-yyyy",font=("Arial",11))
cal.grid(row=0,column=0)
cal.bind("<<CalendarSelected>>",show_data)


top_right_frame = aps.Frame(root,bg="peach puff")
top_right_frame.grid(row=0,column=1,padx=30)

Amount = aps.Label(top_right_frame,text="Enter Amount: ",bg="peach puff").grid(row=0,column=1,pady=17)
Amount_Value = aps.Entry(top_right_frame,font=("Arial",11),width=20)
Amount_Value.grid(row=0,column=2)

Category = aps.Label(top_right_frame,text="Enter Category: ",bg="peach puff").grid(row=1,column=1,pady=17)
Category_text = aps.Entry(top_right_frame,font=("Arial",11),width=20)
Category_text.grid(row=1,column=2)

Date = aps.Label(top_right_frame,text="Date Selected: ",bg="peach puff").grid(row=2,column=1,pady=17)
Date_entered= aps.Entry(top_right_frame,font=("Arial",11),width=20)
Date_entered.grid(row=2,column=2)

Note = aps.Label(top_right_frame,text="Enter the Note: ",bg="peach puff").grid(row=3,column=1,pady=17)
Note_entered = aps.Entry(top_right_frame,font=("Arial",11),width=20)
Note_entered.grid(row=3,column=2)

add_button = aps.Button(root,text="ADD EXPENSE",font=("Arial",10),background="lightblue",command=add_expense).grid(row=0,column=2,padx=15,pady=20,ipadx=5,ipady=5)

# TOP SECTION WORK COMPLETED

note = aps.Label(root,text="NOTE",bg="yellow").grid(row=1,column=0,pady=20)
date = aps.Label(root,text="DATE",bg="yellow").grid(row=1,column=1)
amount = aps.Label(root,text="AMOUNT",bg="yellow").grid(row=1,column=2)
category = aps.Label(root,text="CATEGORY",bg="yellow").grid(row=1,column=3,padx=5)

# matploatlib
matplot = aps.Button(root,text="SHOW GRAPH VISUALS",font=("Arial",10),background="lightgreen",command=show_graph).grid(row=20,column=2,pady=15)
pie = aps.Button(root,text="SHOW PIE CHART",font=("Arial",10),background="lightgreen",command=show_piechart).grid(row=20,column=0,pady=15)

ai_button = aps.Button(
    root,
    text="ASK AI",
    command=ask_ai
)

ai_button.grid(row=20, column=3, pady=15)

ai_output = aps.Text(root, height=10, width=70, wrap="word")
ai_output.grid(row=21, column=0, columnspan=4, padx=20, pady=10)

root.mainloop()
