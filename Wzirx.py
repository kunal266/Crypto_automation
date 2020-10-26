# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import pandas as pd
import numpy as np
import smtplib


# %%
buying_Price = int(input("Input buying price in INR for BTC: "))


# %%
Selling_Price = int(input("What should be your selling price for BTC: "))


# %%
Volume = input("Enter the Volume of the BTC-INR: ")
Volume = float(Volume)


# %%
final_buying_price = (buying_Price)*Volume


# %%
final_selling_price = (Selling_Price)*Volume


# %%
makers_fee = 0.002*(buying_Price)*(Volume)


# %%
takers_fee = 0.002*(Selling_Price)*(Volume)


# %%
Final_fee = makers_fee+takers_fee


# %%
Profit_inc = (Selling_Price - buying_Price)*Volume
Profit_per = (Profit_inc/buying_Price)*100


# %%
Profit_Final = Profit_inc - Final_fee


# %%
url = "https://api.wazirx.com/api/v2/trades?market=btcinr"


# %%
response = requests.get(url)


# %%
response.status_code


# %%
data = response.json()[1]


# %%
response = requests.get(url)
data = response.json()[1]


# %%
with open("BTC_INR.csv","a+") as fp:
    fp.write(f"\n{data['market']},{buying_Price},{Selling_Price},{data['price']},{Profit_inc},{Profit_Final},{data['created_at']},{data['volume']},{data['funds']},{data['id']}")


# %%
sender_email = "SENDER_EMAIL"
rec_mail = "RECEIVER_EMAIL"
password = "PASSWORD"


# %%
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(sender_email,password)


# %%
while True:
    response = requests.get(url)
    data = response.json()[1]
    df = pd.read_csv('BTC_INR.csv', index_col=0)
    cur_Profit_inc = (float(data['price']) - buying_Price)*Volume
    cur_Profit_per = (Profit_inc/buying_Price)*100
    cur_makers_fee = 0.002*(buying_Price)*(Volume)
    cur_takers_fee = 0.002*(float(data['price']))*(Volume)
    cur_Final_fee = cur_makers_fee + cur_takers_fee
    cur_Profit_Final = cur_Profit_inc - cur_Final_fee
    if (data["id"] !=  df.iloc[-1,-1]):
        with open("BTC_INR.csv","a+") as fp:
            fp.seek(0,0)
            if (float(data['price'])>= 0.98*(Selling_Price)):
                message = f"""
                The price is close to your desired Selling Price
                Current Price: {float(data['price'])}
                Current Profit: {cur_Profit_inc}
                Current Final Fee: {cur_Final_fee}
                Current Profit Final: {cur_Profit_Final}
                """
                server.sendmail(sender_email,rec_mail,message)
            if (float(data['price']) <= 1.02*(buying_Price)):
                message = f"""
                The price is close to your desired Buying Price
                Current Price: {float(data['price'])}
                Current Final Fee: {0.002*(float(data['price']))*(Volume)}
                """
                server.sendmail(sender_email,rec_mail,message)
            fp.write(f"\n{data['market']},{buying_Price},{Selling_Price},{data['price']},{cur_Profit_inc},{cur_Profit_Final},{data['created_at']},{data['volume']},{data['funds']},{data['id']}")