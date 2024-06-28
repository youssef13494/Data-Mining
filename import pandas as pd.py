import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from itertools import combinations
from tkinter import *
from tkinter.scrolledtext import ScrolledText

root = Tk()
file_path=''
min_support = tk.DoubleVar()
min_confidence = tk.DoubleVar()
number_record = tk.DoubleVar()
def analyze_data():
    global min_support
    global min_confidence
    global number_record
    Result=''
    Result1='After Apply filter : \n'
    # Read Excel file into a DataFrame
    df = pd.read_csv(file_path)
    value=number_record.get()
    # Calculate the number of records based on the percentage
    num_records = int(len(df) * (value / 100))

    # Select a random sample of records from the DataFrame
    df = df.sample(n=num_records)

    # Initialize an empty list to store the formatted data
    data = []

    # Iterate over the DataFrame
    for index, row in df.iterrows():
        # Extract items for each transaction
        transaction_id = row['TransactionNo']
        items = [item.strip() for item in row['Items'].split(',')]
        # Append the transaction ID and items as a list to the formatted data list
        data.append([transaction_id, items])
    init = []
    for i in data:
        for q in i[1]:
            if(q not in init):
                init.append(q)
    init = sorted(init)

    Result=Result+str(init)+'\n'
    sp = min_confidence.get()
    s = int(sp*len(init))

    Result=Result+str(s)+'\n'

    from collections import Counter
    c = Counter()
    for i in init:
        for d in data:
            if(i in d[1]):
                c[i]+=1
    
    Result=Result+"C1:"+'\n'
    for i in c:
        
        Result=Result+str([i])+": "+str(c[i])+'\n'
    
    Result=Result+'\n'
    l = Counter()
    for i in c:
        if(c[i] >= s):
            l[frozenset([i])]+=c[i]
    
    Result=Result+"L1:"+'\n'
    for i in l:
        Result=Result+str(list(i))+": "+str(l[i])+'\n'
    Result=Result+'\n'
    pl = l
    pos = 1
    for count in range (2,1000):
        nc = set()
        temp = list(l)
        for i in range(0,len(temp)):
            for j in range(i+1,len(temp)):
                t = temp[i].union(temp[j])
                if(len(t) == count):
                    nc.add(temp[i].union(temp[j]))
        nc = list(nc)
        c = Counter()
        for i in nc:
            c[i] = 0
            for q in data:
                temp = set(q[1])
                if(i.issubset(temp)):
                    c[i]+=1
        Result=Result+"C"+str(count)+":"+'\n'
        for i in c:

            Result=Result+str(list(i))+": "+str(c[i])+'\n'
        Result=Result+'\n'
        l = Counter()
        for i in c:
            if(c[i] >= s):
                l[i]+=c[i]
        Result=Result+"L"+str(count)+":"+'\n'
        for i in l:
            Result=Result+str(list(i))+": "+str(l[i])+'\n'
        Result=Result+'\n'
        if(len(l) == 0):
            break
        pl = l
        pos = count
    Result=Result+"Result: "+"\n"
    Result=Result+"L"+str(pos)+":"+"\n"
    for i in pl:
        Result=Result+str(list(i))+": "+str(pl[i])+"\n"
    Result=Result+"\n"
    ###result_text.insert(tk.END, Result) الحل يابروووو
    for l in pl:
        c = [frozenset(q) for q in combinations(l,len(l)-1)]
        mmax = 0
        for a in c:
            b = l-a
            ab = l
            sab = 0
            sa = 0
            sb = 0
            for q in data:
                temp = set(q[1])
                if(a.issubset(temp)):
                    sa+=1
                if(b.issubset(temp)):
                    sb+=1
                if(ab.issubset(temp)):
                    sab+=1
            temp = sab/sa*100
            if(temp > mmax):
                mmax = temp
            temp = sab/sb*100
            if(temp > mmax):
                mmax = temp
            Result=Result+str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%"+"\n"
            Result=Result+str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%"+"\n"
            if (sab/sa*100)>=(min_confidence.get()*100):
                Result1=Result1+str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%"+"\n"
            if (sab/sb*100)>=(min_confidence.get()*100):
                Result1=Result1+str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%"+"\n"

        curr = 1
        Result=Result+"choosing:  "
        for a in c:
            b = l-a
            ab = l
            sab = 0
            sa = 0
            sb = 0
            for q in data:
                temp = set(q[1])
                if(a.issubset(temp)):
                    sa+=1
                if(b.issubset(temp)):
                    sb+=1
                if(ab.issubset(temp)):
                    sab+=1
            temp = sab/sa*100
            if(temp == mmax):
                Result=Result+str(curr)+"  \n"
            curr += 1
            temp = sab/sb*100
            if(temp == mmax):
                Result=Result+str(curr)+"  \n"
            curr += 1
        print()
        Result=Result+"\n"
        print()
        Result=Result+"\n"
        result_text1.insert(tk.END, Result)
        result_text1.insert(tk.END, Result1)
    
def browse_file():
        global file_path
        file_path = filedialog.askopenfilename()

# Create a Tkinter window
root.title("Apriori Analysis")

# Set the background color
root.configure(bg='#F699CD')  # You can use any valid color name or hexadecimal color code

# Set the size of the root window
root.geometry('1000x800')  # Width x Height

# Disable resizing
root.resizable(False, False)

# Frame for file selection
frame_file = Frame(root)
frame_file.pack(pady=10)

label_path = Label(frame_file, text="Select CSV file:")
label_path.grid(row=0, column=0)

entry_path = Entry(frame_file, width=50)
entry_path.grid(row=0, column=1, padx=10)

button_browse = Button(frame_file, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2)

# Frame for minimum support input
frame_support = Frame(root)
frame_support.pack(pady=10)

label_support_min = Label(frame_support, text="Enter minimum support (0-1):")
label_support_min.grid(row=0, column=0)

entry_support_min = Entry(frame_support,textvariable=min_support, width=10)
entry_support_min.grid(row=0, column=1, padx=10)


label_support_max = Label(frame_support, text="Enter min_confidence (0-1):")
label_support_max.grid(row=2, column=0)

entry_support_max = Entry(frame_support,textvariable=min_confidence, width=10)
entry_support_max.grid(row=2, column=1, padx=10)

label_Number_record = Label(frame_support, text="Number of Record")
label_Number_record.grid(row=4, column=0)

entry_Number_record = Entry(frame_support,textvariable=number_record, width=10)
entry_Number_record.grid(row=4, column=1, padx=10)

# Analyze button
button_analyze = Button(root, text="Analyze Data", command=analyze_data)
button_analyze.pack(pady=10)

result_frame = tk.Frame(root)
result_frame.pack(pady=10)

result_label = tk.Label(result_frame, text="Analysis Result:")
result_label.pack()

result_text1= ScrolledText(result_frame, height=35, width=120)
result_text1.pack()
# Run the Tkinter event loop
root.mainloop()