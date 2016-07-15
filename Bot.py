'''
Created on Jul 14, 2016

@author: Hosein
'''
token='212660892:AAEaF5jrzSV2alfi7F8-IZWZ4uO9WTxusEU'
import logging
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import telegram

UP_States={}
STARTED=0
WAITING=1
REGISTERED=2

users={}
def start(bot,update):
    bot.sendMessage(update.message.chat_id,text='Hi I started working so please set your username and password using commands then you can check your grades')
    UP_States[str(update.message.chat_id)]=STARTED

def setuserpass(bot,update):
    bot.sendMessage(update.message.chat_id,text='please enter username and password according to this template then send it to me. template:username-password')
    UP_States[str(update.message.chat_id)]=WAITING

def parsuserpass(bot,update):
    if UP_States[str(update.message.chat_id)]==WAITING :
        striped_message=update.message.text.strip()
        up_list=striped_message.split('-');
        if len(up_list)==2 :
            users[str(update.message.chat_id)]=up_list
            UP_States[str(update.message.chat_id)]=REGISTERED
            bot.sendMessage(update.message.chat_id,text='OK!');
                        
        else:
            bot.sendMessage(update.message.chat_id,text='Sorry.Somethig went wrong!');    
            UP_States[str(update.message.chat_id)]=WAITING

def check(bot,update):
    if UP_States[str(update.message.chat_id)]==REGISTERED:
            try:   
                login=Login.login(users[str(update.message.chat_id)])
                login.encryptUserPassword()
                login.logIn()
                html=login.html
                
                scpr=Scrapper.scrapper(html)
                scpr.make()
                bot.sendMessage(update.message.chat_id,text=scpr.text)
            except BaseException as ex :
                print (ex.args);
                bot.sendMessage(update.message.chat_id,text="An error has occured")
    else:
        bot.sendMessage(update.message.chat_id,text="Please set up username and password at first.")   
        
            

def main():
    updater=Updater(token)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("setuserpass",setuserpass))
    dp.add_handler(CommandHandler("check",check))
    dp.add_handler(MessageHandler([Filters.text], parsuserpass))
    updater.start_polling()
    updater.idle()
                   
if __name__=='__main__':
    main()
