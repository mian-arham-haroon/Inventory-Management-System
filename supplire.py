from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

def delete_supplire(invoice,treeview):
    index=treeview.selection()
    if not index :
        messagebox.showerror('Error','No row is selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s',invoice)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Info','Record is deleted')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

    finally:
        cursor.close()
        connection.close()

def clear(invoice_entry,name_entry,contact_entry,description_text,treeview):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())

def search_supplier(search_value,treeview):
    if search_value=='':
        messagebox.showerror('error','Please enter invoice no.')
    else:
        try:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return
            cursor.execute('use inventory_system')
            cursor.execute ('SELECT * from supplier_data WHERE invoice=%s',search_value)
            record=cursor.fetchone()
            if not record:
                messagebox.showerror('Error','No record found')    
                return
            treeview.delete(*treeview.get_children())
            treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

        finally:
            cursor.close()
            connection.close()


def show_all(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)
        
            
def update_supplire(invoice,name,contact,description,treeview):
    index=treeview.selection()
    if not index :
        messagebox.showerror('Error','No row is selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:        
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', (invoice,))
        current_data = cursor.fetchone()

        if current_data is None:
            messagebox.showerror('Error', 'No supplier found with the given invoice')
            return
        current_data = current_data[1:]
        new_data = (name, contact, description)

        if current_data == new_data:
            messagebox.showinfo('Info', 'No changes detected')
            return
        
        cursor.execute('UPDATE supplier_data SET name=%s,contact=%s,descripition=%s WHERE invoice=%s',(name,contact,description,invoice))
        connection.commit()
        messagebox.showinfo('Info','Data is updated')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

    finally:
        cursor.close()
        connection.close()

def select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content['values']
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(0.1,END)
    invoice_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    description_text.insert(1.0,actual_content[3])


def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('Select * from supplier_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in  records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()    



def add_supplier(invoice,name,contact,description,treeview):
    if invoice=='' or name=='' or contact==''or description=='':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('CREATE TABLE IF NOT EXISTS supplier_data(invoice INT PRIMARY KEY,name VARCHAR(100), contact VARCHAR(15), descripition TEXT)')
            cursor.execute('SELECT * from supplier_data WHERE invoice=%s',invoice)
            if cursor.fetchone():
                messagebox.showerror('Error','Invoice No. already exists')
                return

            cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s)',(invoice,name,contact,description))
            connection.commit()
            messagebox.showinfo('Info','Data is inserted')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()    

      

 


def supplire_form(window):
    global back_image
    supplire_frame=Frame(window,width=1070,height=567,bg='white')
    supplire_frame.place(x=200,y=100)
    
    heading_label=Label(supplire_frame,text='Manage Supplire Details',
                        font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    back_image=PhotoImage(file=('image/back.png'))
    back_button=Button(supplire_frame,image=back_image,bd=0,bg='white',activebackground='white'
                        ,cursor='hand2',command=lambda: supplire_frame.place_forget())
    back_button.place(x=10,y=30)

    left_frame=Frame(supplire_frame,bg='white')
    left_frame.place(x=10,y=100)


    invoice_label=Label(left_frame,text='Invoice No.',font=('times new roman',14,'bold'),bg='white')
    invoice_label.grid(row=0,column=0,padx=(20,40),sticky='w')


    invoice_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    invoice_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text='Supplire Name',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(20,40),sticky='w',pady=20)

    name_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text='Supplire Contact',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=(20,40),sticky='w')

    contact_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    contact_entry.grid(row=2,column=1)

    description_label=Label(left_frame,text='Description',font=('times new roman',14,'bold'),bg='white')
    description_label.grid(row=3,column=0,padx=(20,40),sticky='nw',pady=25)

    description_text=Text(left_frame,width=25,height=6,bd=2,bg='lightyellow',font=('times new roman',14))
    description_text.grid(row=3,column=1,pady=20)


    button_Frame=Frame(left_frame,background='white')
    button_Frame.grid(row=4,columnspan=4,pady=20)

    add_button=Button(button_Frame,text='Add',font=('times new roman',14),width=8,cursor='hand2',fg='white'
                        ,bg='#0f4d7d',activebackground='#0f4d7d',activeforeground='white'
                        ,command=lambda: add_supplier(invoice_entry.get(),contact_entry.get(),name_entry.get(),description_text.get(1.0,END).split(),treeview))
    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(button_Frame,text='Update',font=('times new roman',14),width=8,cursor='hand2',fg='white'
                        ,bg='#0f4d7d',activebackground='#0f4d7d',activeforeground='white',command=lambda: update_supplire(invoice_entry.get(),contact_entry.get()
                                                                                                                          ,name_entry.get(),description_text.get(1.0,END).split()
                                                                                                                          ,treeview))
    update_button.grid(row=0,column=1,padx=20)

    delete_button=Button(button_Frame,text='Delete',font=('times new roman',14),width=8,cursor='hand2',fg='white'
                        ,bg='#0f4d7d',activebackground='#0f4d7d',activeforeground='white',command=lambda: delete_supplire(invoice_entry.get(),treeview))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_Frame,text='Clear',font=('times new roman',14),width=8,cursor='hand2',fg='white'
                        ,bg='#0f4d7d',activebackground='#0f4d7d',activeforeground='white',command=lambda: clear(invoice_entry,name_entry
                                                                                                                ,contact_entry,description_text,treeview))
    clear_button.grid(row=0,column=3,padx=20)

    right_frame=Frame(supplire_frame,bg='white')
    right_frame.place(x=520,y=95,width=500,height=350)


    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))

    num_label=Label(search_frame,text='Invoice No.',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,15),sticky='w')

    search_entry=Entry(search_frame,bg='lightyellow',font=('times new roman',14),width=12)
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',14),width=8,cursor='hand2',fg='white'
                        ,bg='#0f4d7d',activebackground='#0f4d7d',activeforeground='white',command=lambda: search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0,column=2,padx=15)

    show_button=Button(search_frame,text='Show All',font=('times new roman',14),width=8,cursor='hand2',fg='white'
                        ,bg='#0f4d7d',activebackground='#0f4d7d',activeforeground='white',command=lambda: show_all(treeview,search_entry))
    show_button.grid(row=0,column=3)

    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(right_frame,columns=('invoice','name','contact','description'),show='headings'
                          ,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.heading('invoice',text='Invoice Id')
    treeview.heading('name',text='Supplier Name')
    treeview.heading('contact',text='Supplier Contact')
    treeview.heading('description',text='Description')

    treeview.column('invoice',width=80)
    treeview.column('name',width=160)
    treeview.column('contact',width=120)
    treeview.column('description',width=300)


    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event: select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview))
    return supplire_frame