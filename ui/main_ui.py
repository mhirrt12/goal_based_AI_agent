import tkinter as tk
from tkinter import messagebox
from agents.hospital_agent import HospitalBedAgent
from agents.patient import Patient

hospital = HospitalBedAgent(2,4)

root = tk.Tk()
root.title("Smart Hospital Bed Manager")
root.geometry("1150x680")
root.configure(bg="#eef5fb")

# ================= HEADER =================
header = tk.Frame(root,bg="#1f6aa5",height=70)
header.pack(fill=tk.X)

tk.Label(
    header,
    text="🏥 Smart Hospital Bed Management Dashboard",
    bg="#1f6aa5",
    fg="white",
    font=("Arial",20,"bold")
).pack(pady=15)

# ================= MAIN =================
main = tk.Frame(root,bg="#eef5fb")
main.pack(fill=tk.BOTH,expand=True,padx=15,pady=15)

# ================= LEFT PANEL =================
left = tk.Frame(main,bg="#d9ecff",width=300)
left.pack(side=tk.LEFT,fill=tk.Y,padx=(0,10))

tk.Label(left,text="Patient Admission",
         bg="#d9ecff",
         fg="#0a3d62",
         font=("Arial",14,"bold")).pack(pady=15)

# Name
tk.Label(left,text="Patient Name",bg="#d9ecff").pack(anchor="w",padx=15)

name_entry = tk.Entry(left,font=("Arial",11))
name_entry.pack(fill=tk.X,padx=15,pady=5)

# Condition
tk.Label(left,text="Condition",bg="#d9ecff").pack(anchor="w",padx=15,pady=(10,0))

cond_var = tk.StringVar(value="normal")

tk.Radiobutton(left,text="Critical",variable=cond_var,value="critical",bg="#d9ecff").pack(anchor="w",padx=20)
tk.Radiobutton(left,text="Serious",variable=cond_var,value="serious",bg="#d9ecff").pack(anchor="w",padx=20)
tk.Radiobutton(left,text="Normal",variable=cond_var,value="normal",bg="#d9ecff").pack(anchor="w",padx=20)

# Buttons
btn_frame = tk.Frame(left,bg="#d9ecff")
btn_frame.pack(fill=tk.X,padx=15,pady=15)

tk.Button(btn_frame,text="Admit Patient",
          bg="#1f6aa5",fg="white",
          font=("Arial",10,"bold"),
          command=lambda: admit()).pack(fill=tk.X,pady=5)

tk.Button(btn_frame,text="Discharge Patient",
          bg="#3498db",fg="white",
          font=("Arial",10,"bold"),
          command=lambda: discharge()).pack(fill=tk.X,pady=5)

# ================= STATUS =================
tk.Label(left,text="Hospital Status",
         bg="#d9ecff",
         font=("Arial",12,"bold")).pack(pady=(10,5))

status_text = tk.Text(left,height=20,font=("Consolas",9))
status_text.pack(fill=tk.BOTH,expand=True,padx=10,pady=5)

# ================= RIGHT PANEL =================
right = tk.Frame(main,bg="white")
right.pack(side=tk.RIGHT,expand=True,fill=tk.BOTH)

canvas = tk.Canvas(right,width=720,height=540,bg="white")
canvas.pack()

# Titles
canvas.create_text(120,30,text="ICU 🛏",font=("Arial",14,"bold"),fill="#1f6aa5")
canvas.create_text(360,30,text="GENERAL 🛏",font=("Arial",14,"bold"),fill="#1f6aa5")
canvas.create_text(600,30,text="WAITING ⏳",font=("Arial",14,"bold"),fill="#1f6aa5")

BOX_W=130
BOX_H=40
SPACE=8

boxes={}
targets={}
alerts={}

# ================= POSITION =================
def target_pos(name):

    s=hospital.status()

    y=60
    for n,b in s["Allocated"].items():
        if b=="ICU":
            if n==name:
                return (50,y)
            y+=BOX_H+SPACE

    y=60
    for n,b in s["Allocated"].items():
        if b=="General":
            if n==name:
                return (290,y)
            y+=BOX_H+SPACE

    y=60
    for n in s["Waiting Queue"]:
        if n==name:
            return (530,y)
        y+=BOX_H+SPACE

    return (530,y)

# ================= DRAW PATIENT =================
def draw_box(name,cond):

    colors={
        "critical":"#e74c3c",
        "serious":"#f39c12",
        "normal":"#3498db"
    }

    if name not in boxes:

        rect=canvas.create_rectangle(
            0,0,BOX_W,BOX_H,
            fill=colors[cond],
            outline=""
        )

        text=canvas.create_text(
            BOX_W/2,
            BOX_H/2,
            text=f"👤 {name}",
            fill="white",
            font=("Arial",10,"bold")
        )

        boxes[name]=(rect,text)

        if cond=="critical":
            alerts[name]=True

    targets[name]=target_pos(name)

# ================= CRITICAL FLASH =================
def flash():

    for name in alerts:

        rect,_=boxes[name]

        current=canvas.itemcget(rect,"fill")

        if current=="#e74c3c":
            canvas.itemconfig(rect,fill="#ff7675")
        else:
            canvas.itemconfig(rect,fill="#e74c3c")

    root.after(500,flash)

# ================= ANIMATION =================
def animate():

    moving=False

    for name,(rect,text) in boxes.items():

        x,y=canvas.coords(rect)[0:2]
        tx,ty=targets[name]

        dx=(tx-x)/5
        dy=(ty-y)/5

        if abs(dx)>0.5 or abs(dy)>0.5:

            canvas.move(rect,dx,dy)
            canvas.move(text,dx,dy)

            moving=True

    if moving:
        root.after(30,animate)

# ================= STATUS =================
def update_status():

    s=hospital.status()

    status_text.delete("1.0",tk.END)

    status_text.insert(tk.END,f"ICU Beds: {s['ICU Beds']}\n")
    status_text.insert(tk.END,f"General Beds: {s['General Beds']}\n")

    status_text.insert(tk.END,"\nAllocated Patients\n")
    status_text.insert(tk.END,"------------------\n")

    for n,b in s["Allocated"].items():
        status_text.insert(tk.END,f"{n} → {b}\n")

    status_text.insert(tk.END,"\nWaiting Queue\n")
    status_text.insert(tk.END,"-------------\n")

    i=1
    for n in s["Waiting Queue"]:
        status_text.insert(tk.END,f"{i}. {n}\n")
        i+=1

# ================= ADMIT =================
def admit():

    name=name_entry.get().strip()

    if not name:
        messagebox.showwarning("Warning","Enter patient name")
        return

    if name in hospital.patients or any(p.name==name for p in hospital.waiting_queue):
        messagebox.showerror("Error","Patient already exists")
        return

    p=Patient(name,cond_var.get())

    hospital.admit_patient(p)
    hospital.reassign_beds()

    if name in hospital.patients:
        draw_box(name,hospital.patients[name].condition)

    animate()
    update_status()

    name_entry.delete(0,tk.END)

# ================= DISCHARGE =================
def discharge():

    name=name_entry.get().strip()

    if not name:
        messagebox.showwarning("Warning","Enter name")
        return

    hospital.discharge_patient(name)

    if name in boxes:

        rect,text=boxes.pop(name)

        canvas.delete(rect)
        canvas.delete(text)

        targets.pop(name,None)

        alerts.pop(name,None)

    hospital.reassign_beds()

    for n in hospital.patients:
        draw_box(n,hospital.patients[n].condition)

    animate()
    update_status()

    name_entry.delete(0,tk.END)

flash()
update_status()
root.mainloop()