#!/usr/bin/env python3
# coding: utf-8

import logging

from wxpy import *

import csv
groups = {}
reader = csv.reader(open('groupkeys.csv', 'r'))
for k,v in reader:
    groups[k] = v
print(groups)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bot = Bot(console_qr=2, qr_path='qrcode.png' )
#if bot.self.nick_name == 'Joyi':
#    raise ValueError('Wrong User!')

    tuling = Tuling()


def matchGroup(msg):
    if msg.text in groups:
        return groups[msg.text]
    else:
        return None


def invite(user,group_name):
    group = ensure_one(bot.groups().search(group_name))
    if user in group:
        logger.info('{} is already in {}'.format(user, group))
        user.send('你已经加入 {} 啦,不需要再次加入了'.format(group.nick_name))
    else:
        logger.info('inviting {} to {}'.format(user, group))
        group.add_members(user, use_invitation=False)
        user.send('已经把你加入 {} 啦'.format(group.nick_name))


@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    user = msg.card.accept()
    group_name = matchGroup(msg)
    if group_name:
        invite(user, group_name)
    else:
        user.send('你忘了写加群口令啦，快回去看看口令是啥~')


@bot.register(Friend, msg_types=TEXT)
def exist_friends(msg):
    group_name = matchGroup(msg)
    if group_name:
        invite(msg.sender, group_name)
    else:
        tuling.do_reply(msg)


bot.start(False)
embed()
