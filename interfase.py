import dearpygui.dearpygui as dpg
import random
import numpy as np

dpg.create_context()
height_Goods = 50
width_Goods = 150

stat = np.loadtxt('stat.txt', dtype =int)
f = open('names.txt', 'r', encoding='utf-8')
data=[]
for i in f.readlines():
    data.append(i[:-1])


ind = 0
N_column = 3
N_row = 6
Basket = []
tag_product = 'avQEV'
def add_data():
    global ind
    with dpg.table_row(parent="Goods"):
        for i in range(N_column):
            dpg.add_button(label=data[ind], tag=str(ind),height=height_Goods,width=width_Goods, callback=add_basket, user_data=ind); ind+=1
    

def add_basket(sender, add_data, user_data):
    Basket.append(user_data)
    tag = str(random.random())
    with dpg.group(horizontal=True, parent='Basket', tag=tag):
        dpg.add_button(label=data[user_data],height=height_Goods,width=width_Goods, callback=remowe_basket, user_data=[tag,user_data])
    get_stat_product()

def remowe_basket(sender, add_data, user_data):
    dpg.delete_item(user_data[0])
    Basket.remove(user_data[1])
    get_stat_product()


def get_stat_product():
    global tag_product
    buf = np.zeros((1370))
    for el in Basket:
        buf +=stat[el]
    n_product = buf.argsort()[-10:][::-1]
    if len(Basket)>0:
        dpg.delete_item(tag_product)
        tag_product = str(random.random())
        with dpg.group(horizontal=True, parent='product', tag=tag_product):
            for i in n_product:
                dpg.add_button(label=data[i],height=height_Goods,width=width_Goods, callback=add_basket, user_data=i)



with dpg.window(tag="Window"):
    dpg.add_text('Basket')
    with dpg.child_window(autosize_x=True, height=height_Goods+16, horizontal_scrollbar =True):
        with dpg.group(horizontal=True, tag='Basket'):
            pass

    dpg.add_button(label="buy")

    dpg.add_text('Goods')
    with dpg.table(tag='Goods', header_row=False, borders_innerH=True, 
                    borders_outerH=True, borders_innerV=True, borders_outerV=True,
                    height=300,width=475, scrollY=True):
        
        for i in range(N_column):
            dpg.add_table_column()
        for i in range(N_row):
            with dpg.table_row():
                for i in range(N_column):
                    dpg.add_button(label=data[ind], tag=str(ind),height=height_Goods,width=width_Goods, callback=add_basket, user_data=ind); ind+=1
        
        
    dpg.add_button(label="add", callback=add_data)
 
    dpg.add_text('Buy with this product:')
    with dpg.child_window(autosize_x=True, height=height_Goods+16, horizontal_scrollbar =True):
        with dpg.group(horizontal=True, tag='product'):
            pass

dpg.create_viewport(title='Buy with this product', width=600, height=300)
dpg.setup_dearpygui()
dpg.set_primary_window('Window', True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()