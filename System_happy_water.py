import sqlite3
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import requests
import datetime

def createconnection() :
    global conn, cursor
    conn = sqlite3.connect('System.db')
    cursor = conn.cursor()

def loginlayout() :
    global userEntry, pwdEntry, loginFrame

    loginFrame = Frame(root, bg='#e0f2fc')
    loginFrame.rowconfigure((0, 1, 2, 3), weight=1)
    loginFrame.columnconfigure((0, 1), weight=1)

    Label(loginFrame, text="Login", font="Calibri 32 bold", compound=LEFT, bg='#e0f2fc', fg='#227aa9').grid(row=0, columnspan=2)
    Label(loginFrame, text="รหัสพนักงาน : ", bg='#e0f2fc', fg='#227aa9', padx=20).grid(row=1, column=0, sticky='e')
    userEntry = Entry(loginFrame, bg='#FFFFFF',fg="#227aa9", width=20)
    userEntry.grid(row=1, column=1, sticky='w', padx=20)
    pwdEntry = Entry(loginFrame, bg='#FFFFFF',fg="#227aa9", width=20, show='*')
    pwdEntry.grid(row=2, column=1, sticky='w', padx=20)
    Label(loginFrame, text="รหัสผ่าน : ", bg='#e0f2fc', fg='#227aa9', padx=20).grid(row=2, column=0, sticky='e')
    Button(loginFrame, text="Login", width=5, command=login,bg="#1e90ff").grid(row=3, column=1, columnspan=2, pady=20, ipady=5, sticky='e', padx=20)
    
    loginFrame.grid(row=0, column=2, rowspan=2,columnspan=2, sticky='es',padx=120,ipadx=50,ipady=20)
    userEntry.focus_force()

def login() :
    global user , pos
    user = userEntry.get()
    pwd = pwdEntry.get()
    if user:
        if pwd:
            sql = "SELECT * FROM emp_acc WHERE e_num=?"
            cursor.execute(sql,(user,))
            result = cursor.fetchone()
            if result:
                password = result[3]
                if password == pwd:
                    pos = result[4]
                    if pos == "Admin" :
                        homepageA()
                    if pos == "Internal" :
                        homepageI()
                    if pos == "Sales" :
                        homepageS()
                else:
                    messagebox.showwarning("System","รหัสพนักงาน หรือรหัสผ่านไม่ถูกต้อง")    
            else:
                messagebox.showwarning("System","ไม่พบรหัสพนักงาน หรือรหัสผ่านไม่ถูกต้อง")
        else:
            messagebox.showwarning("System", "กรุณากรอก รหัสผ่าน")
            pwdEntry.focus_force()
    else:
        messagebox.showwarning("System", "กรุณากรอก รหัสพนักงาน")
        userEntry.focus_force()

def fetchTree():
    employeeTable.delete(*employeeTable.get_children())
    sql = 'SELECT * FROM emp_acc'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data1 in enumerate(result):
            employeeTable.insert("","end",values=(data1[1],data1[2],data1[5]+" "+data1[6],data1[4],data1[7],data1[8],data1[9],data1[10]))

def fetchTreeForMngPD():
    productTable.delete(*productTable.get_children()) # clear Treeview
    sql = 'SELECT * FROM product'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data1 in enumerate(result):
            productTable.insert("","end",values=(data1[1],data1[3],data1[4]))

def fetchTreeForMngMat():
    MatTable.delete(*MatTable.get_children()) # clear Treeview
    sql = 'SELECT * FROM material'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data1 in enumerate(result):
            MatTable.insert("","end",values=(data1[2],data1[3],data1[4],data1[5]))

def fetchTreeForMngAg():
    agentTable.delete(*agentTable.get_children()) # clear Treeview
    sql = 'SELECT * FROM agent'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data1 in enumerate(result):
            agentTable.insert("","end",values=(data1[1],data1[2],data1[3],data1[4]))

def fetchTreeForMngMatPur():
    matPurchaseTable.delete(*matPurchaseTable.get_children()) # clear Treeview
    
    sql = 'SELECT * FROM material_purchase'
    cursor.execute(sql)
    MatPur = cursor.fetchall()
    if MatPur:
        cursor.execute(''' select mat_num from material''')
        Mat = cursor.fetchone()
    
        for i,data1 in enumerate(MatPur):
            
            cursor.execute(''' select mat_num from material
            where mat_id = ?''',(data1[1],))
            Mat = cursor.fetchone()

            cursor.execute(''' select sup_num from supplier
            where sup_id = ?''',(data1[2],))
            Sup = cursor.fetchone()

            matPurchaseTable.insert("","end",values=(data1[0],Sup[0]+"-"+Mat[0],data1[3],data1[4]))

def fetchTreeForMngCus():
    customerTable.delete(*customerTable.get_children()) # clear Treeview
    sql = 'SELECT * FROM customer'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data1 in enumerate(result):
            customerTable.insert("","end",values=(data1[1],data1[2],data1[3],data1[4]))

def fetchTreeForMngOrder() :
    OrderTable.delete(*OrderTable.get_children()) # clear Treeview
    sql = 'SELECT * FROM "order" '
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data1 in enumerate(result):
            OrderTable.insert("","end",values=(data1[1],data1[4],data1[5],data1[6],data1[7]))

def homepageA() : 
    def manage_account() :
        def saveAddEmp() :
            newID = newIDCard.get()
            name,lname,gen,birth,ph1 = newName.get(),newLastName.get(),selGender.get(),newEmBirth.get(),newPhone1.get()
            newPwd,newCPwd = newPass.get(),newConfirmPass.get()
            ans = messagebox.askquestion("System","คุณแน่ใจหรือว่า จะทำการเพิ่มพนักงาน?")
            if ans == 'yes':
                if newID:
                    if newID.isdigit():
                        if name:
                            if lname:
                                if gen:
                                    if birth:
                                        if ph1:
                                            if ph1.isdigit():
                                                cursor.execute(''' select idCard from emp_acc
                                                where idCard = ?''',(newID,))
                                                result = cursor.fetchall()
                                                if result:
                                                    messagebox.showwarning("System","มีบัตรประชาชนนนี้ในฐานข้อมูลแล้ว") 
                                                else:
                                                    try:
                                                        int_newID = int(newID)
                                                        if len(newID) < 13:         
                                                            messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชนให้ครบ 13 หลัก") 
                                                        elif len(newID) > 13:
                                                            messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชนไม่เกิน 13 หลัก")
                                                        else:
                                                            if newPwd == newCPwd :
                                                                pos = selPos.get()

                                                                current_year = datetime.datetime.now().year
                                                                t_year = current_year+543
                                                                y_id = str(t_year)[2:4]

                                                                if pos == "Admin" :
                                                                    id_ = "1"+y_id+"001"
                                                                    id = int(id_)
                                                                if pos == "Sales" :
                                                                    id_ = "2"+y_id+"001"
                                                                    id = int(id_)
                                                                if pos == "Internal" :
                                                                    id_ = "3"+y_id+"001"
                                                                    id = int(id_)

                                                                sql = '''select e_num from emp_acc
                                                                where e_num = ?'''
                                                                cursor.execute(sql,(id,))
                                                                result = cursor.fetchone()
                                                                while result:
                                                                    id = id+1
                                                                    cursor.execute(sql,(id,))
                                                                    result = cursor.fetchone()
                                                                
                                                                sql = "INSERT INTO emp_acc VALUES(NULL,?,?,?,?,?,?,?,?,?,?)"
                                                                cursor.execute(sql,(id,newIDCard.get(),newPass.get(),selPos.get(),newName.get(),newLastName.get(),selGender.get(),newEmBirth.get(),newPhone1.get(),newPhone2.get(),))
                                                                conn.commit()
                                                                addFrame1.destroy()
                                                                manage_account()
                                                            else:
                                                                messagebox.showwarning("System","กรุณากรอก รหัสผ่านให้ตรงกัน")
                                                    except ValueError:
                                                        messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชนเป็นตัวเลข 13 หลักเท่านั้น")
                                            else:
                                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์ เป็นตัวเลข")
                                        else:
                                            messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")
                                    else:
                                        messagebox.showwarning("System","กรุณากรอก วันเกิด")
                                else:
                                    messagebox.showwarning("System","กรุณาใส่ เพศ")
                            else:
                                messagebox.showwarning("System","กรุณากรอก นามสกุล")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ชื่อจริง")
                    else:
                        messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชน เป็นตัวเลข")
                else:
                    messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชน 13 หลัก")
        def back_mng() :
            addFrame1.destroy()
            manage_account()
        def search() : 
            search = seachEntry.get()
            if search:
                sql = "SELECT * FROM emp_acc WHERE e_num=?"
                cursor.execute(sql,(search,))
                result = cursor.fetchall()
                if result:
                    employeeTable.delete(*employeeTable.get_children())
                    for i,data1 in enumerate(result):
                        employeeTable.insert("","end",values=(data1[1],data1[2],data1[5]+" "+data1[6],data1[4],data1[7],data1[8],data1[9],data1[10]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสพนักงาน ที่ต้องการค้นหา")
                    seachEntry.delete(0,END)
                    employeeTable.delete(*employeeTable.get_children())
                    fetchTree()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสพนักงาน ที่ต้องการค้นหา")
        def add() :
            global addFrame1, newIDCard, newName, newLastName, gMale, gFemale, selPos, newEmBirth, newPhone1, newPhone2, newPass, newConfirmPass
            mngFrame1.destroy()
            addFrame1 = Frame(root,bg="#e0f2fc")
            addFrame1.columnconfigure((0,1,2),weight=1)
            addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame1.configure(width=1000,height=700)
            addFrame1.place(x=200,y=0,width=1000,height=700)

            Label(addFrame1,text="เพิ่มพนักงาน" ,bg="#e0f2fc",font="Calibri 20 bold").place(x=450,y=10)
            Label(addFrame1,text="รหัสบัตรประชาชน" ,bg="#e0f2fc").place(x=225,y=50)
            Label(addFrame1,text="ชื่อจริง" ,bg="#e0f2fc").place(x=225,y=150)
            Label(addFrame1,text="นามสกุล" ,bg="#e0f2fc").place(x=500,y=150)
            Label(addFrame1,text="วันเกิด\nตัวอย่าง : 18/07/2002" ,bg="#e0f2fc").place(x=700,y=150)
            Label(addFrame1,text="เพศ" ,bg="#e0f2fc").place(x=225,y=250)
            Label(addFrame1,text="ตำแหน่ง" ,bg="#e0f2fc").place(x=500,y=250)
            Label(addFrame1,text="โทรศัพท์" ,bg="#e0f2fc").place(x=225,y=350)
            Label(addFrame1,text="โทรศัพท์ สำรอง" ,bg="#e0f2fc").place(x=500,y=350)
            Label(addFrame1,text="รหัสผ่าน" ,bg="#e0f2fc").place(x=225,y=450)
            Label(addFrame1,text="Confirm รหัสผ่าน" ,bg="#e0f2fc").place(x=500,y=450)

            newIDCard = Entry(addFrame1,width=40)
            newIDCard.place(x=225,y=100)

            newName = Entry(addFrame1,width=15)
            newName.place(x=225,y=200)

            newLastName = Entry(addFrame1,width=15)
            newLastName.place(x=500,y=200)

            gMale = Radiobutton(addFrame1,text="ชาย",value="ชาย",variable=selGender,bg="#e0f2fc") #############################
            gMale.place(x=225,y=300)

            gFemale = Radiobutton(addFrame1,text="หญิง",value="หญิง",variable=selGender,bg="#e0f2fc")
            gFemale.place(x=350,y=300)

            selPos.set("Admin")
            optionPos = ["Admin","Internal","Sales"]

            newEmPos = OptionMenu(addFrame1,selPos,*optionPos)
            newEmPos.place(x=500,y=300)

            newEmBirth = Entry(addFrame1,width=10)
            newEmBirth.place(x=700,y=200)

            newPhone1 = Entry(addFrame1,width=15)
            newPhone1.place(x=225,y=400)

            newPhone2 = Entry(addFrame1,width=15)
            newPhone2.place(x=500,y=400)

            newPass = Entry(addFrame1,width=15,show='*')
            newPass.place(x=225,y=500)

            newConfirmPass = Entry(addFrame1,width=15,show='*')
            newConfirmPass.place(x=500,y=500)

            def showPwd():
                password = newPass.get()
                newPass.config(show="")
                newPass.delete(0, END)
                newPass.insert(0, password)

                Cpassword = newConfirmPass.get()
                newConfirmPass.config(show="")
                newConfirmPass.delete(0, END)
                newConfirmPass.insert(0, Cpassword)
            
            def hidePwd():
                newPass.config(show="*")
                newConfirmPass.config(show="*")
            
            Button(addFrame1,text="แสดง",command=showPwd).place(x=225,y=540)
            Button(addFrame1,text="ซ่อน",command=hidePwd).place(x=300,y=540)

            Button(addFrame1,text="บันทึก",width=10,bg="#007bff",command=saveAddEmp).place(x=500,y=600)
            Button(addFrame1,text="กลับ",width=10,bg="#6c757d",command=back_mng).place(x=700,y=600)
        def delete() :
            ans = messagebox.askquestion("System", "แน่ใจหรือว่าจะลบพนักงาน ?")
            selEmployee = employeeTable.item(employeeTable.focus(),'values')
            if ans == 'yes' :
                if selEmployee:
                    selected_employee_id = selEmployee[1]
                    sql = 'DELETE FROM emp_acc WHERE idCard=?'
                    cursor.execute(sql,(selected_employee_id,))
                    conn.commit()
                    messagebox.showinfo("System", "ลบพนักงานเสร็จสิ้น")
                    fetchTree()
                else:
                    messagebox.showwarning("System", "กรุุณาเลือกพนักงานที่ต้องการลบ")        
        def edit(self) :
            e_id.delete(0,END)
            e_fname.delete(0,END)
            e_lname.delete(0,END)
            e_birth.delete(0,END)
            e_phone1.delete(0,END)
            e_phone2.delete(0,END)

            global selected_item
            selected_item = employeeTable.selection()
            values = employeeTable.item(selected_item)['values']
            if values:
                name = values[2]
                name_parts = name.split()
                f_name = name_parts[0]
                s_name = name_parts[-1]
            
                e_id.insert(0, values[1])
                e_fname.insert(0, f_name)
                e_lname.insert(0, s_name)
                selGen.set(values[4])
                
                e_birth.insert(0, values[5])
                e_phone1.insert(0,"0"+str(values[6]))
                e_phone2.insert(0, values[7])    
                selPos.set(values[3]) 
        def saveBtn() :
            olde_id = e_id.get()
            newFname = e_fname.get()
            newLname = e_lname.get()
            newGender = selGen.get()
            newBirth = e_birth.get()
            newPhone1 = e_phone1.get()
            newPhone2 = e_phone2.get()
            newPos = selPos.get()

            selected_item = employeeTable.selection()
            values = employeeTable.item(selected_item)['values']
            if values:
                sameID = str(values[1])

            ans = messagebox.askquestion("System","คุณแน่ใจว่าต้องการแก้ไข ?")
            if ans == 'yes' :
                if olde_id:
                    if len(olde_id) < 13:         
                        messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชนให้ครบ 13 หลัก") 
                    elif len(olde_id) > 13:
                        messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชนไม่เกิน 13 หลัก")
                    else:
                        try:
                            int_OldID = int(olde_id)
                            cursor.execute(''' select idCard from emp_acc ''')
                            result = cursor.fetchall()
                            all_Card = [value for tup in result for value in tup]
                            all_Card.remove(sameID)
                            if olde_id in all_Card:
                                messagebox.showwarning("System","มีบัตรประชาชนนนี้ในฐานข้อมูลแล้ว")                           
                            else:
                                if newFname:
                                    if newLname:
                                        if newBirth:
                                            if newPhone1:
                                                pos = newPos
                                                current_year = datetime.datetime.now().year
                                                t_year = current_year+543
                                                y_id = str(t_year)[2:4]

                                                if pos == "Admin" :
                                                    id_ = "1"+y_id+"001"
                                                    id = int(id_)
                                                elif pos == "Sales" :
                                                    id_ = "2"+y_id+"001"
                                                    id = int(id_)
                                                elif pos == "Internal" :
                                                    id_ = "3"+y_id+"001"
                                                    id = int(id_)

                                                sql = '''select e_num from emp_acc
                                                where e_num = ?'''
                                                cursor.execute(sql,(id,))
                                                result = cursor.fetchone()
                                                while result:
                                                    id = id+1
                                                    cursor.execute(sql,(id,))
                                                    result = cursor.fetchone()
                                                
                                                values = employeeTable.item(selected_item)['values']
                                                e_num = values[0]
                                                sql = '''UPDATE emp_acc
                                                SET idCard=?,e_fname=?,e_lname=?,e_gender=?,e_birth=?,e_phone1=?,e_phone2=?,pos=?,e_num=?
                                                WHERE e_num=?'''
                                                cursor.execute(sql,(olde_id,newFname,newLname,newGender,newBirth,newPhone1,newPhone2,newPos,id,e_num))
                                                conn.commit()
                                                employeeTable.delete(*employeeTable.get_children())
                                                fetchTree()
                                            else:
                                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")
                                        else:
                                            messagebox.showwarning("System","กรุณากรอก วันเกิด")
                                    else:
                                        messagebox.showwarning("System","กรุณากรอก นามสกุล")
                                else:
                                    messagebox.showwarning("System","กรุณากรอก ชื่อจริง")
                        except ValueError:
                            messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชนเป็นตัวเลข 13 หลักเท่านั้น")
                else:
                    messagebox.showwarning("System","กรุณากรอก รหัสบัตรประชาชน 13 หลักที่ต้องการแก้ไข")

        global searchEntry,selSearch,employeeTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        employeeTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5","col6","col7","col8"),selectmode=BROWSE)
        employeeTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        employeeTable.bind('<<TreeviewSelect>>',edit)

        employeeTable.heading('col1', text="รหัสพนักงาน", anchor=W)
        employeeTable.heading('col2', text="หมายเลขประชาชน", anchor=W)
        employeeTable.heading('col3', text="ชื่อ-นามสกุล", anchor=W)
        employeeTable.heading('col4', text="ตำแหน่ง", anchor=W)
        employeeTable.heading('col5', text="เพศ", anchor=W)
        employeeTable.heading('col6', text="วันเกิด", anchor=N)
        employeeTable.heading('col7', text="เบอร์โทรศัพท์", anchor=W)
        employeeTable.heading('col8', text="เบอร์โทรศัพท์ สำรอง", anchor=W)

        employeeTable.column('col1',anchor=W, width=60)
        employeeTable.column('col2',anchor=W, width=100)
        employeeTable.column('col3',anchor=W, width=100)
        employeeTable.column('col4',anchor=W, width=100)
        employeeTable.column('col5',anchor=W, width=100)
        employeeTable.column('col6',anchor=W, width=100)
        employeeTable.column('col7',anchor=W, width=100)
        employeeTable.column('col8',anchor=W, width=100)
        employeeTable.column('#0', width=0, minwidth=0) #default column
        fetchTree()

        # Search Box
        Label(mngFrame1,text="ค้นหา รหัสพนักงาน",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold",padx=50).grid(row=8,column=0,sticky="w",padx=10,pady=20)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=15)
        seachEntry.grid(row=8,column=1,sticky=W,padx=5,pady=20)

        Button(mngFrame1,image=img_search,command=search).place(x=365,y=545)
        
        # Add / Delete / Edit
        Label(mngFrame1,text="แก้ไขข้อมูลบัญชีผู้ใช้",font="Calibri 16 bold",bg="#e0f2fc").grid(row=2,column=1,sticky=W,ipadx=50)

        Label(mngFrame1,text="รหัสบัตรประชาชน",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=1,sticky=SW)
        e_id = Entry(mngFrame1,width=20,bg="#FFFFFF")
        e_id.grid(row=4,column=1,sticky=NW,padx=10)

        Label(mngFrame1,text="ชื่อจริง",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=2,sticky=SW)
        e_fname = Entry(mngFrame1,width=20,bg="#FFFFFF")
        e_fname.grid(row=4,column=2,sticky=NW,padx=10)

        Label(mngFrame1,text="นามสกุล",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=3,sticky=SW)
        e_lname = Entry(mngFrame1,width=20,bg="#FFFFFF")
        e_lname.grid(row=4,column=3,sticky=NW,padx=10)

        Label(mngFrame1,text="เพศ",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=4,sticky=SW)

        global selGen
        selGen.set("ชาย")
        optionGen = ["ชาย","หญิง"]
        g_pos = OptionMenu(mngFrame1,selGen,*optionGen)
        g_pos.grid(row=4,column=4,sticky=NW,ipadx=40)

        Label(mngFrame1,text="วันเกิด",font="Calibri 12",bg="#e0f2fc").grid(row=5,column=1,sticky=SW)
        e_birth = Entry(mngFrame1,width=20,bg="#FFFFFF")
        e_birth.grid(row=6,column=1,sticky=NW,padx=10)

        Label(mngFrame1,text="เบอร์โทรศัพท์",font="Calibri 12",bg="#e0f2fc").grid(row=5,column=2,sticky=SW)
        e_phone1 = Entry(mngFrame1,width=20,bg="#FFFFFF")
        e_phone1.grid(row=6,column=2,sticky=NW,padx=10)

        Label(mngFrame1,text="เบอร์โทรศัพท์ สำรอง",font="Calibri 12",bg="#e0f2fc").grid(row=5,column=3,sticky=SW)
        e_phone2 = Entry(mngFrame1,width=20,bg="#FFFFFF")
        e_phone2.grid(row=6,column=3,sticky=NW,padx=10)

        Label(mngFrame1,text="ตำแหน่ง",font="Calibri 12",bg="#e0f2fc").grid(row=5,column=4,sticky=SW)

        global selPos
        selPos.set("Admin")
        optionPos = ["Admin","Internal","Sales"]
        e_pos = OptionMenu(mngFrame1,selPos,*optionPos)
        e_pos.grid(row=6,column=4,sticky=NW,ipadx=40)

        Label(mngFrame1,text="จัดการบัญชีผู้ใช้",font="Calibri 20 bold",bg="#e0f2fc",padx=50).grid(row=0,column=0)
        Button(mngFrame1,text="เพิ่ม",width=10,bg="#00cc66",command=add,padx=30).grid(row=8,column=4,sticky="e",padx=20)
        Button(mngFrame1,text="ลบ",width=10,bg="#ff0000",command=delete,padx=30).grid(row=8,column=5,sticky="e",padx=20)
        Button(mngFrame1,text="บันทึก",width=10,bg="#007bff",command=saveBtn,padx=30).grid(row=8,column=6,sticky="e",padx=20)
    def manage_product() :
        def edit(self) :
            pd_cap.destroy
            pd_price.destroy
            pd_quantity.destroy

            global selected_item
            selected_item = productTable.selection()
            if selected_item:
                pd_cap.config(text=productTable.item(selected_item)['values'][0])
                pd_price.config(text=productTable.item(selected_item)['values'][1])
                pd_quantity.config(text=productTable.item(selected_item)['values'][2])
        def addBtn() :
            old_amt = pd_quantity.cget("text")
            new_amt = new_quantity.get()
            cap = pd_cap.cget("text")
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าจะ เพิ่มจำนวนสินค้า ?")     
            if ans == 'yes' :
                if new_amt:
                    try:
                        ckint = int(new_amt)
                        if int(new_amt) < 0:
                            messagebox.showwarning("System", "กรุณาใส่ตัวเลขจำนวนเต็ม")
                        else:
                            amt = int(old_amt) + int(new_amt)
                            cursor.execute(''' update product
                            set pd_quantity = ?
                            where pd_cap = ?''',(amt,cap,))
                            conn.commit()
                            pd_cap.config(text='')
                            pd_price.config(text='')
                            pd_quantity.config(text='')
                    except ValueError:
                        messagebox.showwarning("System", "กรุณาใส่ตัวเลข")
                else:
                    messagebox.showwarning("System", "กรุณาใส่จำนวนสินค้าที่การเพิ่ม")
            new_quantity.delete(0,END) 
            
            productTable.delete(*productTable.get_children())
            fetchTreeForMngPD()
        def deleBtn() :
            old_amt = pd_quantity.cget("text")
            new_amt = new_quantity.get()
            cap = pd_cap.cget("text")
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าจะ ลดจำนวนสินค้า ?")
            if ans == 'yes' :
                if new_amt:
                    try:
                        ckint = int(new_amt)
                        if int(new_amt) < 0:
                            messagebox.showwarning("System", "กรุณาใส่ตัวเลขจำนวนเต็ม")
                        else:
                            if int(new_amt) <= int(old_amt):
                                amt = int(old_amt) - int(new_amt)
                                cursor.execute(''' update product
                                set pd_quantity = ?
                                where pd_cap = ?''',(amt,cap,))
                                conn.commit()
                                pd_cap.config(text='')
                                pd_price.config(text='')
                                pd_quantity.config(text='')
                                   
                            else:
                                messagebox.showwarning("System", "กรุณาใส่จำนวนสินค้าให้ถูกต้อง")
                    except ValueError:
                        messagebox.showwarning("System", "กรุณาใส่ตัวเลข")
                else:
                    messagebox.showwarning("System", "กรุณาใส่จำนวนสินค้าที่การลด")
            productTable.delete(*productTable.get_children())
            fetchTreeForMngPD()
            new_quantity.delete(0,END)

        global searchEntry,selSearch,productTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        productTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5"),selectmode=BROWSE)
        productTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        productTable.bind('<<TreeviewSelect>>',edit)

        productTable.heading('col1', text="ขนาด", anchor=W)
        productTable.heading('col2', text="ราคา", anchor=W)
        productTable.heading('col3', text="จำนวน", anchor=W)

        productTable.column('col1',anchor=W, width=60)
        productTable.column('col2',anchor=W, width=60)
        productTable.column('col3',anchor=W, width=80)
        productTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngPD()

        Label(mngFrame1,text="แก้ไขจำนวนสินค้า",font="Calibri 16 bold",bg="#e0f2fc").grid(row=2,column=1,sticky=SW)

        # Add / Delete / Edit
        Label(mngFrame1,text="ขนาด/ขวด",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=2,sticky=SW)
        pd_cap = Label(mngFrame1,width=10,bg="#FFFFFF")
        pd_cap.grid(row=4,column=2,sticky=NW,padx=10)

        Label(mngFrame1,text="ราคา/แพ็ค",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=3,sticky=SW)
        pd_price = Label(mngFrame1,width=10,bg="#FFFFFF")
        pd_price.grid(row=4,column=3,sticky=NW,padx=10)

        Label(mngFrame1,text="จำนวน/แพ็ค",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=4,sticky=SW)
        pd_quantity = Label(mngFrame1,width=10,bg="#FFFFFF")
        pd_quantity.grid(row=4,column=4,sticky=NW,padx=10)

        Label(mngFrame1,text="เพิ่ม/ลบ จำนวนสินค้า",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=5,sticky=SW)
        new_quantity = Entry(mngFrame1,width=10,bg="#FFFFFF")
        new_quantity.grid(row=4,column=5,sticky=NW,padx=10)

        Label(mngFrame1,text="จัดการคลังสินค้า",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=1)
        Button(mngFrame1,text="เพิ่ม",width=10,bg="#00cc66",command=addBtn).grid(row=8,column=4)
        Button(mngFrame1,text="ลบ",width=10,bg="#ff0000",command=deleBtn).grid(row=8,column=5)
    def manage_material() :
        def deleteMT() :
            selected_item = MatTable.selection()
            if selected_item:
                mat_id = MatTable.item(selected_item)['values'][0]
            old_amt,new_amt = quanMat.cget('text'),newquna.get()
            ans = messagebox.askquestion("System","คุณแน่ใจหรือว่าต้องการลบจำนวนวัตถุดิบนี้")
            if ans == 'yes' :
                if old_amt:
                    if new_amt:
                        if new_amt.isdigit():
                            if float(new_amt) > 0:
                                if int(new_amt) < int(old_amt):
                                    amt = int(old_amt) - int(new_amt)
                                    cursor.execute(''' update material
                                    set mat_quantity = ?
                                    where mat_num = ?''',(amt,mat_id,))
                                    conn.commit()
                                    MatTable.delete(*MatTable.get_children())
                                    fetchTreeForMngMat()
                                else:
                                    messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบให้ถูกต้อง")
                                    newquna.delete(0,END)
                            else:
                                messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบเป็นเลขบวก")
                        else:
                            messagebox.showwarning("System","กรุณากรอก เป็นตัวเลข")
                            newquna.delete(0,END)
                    else:
                        messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบที่ต้องการลบ")
                else:
                    messagebox.showwarning("System","กรุณาเลือก วัตถุดิบที่ต้องการลบ")
        def searchMat() : 
            searchMat = seachEntry.get()
            sql = "SELECT * FROM material WHERE mat_num=?"
            cursor.execute(sql,(searchMat,))
            result = cursor.fetchall()
            if searchMat:
                if result:
                    for i,data1 in enumerate(result):
                        MatTable.delete(*MatTable.get_children())
                        MatTable.insert("","end",values=(data1[2],data1[3],data1[4],data1[5]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสวัตถุดิบ")
                    fetchTreeForMngMat()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสวัตถุดิบที่ต้องการค้นหา")
                fetchTreeForMngMat()
        def edit(self) :
            mat_id.destroy
            mat_name.destroy
            quanMat.destroy
            datails.destroy

            selected_item = MatTable.selection()
            if selected_item:
                mat_id.config(text=MatTable.item(selected_item)['values'][0])
                mat_name.config(text=MatTable.item(selected_item)['values'][1])
                quanMat.config(text=MatTable.item(selected_item)['values'][2])
                datails.config(text=MatTable.item(selected_item)['values'][3])

        global searchEntry,selSearch,MatTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        MatTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5"),selectmode=BROWSE)
        MatTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        MatTable.bind('<<TreeviewSelect>>',edit)

        MatTable.heading('col1', text="รหัสวัตถุดิบ", anchor=W)
        MatTable.heading('col2', text="ชื่อ", anchor=W)
        MatTable.heading('col3', text="จำนวน", anchor=W)
        MatTable.heading('col4', text="รายละเอียด", anchor=W)

        MatTable.column('col1',anchor=W, width=150)
        MatTable.column('col2',anchor=W, width=150)
        MatTable.column('col3',anchor=W, width=150)
        MatTable.column('col4',anchor=W, width=280)
        MatTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngMat()

        # Search Box
        Label(mngFrame1,text="ค้นหา รหัสวัตถุดิบ",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=E,padx=10,pady=20)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=15)
        seachEntry.grid(row=8,column=1,sticky=W,padx=5,pady=20)

        # Add / Delete / Edit
        Label(mngFrame1,text="รหัสวัตถุดิบ",font="Calibri 12",bg="#e0f2fc").place(x=140,y=385)
        mat_id = Label(mngFrame1,width=10,bg="#FFFFFF")
        mat_id.place(x=140,y=410)

        Label(mngFrame1,text="ชื่อ",font="Calibri 12",bg="#e0f2fc").place(x=280,y=385)
        mat_name = Label(mngFrame1,width=30,bg="#FFFFFF")
        mat_name.place(x=280,y=410)
        
        Label(mngFrame1,text="จำนวน",font="Calibri 12",bg="#e0f2fc").place(x=640,y=385)
        quanMat = Label(mngFrame1,width=10,bg="#FFFFFF")
        quanMat.place(x=640,y=410)

        Label(mngFrame1,text="รายละเอียด",font="Calibri 12",bg="#e0f2fc").place(x=140,y=450)
        datails = Label(mngFrame1,bg="#FFFFFF",width=50)
        datails.place(x=140,y=475)

        Label(mngFrame1,text="เพิ่ม/ลดจำนวนวัตถุดิบ",font="Calibri 12",bg="#e0f2fc").place(x=780,y=385)
        newquna = Entry(mngFrame1,width=13,bg="#FFFFFF")
        newquna.place(x=780,y=410)
        
        Label(mngFrame1,text="จัดการคลังวัตถุดิบ",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Label(mngFrame1,text="แก้ไขจำนวนวัตถุดิบ",font="Calibri 16 bold",bg="#e0f2fc").place(x=13,y=340)
        
        Button(mngFrame1,text="ลบ",width=10,bg="#ff0000",command=deleteMT).place(x=795,y=445)
        Button(mngFrame1,image=img_search,command=searchMat).place(x=449,y=545)
    def manage_agent() : 
        def edit(self) :
            ag_name.delete(0,END)
            ag_address.delete(0,END)
            ag_phone.delete(0,END)

            selected_item = agentTable.selection()
            if selected_item:
                phone = agentTable.item(selected_item)['values'][3]
                ag_name.insert(0,agentTable.item(selected_item)['values'][1])
                ag_address.insert(0,agentTable.item(selected_item)['values'][2])
                ag_phone.insert(0,"0"+str(phone))
        def searchAg() :
            searchAgent = seachEntry.get()
            sql = '''SELECT * FROM agent
            WHERE ag_num=?'''
            cursor.execute(sql,(searchAgent,))
            result = cursor.fetchall()
            if searchAgent:
                if result:
                    agentTable.delete(*agentTable.get_children())
                    for i,data1 in enumerate(result):
                        agentTable.insert("","end",values=(data1[1],data1[2],data1[3],data1[4]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสตัวแทนจำหน่าย")
                    seachEntry.delete(0,END)
                    fetchTreeForMngAg()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสตัวแทนจำหน่าย")
                fetchTreeForMngAg()
        def saveBtn() :
            selected_item = agentTable.selection()
            if selected_item:
                ag_id = agentTable.item(selected_item)['values'][0]
                name,address,phone = ag_name.get(),ag_address.get(),ag_phone.get()
                ans = messagebox.askquestion("System","คุณแน่ใจหรือว่า ต้องการแก้ไขข้อมูลตัวแทนจำหน่าย")
                if ans == 'yes' :
                    if name:
                        if address:
                            if phone:
                                sql = '''UPDATE agent SET ag_name=?,ag_address=?,ag_phone=?
                                WHERE ag_num=?'''
                                cursor.execute(sql,(name,address,phone,ag_id,))
                                conn.commit()
                                fetchTreeForMngAg()
                            else:
                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ที่อยู่")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อ")
            else:
                messagebox.showwarning("System","กรุณาเลือกตัวแทนจำหน่ายที่ต้องการแก้ไข")
        def deleteBtn() :
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าต้องการลบตัวแทนจำหน่ายนี้ ?")
            if ans == 'yes' :
                selected_item = agentTable.selection()
                if selected_item:
                    ag_num = agentTable.item(selected_item)['values'][0]
                    cursor.execute(''' delete from agent
                    where ag_num = ? ''',(ag_num,))
                    conn.commit()
                    fetchTreeForMngAg()
                else:
                    messagebox.showwarning("System","กรุณาเลือกตัวแทนจำหน่ายที่ต้องการลบ")

        global searchEntry,selSearch,agentTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        agentTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4"),selectmode=BROWSE)
        agentTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        agentTable.bind('<<TreeviewSelect>>',edit)

        agentTable.heading('col1', text="รหัสซัพลลายเออร์", anchor=W)
        agentTable.heading('col2', text="ชื่อ", anchor=W)
        agentTable.heading('col3', text="ที่อยู่", anchor=W)
        agentTable.heading('col4', text="หมายเลขโทรศัพท์", anchor=W)

        agentTable.column('col1',anchor=W, width=50)
        agentTable.column('col2',anchor=W, width=50)
        agentTable.column('col3',anchor=W, width=300)
        agentTable.column('col4',anchor=W, width=50)
        agentTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngAg()

        # Search Box
        Label(mngFrame1,text="ค้นหา รหัสตัวแทนจำหน่าย",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=W,padx=10,pady=20)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=15)
        seachEntry.grid(row=8,column=0,sticky=E,padx=5,pady=20)

        # Add / Delete / Edit
        Label(mngFrame1,text="ชื่อ",font="Calibri 12",bg="#e0f2fc").place(x=160,y=380)
        ag_name = Entry(mngFrame1,width=20,bg="#FFFFFF")
        ag_name.place(x=160,y=405)

        Label(mngFrame1,text="ที่อยู่",font="Calibri 12",bg="#e0f2fc").place(x=160,y=450)
        ag_address = Entry(mngFrame1,width=50,bg="#FFFFFF")
        ag_address.place(x=160,y=475)

        Label(mngFrame1,text="หมายเลขโทรศัพท์",font="Calibri 12",bg="#e0f2fc").place(x=480,y=380)
        ag_phone = Entry(mngFrame1,width=21,bg="#FFFFFF")
        ag_phone.place(x=480,y=405)

        Label(mngFrame1,text="แก้ไขข้อมูลตัวแทนจำหน่าย",font="Calibri 16 bold",bg="#e0f2fc").place(x=10,y=340)

        Label(mngFrame1,text="จัดการทะเบียนตัวแทนจำหน่าย",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Button(mngFrame1,text="บันทึก",bg="#007bff",width=10,command=saveBtn).place(x=540,y=540)
        Button(mngFrame1,text="ลบ",bg="#ff0000",width=10,command=deleteBtn).place(x=700,y=540)
        Button(mngFrame1,image=img_search,command=searchAg).place(x=412,y=545)
    def manage_customer() : 
        def edit_customer(self) :
            cus_name.delete(0,END)
            cus_address.delete(0,END)
            cus_phone.delete(0,END)

            selected_item = customerTable.selection()
            if selected_item:
                phone = "0"+str(customerTable.item(selected_item)['values'][3])
                cus_name.insert(0,customerTable.item(selected_item)['values'][1])
                cus_address.insert(0,customerTable.item(selected_item)['values'][2])
                cus_phone.insert(0,phone)
        def search_customer() :
            searchCUS = cus_seach.get()
            sql = "SELECT * FROM customer WHERE cus_num=?"
            cursor.execute(sql,(searchCUS,))
            result = cursor.fetchall()
            if searchCUS:
                if result:
                    customerTable.delete(*customerTable.get_children())
                    for i,data1 in enumerate(result):
                        customerTable.insert("","end",values=(data1[1],data1[2],data1[3],data1[4]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสลูกค้า")
                    cus_seach.delete(0,END)
                    fetchTreeForMngCus()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสลูกค้า")
        def save_customer() :        
            selected_item = customerTable.selection()
            if selected_item:
                cus_id = customerTable.item(selected_item)['values'][0]
                name,address,phone = cus_name.get(),cus_address.get(),cus_phone.get()
                ans = messagebox.askquestion("System","คุณแน่ใจหรือว่า ต้องการแก้ไขข้อมูลลูกค้า")
                if ans == 'yes' :
                    if name:
                        if address:
                            if phone:
                                sql = '''UPDATE customer SET cus_name=?,cus_address=?,cus_phone=?
                                WHERE cus_num=?'''
                                cursor.execute(sql,(name,address,phone,cus_id,))
                                conn.commit()
                                fetchTreeForMngCus()
                            else:
                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ที่อยู่")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อ")
            else:
                messagebox.showwarning("System","กรุณาเลือกลูกค้าที่ต้องการแก้ไข")
        def delete_customer() :
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าต้องการลบลูกค้านี้ ?")
            if ans == 'yes' :
                selected_item = customerTable.selection()
                if selected_item:
                    cus_num = customerTable.item(selected_item)['values'][0]
                    cursor.execute(''' delete from agent
                    where ag_num = ? ''',(cus_num,))
                    conn.commit()
                    fetchTreeForMngAg()
                else:
                    messagebox.showwarning("System","กรุณาเลือกลูกค้าที่ต้องการลบ")

        global searchEntry,selSearch,customerTable
        mainFrame1.destroy()
        manage_cus_Frame1 = Frame(root,bg="#e0f2fc")
        manage_cus_Frame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        manage_cus_Frame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        manage_cus_Frame1.configure(width=1000,height=700)
        manage_cus_Frame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        customerTable = ttk.Treeview(manage_cus_Frame1, columns=("col1","col2","col3","col4"),selectmode=BROWSE)
        customerTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        customerTable.bind('<<TreeviewSelect>>',edit_customer)

        customerTable.heading('col1', text="รหัสลูกค้า", anchor=W)
        customerTable.heading('col2', text="ชื่อ", anchor=W)
        customerTable.heading('col3', text="ที่อยู่", anchor=W)
        customerTable.heading('col4', text="หมายเลขโทรศัพท์", anchor=W)

        customerTable.column('col1',anchor=W, width=50)
        customerTable.column('col2',anchor=W, width=50)
        customerTable.column('col3',anchor=W, width=300)
        customerTable.column('col4',anchor=W, width=50)
        customerTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngCus()

        # Search Box
        Label(manage_cus_Frame1,text="ค้นหา รหัสลูกค้า",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=W,padx=10,pady=20)
        cus_seach = Entry(manage_cus_Frame1,bg="#FFFFFF",width=15)
        cus_seach.place(x=150,y=550)

        # Add / Delete / Edit
        Label(manage_cus_Frame1,text="ชื่อ",font="Calibri 12",bg="#e0f2fc").place(x=160,y=380)
        cus_name = Entry(manage_cus_Frame1,width=20,bg="#FFFFFF")
        cus_name.place(x=160,y=405)

        Label(manage_cus_Frame1,text="ที่อยู่",font="Calibri 12",bg="#e0f2fc").place(x=160,y=450)
        cus_address = Entry(manage_cus_Frame1,width=50,bg="#FFFFFF")
        cus_address.place(x=160,y=475)

        Label(manage_cus_Frame1,text="หมายเลขโทรศัพท์",font="Calibri 12",bg="#e0f2fc").place(x=480,y=380)
        cus_phone = Entry(manage_cus_Frame1,width=21,bg="#FFFFFF")
        cus_phone.place(x=480,y=405)

        Label(manage_cus_Frame1,text="แก้ไขข้อมูลลูกค้า",font="Calibri 16 bold",bg="#e0f2fc").place(x=10,y=340)

        Label(manage_cus_Frame1,text="จัดการทะเบียนลูกค้า",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Button(manage_cus_Frame1,text="บันทึก",bg="#007bff",width=10,command=save_customer).place(x=540,y=540)
        Button(manage_cus_Frame1,text="ลบ",bg="#ff0000",width=10,command=delete_customer).place(x=700,y=540)
        Button(manage_cus_Frame1,image=img_search,command=search_customer).place(x=320,y=545)
    def manage_MatPur() :
        def show(self) :
            date.destroy
            emp.destroy
            mp_p.destroy
            s_name.destroy
            s_ph.destroy
            s_adr.destroy
            m_name.destroy
            m_amt.destroy
            m_dt.destroy

            selected_item = matPurchaseTable.selection()
            if selected_item:
                id = matPurchaseTable.item(selected_item)['values'][1]
                mat_id = id[7:14]
                sup_id = id[0:6]
                e_num = matPurchaseTable.item(selected_item)['values'][2]

                date.config(text=matPurchaseTable.item(selected_item)['values'][0])
                mp_p.config(text=matPurchaseTable.item(selected_item)['values'][3])

                cursor.execute('''select e_fname,e_lname from emp_acc
                where e_num = ?''',(e_num,))
                name = cursor.fetchone()
                emp.config(text=name[0]+" "+name[1])

                cursor.execute('''select * from supplier
                where sup_num = ?''',(sup_id,))
                sup = cursor.fetchone()
                s_name.config(text=sup[2])
                s_adr.config(text=sup[3])
                s_ph.config(text=sup[4])

                cursor.execute('''select * from material
                where mat_num = ?''',(mat_id,))
                mat = cursor.fetchone()
                m_name.config(text=mat[3])
                m_amt.config(text=mat[4])
                m_dt.config(text=mat[5])            
        def addMatPur() :
            mngFrame1.destroy()
            addFrame1 = Frame(root,bg="#e0f2fc")
            addFrame1.columnconfigure((0,1,2),weight=1)
            addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame1.configure(width=1000,height=700)
            addFrame1.place(x=200,y=0,width=1000,height=700)

            Label(addFrame1,text="รายละเอียดการสั่งซื้อวัตถุดิบ" ,bg="#e0f2fc",font="Calibri 20 bold").place(x=350,y=10)

            def today():
                matpur_date.delete(0,END)
                current_date = datetime.datetime.now()
                day = current_date.day
                month = datetime.datetime.now().strftime("%m")
                year = current_date.year
                matpur_date.insert(0,str(day)+"/"+str(month)+"/"+str(year))
            
            global matpur_date,e_num
            Label(addFrame1,text="วันที่สั่งซื้อ" ,bg="#e0f2fc").place(x=225,y=100)
            matpur_date = Entry(addFrame1,width=20)
            matpur_date.place(x=225,y=150)
            Button(addFrame1,text="วันนี้",width=10,bg="#FFFFFF",command=today).place(x=460,y=140)

            Label(addFrame1,text="รหัสพนักงาน" ,bg="#e0f2fc").place(x=225,y=200)
            e_num = Entry(addFrame1,width=20)
            e_num.place(x=225,y=250)

            def CheckNext() :
                mt_date,emp = matpur_date.get(),e_num.get()

                if mt_date:
                    if emp:
                        cursor.execute(''' select * from emp_acc
                        where e_num = ?''',(emp,))
                        result = cursor.fetchall()
                        if result:
                            addSup()
                        else:
                            messagebox.showwarning("System","ไม่พบ รหัสพนักงาน")
                    else:
                        messagebox.showwarning("System","กรุณากรอก รหัสพนักงานที่สั่งซื้อ")
                else:
                    messagebox.showwarning("System","กรุณากรอก วันที่")

            Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=CheckNext).place(x=700,y=350)
            Button(addFrame1,text="กลับ",width=10,bg="#808080",command=manage_MatPur).place(x=500,y=350)
        def addSup() :
            global addFrame1, supName, supAddr, supPH
            mngFrame1.destroy()
            addFrame1 = Frame(root,bg="#e0f2fc")
            addFrame1.columnconfigure((0,1,2),weight=1)
            addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame1.configure(width=1000,height=700)
            addFrame1.place(x=200,y=0,width=1000,height=700)
            
            Label(addFrame1,text="เพิ่มซัพพลายเออร์" ,bg="#e0f2fc",font="Calibri 20 bold").place(x=450,y=10)
            Label(addFrame1,text="ชื่อ" ,bg="#e0f2fc").place(x=225,y=50)

            global supName, supAddr
            supName = Entry(addFrame1,width=20)
            supName.place(x=225,y=100)
            supAddr = Entry(addFrame1,width=50)
            supPH = Entry(addFrame1,width=20)

            def check_sup2():
                supN,supA,supP = supName.get(),supAddr.get(),supPH.get()
                if supN:
                    if supN.isalpha():
                        if supA:
                            if supP:
                                if supP.isdigit():
                                    addMat()
                                else:
                                    messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์ เป็นตัวเลข")
                            else:
                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์ซัพพลายเออร์")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ที่อยู่ซัพพลายเออร์")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์ เป็นภาษาอังกฤษ")
                else:
                    messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์")

            def check_sup():
                global nextBt
                supN = supName.get()
                if supN:
                    if supN.isalpha():
                        cursor.execute(''' select * from supplier
                        where sup_name = ?''',(supN,))
                        result = cursor.fetchone()
                        if result:
                            addMat()
                        else:
                            checktBt.destroy()
                            nextBt = Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=check_sup2)
                            Label(addFrame1,text="ที่อยู่" ,bg="#e0f2fc").place(x=225,y=150)
                            Label(addFrame1,text="โทรศัพท์" ,bg="#e0f2fc").place(x=225,y=250)
                            nextBt.place(x=700,y=350)
                            supAddr.place(x=225,y=200)
                            supPH.place(x=225,y=300)
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์ เป็นภาษาอังกฤษ")
                else:
                    messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์")
                    
            checktBt = Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=check_sup)
            checktBt.place(x=700,y=350)

            Button(addFrame1,text="กลับ",width=10,bg="#808080",command=addMatPur).place(x=500,y=350)
        def addMat() :
            mngFrame1.destroy()
            addFrame1 = Frame(root,bg="#e0f2fc")
            addFrame1.columnconfigure((0,1,2),weight=1)
            addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame1.configure(width=1000,height=700)
            addFrame1.place(x=200,y=0,width=1000,height=700)
            
            Label(addFrame1,text="เพิ่มวัตถุดิบ",bg="#e0f2fc",font="Calibri 20 bold").place(x=450,y=10)

            Label(addFrame1,text="ชื่อ",bg="#e0f2fc").place(x=225,y=100)
            matName = Entry(addFrame1,width=20)
            matName.place(x=225,y=150)

            Label(addFrame1,text="จำนวน",bg="#e0f2fc").place(x=500,y=100)
            matAmt = Entry(addFrame1,width=20)
            matAmt.place(x=500,y=150)

            Label(addFrame1,text="ราคาวัตถุดิบต่อหน่วย",bg="#e0f2fc").place(x=225,y=200)
            mat_pr = Entry(addFrame1,width=20)
            mat_pr.place(x=225,y=250)
            
            matdt = Entry(addFrame1,width=20)

            def check_mat2() :
                mp_date,m_price,num = matpur_date.get(),mat_pr.get(),e_num.get()
                m_name,m_amt,m_dt = matName.get(),matAmt.get(),matdt.get()
                ans = messagebox.askquestion("System","คุณแน่ใจว่าต้องการเพิ่มข้อมูลการสั่งซื้อวัตถุดิบ ?")
                if ans == 'yes' :
                    if m_name:
                        if m_name.isalpha():
                            if m_amt:
                                if m_amt.isdigit():
                                    if m_price:
                                        if m_price.isdigit():
                                            if m_dt:
                                                ############ Supplier ################
                                                sup_name,sup_addr,sup_phone = supName.get(),supAddr.get(),supPH.get()
                                                sname_id = sup_name.upper()[0:3]
                                                sup_num = sname_id+"001"
                                                cursor.execute(''' select sup_num from supplier''')
                                                result = cursor.fetchall()
                                                all_sup_num = [t[0] for t in result]
                                                while sup_num in all_sup_num:
                                                    number = int(sup_num[3:6])
                                                    number+=1
                                                    if len(str(number)) == 1:
                                                        sup_num = sname_id+"00"+str(number)
                                                    elif len(str(number)) == 2:
                                                        sup_num = sname_id+"0"+str(number)
                                                    elif len(str(number)) == 3:
                                                        sup_num = sname_id+str(number)

                                                cursor.execute(''' select * from supplier
                                                where sup_name = ?''',(sup_name,))
                                                result = cursor.fetchone()
                                                if result:
                                                    sup_id = result[0]
                                                else:
                                                    cursor.execute(''' insert into supplier
                                                    values(NULL,?,?,?,?)''',(sup_num,sup_name,sup_addr,sup_phone,))
                                                    sup_id = cursor.lastrowid
                                                
                                                ############ Material ################
                                                cursor.execute('''select mat_num from material ''')
                                                result = cursor.fetchall()

                                                mname_id = m_name.upper()[0:3]
                                                mat_num = mname_id+"001"
                                                all_mat_num = [t[0] for t in result]
                                                while mat_num in all_mat_num:
                                                    number = int(mat_num[3:6])
                                                    number+=1
                                                    if len(str(number)) == 1:
                                                        mat_num = mname_id+"00"+str(number)
                                                    elif len(str(number)) == 2:
                                                        mat_num = mname_id+"0"+str(number)
                                                    elif len(str(number)) == 3:
                                                        mat_num = mname_id+str(number)

                                                cursor.execute('''insert into material
                                                values(NULL,?,?,?,?,?)''',(sup_id,mat_num,m_name,m_amt,m_dt))
                                                mat_id = cursor.lastrowid

                                                ############ Material Purchase ################
                                                cursor.execute('''insert into material_purchase
                                                values(?,?,?,?,?)''',(mp_date,mat_id,sup_id,num,m_price,))
                                                conn.commit()
                                                manage_MatPur()
                                            else:
                                                messagebox.showwarning("System","กรุณากรอก รายละเอียดวัตถุดิบ")
                                        else:
                                            messagebox.showwarning("System","กรุณากรอก ราคา เป็นตัวเลข")
                                    else:
                                        messagebox.showwarning("System","กรุณากรอก ราคาวัตถุดิบต่อหน่วย")
                                else:
                                    messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบ เป็นตัวเลข")
                            else:
                                messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบ")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ เป็นภาษาอังกฤษ")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ")

    
            nextBt = Button(addFrame1,text="บันทึก",command=check_mat2,width=10,bg="#FFFFFF")  
            
            def check_mat() :
                mp_date,m_price,num = matpur_date.get(),mat_pr.get(),e_num.get()
                m_name,m_amt = matName.get(),matAmt.get()
                if m_name:
                    if m_name.isalpha():
                        if m_amt:
                            if m_price:
                                if m_price.isdigit():
                                    cursor.execute(''' select * from material
                                    where mat_name = ?''',(m_name,))
                                    result = cursor.fetchone()
                                    if result:
                                        ans = messagebox.askquestion("System","คุณแน่ใจว่าต้องการเพิ่มข้อมูลการสั่งซื้อวัตถุดิบ ?")
                                        if ans == 'yes' :                   
                                            ############ Supplier ################
                                            sup_name,sup_addr,sup_phone = supName.get(),supAddr.get(),supPH.get()
                                            sname_id = sup_name.upper()[0:3]
                                            sup_num = sname_id+"001"
                                            cursor.execute(''' select sup_num from supplier''')
                                            result = cursor.fetchall()
                                            all_sup_num = [t[0] for t in result]
                                            while sup_num in all_sup_num:
                                                number = int(sup_num[3:6])
                                                number+=1
                                                if len(str(number)) == 1:
                                                    sup_num = sname_id+"00"+str(number)
                                                elif len(str(number)) == 2:
                                                    sup_num = sname_id+"0"+str(number)
                                                elif len(str(number)) == 3:
                                                    sup_num = sname_id+str(number)

                                            cursor.execute(''' select * from supplier
                                            where sup_name = ?''',(sup_name,))
                                            result = cursor.fetchone()
                                            if result:
                                                sup_id = result[0]
                                            else:
                                                cursor.execute(''' insert into supplier
                                                values(NULL,?,?,?,?)''',(sup_num,sup_name,sup_addr,sup_phone,))
                                                sup_id = cursor.lastrowid

                                            ############ Material ################
                                            cursor.execute(''' select mat_quantity from material
                                            where mat_name = ?''',(m_name,))
                                            result = cursor.fetchone()
                                            m_amt = matAmt.get()
                                            new_amt = int(result[0]) + int(m_amt)
                                            cursor.execute(''' update material
                                            set mat_quantity = ?
                                            where mat_name = ?''',(new_amt,m_name))
                                            cursor.execute(''' select * from material
                                            where mat_name = ?''',(m_name,))
                                            result = cursor.fetchone()
                                            mat_id = result[0]
                                            
                                            ############ Material Purchase ################
                                            cursor.execute('''insert into material_purchase
                                            values(?,?,?,?,?)''',(mp_date,mat_id,sup_id,num,m_price,))
                                            conn.commit()
                                            manage_MatPur()
                                    else:
                                        check_bt.destroy()
                                        Label(addFrame1,text="รายละเอียด",bg="#e0f2fc").place(x=500,y=200)
                                        matdt.place(x=500,y=250)
                                        nextBt.place(x=700,y=350)
                                else:
                                    messagebox.showwarning("System","กรุณากรอก ราคา เป็นตัวเลข")
                            else:
                                messagebox.showwarning("System","กรุณากรอก ราคาวัตถุดิบต่อหน่วย")
                        else:
                            messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบ")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ เป็นภาษาอังกฤษ")
                else:
                    messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ")

            check_bt = Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=check_mat)
            check_bt.place(x=700,y=350)

            Button(addFrame1,text="กลับ",width=10,bg="#808080",command=addSup).place(x=500,y=350)           
        def deleteMP() : 
            ans = messagebox.askquestion("System", "คุณแน่ใจว่าต้องการลบรายการสั่งซื้อวัตถดิบนี้ ?")
            selMP = matPurchaseTable.item(matPurchaseTable.focus(), 'values')
            if selMP:
                if ans == 'yes' :
                    cursor.execute(''' select mat_id from material
                    where mat_num = ?''',(selMP[1],))
                    mat_id = cursor.fetchone()
                    
                    cursor.execute(''' select sup_id from supplier
                    where sup_num = ?''',(selMP[2],))
                    sup_id = cursor.fetchone()

                    cursor.execute(''' delete from material_purchase
                    where mat_date=? AND mat_id=? AND sup_id=? AND e_num=? AND mat_price=?
                    ''',(selMP[0],mat_id[0],sup_id[0],selMP[3],selMP[4],))
                    
                    conn.commit()
                    manage_MatPur()
            else:
                messagebox.showwarning("System","กรุณากรอก เลือกรายการสั่งซื้อที่ต้องการลบ")
        def searchMP() : 
            searchMP = seachEntry.get()
            matPurchaseTable.delete(*matPurchaseTable.get_children())
            if searchMP:
                sql = '''SELECT * FROM material_purchase WHERE mat_date=?'''
                cursor.execute(sql,(searchMP,))
                MatPur = cursor.fetchall()
                if MatPur:
                    cursor.execute(''' select mat_num from material''')
                    Mat = cursor.fetchone()
                
                    for i,data1 in enumerate(MatPur):
                        
                        cursor.execute(''' select mat_num from material
                        where mat_id = ?''',(data1[1],))
                        Mat = cursor.fetchone()

                        cursor.execute(''' select sup_num from supplier
                        where sup_id = ?''',(data1[2],))
                        Sup = cursor.fetchone()

                        matPurchaseTable.insert("","end",values=(data1[0],Sup[0]+"-"+Mat[0],data1[3],data1[4]))
                else:
                    messagebox.showwarning("System","ไม่พบวันที่สั่งซื้อสินค้า")
                    seachEntry.delete(0,END)
            else:
                messagebox.showwarning("System","กรุณากรอก วันที่สั่งซื้อสินค้า")
                manage_MatPur()

        global searchEntry,selSearch,matPurchaseTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        matPurchaseTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5"),selectmode=BROWSE)
        matPurchaseTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        matPurchaseTable.bind('<<TreeviewSelect>>',show)

        matPurchaseTable.heading('col1', text="วันที่สั่งซื้อ", anchor=W)
        matPurchaseTable.heading('col2', text="รหัสการสั่งซื้อ", anchor=W)
        matPurchaseTable.heading('col3', text="รหัสพนักงาน", anchor=W)
        matPurchaseTable.heading('col4', text="ราคาวัตถุดิบ", anchor=W)

        matPurchaseTable.column('col1',anchor=W, width=200)
        matPurchaseTable.column('col2',anchor=W, width=200)
        matPurchaseTable.column('col3',anchor=W, width=200)
        matPurchaseTable.column('col4',anchor=W, width=200)
        matPurchaseTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngMatPur()

        # Add / Delete / Edit
        Label(mngFrame1,text="ค้นหา วันที่สั่งซื้อ :",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=E)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=20)
        seachEntry.grid(row=8,column=1,sticky=W)

        Label(mngFrame1,text="วันที่สั่งซื้อ",font="Calibri 12",bg="#e0f2fc").place(x=110,y=335)
        date = Label(mngFrame1,width=15,bg="#FFFFFF")
        date.place(x=110,y=360)

        Label(mngFrame1,text="ชื่อพนักงานที่สั่งซื้อ",font="Calibri 12",bg="#e0f2fc").place(x=300,y=335)
        emp = Label(mngFrame1,width=20,bg="#FFFFFF")
        emp.place(x=300,y=360)

        Label(mngFrame1,text="ราคาวัตถุดิบ/หน่วย",font="Calibri 12",bg="#e0f2fc").place(x=550,y=335)
        mp_p = Label(mngFrame1,width=15,bg="#FFFFFF")
        mp_p.place(x=550,y=360)
        #############################################
        Label(mngFrame1,text="ชื่อ ซัพพลายเออร์",font="Calibri 12",bg="#e0f2fc").place(x=20,y=395)
        s_name = Label(mngFrame1,width=15,bg="#FFFFFF")
        s_name.place(x=20,y=420)

        Label(mngFrame1,text="ที่อยู่",font="Calibri 12",bg="#e0f2fc").place(x=200,y=395)
        s_adr = Label(mngFrame1,font="Calibri 13 bold",width=67,bg="#FFFFFF")
        s_adr.place(x=200,y=423)

        Label(mngFrame1,text="หมายเลขโทรศัพท์",font="Calibri 12",bg="#e0f2fc").place(x=820,y=395)
        s_ph = Label(mngFrame1,width=15,bg="#FFFFFF")
        s_ph.place(x=820,y=420)
        #############################################
        
        Label(mngFrame1,text="ชื่อ วัตถุดิบ",font="Calibri 12",bg="#e0f2fc").place(x=20,y=455)
        m_name = Label(mngFrame1,width=20,bg="#FFFFFF")
        m_name.place(x=20,y=480)

        Label(mngFrame1,text="จำนวน ปัจจุบัน",font="Calibri 12",bg="#e0f2fc").place(x=255,y=455)
        m_amt = Label(mngFrame1,width=10,bg="#FFFFFF")
        m_amt.place(x=255,y=480)

        Label(mngFrame1,text="รายละเอียด",font="Calibri 12",bg="#e0f2fc").place(x=380,y=455)
        m_dt = Label(mngFrame1,width=40,bg="#FFFFFF")
        m_dt.place(x=380,y=480)

        Label(mngFrame1,text="จัดการรายการสั่งซื้อวัตถุดิบ",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Button(mngFrame1,text="เพิ่ม",width=10,bg='#00cc66',command=addMatPur).grid(row=8,column=4,sticky="e",pady=20)
        Button(mngFrame1,text="ลบ",width=10,bg='#ff0000',command=deleteMP).grid(row=8,column=5,sticky="e",pady=20)
        Button(mngFrame1,image=img_search,command=searchMP).place(x=565,y=538)
    def order_report() :
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)
        
        Label(mngFrame1,text="สรุปยอดขายต่อเดือน",font="Calibri 20 bold",bg="#e0f2fc").place(x=380,y=20)
        month_entry = Entry(mngFrame1,width=20)
        month_entry.place(x=380,y=100)
        
        def month_sum() :
            month = month_entry.get()
            if month:
                cursor.execute(''' select date_time,pd_cap,order_quantity,order_total
                from "order" ''')
                result = cursor.fetchall()

                only_month = [item for item in result if item[0].split('/')[1] == "0"+str(month)]
                cap1,cap2,cap3 = 0,0,0
                for item in only_month:
                    if item[1] == 350:
                        cap1 += item[2]
                    if item[1] == 600:
                        cap2 += item[2]
                    if item[1] == 1500:
                        cap3 += item[2]
                
                cursor.execute(''' select pd_price from product''')
                pd_price = cursor.fetchall()
                t1,t2,t3 = cap1*pd_price[0][0],cap2*pd_price[1][0],cap3*pd_price[2][0]
                sum = t1+t2+t3

                report_table = ttk.Treeview(mngFrame1, columns=("col1","col2","col3"))
                report_table.grid(row=4, column=3, columnspan=5, padx=20, pady=10, ipadx=280, ipady=40)

                total = Label(mngFrame1,text="ยอดขายรวม {} บาท".format(sum),font="Calibri 22 bold",bg="#e0f2fc")
                total.grid(row=5,column=5,ipadx=30)

                report_table.heading("col1", text='ความจุ', anchor=N)
                report_table.heading("col2", text='จำนวน', anchor=N)
                report_table.heading("col3", text='รวม', anchor=N)

                report_table.column('col1', width=100, anchor="w")
                report_table.column('col2', width=100, anchor="center")
                report_table.column('col3', width=100, anchor="w")

                report_table.column('#0', width=0, minwidth=0)

                report_table.delete(*report_table.get_children())

                report_table.insert("","end",values=("350",cap1,t1))
                report_table.insert("","end",values=("500",cap2,t2))
                report_table.insert("","end",values=("1500",cap3,t3))
            else:
                messagebox.showwarning("System","กรุณากรอกเดือนที่ต้องการสรุปยอด\nกรุณากรอกเป็นเลขจำนวนเต็ม เช่น 1 - 12")

        Label(mngFrame1,text="เดือนที่ต้องการสรุป",font="Calibri 16 bold",bg="#e0f2fc").place(x=195,y=100)
        month_input = Button(mngFrame1,text="สรุป",command=month_sum)
        month_input.place(x=610,y=90)
        
    mngFrame1 = Frame(root,bg="#e0f2fc")
    mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
    mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
    mngFrame1.configure(width=1000,height=700)

    manage_cus_Frame1 = Frame(root,bg="#e0f2fc")
    manage_cus_Frame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
    manage_cus_Frame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
    manage_cus_Frame1.configure(width=1000,height=700)

    ######### Frame Menu ###########
    loginFrame.destroy()
    homeFrame1 = Frame(root,bg="#227aa9")
    homeFrame1.configure(width=200, height=700)
    homeFrame1.columnconfigure((0),weight=1)
    homeFrame1.rowconfigure((0,1,2,3,4,5,6,7,8),weight=1)
    homeFrame1.place(x=0,y=0,width=200,height=700)

    # Left Side Button Menu #
    Button(homeFrame1,text = "จัดการบัญชีผู้ใช้งาน", command = manage_account, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=0,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการคลังสินค้า", command = manage_product, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=1,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการคลังวัตถุดิบ", command = manage_material, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=2,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการทะเบียน\nตัวแทนจำหน่าย", command = manage_agent, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=3,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการทะเบียนลูกค้า", command = manage_customer, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=4,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการรายการ\nสั่งซื้อวัตถุดิบ", command = manage_MatPur, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=5,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดพิมพ์รายงาน\nเเสดงผลการดำเนินงาน", command = order_report, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=6,sticky="ew",pady=10,padx=5,ipady=10)
    
    ######### Frame window ##########
    mainFrame1 = Frame(root,bg="#e0f2fc")
    mainFrame1.columnconfigure((0,1,2),weight=1)
    mainFrame1.rowconfigure((0,1,2,3,4),weight=1)
    mainFrame1.configure(width=1000,height=700)
    mainFrame1.place(x=200,y=0,width=1000,height=700)

    # Pull name From Database #
    sql = "SELECT e_fname,e_lname FROM emp_acc WHERE e_num=?"
    cursor.execute(sql,[user])
    name_ = cursor.fetchone()
    name = name_[0]+" "+name_[1]

    # Label Profile
    Label(mainFrame1,bg="#e0f2fc",image=img_profile).grid(column=1,row=1,ipadx=380,ipady=100,sticky='s')
    Label(mainFrame1,text="Welcome, "+name,bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").grid(column=1,row=2,ipady=10,sticky="n")
    Label(mainFrame1,text="Position : Admin",bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").grid(column=1,row=3,ipady=10,sticky="n")
    Label(mainFrame1,text="",bg="#e0f2fc",fg="#e0f2fc").grid(column=1,row=4,ipady=80,sticky="n")

def homepageI() : 
    def manage_product() :
        def edit(self) :
            pd_cap.destroy
            pd_price.destroy
            pd_quantity.destroy

            global selected_item
            selected_item = productTable.selection()
            if selected_item:
                pd_cap.config(text=productTable.item(selected_item)['values'][0])
                pd_price.config(text=productTable.item(selected_item)['values'][1])
                pd_quantity.config(text=productTable.item(selected_item)['values'][2])
        def addBtn() :
            old_amt = pd_quantity.cget("text")
            new_amt = new_quantity.get()
            cap = pd_cap.cget("text")
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าจะ เพิ่มจำนวนสินค้า ?")     
            if ans == 'yes' :
                if new_amt:
                    try:
                        ckint = int(new_amt)
                        if int(new_amt) < 0:
                            messagebox.showwarning("System", "กรุณาใส่ตัวเลขจำนวนเต็ม")
                        else:
                            amt = int(old_amt) + int(new_amt)
                            cursor.execute(''' update product
                            set pd_quantity = ?
                            where pd_cap = ?''',(amt,cap,))
                            conn.commit()
                            pd_cap.config(text='')
                            pd_price.config(text='')
                            pd_quantity.config(text='')
                    except ValueError:
                        messagebox.showwarning("System", "กรุณาใส่ตัวเลข")
                else:
                    messagebox.showwarning("System", "กรุณาใส่จำนวนสินค้าที่การเพิ่ม")
            new_quantity.delete(0,END) 
            
            productTable.delete(*productTable.get_children())
            fetchTreeForMngPD()
        def deleBtn() :
            old_amt = pd_quantity.cget("text")
            new_amt = new_quantity.get()
            cap = pd_cap.cget("text")
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าจะ ลดจำนวนสินค้า ?")
            if ans == 'yes' :
                if new_amt:
                    try:
                        ckint = int(new_amt)
                        if int(new_amt) < 0:
                            messagebox.showwarning("System", "กรุณาใส่ตัวเลขจำนวนเต็ม")
                        else:
                            if int(new_amt) <= int(old_amt):
                                amt = int(old_amt) - int(new_amt)
                                cursor.execute(''' update product
                                set pd_quantity = ?
                                where pd_cap = ?''',(amt,cap,))
                                conn.commit()
                                pd_cap.config(text='')
                                pd_price.config(text='')
                                pd_quantity.config(text='')
                                   
                            else:
                                messagebox.showwarning("System", "กรุณาใส่จำนวนสินค้าให้ถูกต้อง")
                    except ValueError:
                        messagebox.showwarning("System", "กรุณาใส่ตัวเลข")
                else:
                    messagebox.showwarning("System", "กรุณาใส่จำนวนสินค้าที่การลด")
            productTable.delete(*productTable.get_children())
            fetchTreeForMngPD()
            new_quantity.delete(0,END)

        global searchEntry,selSearch,productTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        productTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5"),selectmode=BROWSE)
        productTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        productTable.bind('<<TreeviewSelect>>',edit)

        productTable.heading('col1', text="ขนาด", anchor=W)
        productTable.heading('col2', text="ราคา", anchor=W)
        productTable.heading('col3', text="จำนวน", anchor=W)

        productTable.column('col1',anchor=W, width=60)
        productTable.column('col2',anchor=W, width=60)
        productTable.column('col3',anchor=W, width=80)
        productTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngPD()

        Label(mngFrame1,text="แก้ไขจำนวนสินค้า",font="Calibri 16 bold",bg="#e0f2fc").grid(row=2,column=1,sticky=SW)

        # Add / Delete / Edit
        Label(mngFrame1,text="ขนาด/ขวด",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=2,sticky=SW)
        pd_cap = Label(mngFrame1,width=10,bg="#FFFFFF")
        pd_cap.grid(row=4,column=2,sticky=NW,padx=10)

        Label(mngFrame1,text="ราคา/แพ็ค",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=3,sticky=SW)
        pd_price = Label(mngFrame1,width=10,bg="#FFFFFF")
        pd_price.grid(row=4,column=3,sticky=NW,padx=10)

        Label(mngFrame1,text="จำนวน/แพ็ค",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=4,sticky=SW)
        pd_quantity = Label(mngFrame1,width=10,bg="#FFFFFF")
        pd_quantity.grid(row=4,column=4,sticky=NW,padx=10)

        Label(mngFrame1,text="เพิ่ม/ลบ จำนวนสินค้า",font="Calibri 12",bg="#e0f2fc").grid(row=3,column=5,sticky=SW)
        new_quantity = Entry(mngFrame1,width=10,bg="#FFFFFF")
        new_quantity.grid(row=4,column=5,sticky=NW,padx=10)

        Label(mngFrame1,text="จัดการคลังสินค้า",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=1)
        Button(mngFrame1,text="เพิ่ม",width=10,bg="#00cc66",command=addBtn).grid(row=8,column=4)
        Button(mngFrame1,text="ลบ",width=10,bg="#ff0000",command=deleBtn).grid(row=8,column=5)
    def manage_material() :
        def deleteMT() :
            selected_item = MatTable.selection()
            if selected_item:
                mat_id = MatTable.item(selected_item)['values'][0]
            old_amt,new_amt = quanMat.cget('text'),newquna.get()
            ans = messagebox.askquestion("System","คุณแน่ใจหรือว่าต้องการลบจำนวนวัตถุดิบนี้")
            if ans == 'yes' :
                if old_amt:
                    if new_amt:
                        if new_amt.isdigit():
                            if float(new_amt) > 0:
                                if int(new_amt) < int(old_amt):
                                    amt = int(old_amt) - int(new_amt)
                                    cursor.execute(''' update material
                                    set mat_quantity = ?
                                    where mat_num = ?''',(amt,mat_id,))
                                    conn.commit()
                                    MatTable.delete(*MatTable.get_children())
                                    fetchTreeForMngMat()
                                else:
                                    messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบให้ถูกต้อง")
                                    newquna.delete(0,END)
                            else:
                                messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบเป็นเลขบวก")
                        else:
                            messagebox.showwarning("System","กรุณากรอก เป็นตัวเลข")
                            newquna.delete(0,END)
                    else:
                        messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบที่ต้องการลบ")
                else:
                    messagebox.showwarning("System","กรุณาเลือก วัตถุดิบที่ต้องการลบ")
        def searchMat() : 
            searchMat = seachEntry.get()
            sql = "SELECT * FROM material WHERE mat_num=?"
            cursor.execute(sql,(searchMat,))
            result = cursor.fetchall()
            if searchMat:
                if result:
                    for i,data1 in enumerate(result):
                        MatTable.delete(*MatTable.get_children())
                        MatTable.insert("","end",values=(data1[2],data1[3],data1[4],data1[5]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสวัตถุดิบ")
                    fetchTreeForMngMat()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสวัตถุดิบที่ต้องการค้นหา")
                fetchTreeForMngMat()
        def edit(self) :
            mat_id.destroy
            mat_name.destroy
            quanMat.destroy
            datails.destroy

            selected_item = MatTable.selection()
            if selected_item:
                mat_id.config(text=MatTable.item(selected_item)['values'][0])
                mat_name.config(text=MatTable.item(selected_item)['values'][1])
                quanMat.config(text=MatTable.item(selected_item)['values'][2])
                datails.config(text=MatTable.item(selected_item)['values'][3])

        global searchEntry,selSearch,MatTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        MatTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5"),selectmode=BROWSE)
        MatTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        MatTable.bind('<<TreeviewSelect>>',edit)

        MatTable.heading('col1', text="รหัสวัตถุดิบ", anchor=W)
        MatTable.heading('col2', text="ชื่อ", anchor=W)
        MatTable.heading('col3', text="จำนวน", anchor=W)
        MatTable.heading('col4', text="รายละเอียด", anchor=W)

        MatTable.column('col1',anchor=W, width=150)
        MatTable.column('col2',anchor=W, width=150)
        MatTable.column('col3',anchor=W, width=150)
        MatTable.column('col4',anchor=W, width=280)
        MatTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngMat()

        # Search Box
        Label(mngFrame1,text="ค้นหา รหัสวัตถุดิบ",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=E,padx=10,pady=20)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=15)
        seachEntry.grid(row=8,column=1,sticky=W,padx=5,pady=20)

        # Add / Delete / Edit
        Label(mngFrame1,text="รหัสวัตถุดิบ",font="Calibri 12",bg="#e0f2fc").place(x=140,y=385)
        mat_id = Label(mngFrame1,width=10,bg="#FFFFFF")
        mat_id.place(x=140,y=410)

        Label(mngFrame1,text="ชื่อ",font="Calibri 12",bg="#e0f2fc").place(x=280,y=385)
        mat_name = Label(mngFrame1,width=30,bg="#FFFFFF")
        mat_name.place(x=280,y=410)
        
        Label(mngFrame1,text="จำนวน",font="Calibri 12",bg="#e0f2fc").place(x=640,y=385)
        quanMat = Label(mngFrame1,width=10,bg="#FFFFFF")
        quanMat.place(x=640,y=410)

        Label(mngFrame1,text="รายละเอียด",font="Calibri 12",bg="#e0f2fc").place(x=140,y=450)
        datails = Label(mngFrame1,bg="#FFFFFF",width=50)
        datails.place(x=140,y=475)

        Label(mngFrame1,text="เพิ่ม/ลดจำนวนวัตถุดิบ",font="Calibri 12",bg="#e0f2fc").place(x=780,y=385)
        newquna = Entry(mngFrame1,width=13,bg="#FFFFFF")
        newquna.place(x=780,y=410)
        
        Label(mngFrame1,text="จัดการคลังวัตถุดิบ",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Label(mngFrame1,text="แก้ไขจำนวนวัตถุดิบ",font="Calibri 16 bold",bg="#e0f2fc").place(x=13,y=340)
        
        Button(mngFrame1,text="ลบ",width=10,bg="#ff0000",command=deleteMT).place(x=795,y=445)
        Button(mngFrame1,image=img_search,command=searchMat).place(x=449,y=545)
    def manage_MatPur() :
        def show(self) :
            date.destroy
            emp.destroy
            mp_p.destroy
            s_name.destroy
            s_ph.destroy
            s_adr.destroy
            m_name.destroy
            m_amt.destroy
            m_dt.destroy

            selected_item = matPurchaseTable.selection()
            if selected_item:
                id = matPurchaseTable.item(selected_item)['values'][1]
                mat_id = id[7:14]
                sup_id = id[0:6]
                e_num = matPurchaseTable.item(selected_item)['values'][2]

                date.config(text=matPurchaseTable.item(selected_item)['values'][0])
                mp_p.config(text=matPurchaseTable.item(selected_item)['values'][3])

                cursor.execute('''select e_fname,e_lname from emp_acc
                where e_num = ?''',(e_num,))
                name = cursor.fetchone()
                emp.config(text=name[0]+" "+name[1])

                cursor.execute('''select * from supplier
                where sup_num = ?''',(sup_id,))
                sup = cursor.fetchone()
                s_name.config(text=sup[2])
                s_adr.config(text=sup[3])
                s_ph.config(text=sup[4])

                cursor.execute('''select * from material
                where mat_num = ?''',(mat_id,))
                mat = cursor.fetchone()
                m_name.config(text=mat[3])
                m_amt.config(text=mat[4])
                m_dt.config(text=mat[5])            
        def addMatPur() :
            mngFrame1.destroy()
            addFrame1 = Frame(root,bg="#e0f2fc")
            addFrame1.columnconfigure((0,1,2),weight=1)
            addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame1.configure(width=1000,height=700)
            addFrame1.place(x=200,y=0,width=1000,height=700)

            Label(addFrame1,text="รายละเอียดการสั่งซื้อวัตถุดิบ" ,bg="#e0f2fc",font="Calibri 20 bold").place(x=350,y=10)

            def today():
                matpur_date.delete(0,END)
                current_date = datetime.datetime.now()
                day = current_date.day
                month = datetime.datetime.now().strftime("%m")
                year = current_date.year
                matpur_date.insert(0,str(day)+"/"+str(month)+"/"+str(year))
            
            global matpur_date,e_num
            Label(addFrame1,text="วันที่สั่งซื้อ" ,bg="#e0f2fc").place(x=225,y=100)
            matpur_date = Entry(addFrame1,width=20)
            matpur_date.place(x=225,y=150)
            Button(addFrame1,text="วันนี้",width=10,bg="#FFFFFF",command=today).place(x=460,y=140)

            Label(addFrame1,text="รหัสพนักงาน" ,bg="#e0f2fc").place(x=225,y=200)
            e_num = Entry(addFrame1,width=20)
            e_num.place(x=225,y=250)

            def CheckNext() :
                mt_date,emp = matpur_date.get(),e_num.get()

                if mt_date:
                    if emp:
                        cursor.execute(''' select * from emp_acc
                        where e_num = ?''',(emp,))
                        result = cursor.fetchall()
                        if result:
                            addSup()
                        else:
                            messagebox.showwarning("System","ไม่พบ รหัสพนักงาน")
                    else:
                        messagebox.showwarning("System","กรุณากรอก รหัสพนักงานที่สั่งซื้อ")
                else:
                    messagebox.showwarning("System","กรุณากรอก วันที่")

            Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=CheckNext).place(x=700,y=350)
            Button(addFrame1,text="กลับ",width=10,bg="#808080",command=manage_MatPur).place(x=500,y=350)
        def addSup() :
            global addFrame1, supName, supAddr, supPH
            mngFrame1.destroy()
            addFrame1 = Frame(root,bg="#e0f2fc")
            addFrame1.columnconfigure((0,1,2),weight=1)
            addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame1.configure(width=1000,height=700)
            addFrame1.place(x=200,y=0,width=1000,height=700)
            
            Label(addFrame1,text="เพิ่มซัพพลายเออร์" ,bg="#e0f2fc",font="Calibri 20 bold").place(x=450,y=10)
            Label(addFrame1,text="ชื่อ" ,bg="#e0f2fc").place(x=225,y=50)

            global supName, supAddr
            supName = Entry(addFrame1,width=20)
            supName.place(x=225,y=100)
            supAddr = Entry(addFrame1,width=50)
            supPH = Entry(addFrame1,width=20)

            def check_sup2():
                supN,supA,supP = supName.get(),supAddr.get(),supPH.get()
                if supN:
                    if supN.isalpha():
                        if supA:
                            if supP:
                                if supP.isdigit():
                                    addMat()
                                else:
                                    messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์ เป็นตัวเลข")
                            else:
                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์ซัพพลายเออร์")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ที่อยู่ซัพพลายเออร์")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์ เป็นภาษาอังกฤษ")
                else:
                    messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์")

            def check_sup():
                global nextBt
                supN = supName.get()
                if supN:
                    if supN.isalpha():
                        cursor.execute(''' select * from supplier
                        where sup_name = ?''',(supN,))
                        result = cursor.fetchone()
                        if result:
                            addMat()
                        else:
                            checktBt.destroy()
                            nextBt = Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=check_sup2)
                            Label(addFrame1,text="ที่อยู่" ,bg="#e0f2fc").place(x=225,y=150)
                            Label(addFrame1,text="โทรศัพท์" ,bg="#e0f2fc").place(x=225,y=250)
                            nextBt.place(x=700,y=350)
                            supAddr.place(x=225,y=200)
                            supPH.place(x=225,y=300)
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์ เป็นภาษาอังกฤษ")
                else:
                    messagebox.showwarning("System","กรุณากรอก ชื่อซัพพลายเออร์")
                    
            checktBt = Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=check_sup)
            checktBt.place(x=700,y=350)

            Button(addFrame1,text="กลับ",width=10,bg="#808080",command=addMatPur).place(x=500,y=350)
        def addMat() :
            mngFrame1.destroy()
            addFrame1 = Frame(root,bg="#e0f2fc")
            addFrame1.columnconfigure((0,1,2),weight=1)
            addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame1.configure(width=1000,height=700)
            addFrame1.place(x=200,y=0,width=1000,height=700)
            
            Label(addFrame1,text="เพิ่มวัตถุดิบ",bg="#e0f2fc",font="Calibri 20 bold").place(x=450,y=10)

            Label(addFrame1,text="ชื่อ",bg="#e0f2fc").place(x=225,y=100)
            matName = Entry(addFrame1,width=20)
            matName.place(x=225,y=150)

            Label(addFrame1,text="จำนวน",bg="#e0f2fc").place(x=500,y=100)
            matAmt = Entry(addFrame1,width=20)
            matAmt.place(x=500,y=150)

            Label(addFrame1,text="ราคาวัตถุดิบต่อหน่วย",bg="#e0f2fc").place(x=225,y=200)
            mat_pr = Entry(addFrame1,width=20)
            mat_pr.place(x=225,y=250)
            
            matdt = Entry(addFrame1,width=20)

            def check_mat2() :
                mp_date,m_price,num = matpur_date.get(),mat_pr.get(),e_num.get()
                m_name,m_amt,m_dt = matName.get(),matAmt.get(),matdt.get()
                ans = messagebox.askquestion("System","คุณแน่ใจว่าต้องการเพิ่มข้อมูลการสั่งซื้อวัตถุดิบ ?")
                if ans == 'yes' :
                    if m_name:
                        if m_name.isalpha():
                            if m_amt:
                                if m_amt.isdigit():
                                    if m_price:
                                        if m_price.isdigit():
                                            if m_dt:
                                                ############ Supplier ################
                                                sup_name,sup_addr,sup_phone = supName.get(),supAddr.get(),supPH.get()
                                                sname_id = sup_name.upper()[0:3]
                                                sup_num = sname_id+"001"
                                                cursor.execute(''' select sup_num from supplier''')
                                                result = cursor.fetchall()
                                                all_sup_num = [t[0] for t in result]
                                                while sup_num in all_sup_num:
                                                    number = int(sup_num[3:6])
                                                    number+=1
                                                    if len(str(number)) == 1:
                                                        sup_num = sname_id+"00"+str(number)
                                                    elif len(str(number)) == 2:
                                                        sup_num = sname_id+"0"+str(number)
                                                    elif len(str(number)) == 3:
                                                        sup_num = sname_id+str(number)

                                                cursor.execute(''' select * from supplier
                                                where sup_name = ?''',(sup_name,))
                                                result = cursor.fetchone()
                                                if result:
                                                    sup_id = result[0]
                                                else:
                                                    cursor.execute(''' insert into supplier
                                                    values(NULL,?,?,?,?)''',(sup_num,sup_name,sup_addr,sup_phone,))
                                                    sup_id = cursor.lastrowid
                                                
                                                ############ Material ################
                                                cursor.execute('''select mat_num from material ''')
                                                result = cursor.fetchall()

                                                mname_id = m_name.upper()[0:3]
                                                mat_num = mname_id+"001"
                                                all_mat_num = [t[0] for t in result]
                                                while mat_num in all_mat_num:
                                                    number = int(mat_num[3:6])
                                                    number+=1
                                                    if len(str(number)) == 1:
                                                        mat_num = mname_id+"00"+str(number)
                                                    elif len(str(number)) == 2:
                                                        mat_num = mname_id+"0"+str(number)
                                                    elif len(str(number)) == 3:
                                                        mat_num = mname_id+str(number)

                                                cursor.execute('''insert into material
                                                values(NULL,?,?,?,?,?)''',(sup_id,mat_num,m_name,m_amt,m_dt))
                                                mat_id = cursor.lastrowid

                                                ############ Material Purchase ################
                                                cursor.execute('''insert into material_purchase
                                                values(?,?,?,?,?)''',(mp_date,mat_id,sup_id,num,m_price,))
                                                conn.commit()
                                                manage_MatPur()
                                            else:
                                                messagebox.showwarning("System","กรุณากรอก รายละเอียดวัตถุดิบ")
                                        else:
                                            messagebox.showwarning("System","กรุณากรอก ราคา เป็นตัวเลข")
                                    else:
                                        messagebox.showwarning("System","กรุณากรอก ราคาวัตถุดิบต่อหน่วย")
                                else:
                                    messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบ เป็นตัวเลข")
                            else:
                                messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบ")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ เป็นภาษาอังกฤษ")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ")

    
            nextBt = Button(addFrame1,text="บันทึก",command=check_mat2,width=10,bg="#FFFFFF")  
            
            def check_mat() :
                mp_date,m_price,num = matpur_date.get(),mat_pr.get(),e_num.get()
                m_name,m_amt = matName.get(),matAmt.get()
                if m_name:
                    if m_name.isalpha():
                        if m_amt:
                            if m_price:
                                if m_price.isdigit():
                                    cursor.execute(''' select * from material
                                    where mat_name = ?''',(m_name,))
                                    result = cursor.fetchone()
                                    if result:
                                        ans = messagebox.askquestion("System","คุณแน่ใจว่าต้องการเพิ่มข้อมูลการสั่งซื้อวัตถุดิบ ?")
                                        if ans == 'yes' :                   
                                            ############ Supplier ################
                                            sup_name,sup_addr,sup_phone = supName.get(),supAddr.get(),supPH.get()
                                            sname_id = sup_name.upper()[0:3]
                                            sup_num = sname_id+"001"
                                            cursor.execute(''' select sup_num from supplier''')
                                            result = cursor.fetchall()
                                            all_sup_num = [t[0] for t in result]
                                            while sup_num in all_sup_num:
                                                number = int(sup_num[3:6])
                                                number+=1
                                                if len(str(number)) == 1:
                                                    sup_num = sname_id+"00"+str(number)
                                                elif len(str(number)) == 2:
                                                    sup_num = sname_id+"0"+str(number)
                                                elif len(str(number)) == 3:
                                                    sup_num = sname_id+str(number)

                                            cursor.execute(''' select * from supplier
                                            where sup_name = ?''',(sup_name,))
                                            result = cursor.fetchone()
                                            if result:
                                                sup_id = result[0]
                                            else:
                                                cursor.execute(''' insert into supplier
                                                values(NULL,?,?,?,?)''',(sup_num,sup_name,sup_addr,sup_phone,))
                                                sup_id = cursor.lastrowid

                                            ############ Material ################
                                            cursor.execute(''' select mat_quantity from material
                                            where mat_name = ?''',(m_name,))
                                            result = cursor.fetchone()
                                            m_amt = matAmt.get()
                                            new_amt = int(result[0]) + int(m_amt)
                                            cursor.execute(''' update material
                                            set mat_quantity = ?
                                            where mat_name = ?''',(new_amt,m_name))
                                            cursor.execute(''' select * from material
                                            where mat_name = ?''',(m_name,))
                                            result = cursor.fetchone()
                                            mat_id = result[0]
                                            
                                            ############ Material Purchase ################
                                            cursor.execute('''insert into material_purchase
                                            values(?,?,?,?,?)''',(mp_date,mat_id,sup_id,num,m_price,))
                                            conn.commit()
                                            manage_MatPur()
                                    else:
                                        check_bt.destroy()
                                        Label(addFrame1,text="รายละเอียด",bg="#e0f2fc").place(x=500,y=200)
                                        matdt.place(x=500,y=250)
                                        nextBt.place(x=700,y=350)
                                else:
                                    messagebox.showwarning("System","กรุณากรอก ราคา เป็นตัวเลข")
                            else:
                                messagebox.showwarning("System","กรุณากรอก ราคาวัตถุดิบต่อหน่วย")
                        else:
                            messagebox.showwarning("System","กรุณากรอก จำนวนวัตถุดิบ")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ เป็นภาษาอังกฤษ")
                else:
                    messagebox.showwarning("System","กรุณากรอก ชื่อวัตถุดิบ")

            check_bt = Button(addFrame1,text="ต่อไป",width=10,bg="#FFFFFF",command=check_mat)
            check_bt.place(x=700,y=350)

            Button(addFrame1,text="กลับ",width=10,bg="#808080",command=addSup).place(x=500,y=350)           
        def deleteMP() : 
            ans = messagebox.askquestion("System", "คุณแน่ใจว่าต้องการลบรายการสั่งซื้อวัตถดิบนี้ ?")
            selMP = matPurchaseTable.item(matPurchaseTable.focus(), 'values')
            if selMP:
                if ans == 'yes' :
                    cursor.execute(''' select mat_id from material
                    where mat_num = ?''',(selMP[1],))
                    mat_id = cursor.fetchone()
                    
                    cursor.execute(''' select sup_id from supplier
                    where sup_num = ?''',(selMP[2],))
                    sup_id = cursor.fetchone()

                    cursor.execute(''' delete from material_purchase
                    where mat_date=? AND mat_id=? AND sup_id=? AND e_num=? AND mat_price=?
                    ''',(selMP[0],mat_id[0],sup_id[0],selMP[3],selMP[4],))
                    
                    conn.commit()
                    manage_MatPur()
            else:
                messagebox.showwarning("System","กรุณากรอก เลือกรายการสั่งซื้อที่ต้องการลบ")
        def searchMP() : 
            searchMP = seachEntry.get()
            matPurchaseTable.delete(*matPurchaseTable.get_children())
            if searchMP:
                sql = '''SELECT * FROM material_purchase WHERE mat_date=?'''
                cursor.execute(sql,(searchMP,))
                MatPur = cursor.fetchall()
                if MatPur:
                    cursor.execute(''' select mat_num from material''')
                    Mat = cursor.fetchone()
                
                    for i,data1 in enumerate(MatPur):
                        
                        cursor.execute(''' select mat_num from material
                        where mat_id = ?''',(data1[1],))
                        Mat = cursor.fetchone()

                        cursor.execute(''' select sup_num from supplier
                        where sup_id = ?''',(data1[2],))
                        Sup = cursor.fetchone()

                        matPurchaseTable.insert("","end",values=(data1[0],Sup[0]+"-"+Mat[0],data1[3],data1[4]))
                else:
                    messagebox.showwarning("System","ไม่พบวันที่สั่งซื้อสินค้า")
                    seachEntry.delete(0,END)
            else:
                messagebox.showwarning("System","กรุณากรอก วันที่สั่งซื้อสินค้า")
                manage_MatPur()

        global searchEntry,selSearch,matPurchaseTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        matPurchaseTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5"),selectmode=BROWSE)
        matPurchaseTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        matPurchaseTable.bind('<<TreeviewSelect>>',show)

        matPurchaseTable.heading('col1', text="วันที่สั่งซื้อ", anchor=W)
        matPurchaseTable.heading('col2', text="รหัสการสั่งซื้อ", anchor=W)
        matPurchaseTable.heading('col3', text="รหัสพนักงาน", anchor=W)
        matPurchaseTable.heading('col4', text="ราคาวัตถุดิบ", anchor=W)

        matPurchaseTable.column('col1',anchor=W, width=200)
        matPurchaseTable.column('col2',anchor=W, width=200)
        matPurchaseTable.column('col3',anchor=W, width=200)
        matPurchaseTable.column('col4',anchor=W, width=200)
        matPurchaseTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngMatPur()

        # Add / Delete / Edit
        Label(mngFrame1,text="ค้นหา วันที่สั่งซื้อ :",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=E)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=20)
        seachEntry.grid(row=8,column=1,sticky=W)

        Label(mngFrame1,text="วันที่สั่งซื้อ",font="Calibri 12",bg="#e0f2fc").place(x=110,y=335)
        date = Label(mngFrame1,width=15,bg="#FFFFFF")
        date.place(x=110,y=360)

        Label(mngFrame1,text="ชื่อพนักงานที่สั่งซื้อ",font="Calibri 12",bg="#e0f2fc").place(x=300,y=335)
        emp = Label(mngFrame1,width=20,bg="#FFFFFF")
        emp.place(x=300,y=360)

        Label(mngFrame1,text="ราคาวัตถุดิบ/หน่วย",font="Calibri 12",bg="#e0f2fc").place(x=550,y=335)
        mp_p = Label(mngFrame1,width=15,bg="#FFFFFF")
        mp_p.place(x=550,y=360)
        #############################################
        Label(mngFrame1,text="ชื่อ ซัพพลายเออร์",font="Calibri 12",bg="#e0f2fc").place(x=20,y=395)
        s_name = Label(mngFrame1,width=15,bg="#FFFFFF")
        s_name.place(x=20,y=420)

        Label(mngFrame1,text="ที่อยู่",font="Calibri 12",bg="#e0f2fc").place(x=200,y=395)
        s_adr = Label(mngFrame1,font="Calibri 13 bold",width=67,bg="#FFFFFF")
        s_adr.place(x=200,y=423)

        Label(mngFrame1,text="หมายเลขโทรศัพท์",font="Calibri 12",bg="#e0f2fc").place(x=820,y=395)
        s_ph = Label(mngFrame1,width=15,bg="#FFFFFF")
        s_ph.place(x=820,y=420)
        #############################################
        
        Label(mngFrame1,text="ชื่อ วัตถุดิบ",font="Calibri 12",bg="#e0f2fc").place(x=20,y=455)
        m_name = Label(mngFrame1,width=20,bg="#FFFFFF")
        m_name.place(x=20,y=480)

        Label(mngFrame1,text="จำนวน ปัจจุบัน",font="Calibri 12",bg="#e0f2fc").place(x=255,y=455)
        m_amt = Label(mngFrame1,width=10,bg="#FFFFFF")
        m_amt.place(x=255,y=480)

        Label(mngFrame1,text="รายละเอียด",font="Calibri 12",bg="#e0f2fc").place(x=380,y=455)
        m_dt = Label(mngFrame1,width=40,bg="#FFFFFF")
        m_dt.place(x=380,y=480)

        Label(mngFrame1,text="จัดการรายการสั่งซื้อวัตถุดิบ",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Button(mngFrame1,text="เพิ่ม",width=10,bg='#00cc66',command=addMatPur).grid(row=8,column=4,sticky="e",pady=20)
        Button(mngFrame1,text="ลบ",width=10,bg='#ff0000',command=deleteMP).grid(row=8,column=5,sticky="e",pady=20)
        Button(mngFrame1,image=img_search,command=searchMP).place(x=565,y=538)

    ######### Frame Menu ###########
    loginFrame.destroy()
    homeFrame1 = Frame(root,bg="#227aa9")
    homeFrame1.configure(width=200, height=700)
    homeFrame1.columnconfigure((0),weight=1)
    homeFrame1.rowconfigure((0,1,2,3,4,5,6,7,8),weight=1)
    homeFrame1.place(x=0,y=0,width=200,height=700)

    # Left Side Button Menu #
    Button(homeFrame1,text = "จัดการคลังสินค้า", command = manage_product, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12").grid(column=0,row=0,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการคลังวัตถุดิบ", command = manage_material, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12").grid(column=0,row=1,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการรายการสั่งซื้อวัตถุดิบ", command = manage_MatPur, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12").grid(column=0,row=2,sticky="ew",pady=10,padx=5,ipady=10)
    
    ######### Frame window ##########
    mainFrame1 = Frame(root,bg="#e0f2fc")
    mainFrame1.columnconfigure((0,1,2),weight=1)
    mainFrame1.rowconfigure((0,1,2,3,4),weight=1)
    mainFrame1.configure(width=1000,height=700)
    mainFrame1.place(x=200,y=0,width=1000,height=700)

    # Pull name From Database #
    sql = "SELECT e_fname,e_lname FROM emp_acc WHERE e_num=?"
    cursor.execute(sql,[user])
    name_ = cursor.fetchone()
    name = name_[0]+" "+name_[1]

    # Label Profile
    Label(mainFrame1,bg="#e0f2fc",image=img_profile).grid(column=1,row=1,ipadx=380,ipady=100,sticky='s')
    Label(mainFrame1,text="Welcome, "+name,bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").grid(column=1,row=2,ipady=10,sticky="n")
    Label(mainFrame1,text="Position : Internal",bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").grid(column=1,row=3,ipady=10,sticky="n")
    Label(mainFrame1,text="",bg="#e0f2fc",fg="#e0f2fc").grid(column=1,row=4,ipady=80,sticky="n")

def homepageS() : 
    def manage_agent() : 
        def edit(self) :
            ag_name.delete(0,END)
            ag_address.delete(0,END)
            ag_phone.delete(0,END)

            selected_item = agentTable.selection()
            if selected_item:
                phone = agentTable.item(selected_item)['values'][3]
                ag_name.insert(0,agentTable.item(selected_item)['values'][1])
                ag_address.insert(0,agentTable.item(selected_item)['values'][2])
                ag_phone.insert(0,"0"+str(phone))
        def searchAg() :
            searchAgent = seachEntry.get()
            sql = '''SELECT * FROM agent
            WHERE ag_num=?'''
            cursor.execute(sql,(searchAgent,))
            result = cursor.fetchall()
            if searchAgent:
                if result:
                    agentTable.delete(*agentTable.get_children())
                    for i,data1 in enumerate(result):
                        agentTable.insert("","end",values=(data1[1],data1[2],data1[3],data1[4]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสตัวแทนจำหน่าย")
                    seachEntry.delete(0,END)
                    fetchTreeForMngAg()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสตัวแทนจำหน่าย")
                fetchTreeForMngAg()
        def saveBtn() :
            selected_item = agentTable.selection()
            if selected_item:
                ag_id = agentTable.item(selected_item)['values'][0]
                name,address,phone = ag_name.get(),ag_address.get(),ag_phone.get()
                ans = messagebox.askquestion("System","คุณแน่ใจหรือว่า ต้องการแก้ไขข้อมูลตัวแทนจำหน่าย")
                if ans == 'yes' :
                    if name:
                        if address:
                            if phone:
                                sql = '''UPDATE agent SET ag_name=?,ag_address=?,ag_phone=?
                                WHERE ag_num=?'''
                                cursor.execute(sql,(name,address,phone,ag_id,))
                                conn.commit()
                                fetchTreeForMngAg()
                            else:
                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ที่อยู่")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อ")
            else:
                messagebox.showwarning("System","กรุณาเลือกตัวแทนจำหน่ายที่ต้องการแก้ไข")
        def deleteBtn() :
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าต้องการลบตัวแทนจำหน่ายนี้ ?")
            if ans == 'yes' :
                selected_item = agentTable.selection()
                if selected_item:
                    ag_num = agentTable.item(selected_item)['values'][0]
                    cursor.execute(''' delete from agent
                    where ag_num = ? ''',(ag_num,))
                    conn.commit()
                    fetchTreeForMngAg()
                else:
                    messagebox.showwarning("System","กรุณาเลือกตัวแทนจำหน่ายที่ต้องการลบ")

        global searchEntry,selSearch,agentTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        agentTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4"),selectmode=BROWSE)
        agentTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        agentTable.bind('<<TreeviewSelect>>',edit)

        agentTable.heading('col1', text="รหัสซัพลลายเออร์", anchor=W)
        agentTable.heading('col2', text="ชื่อ", anchor=W)
        agentTable.heading('col3', text="ที่อยู่", anchor=W)
        agentTable.heading('col4', text="หมายเลขโทรศัพท์", anchor=W)

        agentTable.column('col1',anchor=W, width=50)
        agentTable.column('col2',anchor=W, width=50)
        agentTable.column('col3',anchor=W, width=300)
        agentTable.column('col4',anchor=W, width=50)
        agentTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngAg()

        # Search Box
        Label(mngFrame1,text="ค้นหา รหัสตัวแทนจำหน่าย",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=W,padx=10,pady=20)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=15)
        seachEntry.grid(row=8,column=0,sticky=E,padx=5,pady=20)

        # Add / Delete / Edit
        Label(mngFrame1,text="ชื่อ",font="Calibri 12",bg="#e0f2fc").place(x=160,y=380)
        ag_name = Entry(mngFrame1,width=20,bg="#FFFFFF")
        ag_name.place(x=160,y=405)

        Label(mngFrame1,text="ที่อยู่",font="Calibri 12",bg="#e0f2fc").place(x=160,y=450)
        ag_address = Entry(mngFrame1,width=50,bg="#FFFFFF")
        ag_address.place(x=160,y=475)

        Label(mngFrame1,text="หมายเลขโทรศัพท์",font="Calibri 12",bg="#e0f2fc").place(x=480,y=380)
        ag_phone = Entry(mngFrame1,width=21,bg="#FFFFFF")
        ag_phone.place(x=480,y=405)

        Label(mngFrame1,text="แก้ไขข้อมูลตัวแทนจำหน่าย",font="Calibri 16 bold",bg="#e0f2fc").place(x=10,y=340)

        Label(mngFrame1,text="จัดการทะเบียนตัวแทนจำหน่าย",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Button(mngFrame1,text="บันทึก",bg="#007bff",width=10,command=saveBtn).place(x=540,y=540)
        Button(mngFrame1,text="ลบ",bg="#ff0000",width=10,command=deleteBtn).place(x=700,y=540)
        Button(mngFrame1,image=img_search,command=searchAg).place(x=412,y=545)
    def manage_customer() : 
        def edit_customer(self) :
            cus_name.delete(0,END)
            cus_address.delete(0,END)
            cus_phone.delete(0,END)

            selected_item = customerTable.selection()
            if selected_item:
                phone = "0"+str(customerTable.item(selected_item)['values'][3])
                cus_name.insert(0,customerTable.item(selected_item)['values'][1])
                cus_address.insert(0,customerTable.item(selected_item)['values'][2])
                cus_phone.insert(0,phone)
        def search_customer() :
            searchCUS = cus_seach.get()
            sql = "SELECT * FROM customer WHERE cus_num=?"
            cursor.execute(sql,(searchCUS,))
            result = cursor.fetchall()
            if searchCUS:
                if result:
                    customerTable.delete(*customerTable.get_children())
                    for i,data1 in enumerate(result):
                        customerTable.insert("","end",values=(data1[1],data1[2],data1[3],data1[4]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสลูกค้า")
                    cus_seach.delete(0,END)
                    fetchTreeForMngCus()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสลูกค้า")
        def save_customer() :        
            selected_item = customerTable.selection()
            if selected_item:
                cus_id = customerTable.item(selected_item)['values'][0]
                name,address,phone = cus_name.get(),cus_address.get(),cus_phone.get()
                ans = messagebox.askquestion("System","คุณแน่ใจหรือว่า ต้องการแก้ไขข้อมูลลูกค้า")
                if ans == 'yes' :
                    if name:
                        if address:
                            if phone:
                                sql = '''UPDATE customer SET cus_name=?,cus_address=?,cus_phone=?
                                WHERE cus_num=?'''
                                cursor.execute(sql,(name,address,phone,cus_id,))
                                conn.commit()
                                fetchTreeForMngCus()
                            else:
                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")
                        else:
                            messagebox.showwarning("System","กรุณากรอก ที่อยู่")
                    else:
                        messagebox.showwarning("System","กรุณากรอก ชื่อ")
            else:
                messagebox.showwarning("System","กรุณาเลือกลูกค้าที่ต้องการแก้ไข")
        def delete_customer() :
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าต้องการลบลูกค้านี้ ?")
            if ans == 'yes' :
                selected_item = customerTable.selection()
                if selected_item:
                    cus_num = customerTable.item(selected_item)['values'][0]
                    cursor.execute(''' delete from agent
                    where ag_num = ? ''',(cus_num,))
                    conn.commit()
                    fetchTreeForMngAg()
                else:
                    messagebox.showwarning("System","กรุณาเลือกลูกค้าที่ต้องการลบ")

        global searchEntry,selSearch,customerTable
        mainFrame1.destroy()
        manage_cus_Frame1 = Frame(root,bg="#e0f2fc")
        manage_cus_Frame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        manage_cus_Frame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        manage_cus_Frame1.configure(width=1000,height=700)
        manage_cus_Frame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        customerTable = ttk.Treeview(manage_cus_Frame1, columns=("col1","col2","col3","col4"),selectmode=BROWSE)
        customerTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        customerTable.bind('<<TreeviewSelect>>',edit_customer)

        customerTable.heading('col1', text="รหัสลูกค้า", anchor=W)
        customerTable.heading('col2', text="ชื่อ", anchor=W)
        customerTable.heading('col3', text="ที่อยู่", anchor=W)
        customerTable.heading('col4', text="หมายเลขโทรศัพท์", anchor=W)

        customerTable.column('col1',anchor=W, width=50)
        customerTable.column('col2',anchor=W, width=50)
        customerTable.column('col3',anchor=W, width=300)
        customerTable.column('col4',anchor=W, width=50)
        customerTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngCus()

        # Search Box
        Label(manage_cus_Frame1,text="ค้นหา รหัสลูกค้า",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=8,column=0,sticky=W,padx=10,pady=20)
        cus_seach = Entry(manage_cus_Frame1,bg="#FFFFFF",width=15)
        cus_seach.place(x=150,y=550)

        # Add / Delete / Edit
        Label(manage_cus_Frame1,text="ชื่อ",font="Calibri 12",bg="#e0f2fc").place(x=160,y=380)
        cus_name = Entry(manage_cus_Frame1,width=20,bg="#FFFFFF")
        cus_name.place(x=160,y=405)

        Label(manage_cus_Frame1,text="ที่อยู่",font="Calibri 12",bg="#e0f2fc").place(x=160,y=450)
        cus_address = Entry(manage_cus_Frame1,width=50,bg="#FFFFFF")
        cus_address.place(x=160,y=475)

        Label(manage_cus_Frame1,text="หมายเลขโทรศัพท์",font="Calibri 12",bg="#e0f2fc").place(x=480,y=380)
        cus_phone = Entry(manage_cus_Frame1,width=21,bg="#FFFFFF")
        cus_phone.place(x=480,y=405)

        Label(manage_cus_Frame1,text="แก้ไขข้อมูลลูกค้า",font="Calibri 16 bold",bg="#e0f2fc").place(x=10,y=340)

        Label(manage_cus_Frame1,text="จัดการทะเบียนลูกค้า",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Button(manage_cus_Frame1,text="บันทึก",bg="#007bff",width=10,command=save_customer).place(x=540,y=540)
        Button(manage_cus_Frame1,text="ลบ",bg="#ff0000",width=10,command=delete_customer).place(x=700,y=540)
        Button(manage_cus_Frame1,image=img_search,command=search_customer).place(x=320,y=545)
    def manage_order() :
        def edit(self) :
            selected_item = OrderTable.selection()
        def search() : 
            search = seachEntry.get()
            sql = '''SELECT * FROM "order" WHERE order_num = ?'''
            cursor.execute(sql,(search,))
            result = cursor.fetchall()
            if search:
                if result:
                    employeeTable.delete(*employeeTable.get_children())
                    for i,data1 in enumerate(result):
                        employeeTable.insert("","end",values=(data1[1],data1[4],data1[5],data1[6],data1[7]))
                else:
                    messagebox.showwarning("System","ไม่พบ รหัสการสั่งซื้อ")
                    fetchTreeForMngOrder()
            else:
                messagebox.showwarning("System","กรุณากรอก รหัสการสั่งซื้อ")
        def checkpos2() :
            pos,cap,date,amt,name,phone,addr = selpos.get(),d_cap.get(),newDate.get(),newAmt.get(),newName.get(),newPhone.get(),newAddr.get()
            ans = messagebox.askquestion("System","คุณแน่ใจว่าต้องการเพิ่มข้อมูลการสั่งซื้อวัตถุดิบ ?")
            if ans == 'yes' :
                if date:
                    if amt:
                        if amt.isdigit():
                            cursor.execute(''' select pd_quantity from product
                            where pd_cap = ?''',(cap,))
                            old_amt = cursor.fetchone()
                            if int(old_amt[0]) < int(amt):
                                messagebox.showwarning("System","มีสินค้าไม่พอ")
                            else:
                                new_amt = int(old_amt[0]) - int(amt)
                                cursor.execute(''' update product
                                set pd_quantity = ?
                                where pd_cap = ?''',(new_amt,cap,))
                                if pos:
                                    if name:
                                        if phone:
                                            if phone.isdigit():
                                                if addr:
                                                    if pos == "Customer":
                                                        cus_num = "C1"
                                                        cursor.execute(''' select cus_num from customer''')
                                                        all_cus_num = cursor.fetchall()
                                                        _cus_num = [item[0] for item in all_cus_num]
                                                        while cus_num in _cus_num:
                                                            num = int(cus_num[1])+1
                                                            cus_num = "C"+str(num)

                                                        cursor.execute(''' select pd_quantity from product
                                                        where pd_cap = ?''',(cap,))
                                                        old_amt = cursor.fetchone()
                                                        new_amt = int(old_amt[0]) - int(amt)
                                                        cursor.execute(''' update product
                                                        set pd_quantity = ?
                                                        where pd_cap = ?''',(new_amt,cap,))

                                                        cursor.execute(''' insert into customer
                                                        values(NULL,?,?,?,?) ''',(cus_num,name,addr,phone,))
                                                        cus_id = cursor.lastrowid
                                                        order_num = cus_num[0]+date[0:2]+date[3:5]+date[8:10]+cus_num[1:]

                                                        cursor.execute(''' select pd_price from product
                                                        where pd_cap = ?''',(cap,))
                                                        price = cursor.fetchone()
                                                        total = float(amt) * float(price[0])

                                                        cursor.execute(''' insert into "order"
                                                        values(NULL,?,?,NULL,?,?,?,?)''',(order_num,cus_id,date,cap,amt,total))
                                                        conn.commit()

                                                        save2.destroy()
                                                        save.destroy()
                                                        back.destroy()
                                                        manage_order()
                                                    
                                                    if pos == "Agent":
                                                        ag_num = "A1"
                                                        cursor.execute(''' select ag_num from agent''')
                                                        all_ag_num = cursor.fetchall()
                                                        _ag_num = [item[0] for item in all_ag_num]
                                                        while ag_num in _ag_num:
                                                            num = int(ag_num[1])+1
                                                            ag_num = "A"+str(num)

                                                        cursor.execute(''' select pd_quantity from product
                                                        where pd_cap = ?''',(cap,))
                                                        old_amt = cursor.fetchone()
                                                        new_amt = int(old_amt[0]) - int(amt)
                                                        cursor.execute(''' update product
                                                        set pd_quantity = ?
                                                        where pd_cap = ?''',(new_amt,cap,))

                                                        cursor.execute(''' insert into agent
                                                        values(NULL,?,?,?,?) ''',(ag_num,name,addr,phone,))
                                                        ag_id = cursor.lastrowid
                                                        order_num = ag_num[0]+date[0:2]+date[3:5]+date[8:10]+ag_num[1:]

                                                        cursor.execute(''' select pd_price from product
                                                        where pd_cap = ?''',(cap,))
                                                        price = cursor.fetchone()
                                                        total = float(amt) * float(price[0])

                                                        cursor.execute(''' insert into "order"
                                                        values(NULL,?,?,NULL,?,?,?,?)''',(order_num,ag_id,date,cap,amt,total))
                                                        conn.commit()

                                                        save2.destroy()
                                                        save.destroy()
                                                        back.destroy()
                                                        manage_order()
                                                else:
                                                    messagebox.showwarning("System","กรุณากรอก ที่อยู่ เพื่อทำการจัดส่ง")
                                            else:
                                                messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์ เป็นตัวเลข")
                                        else:
                                            messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")  
                                    else:
                                        messagebox.showwarning("System","กรุณากรอก ชื่อ")   
                                else:
                                    messagebox.showwarning("System","กรุณาเลือก ตำแหน่ง")  
                        else:
                                messagebox.showwarning("System","กรุณากรอก จำนวน ให้ถูกต้อง")    
                    else:
                        messagebox.showwarning("System","กรุณากรอก จำนวนที่สั่งซื้อ")    
                else:
                    messagebox.showwarning("System","กรุณากรอก วันที่สั่งซื้อ")
        def checkpos() :
            pos,cap,date,amt,name,phone = selpos.get(),d_cap.get(),newDate.get(),newAmt.get(),newName.get(),newPhone.get()
            if pos == "Customer":
                cursor.execute(''' select * from customer
                where cus_name = ? AND cus_phone = ?''',(name,phone,))
            if pos == "Agent":
                cursor.execute(''' select * from agent
                where ag_name = ? AND ag_phone = ?''',(name,phone,))
            result = cursor.fetchone()
            if date:
                if amt:
                    if amt.isdigit():
                        cursor.execute(''' select pd_quantity from product
                        where pd_cap = ?''',(cap,))
                        old_amt = cursor.fetchone()
                        if int(old_amt[0]) < int(amt):
                            messagebox.showwarning("System","มีสินค้าไม่พอ")
                        else:
                            new_amt = int(old_amt[0]) - int(amt)
                            cursor.execute(''' update product
                            set pd_quantity = ?
                            where pd_cap = ?''',(new_amt,cap,))
                            if pos:
                                if name:
                                    if phone:
                                        if phone.isdigit():
                                            if result:
                                                ans = messagebox.askquestion("System","คุณแน่ใจว่าต้องการเพิ่มรายการสั่งซื้อ ?")
                                                if ans == 'yes' :
                                                    if pos == "Customer":
                                                        cus_id = result[0]
                                                        cus_num = result[1]
                                                        order_num = cus_num[0]+date[0:2]+date[3:5]+date[8:10]+cus_num[1:]

                                                        cursor.execute(''' select pd_price from product
                                                        where pd_cap = ?''',(cap,))
                                                        price = cursor.fetchone()
                                                        total = float(amt) * float(price[0])

                                                        cursor.execute(''' insert into "order"
                                                        values(NULL,?,?,NULL,?,?,?,?)''',(order_num,cus_id,date,cap,amt,str(total)))
                                                        
                                                        save.destroy()
                                                        back.destroy()
                                                        conn.commit()
                                                        manage_order()

                                                    if pos == "Agent":
                                                        ag_id = result[0]
                                                        ag_num = result[1]
                                                        order_num = ag_num[0]+date[0:2]+date[3:5]+date[8:10]+ag_num[1:]

                                                        cursor.execute(''' select pd_price from product
                                                        where pd_cap = ?''',(cap,))
                                                        price = cursor.fetchone()
                                                        total = float(amt) * float(price[0])

                                                        cursor.execute(''' select pd_quantity from product
                                                        where pd_cap = ?''',(cap,))
                                                        old_amt = cursor.fetchone()
                                                        new_amt = int(old_amt[0]) - int(amt)
                                                        cursor.execute(''' update product
                                                        set pd_quantity = ?
                                                        where pd_cap = ?''',(new_amt,cap,))

                                                        cursor.execute(''' insert into "order"
                                                        values(NULL,?,NULL,?,?,?,?,?)''',(order_num,ag_id,date,cap,amt,str(total)))
                                                        conn.commit()

                                                        save.destroy()
                                                        back.destroy()
                                                        manage_order()
                                            else:
                                                Label(addFrame2,text="ที่อยู่",bg="#e0f2fc").place(x=225,y=400)
                                                newAddr.place(x=225,y=435)
                                                save2.place(x=700,y=600)
                                        else:
                                            messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์ เป็นตัวเลข")
                                    else:
                                        messagebox.showwarning("System","กรุณากรอก หมายเลขโทรศัพท์")  
                                else:
                                    messagebox.showwarning("System","กรุณากรอก ชื่อ")  
                            else:
                                messagebox.showwarning("System","กรุณาเลือก ตำแหน่ง")    
                    else:    
                        messagebox.showwarning("System","กรุณากรอก จำนวน ให้ถูกต้อง")    
                else:    
                    messagebox.showwarning("System","กรุณากรอก จำนวนที่สั่งซื้อ")    
            else:
                messagebox.showwarning("System","กรุณากรอก วันที่สั่งซื้อ")
        def add() :
            global addFrame2, newName , newAddr, selpos , d_cap, newPhone, newAmt, newDate
            mngFrame1.destroy()
            addFrame2 = Frame(root,bg="#e0f2fc")
            addFrame2.columnconfigure((0,1,2),weight=1)
            addFrame2.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
            addFrame2.configure(width=1000,height=700)
            addFrame2.place(x=200,y=0,width=1000,height=700)

            Label(addFrame2,text="เพิ่มรายการสั่งซื้อสินค้า" ,bg="#e0f2fc",font="Calibri 20 bold").place(x=350,y=10)

            Label(addFrame2,text="วันที่",bg="#e0f2fc").place(x=225,y=70)
            newDate = Entry(addFrame2,width=15)
            newDate.place(x=225,y=100)

            def today() :
                newDate.delete(0,END)
                today = datetime.date.today()
                current_date = today.strftime("%d/%m/%Y")
                newDate.insert(0,current_date)
            
            Button(addFrame2,text="วันนี้",bg='white',width=10,command=today).place(x=400,y=90)

            Label(addFrame2,text="ความจุ",bg="#e0f2fc").place(x=225,y=150)
            d_cap.set("350")
            optioncap = ["350","600","1500"]
            cap = OptionMenu(addFrame2,d_cap,*optioncap)
            cap.place(x=225,y=185)

            Label(addFrame2,text="จำนวน",bg="#e0f2fc").place(x=330,y=150)
            newAmt = Entry(addFrame2,width=15)
            newAmt.place(x=330,y=190)
            
            Label(addFrame2,text="ตำแหน่ง" ,bg="#e0f2fc").place(x=225,y=250)
            pCus = Radiobutton(addFrame2,text="ลูกค้า",value="Customer",variable=selpos,bg="#e0f2fc")
            pCus.place(x=225,y=280)
            pAge = Radiobutton(addFrame2,text="ตัวแทนจำหน่าย",value="Agent",variable=selpos,bg="#e0f2fc")
            pAge.place(x=355,y=280)

            Label(addFrame2,text="ชื่อ" ,bg="#e0f2fc").place(x=225,y=330)
            newName = Entry(addFrame2,width=20)
            newName.place(x=225,y=360)

            Label(addFrame2,text="เบอร์โทรศัพท์" ,bg="#e0f2fc").place(x=500,y=330)
            newPhone = Entry(addFrame2,width=20)
            newPhone.place(x=500,y=360)
            
            newAddr = Entry(addFrame2,width=50)

            global save,save2,back
            save = Button(addFrame2,text="บันทึก",bg="#007bff",width=10,command=checkpos)
            save.place(x=700,y=600)
            save2 = Button(addFrame2,text="บันทึก",bg="#007bff",width=10,command=checkpos2)
            back = Button(addFrame2,text="กลับ",bg="#6c757d",width=10,command=back_mng)
            back.place(x=560,y=600)
        def delete() :
            ans = messagebox.askquestion("System", "คุณแน่ใจหรือว่าต้องการลบรายการสั่งซื้อนี้ ?")
            if ans == 'yes' :
                selected_item = OrderTable.selection()
                if selected_item:
                    order_num = OrderTable.item(selected_item)['values'][0]
                    date_time = OrderTable.item(selected_item)['values'][1]
                    pd_cap = OrderTable.item(selected_item)['values'][2]
                    order_quantity = OrderTable.item(selected_item)['values'][3]
                    order_total = OrderTable.item(selected_item)['values'][4]
                    cursor.execute(''' delete from "order"
                    where order_num=? AND date_time=? AND pd_cap=? AND order_quantity=? AND order_total=?
                    ''',(order_num,date_time,pd_cap,order_quantity,order_total))
                    conn.commit()
                    fetchTreeForMngOrder()
                else:
                    messagebox.showwarning("System","กรุณาเลือกรายการสั่งซื้อที่ต้องการลบ")
        def back_mng() :
            addFrame2.destroy()
            save.destroy()
            save2.destroy()
            back.destroy()
            manage_order()
        
        global searchEntry,selSearch,OrderTable
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        # Tree table
        OrderTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5"),selectmode=BROWSE)
        OrderTable.grid(row=1, column=0, columnspan=10, sticky='news',padx=20,pady=10,ipadx=100)
        OrderTable.bind('<<TreeviewSelect>>',edit)

        OrderTable.heading('col1', text="รหัสการสั่งซื้อ", anchor=W)
        OrderTable.heading('col2', text="วันที่", anchor=W)
        OrderTable.heading('col3', text="ขนาด", anchor=W)
        OrderTable.heading('col4', text="จำนวน", anchor=W)
        OrderTable.heading('col5', text="ราคาสุทธิ", anchor=W)

        OrderTable.column('col1',anchor=W, width=100)
        OrderTable.column('col2',anchor=W, width=100)
        OrderTable.column('col3',anchor=W, width=100)
        OrderTable.column('col4',anchor=W, width=100)
        OrderTable.column('col5',anchor=W, width=100)
        OrderTable.column('#0', width=0, minwidth=0) #default column
        fetchTreeForMngOrder()

        # Search Box
        Label(mngFrame1,text="ค้นหา รหัสการจัดส่ง",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").grid(row=5,column=0,sticky=E,padx=10,pady=20)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=15)
        seachEntry.grid(row=5,column=1,sticky="w",padx=5,pady=20)
        Button(mngFrame1,image=img_search,command=search).grid(row=5,column=1,sticky=E,ipadx=5,ipady=5,padx=5)

        Label(mngFrame1,text="จัดการรายการสั่งซื้อ",font="Calibri 20 bold",bg="#e0f2fc").grid(row=0,column=0)
        Button(mngFrame1,text="เพิ่ม",bg="#00cc66",width=10,command=add).grid(row=5,column=4,sticky="e",pady=20)
        Button(mngFrame1,text="ลบ",bg="#ff0000",width=10,command=delete).grid(row=5,column=5,sticky="e",pady=20)
    def payment() : 
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)
        
        def select(self) :
            date.destroy
            name.destroy
            cap.destroy
            amt.destroy
            total.destroy

            selected_item = PayTable.selection()
            if selected_item:
                s_name = PayTable.item(selected_item)['values'][1]
                sh_name = s_name[0]+s_name[7:]
                if s_name[0] == "C" :
                    cursor.execute(''' select cus_name from customer
                    where cus_num = ?''',(sh_name,))
                    result = cursor.fetchone()
                    show_name = result[0]
                if s_name[0] == "A" :
                    cursor.execute(''' select ag_name from agent
                    where ag_num = ?''',(sh_name,))
                    result = cursor.fetchone()
                    show_name = result[0]
                date.config(text=str(PayTable.item(selected_item)['values'][2]))
                name.config(text=show_name)
                cap.config(text=str(PayTable.item(selected_item)['values'][3])+" มิลลิลิตร")
                amt.config(text=str(PayTable.item(selected_item)['values'][4])+" แพ็ค")
                total.config(text=str(PayTable.item(selected_item)['values'][5])+" บาท")

        global PayTable
        PayTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5","col6"),selectmode=BROWSE)
        PayTable.place(x=200,y=150)
        PayTable.bind('<<TreeviewSelect>>',select)

        PayTable.heading('col1', text="ลำดับ", anchor=W)
        PayTable.heading('col2', text="รหัสการสั่งซื้อ", anchor=W)
        PayTable.heading('col3', text="วันที่", anchor=W)
        PayTable.heading('col4', text="ขนาด", anchor=W)
        PayTable.heading('col5', text="จำนวน", anchor=W)
        PayTable.heading('col6', text="ราคาสุทธิ", anchor=W)

        PayTable.column('col1',anchor=W, width=100)
        PayTable.column('col2',anchor=W, width=100)
        PayTable.column('col3',anchor=W, width=100)
        PayTable.column('col4',anchor=W, width=100)
        PayTable.column('col5',anchor=W, width=100)
        PayTable.column('col6',anchor=W, width=100)
        PayTable.column('#0', width=0, minwidth=0) #default column

        def searchAg() :
            searchOrder = seachEntry.get()
            PayTable.delete(*PayTable.get_children()) # clear Treeview
            sql = '''SELECT * FROM "order" 
            where order_num = ?'''
            cursor.execute(sql,(searchOrder,))
            result = cursor.fetchall()
            if result:
                for i,data1 in enumerate(result):
                    PayTable.insert("","end",values=(data1[0],data1[1],data1[4],data1[5],data1[6],data1[7]))
            else:
                messagebox.showwarning("System","ไม่พบ รหัสการสั่งซื้อ")
                payment()

        Label(mngFrame1,text="วันที่ : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=400)
        date = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        date.place(x=255,y=400)

        Label(mngFrame1,text="ชื่อ : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=440)
        name = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        name.place(x=243,y=440)

        Label(mngFrame1,text="ขนาด : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=480)
        cap = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        cap.place(x=270,y=480)
        
        Label(mngFrame1,text="จำนวน : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=520)
        amt = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        amt.place(x=280,y=520)
        
        Label(mngFrame1,text="ราคาสุทธิ : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=560)
        total = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        total.place(x=300,y=560)

        def payment_notification() :
            selected_item = PayTable.selection()
            if selected_item:
                name_ = name.cget('text')
                num = PayTable.item(selected_item)['values'][1]
                date = PayTable.item(selected_item)['values'][2]
                cap = PayTable.item(selected_item)['values'][3]
                amt = PayTable.item(selected_item)['values'][4]
                price = PayTable.item(selected_item)['values'][5]

                msg = "บริษัท เก้ามิถุนา จํากัด ขอขอบคุณ "+str(name_)+" ที่ทำรายการสั่งซื้อเลขที่ #"+str(num)+" ในวันที่ "+str(date)+" เป็นน้ำดื่มขนาด "+str(cap)+" มิลลิลิตร จำนวน "+str(amt)+" แพ็ค ราคาสุทธิ "+str(price)+" บาท กรุณาชำระเงินภายใน 7 วัน"
                
                requests.post(url,headers=header,data={'message':msg})
            else:
                messagebox.showwarning("System","กรุณาเลือกการสั่งซื้อ")
            
        def send_payment_proof() :
            selected_item = PayTable.selection()
            if selected_item:
                requests.post(url,headers=header,data={'message':'บริษัท เก้ามิถุนา จํากัด ได้รับการแจ้งโอนเงินแล้ว กรุณารอการยืนยัน'}) 
            else:
                messagebox.showwarning("System","กรุณาเลือกการสั่งซื้อ")

        notifi = Button(mngFrame1,text="แจ้งเตือนการชำระเงิน",bg='yellow',command=payment_notification)
        notifi.place(x=593,y=420)
        payproof = Button(mngFrame1,text="ส่งหลักฐานการชะเงิน",bg='#00D100',command=send_payment_proof)
        payproof.place(x=593,y=480)
        
        Label(mngFrame1,text='ส่งแจ้งเตือน การชำระเงิน',bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").place(x=350,y=20)
        Label(mngFrame1,text="ค้นหา รหัสการสั่งซื้อ",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").place(x=240,y=100)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=20)
        seachEntry.place(x=430,y=100)
        Button(mngFrame1,image=img_search,command=searchAg).place(x=655,y=95)
    def shipping() :
        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)

        mainFrame1.destroy()
        mngFrame1 = Frame(root,bg="#e0f2fc")
        mngFrame1.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1)
        mngFrame1.rowconfigure((0,1,2,3,4,5,6,7),weight=1)
        mngFrame1.configure(width=1000,height=700)
        mngFrame1.place(x=200,y=0,width=1000,height=600)
        
        def select(self) :
            date.destroy
            name.destroy
            cap.destroy
            amt.destroy
            total.destroy
            addr.destroy

            selected_item = PayTable.selection()
            if selected_item:
                s_name = PayTable.item(selected_item)['values'][1]
                sh_name = s_name[0]+s_name[7:]
                if s_name[0] == "C" :
                    cursor.execute(''' select * from customer
                    where cus_num = ?''',(sh_name,))
                    result = cursor.fetchone()
                    show_name = result[2]
                    address = result[3]
                if s_name[0] == "A" :
                    cursor.execute(''' select * from agent
                    where ag_num = ?''',(sh_name,))
                    result = cursor.fetchone()
                    show_name = result[2]
                    address = result[3]
                date.config(text=str(PayTable.item(selected_item)['values'][2]))
                name.config(text=show_name)
                cap.config(text=str(PayTable.item(selected_item)['values'][3])+" มิลลิลิตร")
                amt.config(text=str(PayTable.item(selected_item)['values'][4])+" แพ็ค")
                total.config(text=str(PayTable.item(selected_item)['values'][5])+" บาท")
                addr.config(text=address)

        global PayTable
        PayTable = ttk.Treeview(mngFrame1, columns=("col1","col2","col3","col4","col5","col6"),selectmode=BROWSE)
        PayTable.place(x=200,y=150)
        PayTable.bind('<<TreeviewSelect>>',select)

        PayTable.heading('col1', text="ลำดับ", anchor=W)
        PayTable.heading('col2', text="รหัสการสั่งซื้อ", anchor=W)
        PayTable.heading('col3', text="วันที่", anchor=W)
        PayTable.heading('col4', text="ขนาด", anchor=W)
        PayTable.heading('col5', text="จำนวน", anchor=W)
        PayTable.heading('col6', text="ราคาสุทธิ", anchor=W)

        PayTable.column('col1',anchor=W, width=100)
        PayTable.column('col2',anchor=W, width=100)
        PayTable.column('col3',anchor=W, width=100)
        PayTable.column('col4',anchor=W, width=100)
        PayTable.column('col5',anchor=W, width=100)
        PayTable.column('col6',anchor=W, width=100)
        PayTable.column('#0', width=0, minwidth=0) #default column

        def searchAg() :
            searchOrder = seachEntry.get()
            PayTable.delete(*PayTable.get_children()) # clear Treeview
            sql = '''SELECT * FROM "order" 
            where order_num = ?'''
            cursor.execute(sql,(searchOrder,))
            result = cursor.fetchall()
            if result:
                for i,data1 in enumerate(result):
                    PayTable.insert("","end",values=(data1[0],data1[1],data1[4],data1[5],data1[6],data1[7]))
            else:
                messagebox.showwarning("System","ไม่พบ รหัสการสั่งซื้อ")
                payment()

        Label(mngFrame1,text="วันที่ : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=380)
        date = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        date.place(x=255,y=380)

        Label(mngFrame1,text="ชื่อ : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=410)
        name = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        name.place(x=243,y=410)

        Label(mngFrame1,text="ขนาด : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=440)
        cap = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        cap.place(x=270,y=440)
        
        Label(mngFrame1,text="จำนวน : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=470)
        amt = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        amt.place(x=280,y=470)
        
        Label(mngFrame1,text="ราคาสุทธิ : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=500)
        total = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=20,anchor='w')
        total.place(x=300,y=500)

        Label(mngFrame1,text="ที่อยู่ : ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=200,y=530)
        addr = Label(mngFrame1,bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold",width=70,anchor='w')
        addr.place(x=255,y=530)

        Label(mngFrame1,text="รหัสพัสดุ",bg="#e0f2fc",fg="#227aa9",font="Calibri 16 bold").place(x=768,y=396)
        parcel_code = Entry(mngFrame1,bg="white",font="Calibri 16 bold",width=11)
        parcel_code.place(x=768,y=427)

        def preparing_for_delivery() :
            selected_item = PayTable.selection()
            if selected_item:
                price = PayTable.item(selected_item)['values'][5]
                msg = "บริษัท เก้ามิถุนา จํากัด ได้รับยอดเงิน "+price+" บาท กำลังเตรียมการจัดส่ง"
                requests.post(url,headers=header,data={'message':msg})
            else:
                messagebox.showwarning("System","กรุณาเลือกการสั่งซื้อ")
            
        def send_parcel_code() :
            selected_item = PayTable.selection()
            parcel,address = parcel_code.get(),addr.cget('text')
            if selected_item:
                if parcel:
                    msg = 'บริษัท เก้ามิถุนา จํากัด ได้จัดส่งสินค้าของคุณแล้ว ไปยังที่อยู่ : '+address+' รหัสพัดสดุ คือ '+parcel
                    requests.post(url,headers=header,data={'message':msg})
                else:
                    messagebox.showwarning("System","กรุณากรอกรหัสพัสดุ")
            else:
                messagebox.showwarning("System","กรุณาเลือกการสั่งซื้อ")

        notifi = Button(mngFrame1,text="เตรียมการจัดส่ง",bg='orange',command=preparing_for_delivery)
        notifi.place(x=593,y=460)
        payproof = Button(mngFrame1,text="ส่งรหัสพัสดุ",bg='#0E86D4',command=send_parcel_code)
        payproof.place(x=770,y=460)
        
        Label(mngFrame1,text='ส่งแจ้งเตือน การจัดส่ง',bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").place(x=350,y=20)
        Label(mngFrame1,text="ค้นหา รหัสการสั่งซื้อ",bg="#e0f2fc",fg="#227aa9",font="Calibri 14 bold").place(x=240,y=100)
        seachEntry = Entry(mngFrame1,bg="#FFFFFF",width=20)
        seachEntry.place(x=430,y=100)
        Button(mngFrame1,image=img_search,command=searchAg).place(x=655,y=95)

    url = 'https://notify-api.line.me/api/notify'
    token = 'kOvrEdERclK780etb9WcJr7j7etYWShjr3n985Ftzgs'
    # token = 'kT3NPWvCpWoRNoTfuWcq6xJDytE07BaErYIzVdc1odv'
    header = {'Content-Type':'application/x-www-form-urlencoded',
            'Authorization':'Bearer '+token}
        
    img_pay = 'https://scontent.fbkk9-3.fna.fbcdn.net/v/t1.6435-9/123660618_3734312483288192_9101022654198231459_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=730e14&_nc_eui2=AeGMJisDk5UsVtZWTxA9buc2mRCFTQ1x9huZEIVNDXH2Gz5U_Qylthq1VnHONhUD3bVNQPZ0Cf3rMH1mYoe_1n5j&_nc_ohc=ZQJfuh62XH8AX-OxS-d&_nc_ht=scontent.fbkk9-3.fna&oh=00_AfDt8uiEcWG__ADsBEmsiPwf1zScsvjrkJhAYSlt0J_yag&oe=64637792'
    img_rec = 'https://scontent.fbkk12-4.fna.fbcdn.net/v/t1.15752-9/331109395_1153281992048394_5641006229207564574_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=ae9488&_nc_eui2=AeFPaY0LLieimyIBkAgEXA2a4WmKIYL3Ex_haYohgvcTH9zQI_KsKdsi8URrePrph1m4Z4kLjP-XOE-_jGQrsk2Z&_nc_ohc=8VqcHlVnpFcAX_7LQB7&_nc_ht=scontent.fbkk12-4.fna&oh=03_AdRFnAaiWea0cRiLwPWqcbTNHE9zJu4SXTg83eHTY46WRg&oe=64639485'

    ######### Frame Menu ###########
    loginFrame.destroy()
    homeFrame1 = Frame(root,bg="#227aa9")
    homeFrame1.configure(width=200, height=700)
    homeFrame1.columnconfigure((0),weight=1)
    homeFrame1.rowconfigure((0,1,2,3,4,5,6,7,8),weight=1)
    homeFrame1.place(x=0,y=0,width=200,height=700)

    ######### Frame window ##########
    mainFrame1 = Frame(root,bg="#e0f2fc")
    mainFrame1.columnconfigure((0,1,2),weight=1)
    mainFrame1.rowconfigure((0,1,2,3,4),weight=1)
    mainFrame1.configure(width=1000,height=700)
    mainFrame1.place(x=200,y=0,width=1000,height=700)

    addFrame1 = Frame(root,bg="#e0f2fc")
    addFrame1.columnconfigure((0,1,2),weight=1)
    addFrame1.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
    addFrame1.configure(width=1000,height=700)
    
    addFrame2 = Frame(root,bg="#e0f2fc")
    addFrame2.columnconfigure((0,1,2),weight=1)
    addFrame2.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)
    addFrame2.configure(width=1000,height=700)
    
    # Left Side Button Menu #
    Button(homeFrame1,text = "จัดการทะเบียน\nตัวแทนจำหน่าย", command = manage_agent, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=0,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "จัดการทะเบียนลูกค้า", command = manage_customer, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=1,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "ขายสินค้า", command = manage_order, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=2,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "รับชำระค่าสินค้า", command = payment, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=3,sticky="ew",pady=10,padx=5,ipady=10)
    Button(homeFrame1,text = "การจัดส่งสินค้า", command = shipping, fg = "#FFFFFF", bg="#227aa9",font="Calibri 12 bold").grid(column=0,row=4,sticky="ew",pady=10,padx=5,ipady=10)   

    # Pull name From Database #
    sql = "SELECT e_fname,e_lname FROM emp_acc WHERE e_num=?"
    cursor.execute(sql,[user])
    name_ = cursor.fetchone()
    name = name_[0]+" "+name_[1]

    # Label Profile
    Label(mainFrame1,bg="#e0f2fc",image=img_profile).grid(column=1,row=1,ipadx=380,ipady=100,sticky='s')
    Label(mainFrame1,text="Welcome, "+name,bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").grid(column=1,row=2,ipady=10,sticky="n")
    Label(mainFrame1,text="Position : Sales",bg="#e0f2fc",fg="#227aa9",font="Calibri 20 bold").grid(column=1,row=3,ipady=10,sticky="n")
    Label(mainFrame1,text="",bg="#e0f2fc",fg="#e0f2fc").grid(column=1,row=4,ipady=80,sticky="n")

w = 1200
h = 700

createconnection()

root = Tk()
root.geometry("%dx%d"%(w, h))
root.title("Happy Water Application")
root.option_add('*font', "Calibri 16 bold")
root.columnconfigure((0,1,2,3,4), weight = 1)
root.rowconfigure((0,1,2), weight = 1)

img_logo = PhotoImage(file="img/happy-water-logo.png")
myLabel = Label(root,image=img_logo)
myLabel.grid(row=0,column=0,columnspan=3,rowspan=4,sticky="news")

loginlayout()
# image & Variable
selSearch = StringVar()
searchEntry = StringVar()
searchEm = StringVar()
selPos = StringVar()
selGen = StringVar()
selpos = StringVar()
d_cap = StringVar()
selGender = StringVar()
newIDCard = StringVar()
newName = StringVar()
newLastName = StringVar()
newPhone1 = StringVar()
newPhone2 = StringVar()
newPass = StringVar()
newConfirmPass = StringVar()
newGender = StringVar()
newEmPos = StringVar()
newEmBirth = StringVar()
spycus_id = StringVar()
cus_title1 = StringVar()
ag_title1 = StringVar()
title2 = StringVar()
title3 = StringVar()
newAddr = StringVar()
newPhone = StringVar()
newDate = StringVar()
newAmt = StringVar()

img_profile = PhotoImage(file="img/profile.png").subsample(2,2)
img_search = PhotoImage(file="img/search.png").subsample(16,16)
root.mainloop()
cursor.close() #close cursor
conn.close() #close database connection