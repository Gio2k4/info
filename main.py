from keep_alive import keep_alive

keep_alive()
import requests, datetime, re
from telebot import types, TeleBot

TOKEN_FB = 'EAABwzLixnjYBO9QxEjKBZAkaEdGBUoaa3tLvMsdBDfVhn04IDwFjZA2FvvoJKKpwDfO3cPqab6GR2AtLG2L8q3a8CH3P3lMixUG0UBpxXCEdip8uFE1yL0E76VXH4ffx1uCGMmD1NlCi3ZCpamQEXyua5P9qQfXX3hhcFiQogNzMN32wXJLVXNLniSyUBCGaJUZD'
bot = TeleBot('6022112349:AAHsE3sZYHZzQzAQBi9vFXCzpHXZYiEBO2U')
keyboard1 = types.InlineKeyboardMarkup(row_width=1)
keyboard1.add(types.InlineKeyboardButton("Contact", callback_data='ct'))


@bot.message_handler(commands=['start', 'help'])
def hello(message):
  user = message.from_user.username
  bot.reply_to(
      message,
      f"@{user} Xin chào, tôi là bot Get Info Facebook.\nSử dụng /checkinfo + [link fb] để kiểm tra thông tin Facebook",
      reply_markup=keyboard1)


def wind(cc, user, msg):

  def find_id(cc):
    headers = {
        'authority': 'id.traodoisub.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language':
        'vi-VN,vi;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-AU;q=0.6,en;q=0.5,fr-FR;q=0.4,fr;q=0.3,en-US;q=0.2',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://id.traodoisub.com',
        'referer': 'https://id.traodoisub.com/',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent':
        'Mozilla/5.0 (Linux; Android 12; SM-A037F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'link': cc,
    }
    response = requests.post('https://id.traodoisub.com/api.php',
                             headers=headers,
                             data=data).json()
    # bot.reply_to(msg, str(response))
    try:
      if response['code'] == 200:
        id = response['id']
        bot.reply_to(msg, f"@{user} Get Thành Công Uid: {id}")
      else:
        check = re.findall(r'id=(\d+)', cc)
        if len(check) == 2 or len(check) == 1:
          id = check[0]
        elif check == []:
          try:
            id = cc
            afk = int(id)
          except:
            return False
        else:
          return False
      return id
    except:
      return False

  id = find_id(cc)
  if not id:
    bot.reply_to(msg, f"@{user} Vui lòng kiểm tra lại link Facebook!")
    return
  field = 'name, location, hometown, gender, birthday, subscribers, relationship_status, locale, about, website'
  check = requests.get(
      f'https://graph.facebook.com/{id}?fields={field}&access_token={TOKEN_FB}'
  ).json()
  try:
    if 'name' in str(check): ten = check['name']
    else: ten = None
    if 'location' in str(check): lct = check['location']['name']
    else: lct = None
    if 'hometown' in str(check): htw = check['hometown']['name']
    else: htw = None
    if 'gender' in str(check): gth = check['gender']
    else: gth = None
    if 'birthday' in str(check): birth = check['birthday']
    else: birth = None
    if 'subscribers' in str(check):
      sub = check['subscribers']['summary']['total_count']
    else:
      sub = None
    if 'relationship_status' in str(check): rela = check['relationship_status']
    else: rela = None
    if 'locale' in str(check): loc = check['locale']
    else: loc = None
    if 'about' in str(check): abo = check['about']
    else: abo = None
    if 'website' in str(check): web = check['website']
    else: web = None
  except:
    bot.reply_to(msg, f"@{user} Vui lòng kiểm tra lại link Facebook!")
    return
  decs = (f"""@{user} Check thành công !!!
📌 Thông tin ID: {id} 📌
    👤 Họ và tên: {ten}
    👥 Giới tính: {gth}
    👪 Ngày sinh (tháng/ngày): {birth}
    💟 Tình trạng: {rela}
    📍 Vị trí: {lct}
    🏡 Quê quán: {htw}
    🌎 Quốc Tịch: {loc}
    🕵️ About: {abo}
    🌐 Website: {web}
    💚 Có: {sub} người theo dõi """)
  bot.send_photo(
      msg.chat.id,
      f'https://graph.facebook.com/{id}/picture?height=720&width=720&access_token=6628568379%7Cc1e620fa708a1d5696fb991c1bde5662',
      caption=decs)


@bot.message_handler(commands=['checkinfo'])
def info(message):
  user = message.from_user.username
  try:
    args = message.text.split(' ', 1)[1]
  except:
    bot.reply_to(message, f"@{user} Sử dụng /checkinfo + link fb")
    return
  bot.reply_to(message, f"@{user} Vui lòng chờ..")
  wind(args, user, message)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  if call.data == 'ct':
    bot.send_message(
        chat_id=call.message.chat.id,
        text=
        '💬 Liên hệ với Admin Bot:\n[Telegram](https://t.me/wind_2004) | [Facebook](https://www.facebook.com/profile.php?id=100028127719093)',
        parse_mode='Markdown')


bot.polling()
