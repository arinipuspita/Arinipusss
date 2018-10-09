from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests
import re

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('yedyEQI4iYlgdf6Y1NeXNIPCwtkRxDej+z9N/vn0vU80pGtpUO5UitOcQi98lIeVG7V/Dln4AcVtitVmOy4yuORb0T75x1HanlnOijX5xsSKtQGZoOp9Mt3BvLVntct/WG6kcpMnpVvOFkDRchw7ZQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a4f818fc0c5aa0b0b333c63def153323')
#===========[ NOTE SAVER ]=======================
notes = {}
#REQUEST DATA MHS dibawah notes = {}
def carimhs(nrp):
    URLmhs = "http://www.aditmasih.tk/api_arinip/view.php?nrp=" + nrp
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nrp = data['data_angkatan'][0]['nrp']
        nama = data['data_angkatan'][0]['nama']
        alamat = data['data_angkatan'][0]['alamat']

        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "nama : "+nama+"\nnrp : "+nrp+"\nalamat : "+alamat
        return data
        # return all_data

    elif(flag == "0"):
        return err

def inputmhs(nama, nrp, alamat):
    r = requests.post("http://www.aditmasih.tk/api_arinip/insert.php", data={'nama': nama, 'nrp': nrp, 'alamat': alamat})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nama+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'
    
def hapusmhs(nrp):
    r = requests.post("http://www.aditmasih.tk/api_arinip/delete.php", data={'nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'
    
def updatemhs(nrpLama,nrp,nama,kosan):
    URLmhs = "http://www.aditmasih.tk/api_arinip/view.php?nrp=" + nrpLama
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    nrp_lama=nrpLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api_arinip/update.php", data={'nrp': nrp, 'nama': nama, 'alamat': alamat, 'nrp_lama':nrp_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+nrp_lama+'berhasil diupdate\n'
        elif(flag == "0"):
            return 'Data gagal diupdate\n'

    elif(flag == "0"):
        return err

    
# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receive message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)

    data=text.split('-')
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carimhs(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2],data[3])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusmhs(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatemhs(data[1],data[2],data[3],data[4])))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text + ' ' + profile.display_name))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
