from tkinter import *
from employees import employee_form
from supplire import supplire_form
from category import category_form
from products import product_form
from employees import connect_database
from tkinter import messagebox
import time

def update():
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system') 
    cursor.execute('SELECT * from employee_data')
    emp_records=cursor.fetchall()
    # print(len(records))
    total_emp_count_label.config(text=len(emp_records))

    cursor.execute('SELECT * from supplier_data')
    sup_records=cursor.fetchall()
    total_sup_count_label.config(text=len(sup_records))

    cursor.execute('SELECT * from category_data')
    cat_records=cursor.fetchall()
    total_cat_count_label.config(text=len(cat_records))

    cursor.execute('SELECT * from product_data')
    prod_records=cursor.fetchall()
    total_prod_count_label.config(text=len(prod_records))
     
    # current_time=time.strftime('%A %I:%M:%S %p')    
    # current_date=time.strftime('%d/%m/%Y')          #%B
    date_time=time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Wellcome Admin\t\t\t\t\t\t\t Date:{date_time}')
    subtitleLabel.after(400,update)

def tax_window():
    def save_tax():
        value=tax_count.get()
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE if not exists tax_table(id int primary key, tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id=1')
        if cursor.fetchall():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id=1',value)
        else:
            cursor.execute('insert into tax_table(id,tax) VALUES(1,%s)',value)
        connection.commit()
        messagebox.showinfo('Success',f'tax is set to {value}% and sucessfully',parent=tax_root)

    tax_root=Toplevel()
    tax_root.title('Enter Tax Percentage')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage=Label(tax_root,text='Enter Tax Percentage(%)',font=('arial 12'))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root,from_=0,to=100,font=('arial 12'))
    tax_count.pack(pady=10)
    save_button=Button(tax_root,text='Save',font=('arial',12,'bold'),bg='#4d636d',fg='white',width=10,command=save_tax)
    save_button.pack(pady=20)

current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)



window=Tk()
window.title("Dashboard")
window.geometry('1270x675+0+0')
window.resizable(0,0)
window.config(bg='white')


bg_image=PhotoImage(file='image/inventory.png')

titleLabel=Label(window,image=bg_image,compound=LEFT,text='Inventory Management System  ',fg='white'
                 ,anchor='w',padx=20,font=('times new roman',40,'bold'),bg='#010c48')
titleLabel.place(x=0,y=0,relwidth=1)

logoutButton=Button(window,font=('times new roman',20,'bold'),text='Logout',fg='#010c48',activeforeground='#010c48')
logoutButton.place(x=1100,y=10)

subtitleLabel=Label(window,fg='white',
                 font=('times new roman',15,),bg='#4d636d')
subtitleLabel.place(x=0,y=70,relwidth=1)

leftFrame=Frame(window)
leftFrame.place(x=0,y=102,width=200,height=570)


logoImage=PhotoImage(file="image/logo.png")
imageLabel=Label(leftFrame,image=logoImage)
imageLabel.pack()

employee_icon=PhotoImage(file='image/employee.png')
employee_button=Button(leftFrame,text=' Employee',compound=LEFT,image=employee_icon,
                       font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda: show_form(employee_form))
employee_button.pack(fill=X)

supplier_icon=PhotoImage(file='image/supplier.png')
supplier_button=Button(leftFrame,text=' Suppliers',compound=LEFT,image=supplier_icon,font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda: show_form(supplire_form))
supplier_button.pack(fill=X)

category_icon=PhotoImage(file='image/category.png')
category_button=Button(leftFrame,text=' Categories',compound=LEFT,image=category_icon,font=('times new roman',20,'bold')
                       ,anchor='w',padx=10,command=lambda: show_form(category_form))
category_button.pack(fill=X)

products_icon=PhotoImage(file='image/product.png')
products_button=Button(leftFrame,text=' Products',compound=LEFT,image=products_icon,font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda: show_form(product_form))
products_button.pack(fill=X)

sales_icon=PhotoImage(file='image/sales.png')
sales_button=Button(leftFrame,text=' Sales',compound=LEFT,image=sales_icon,font=('times new roman',20,'bold'),anchor='w',padx=10)
sales_button.pack(fill=X)

tax_icon=PhotoImage(file='image/tax.png')
tax_button=Button(leftFrame,text=' Tax',compound=LEFT,image=tax_icon,font=('times new roman',20,'bold'),anchor='w',padx=10,command=tax_window)
tax_button.pack(fill=X)

exit_icon=PhotoImage(file='image/exit.png')
exit_button=Button(leftFrame,text=' Exit',compound=LEFT,image=exit_icon,font=('times new roman',20,'bold'),anchor='w',padx=10)
exit_button.pack(fill=X)


emp_frame=Frame(window,bg='#2c3e50',bd=3,relief=RAISED)
emp_frame.place(x=400,y=125,height=170,width=280)

totol_emp_icon=PhotoImage(file='image/total_emp.png') 
totol_emp_icon_label=Label(emp_frame,image=totol_emp_icon,bg='#2c3e50')
totol_emp_icon_label.pack(pady=10)

total_emp_label=Label(emp_frame,fg='white',text='Total Employees',bg='#2c3e50'
                           ,font=('times new roman',15,'bold'))
total_emp_label.pack()

total_emp_count_label=Label(emp_frame,fg='white',bg='#2c3e50'
                           ,font=('times new roman',30,'bold'))
total_emp_count_label.pack()



sup_frame=Frame(window,bg='#8e44ad',bd=3,relief=RAISED)
sup_frame.place(x=800,y=125,height=170,width=280)

totol_sup_icon=PhotoImage(file='image/total_sup.png') 
totol_sup_icon_label=Label(sup_frame,image=totol_sup_icon,bg='#8e44ad')
totol_sup_icon_label.pack(pady=10)

total_sup_label=Label(sup_frame,fg='white',text='Total Supplires',bg='#8e44ad'
                           ,font=('times new roman',15,'bold'))
total_sup_label.pack()

total_sup_count_label=Label(sup_frame,fg='white',text='0',bg='#8e44ad'
                           ,font=('times new roman',30,'bold'))
total_sup_count_label.pack()



cat_frame=Frame(window,bg='#27ae60',bd=3,relief=RAISED)
cat_frame.place(x=400,y=310,height=170,width=280)

totol_cat_icon=PhotoImage(file='image/total_cat.png') 
totol_cat_icon_label=Label(cat_frame,image=totol_cat_icon,bg='#27ae60')
totol_cat_icon_label.pack(pady=10)

total_cat_label=Label(cat_frame,fg='white',text='Total Categories',bg='#27ae60'
                           ,font=('times new roman',15,'bold'))
total_cat_label.pack()

total_cat_count_label=Label(cat_frame,fg='white',text='0',bg='#27ae60'
                           ,font=('times new roman',30,'bold'))
total_cat_count_label.pack()


prod_frame=Frame(window,bg='#2980b9',bd=3,relief=RAISED)
prod_frame.place(x=800,y=310,height=170,width=280)

totol_prod_icon=PhotoImage(file='image/total_prod.png') 
totol_prod_icon_label=Label(prod_frame,image=totol_prod_icon,bg='#2980b9')
totol_prod_icon_label.pack(pady=10)

total_prod_label=Label(prod_frame,fg='white',text='Total Categories',bg='#2980b9'
                           ,font=('times new roman',15,'bold'))
total_prod_label.pack()

total_prod_count_label=Label(prod_frame,fg='white',text='0',bg='#2980b9'
                           ,font=('times new roman',30,'bold'))
total_prod_count_label.pack()


sales_frame=Frame(window,bg='#e74c3c',bd=3,relief=RAISED)
sales_frame.place(x=600,y=495,height=170,width=280)

totol_sales_icon=PhotoImage(file='image/total_sales.png') 
totol_sales_icon_label=Label(sales_frame,image=totol_sales_icon,bg='#e74c3c')
totol_sales_icon_label.pack(pady=10)

total_sales_label=Label(sales_frame,fg='white',text='Total Sales',bg='#e74c3c'
                           ,font=('times new roman',15,'bold'))
total_sales_label.pack()

total_sales_count_label=Label(sales_frame,fg='white',text='0',bg='#e74c3c'
                           ,font=('times new roman',30,'bold'))
total_sales_count_label.pack()








update()
window.mainloop()