#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *

superAdmin = {

};
fowordMsg = u"%s 说：\n---------\n%s"
fowordPic = u"%s 发来图片："
fowordVoice = u"%s 发来语音："
fowordFile = u"%s 发来文件："
fowordOther = u"%s 发来：%s"



class MyWXBot(WXBot):
    def got_contact(self):
        self.superUser = []
        print "Super users:"
        for name in superAdmin:
            uid = self.get_user_id(name)
            if uid:
                self.superUser.append(uid);
                print name, uid
            pass
        pass
    def handle_msg_all(self, msg):
        print "Content", msg['content']
        print "User:", msg['user']
        print "Msg", msg
        if msg['msg_type_id'] == 4:
            pass
            if  msg['user']['id'] in self.superUser :
                print "!!!!! from ADMIN !!!!!";
                if not self.handleCommad(msg):
                    if not self.handleMoneyInfo(msg):
                        self.handleFoword(msg);

            # if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            #   self.send_msg_by_uid(u'hi', msg['user']['id'])
            #     self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            #     self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
    def handleCommad(self, msg):
        pass 
        return False;
    def handleFoword(self, msg):
        fromUid = msg['user']['id'];
        fromName = msg['user']['name']
        content = msg['content']['data'];
        contentType = msg['content']['type'];
        file_name = msg['content']['file_name'] if "file_name" in msg['content'] else None;
        if contentType == 0:
            self.sendToAdmin(fromUid, fowordMsg % (fromName, content))
        elif contentType in [3, 4, 6, 8, 13]:
            if contentType == 3 :
                self.sendToAdmin(fromUid, fowordPic % (fromName), file_name)
            elif contentType == 4 :
                self.sendToAdmin(fromUid, fowordVoice % (fromName), file_name, False)
                pass
            elif file_name:
                self.sendToAdmin(fromUid, fowordFile % (fromName), file_name, False)
            else :
                print msg['content']['data']
                self.sendToAdmin(fromUid, fowordOther % (fromName, msg['content']))
                pass
        elif contentType == 7 :
            msg = u"%s分享了一个%s来源%s\n%s\n%s" % \
            (fromName, content['type'], content['from'], content['title'], content['desc'])
            self.sendToAdmin(fromUid, msg)
            self.sendToAdmin(fromUid, content['url'])
            pass
        elif contentType == 5 :
            msg = u"%s分享了一张名片\n昵称：%s 性别：%s" % \
            (fromName, content['nickname'], content['genderCN'])
            self.sendToAdmin(fromUid, msg)
            pass
            # self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            # self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
        pass
        return False;
    def sendToAdmin(self, fromUid, text=None, file_name = None, is_pic = True):
        if text:
            for au in self.superUser:
                if (fromUid != au):
                    self.send_msg_by_uid(text, au)    
                pass
        if file_name:
            file_name = os.path.join(self.temp_pwd,file_name)
            for au in self.superUser:
                if (fromUid != au):
                    if is_pic:
                        self.send_img_msg_by_uid(file_name, au)
                    else:
                        self.send_file_msg_by_uid(file_name, au)
                pass
            
        pass
    def handleMoneyInfo(self, msg):
        pass
        return False;
'''
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.is_big_contact = False   #如果确定通讯录过大，无法获取，可以直接配置，跳过检查。假如不是过大的话，这个方法可能无法获取所有的联系人
    bot.run()


if __name__ == '__main__':
    main()
