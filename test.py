#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *

superAdmin = {
    u'标admin', # name of super users who want to get notify
    u'果果admin'
};
notifyGroupName = u"金智宝贝内勤队"
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
                print name.encode("utf8"), uid
            pass
        pass
        self.notifyToGroup = self.get_user_id(notifyGroupName)
        if self.notifyToGroup:
            print "Our Group:", notifyGroupName.encode("utf8"), self.notifyToGroup
    def handle_msg_all(self, msg):
        # print "Content", msg['content']
        # print "User:", msg['user']
        # print "Msg", msg
        if not self.handleMoneyInfo(msg):
            if msg['msg_type_id'] == 4:
                # if  msg['user']['id'] in self.superUser :
                #     print "!!!!! from ADMIN !!!!!";
                if not self.handleCommad(msg):
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
            if (contentType == 3 or contentType == 6):
                if file_name:
                    self.sendToAdmin(fromUid, fowordPic % (fromName), file_name, True)
                else:
                    self.sendToAdmin(fromUid, fowordPic % (fromName) + "动画表情")
            elif contentType == 4 :
                self.sendToAdmin(fromUid, fowordVoice % (fromName), file_name)
                pass
            elif file_name:
                self.sendToAdmin(fromUid, fowordFile % (fromName), file_name)
            else :
                self.sendToAdmin(fromUid, fowordOther % (fromName, msg['content']))
                pass
        elif contentType == 7 :
            msg = u"%s分享了一个%s链接（来源：%s）\n%s\n%s" % \
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
    def sendToAdmin(self, fromUid, text=None, file_name = None, is_pic = False, to_group = True):
        # fromUid = None
        if text:
            for au in self.superUser:
                if (fromUid != au):
                    self.send_msg_by_uid(text, au)
                pass
            if to_group:
                self.send_msg_by_uid(text, self.notifyToGroup)
        if file_name:
            file_name = os.path.join(self.temp_pwd,file_name)
            for au in self.superUser:
                if (fromUid != au):
                    if is_pic:
                        self.send_img_msg_by_uid(file_name, au)
                        if to_group:
                            self.send_img_msg_by_uid(file_name, self.notifyToGroup)
                    else:
                        self.send_file_msg_by_uid(file_name, au)
                        if to_group:
                            self.send_file_msg_by_uid(file_name, self.notifyToGroup)
                pass

        pass
    def handleMoneyInfo(self, msg):
        fromUid = msg['user']['id'];
        fromName = msg['user']['name'];
        say = None
        if 'sub_type' in msg['content']:
            if msg['content']['sub_type'] == 'payf2f':
                say = "\n".join(msg['content']['sub_data'])
            if msg['content']['sub_type'] == 'transfer_money':
                say = "\n".join(msg['content']['sub_data'])
                say = u'%s发起%s\n需要在手机上点击的确认。' %(fromName, say);
        if msg['content']['type'] == 12 and u'红包' in msg['content']['data']:
            say = u'%s发来红包，需要在手机上点击领取。' %(fromName);
        pass
        if say :
            self.sendToAdmin(fromUid, say, to_group=True)
            return True;
        return False;
'''
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''
# @staticmethod
def search_content(key, content, fmat='attr', withTag=False):
    returnValue = None;
    if fmat == 'attr':
        pm = re.search(key + '\s?=\s?"([^"<]+)"', content)
        if pm:
            returnValue = pm.group(1)
    elif fmat == 'xml':
        if not withTag:
            pm = re.search('<{0}>([^<]+)</{0}>'.format(key), content)
            if pm:
                returnValue = pm.group(1)
        else :
            pm = re.search('<{0}>(.*?)</{0}>'.format(key), content)
            if pm:
                returnValue = pm.group(1)

        if type(key) == list:
            mostInner ='<{0}>(.*?)</{0}>'
            if len(key) == 1:
                rex = mostInner.format(key[0])
                matches = re.findall(rex, content)
                return matches;
            else:
                key.reverse()
                outer = '<{0}>.*?{1}.*?</{0}>'
                rex = None;
                for keyname in key:
                    if not rex:
                        rex = mostInner.format(keyname)
                    else :
                        rex = outer.format(keyname, rex)
                    pass
                pm = re.search(rex, content)
                if pm:
                    returnValue = pm.group(1)
    if returnValue :
        cdr = '^<!\[CDATA\[(.*?)]]>$'
        pm = re.search(cdr, returnValue)
        if pm:
            return pm.group(1)
        else:
            return returnValue
    return 'unknown'
def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
    bot.is_big_contact = False   #如果确定通讯录过大，无法获取，可以直接配置，跳过检查。假如不是过大的话，这个方法可能无法获取所有的联系人
    bot.run()


if __name__ == '__main__':
    main()
