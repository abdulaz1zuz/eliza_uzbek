#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  eliza.py
#
#  a cheezy little Eliza knock-off by Joe Strout
#  with some updates by Jeff Epler
#  hacked into a module and updated by Jez Higgins
#----------------------------------------------------------------------

import string
import re
import random

class Eliza:
  def __init__(self):
    self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE), gPats))
    self.values = list(map(lambda x: x[1], gPats))

  #----------------------------------------------------------------------
  # translate: take a string, replace any words found in vocabulary.keys()
  #  with the corresponding vocabulary.values()
  #----------------------------------------------------------------------
  def translate(self, text, vocabulary):
    words = text.lower().split()
    keys = vocabulary.keys();
    for i in range(0, len(words)):
      if words[i] in keys:
        words[i] = vocabulary[words[i]]
    return ' '.join(words)

  #----------------------------------------------------------------------
  #  respond: take a string, a set of regexps, and a corresponding
  #    set of response lists; find a match, and return a randomly
  #    chosen response from the corresponding list.
  #----------------------------------------------------------------------
  def respond(self, text):
    # find a match among keys
    for i in range(0, len(self.keys)):
      match = self.keys[i].match(text)
      if match:
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        resp = random.choice(self.values[i])
        # we've got a response... stuff in reflected text where indicated
        pos = resp.find('%')
        while pos > -1:
          num = int(resp[pos+1:pos+2])
          resp = resp[:pos] + \
            self.translate(match.group(num), gReflections) + \
            resp[pos+2:]
          pos = resp.find('%')
        # fix munged punctuation at the end
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp
    return None

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "me"  : "you"
}

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as
#  %1, %2, etc.
#----------------------------------------------------------------------
gPats = [
 [r'Menga (.*) kerak',
  [ "Nima uchun sizga %1 kerak?",
    "Bu sizga %1 ni olishga yordam beradimi?",
    "Sizga %1 kerakmi?"]],

  [r'Nega siz ([^\?]*)\??',
  [ "Siz meni %1 emas deb o'ylaysizmi?",
    "Ehtimol, men %1 ga erishaman.",
    "Haqiqatan ham %1 qilishimni xohlaysizmi?"]],

  [r'Nega men ([^\?]*)\?? qila olmayman',
  [ "Siz %1 ga ega bo'lishingiz kerak deb o'ylaysizmi?",
    "Agar sizda %1 bo'lsa, nima qilgan bo'lardingiz?",
    "Bilmayman -- nega siz %1 qila olmaysiz?",
    "Siz haqiqatan ham sinab ko'rdingizmi?"]],

  [r'Men qila olmayman (.*)',
  [ "% 1 qila olmasligingizni qayerdan bilasiz?",
    "Ehtimol, agar urinib ko'rsangiz, %1 bo'lardi.",
    "% 1 uchun nima kerak?"]],

  [r'Men (.*)',
  [ "Menga %1 bo'lganingiz uchun keldingizmi?",
    "Siz qachondan beri %1siz?",
    "%1 bo'lishga qanday munosabatdasiz?"]],

  [r'I\'?m (.*)',
  [ "%1 bo'lish sizni qanday his qiladi?",
    "%1 bo'lish sizga yoqadimi?",
    "Nega menga %1 ekanligingizni aytasiz?",
    "Nega o'zingizni %1 deb o'ylaysiz?"]],

  [r'Siz ([^\?]*)\??',
  [ "Nega mening %1 ekanligim muhim?",
    "Agar men %1 bo'lmaganimda buni afzal ko'rasizmi?",
    "Ehtimol, siz meni %1 ekanligimga ishonasiz.",
    "Men %1 bo'lishim mumkin -- nima deb o'ylaysiz?"]],

  [r'Nima (.*)',
  [  "Nega so'rayapsiz?",
    "Buning javobi sizga qanday yordam beradi?",
    "Siz nima deb o'ylaysiz?"]],

  [r'Qanday qilib (.*)',
  [ "Qanday deb o'ylaysiz?",
    "Ehtimol, o'z savolingizga javob berarsiz."
    "Siz nimani so'rayapsiz?"]],

  [r'Chunki (.*)',
  [ "Bu haqiqiy sababmi?",
    "Yana qanday sabablar xayolga keladi?",
    "Bu sabab boshqa narsaga tegishlimi?",
    "Agar %1 bo'lsa, yana nima to'g'ri bo'lishi kerak?"]],

  [r'(.*) kechirasiz (.*)',
  [ "Ko'p hollarda kechirim so'rash kerak emas.",
    "Kechirim so'raganingizda qanday his-tuyg'ularni boshdan kechirasiz?"]],

  [r'Salom(.*)',
  [ "Salom... Bugun kelishingizdan xursandman.",
    "Salom... bugun qandaysiz?",
    "Salom, bugun o'zingizni qanday his qilyapsiz?"]],

  [r'Menimcha (.*)',
  [ "Siz %1 ga shubha qilyapsizmi?",
    "Siz haqiqatan ham shunday deb o'ylaysizmi?",
    "Ammo siz %1 ga ishonchingiz komil emasmi?"]],

  [r'(.*) dost (.*)',
  ["Do'stlaringiz haqida ko'proq gapiring.",
    "Do'st haqida o'ylaganingizda, xayolingizga nima keladi?",
    "Nega menga bolalikdagi do'stingiz haqida gapirmaysiz?"]],

  [r'Ha',
  ["Siz juda ishonchli ko'rinyapsiz.",
    "Yaxshi, lekin biroz tushuntirib bera olasizmi?"]],

  [r'(.*) kompyuter(.*)',
  ["Siz haqiqatan ham men haqimda gapiryapsizmi?",
    "Kompyuter bilan gaplashish g'alati tuyuladimi?",
    "Kompyuterlar sizni qanday his qiladi?",
    "Sizga kompyuter tahdid solayotganini his qilyapsizmi?"]],

  [r'Bu (.*)',
  [ "Siz bu %1 deb o'ylaysizmi?",
    "Ehtimol, bu %1 -- nima deb o'ylaysiz?",
    "Agar %1 bo'lsa, nima qilgan bo'lardingiz?",
    "Bu %1 bo'lishi mumkin."]],

  [r'Bu (.*)',
  ["Siz juda aniq ko'rinyapsiz.",
    "Agar men sizga bu %1 emasligini aytsam, nimani his qilgan bo'lardingiz?"]],

  [r'Men qila olmanami ([^\?]*)\? ni?',
  [ "Nima sizni %1 qila olmayman deb o'ylaysiz?",
    "Agar men %1 qila olsam, nima bo'ladi?",
    "Nega men %1 qila olamanmi?"]],

  [r'Bolishi mumkinmi ([^\?]*)\??',
  [ "Ehtimol, siz %1ni xohlamaysiz.",
    "% 1 ga ega bo'lishni xohlaysizmi?",
    "Agar sizda %1 bo'lsa edi?"]],

  [r'Sen (.*)',
  [ "Nega meni %1 deb o'ylaysiz?",
    "Meni %1 deb o'ylash sizni xursand qiladimi?",
    "Ehtimol, siz meni %1 bo'lishimni xohlarsiz.",
    "Ehtimol, siz haqiqatan ham o'zingiz haqingizda gapiryapsiz?"]],

  [r'Sen\'?re (.*)',
  [ "Nega men %1man deysiz?",
    "Nega meni %1 deb o'ylaysiz?",
    "Biz siz haqingizdami yoki men haqingizdami?"]],

  [r'men\'?t (.*)',
  [ "Siz haqiqatan ham %1 emasmisiz?",
    "Nega %1 emas?",
    "%1 istaysizmi?"]],

  [r'Men his qilaman (.*)',
  ["Yaxshi, menga bu his-tuyg'ular haqida ko'proq gapirib bering.",
    "Sizni tez-tez %1 his qilasizmi?",
    "Odatda qachon o'zingizni %1 his qilasiz?",
    "%1 ni his qilganingizda nima qilasiz?"]],

  [r'Menda (.*)',
  [ "Nega menga %1 borligini aytyapsiz?",
    "Sizda haqiqatan ham %1 bormi?",
    "Endi sizda %1 bor, keyin nima qilasiz?"]],

  [r'Men (.*) bolardim',
  [ "Nima uchun %1 ni tanlaganingizni tushuntirib bera olasizmi?",
    "Nima uchun siz %1?",
    "% 1 bo'lishini yana kim biladi?"]],

  [r'U borm (.*)',
  [ "Sizningcha, %1 bormi?",
    "Ehtimol, %1 mavjud.",
    "% 1 bo'lishini xohlaysizmi?"]],

  [r'Mening (.*)',
  [ "Ko'rdim, sizning %1.",
    "Nima uchun sizning %1 deyapsiz?",
    "% 1 bo'lsa, o'zingizni qanday his qilasiz?"]],  

  [r'(.*)\?',
  [ "Nega buni so'rayapsiz?",
    "Iltimos, o'zingizning savolingizga javob bera olasizmi yoki yo'qligini o'ylab ko'ring."
    "Balki javob o'zingizdadir?",
    "Nega menga aytmaysiz?"]],

  [r'Hayrr',
  ["Men bilan suhbatlashganingiz uchun tashakkur.",
    "Xayr.",
    "Rahmat, bu $150 bo'ladi. Kuningiz xayrli o'tsin!"]],

  [r'(.*)',
  ["Iltimos, menga ko'proq ma'lumot bering.",
    "Keling, diqqatni biroz o'zgartiraylik... Oilangiz haqida gapirib bering."
    "Bu haqda batafsil ma'lumot bera olasizmi?",
    "Nega buni %1 deyapsiz?",
    "Men ko'ryapman.",
    "Juda qiziqarli.",
    "% 1.",
    "Tushundim. Va bu sizga nimani anglatadi?",
    "Bu sizni qanday his qiladi?",
    "Buni aytganingizda o'zingizni qanday his qilasiz?"]]
  ]

#----------------------------------------------------------------------
#  command_interface
#----------------------------------------------------------------------
def command_interface():
  print('Men Ozbek tilida gaplasha oladigan Elizaman')
  print('Hayr amali bilan tugata olasiz.')
  print('='*72)
  print('Salom! Ahvollaringiz yaxshimi?')

  s = ''
  therapist = Eliza();
  while s != 'hayr':
    try:
      s = input('> ')
    except EOFError:
      s = 'hayr'
    print(s)
    while s[-1] in '!.':
      s = s[:-1]
    print(therapist.respond(s))


if __name__ == "__main__":
  command_interface()
