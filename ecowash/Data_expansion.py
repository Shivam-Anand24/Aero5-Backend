#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


fabrication = pd.read_excel("Washing machine manufacturing company.xlsx",sheet_name = "fabrication")


# In[3]:


fabrication


# In[4]:


item_raw_material = fabrication.groupby('item')['raw material'].unique().to_dict()


# In[5]:


fabrication['raw material'].unique()


# In[6]:


raw_material_unit = {'sheet steel' : 'sqft', 'plastics' : 'kg', 'stainless steel' : 'kg/m3', ' plastic' : 'kg', '(enameling iron) Porcelain coating' : 'gauge', 'cast aluminum' : 'ingots', 'steel (enameling iron) Porcelain coating' : 'kg/m3', 'porcelain enamel' : 'gauge'}


# In[56]:


import random
import datetime


# In[57]:


def get_date(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    # generate a random date between start and end dates
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return str(random_date)


# In[58]:


get_date('2020-08-03','2023-01-03')


# In[10]:


for i in range (131, 40001):
    item = random.choice(list(item_raw_material.keys()))
    item_id = 'T'+str(i)
    raw_material = random.choice(item_raw_material[item])
    quantity = random.randint(3,30)
    unit = raw_material_unit[raw_material]
    if unit == 'ingots':
        quantity = unit + '—' + str(quantity)
    else:
        quantity = str(quantity) + ' ' + unit
    start_date = get_date('2020-01-01','2023-01-30')
    end_date = get_date(start_date, '2023-02-10')
    fabrication.loc[len(fabrication)] = [item, item_id, raw_material, quantity, start_date, end_date]


# In[11]:


fabrication.tail


# In[15]:


fabrication[fabrication['item id'] == "T1001"].iloc[0]['out date']


# In[28]:


sub_assembly = pd.read_excel("Washing machine manufacturing company.xlsx",sheet_name = "sub-assembly")


# In[30]:


sub_assembly.head


# In[32]:


date_string = '2020-04-10 00:00:00'
datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
sub_assembly = sub_assembly.drop(datetime_obj,axis = 1)

date_string = '2020-06-15 00:00:00'
datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
sub_assembly = sub_assembly.drop(datetime_obj,axis = 1)

date_string = '2020-06-24 00:00:00'
datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
sub_assembly = sub_assembly.drop(datetime_obj,axis = 1)

date_string = '2020-08-17 00:00:00'
datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
sub_assembly = sub_assembly.drop(datetime_obj,axis = 1)


# In[33]:


print(sub_assembly.columns)


# In[36]:


unique_process = list(sub_assembly['process'].unique())
unique_process


# In[40]:


unique_item_id = ['T','WM']


# In[73]:


sub_assembly.drop(42)


# In[84]:


a = 120
b = 165
c = 165
for i in range(3072, 40001):
    assembly_id = 'SAWM'+str(i)
    process = random.choice(unique_process)
    item_id = random.choice(unique_item_id)
    ide=''
    if a==121:
        a=a+1
    if item_id == 'T':
        ide = item_id+str(a)
        a=a+1
    else:
        ide = item_id+str(b)
        b=b+1
    machine_id = 'FA_WM'+str(c)
    c=c+1
    start_date=''
    if item_id == 'T':
        date_str = str(fabrication[fabrication['item id'] == ide].iloc[0]['out date'])
        date_str = date_str.split()[0]
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            try:
                date1 = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
                date = date1.strftime('%Y-%m-%d')
            except ValueError:
                    print('error')
        start_date = get_date(str(date),'2023-05-10')
    else:
        start_date = get_date('2020-08-03','2023-05-10')
    end_date = get_date(start_date,'2023-05-20')
    sub_assembly.loc[len(sub_assembly)] = [assembly_id, process, ide, machine_id, start_date, end_date]


# In[85]:


sub_assembly.tail


# In[86]:


assembly = pd.read_excel("Washing machine manufacturing company.xlsx",sheet_name = "assembly")


# In[87]:


assembly


# In[89]:


date_string = '2020-09-03 00:00:00'
datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
assembly = assembly.drop(datetime_obj,axis = 1)

date_string = '2020-11-30 00:00:00'
datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
assembly = assembly.drop(datetime_obj,axis = 1)

date_string = '2020-12-02 00:00:00'
datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
assembly = assembly.drop(datetime_obj,axis = 1)

date_string = '2021-02-02 00:00:00'
datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
assembly = assembly.drop(datetime_obj,axis = 1)


# In[90]:


assembly


# In[91]:


unique_process_assembly = list(assembly['process'].unique())
unique_process_assembly


# In[96]:


a = 3043
b = 169
for i in range(3020115,3041000):
    process = random.choice(unique_process_assembly)
    a = random.randint(a,a+3)
    process_id = 'SAWM'+str(a)+'_FA_WM'+str(b)
    b = b+1
    machine_id = 'MAII1017ECME'+str(i)
    #print('SAWM',a)
    date_str = str(sub_assembly[sub_assembly['Assembly ID'] == 'SAWM'+str(a)].iloc[0]['end date'])
    date_str = date_str.split()[0]
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        try:
            date1 = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
            date = date1.strftime('%Y-%m-%d')
        except ValueError:
                print('error')
    start_date = get_date(str(date),'2023-05-25')
    end_date = get_date(str(start_date), '2023-05-30')
    assembly.loc[len(assembly)] = [process, process_id, machine_id, start_date, end_date]


# In[106]:


fabrication.to_csv('fabrication_.csv', index=False)
sub_assembly.to_csv('sub_assembly_.csv', index=False)
assembly.to_csv('assembly_.csv', index=False)


# In[ ]:




