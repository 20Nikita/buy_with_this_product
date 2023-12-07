import dearpygui.dearpygui as dpg
import random
import numpy as np
import torch

import perceptron_net
import lstm
import statistic_predict

dpg.create_context()
height_Goods = 50
width_Goods = 150


f = open('names.txt', 'r', encoding='utf-8')
data=[]
for i in f.readlines():
    data.append(i[:-1])

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
ind = 0
N_column = 10
N_row = 12
Radio = 0
N = 1370
num_level=1
hide_neuron=32
per_net = perceptron_net.MyNet(N).to(device)
lstm_net = lstm.LSTM(N+1,hide_neuron,num_level)
with dpg.font_registry():
    with dpg.font(f'C:\\Windows\\Fonts\\trebucbd.ttf', 13, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    
dpg.bind_font("Default font")

Basket = []
tag_product = 'avQEV'
def add_data():
    global ind
    for i in range(N_row):
        with dpg.table_row(parent="Goods"):
            for i in range(N_column):
                dpg.add_button(label=data[ind], tag=str(ind),height=height_Goods,width=width_Goods, callback=add_basket, user_data=ind); ind+=1
    

def add_basket(sender, add_data, user_data):
    Basket.append(user_data)
    tag = str(random.random())
    with dpg.group(horizontal=True, parent='Basket', tag=tag):
        dpg.add_button(label=data[user_data],height=height_Goods,width=width_Goods, callback=remowe_basket, user_data=[tag,user_data])
    get_stat_product()
    # print(Basket)

def remowe_basket(sender, add_data, user_data):
    dpg.delete_item(user_data[0])
    Basket.remove(user_data[1])
    get_stat_product()

def get_stat_product():
    global tag_product
    if len(Basket)>0:
        if Radio == 0:
            n_product = statistic_predict.statistic_predict(Basket, N, N_column)
        elif Radio == 1:
            n_product = perceptron_net.predict(Basket, per_net, N, N_column)
        elif Radio == 2:
            n_product = lstm.predict(Basket, lstm_net, N, N_column,num_level,hide_neuron)
        dpg.delete_item(tag_product)
        tag_product = str(random.random())
        with dpg.group(horizontal=True, parent='product', tag=tag_product):
            for i in n_product:
                dpg.add_button(label=data[i],height=height_Goods,width=width_Goods, callback=add_basket, user_data=i)
    else:
        dpg.delete_item(tag_product)
def radio(sender, add_data, user_data):
    global Radio
    if add_data == "Cтатистика":
        Radio = 0
    elif add_data == "Перцерптрон":
        Radio = 1
    elif add_data == "LSTM":
        Radio = 2
    get_stat_product()

with dpg.window(tag="Window"):
    dpg.add_text('Корзина')
    with dpg.child_window(width=N_column*(width_Goods+10), height=height_Goods+16, horizontal_scrollbar =True):
        with dpg.group(horizontal=True, tag='Basket'):
            pass

    dpg.add_button(label="Купить")

    dpg.add_text('Товары')
    with dpg.table(tag='Goods', header_row=False, borders_innerH=True, 
                    borders_outerH=True, borders_innerV=True, borders_outerV=True,
                    height=N_row*(height_Goods+5),width=N_column*(width_Goods+10), scrollY=True):
        
        for i in range(N_column):
            dpg.add_table_column()
        for i in range(N_row):
            with dpg.table_row():
                for i in range(N_column):
                    dpg.add_button(label=data[ind], tag=str(ind),height=height_Goods,width=width_Goods, callback=add_basket, user_data=ind); ind+=1
        
        
    dpg.add_button(label="Еще", callback=add_data)
 
    dpg.add_text('С этим товаром покупают:')
    with dpg.group(horizontal=True):
        dpg.add_text('Метод оценки:')
        dpg.add_radio_button(("Cтатистика", "Перцерптрон", "LSTM"), callback=radio, horizontal=True, tag="radio")
    with dpg.child_window(autosize_x=False, height=height_Goods+16,width=N_column*(width_Goods+10), horizontal_scrollbar =True):
        with dpg.group(horizontal=True, tag='product'):
            pass


# dpg.show_item_registry()
dpg.create_viewport(title='Buy with this product', width=N_column*(width_Goods+10)+50, height=1000)
dpg.setup_dearpygui()
dpg.set_primary_window('Window', True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()