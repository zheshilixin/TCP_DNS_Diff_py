# -*- coding: utf-8 -*-
false = False
true  = True

class find_path(object):
    def __init__(self,target):
        self.target=target     #查询的字典/列表

    def find_the_key(self, target, key, path_list=None):
        '''输入：只是用来查询目的key所在的dict；输出：然后以dict作为value 调用find_dict 查询
        '''
        if isinstance(target, dict):  # 判断了它是字典
            dict1 = target.copy()
            for k, v in dict1.items():
                if str(key) == str(k):
                    path = str([k])
                    self.find_dict_path(self.target, dict1, path, path_list)
                else:
                    self.find_the_key(v, key, path_list)  # 此key不是所查找的，那么调用自身遍历这个v，看所找的key是否在里面

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            list1 = target.copy()
            for i in list1:
                self.find_the_key(i, key, path_list) # 调用自身遍历这个I，看所找的key是否在里面


    def find_in_value(self,target, value, path='',path_list=None):
        '''查询的value只能是str/int，遍历字典跟列表，
        如果里面的元素是str，那么就判断该元素是否包含value(包含匹配)，
                           如果是是的话，那么就把当前的元素所在的dict/list当作关键字用find_dict查询
        如果元素不是str，那么继续循环自身'''
        if isinstance(target, dict):  # 判断了它是字典
            dict1 = target.copy()
            for k, v in dict1.items():
                if isinstance(v, (str, int)) : #当字典的v是str时才进一步判断
                    if  str(value) in str(v):  # 如果某个value就是要找的，就把k放进path，
                        path1 = path
                        path1 = str([k]) + path1#把此v所在的dict作为所查找的value，调用find_dict得到路径path
                        self.find_dict_path(self.target, dict1, path1, path_list)
                else:
                    self.find_in_value(v, value, path, path_list)#此v可能是dict/list，调用自身确认里面是否有所查询的value

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            list1 = target.copy()
            for i in list1:
                if isinstance(i, (str, int)) :#当列表的i是str时才进一步判断
                    if str(value) in str(i):
                        path1 = path
                        posi = list1.index(i)
                        path1 = '[%s]' % posi + path1 #把此i所在的list作为所查找的value，调用find_dict得到路径path
                        self.find_dict_path(self.target, list1, path1, path_list)
                else:
                    self.find_in_value(i, value, path, path_list) #此i可能是dict/list，调用自身确认里面是否有所查询的value

    def find_the_value(self,target, value, path='',path_list=None):
        '''上同，差别在于 这个是”完全匹配“'''
        if isinstance(target, dict):
            dict1 = target.copy()
            for k, v in dict1.items():
                if isinstance(v, (str, int)) :
                    if  str(value) ==str(v):   #必须完全相同
                        path1 = path
                        path1 = str([k]) + path1
                        self.find_dict_path(self.target, dict1, path1, path_list)
                else:
                    self.find_the_value(v, value, path, path_list)

        elif isinstance(target, (list, tuple)):
            list1 = target.copy()
            for i in list1:  # 遍历列表
                if isinstance(i, (str, int)) :
                    if str(value)== str(i):  #必须完全相同
                        path1 = path
                        posi = list1.index(i)
                        path1 = '[%s]' % posi + path1
                        self.find_dict_path(self.target, list1, path1, path_list)
                else:
                    self.find_the_value(i, value, path, path_list)


    def find_dict_path(self,target, value, path='',path_list=None):
        '''查询的value只能是dict/list整体，str类型不能再这里验证，这是最后步骤'''

        if self.target==value:
            path_list.append(path) if path not in path_list else None

        elif isinstance(target, dict):  # 判断了它是字典
            dict1 = target.copy()
            for k, v in dict1.items():
                if isinstance(v, (list, tuple,dict)) :  #只有当v是dict/list时才判断
                    if value == v:  # 如果某个value就是要找的，就把k放进path，然后把这个字典作为新的value循环
                        path1=path
                        path1=str([k])+path1
                        self.find_dict_path(self.target, dict1, path1,path_list)
                    else:
                        self.find_dict_path(v, value, path,path_list)  # 此值v不是要找的，那么遍历这个v，看所找的value是否在里面

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            list1 = target.copy()
            for i in list1:  # 遍历列表
                if isinstance(i, (list, tuple, dict)):  #只有当v是dict/list时才判断
                    if i == value:  # 如果某个元素就是要找的，就把posi放进path，然后把这个列表作为新的value循环
                        path1 = path
                        posi = list1.index(i)
                        path1 = '[%s]'%posi + path1
                        self.find_dict_path(self.target, list1, path1,path_list)
                    else:
                        self.find_dict_path(i, value, path,path_list)  # 此元素不是要找的，那么遍历这个i，看所找的value是否在里面


    def in_value_path(self,value):
        '''包含匹配value'''
        path_list=[]
        self.find_in_value(self.target, value,path_list=path_list)
        return path_list

    def the_value_path(self,value):
        '''完全匹配value'''
        path_list=[]
        self.find_the_value(self.target, value,path_list=path_list)
        return path_list

    def the_key_path(self,value):
        '''只查找key'''
        path_list = []
        self.find_the_key( self.target, value,path_list=path_list)
        return path_list

if __name__ == '__main__':
    dict1 = {
    "a": 5,
    "recommend_summoner_skill_tips": "闪现：向指定方向位移一段距离",
    "text_price": "",
    "be_restrained_hero": [
        {
            "hero_id": "3",
            "name": "赵云",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005ecc2eda6.png"
        },
        {
            "hero_id": "24",
            "name": "宫本武藏",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005ee432c52.png"
        },
        {
            "hero_id": "39",
            "name": "韩信",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005eff2e35f.png"
        }
    ],
    "rec_inscriptions": [
        {
            "title": "four",
            "list": [
                {
                    "name": "阳炎",
                    "icon": "http://pictest.wankacn.com/2017-04-27_5901c32aec40d.png",
                    "attrs": "法术攻击+2.5|法术穿透+1.4",
                    "level": "4"
                },
                {
                    "text": 10
                },
                {
                    "name": "渴血",
                    "icon": "http://pictest.wankacn.com/2017-04-27_5901c33051946.png",
                    "attrs": "法术攻击+1.4|法术吸血+0.8%|法术防御+1.6",
                    "level": "4"
                },
                {
                    "name": "侵蚀",
                    "icon": "http://pictest.wankacn.com/2017-04-27_5901c3367da4c.png",
                    "attrs": "法术攻击+0.9|法术穿透+3.8",
                    "level": "4"
                }
            ]
        },
        {
            "title": "five",
            "list": [
                {
                    "name": "圣人",
                    "icon": "http://pictest.wankacn.com/2017-04-27_5901c32b7c6eb.png",
                    "attrs": "法术攻击+5.3",
                    "level": "5"
                },
                {
                    "name": "轮回",
                    "icon": "http://pictest.wankacn.com/2017-04-27_5901c3325134d.png",
                    "attrs": "法术攻击+2.4|法术吸血+1%",
                    "level": "5"
                },
                {
                    "name": "怜悯",
                    "icon": "http://pictest.wankacn.com/2017-04-27_5901c3384f95c.png",
                    "attrs": "冷却缩减-1%",
                    "level": "5"
                }
            ]
        }
    ],
    "skill_list": [
        {
            "attrs": [ ],
            "intro": "被动",
            "description": "被动：王昭君脱离战斗后会获得可抵免450<span style=\"color:#6edbc8\">(+52%法术加成)</span>点伤害的寒冰护盾，护盾破裂时对附近敌人造成一次冰霜冲击，造成450<span style=\"color:#6edbc8\">(+52%法术加成)</span>点<span style=\"color:#7575d9\">法术伤害</span>与减速效果；寒冰护盾有3秒的回复冷却时间",
            "mana_cost": "",
            "cd": "",
            "tags": "法术",
            "name": "冰封之心",
            "icon": "http://pic.wankacn.com/2017-08-28_59a37c3ac17e6.png"
        },
        {
            "attrs": [
                "基础伤害|400|480|560|640|720|800"
            ],
            "intro": "主升",
            "description": "王昭君操控碎裂冰晶绽开，对范围内的敌军造成400<span style=\"color:#6edbc8\">(+65%法术加成)</span>点<span style=\"color:#7575d9\">法术伤害</span>与减速，并获得他们的视野持续2秒",
            "mana_cost": "80",
            "cd": "5",
            "tags": "法术/控制",
            "name": "凋零冰晶",
            "icon": "http://pic.wankacn.com/2017-08-28_59a37c3de40b4.png"
        },
        {
            "attrs": [
                "基础伤害|250|280|310|340|370|400",
                "冷却时间|10|9.2|8.4|7.6|6.8|6"
            ],
            "intro": "副升",
            "description": "王昭君引领寒霜之力，一定时间后将范围内敌人冰冻并造成250<span style=\"color:#6edbc8\">(+47%法术加成)</span>点<span style=\"color:#7575d9\">法术伤害</span>；被动：对被冰冻的敌人造成额外250<span style=\"color:#6edbc8\">(+50%法术加成)</span>点<span style=\"color:#7575d9\">法术伤害</span>",
            "mana_cost": "80",
            "cd": "8",
            "tags": "法术/控制",
            "name": "禁锢寒霜",
            "icon": "http://pic.wankacn.com/2017-08-28_59a37c4140712.png"
        },
        {
            "attrs": [
                "基础伤害|300|375|450",
                "冷却时间|50|45|40"
            ],
            "intro": "有大点大",
            "description": "王昭君召唤寒冬之力，在指定位置降下暴风雪对范围内敌人每次打击造成300<span style=\"color:#6edbc8\">(+50%法术加成)</span>点<span style=\"color:#7575d9\">法术伤害</span>与减速，期间获得600护甲加成",
            "mana_cost": "150",
            "cd": "50",
            "tags": "法术/控制",
            "name": "凛冬已至",
            "icon": "http://pic.wankacn.com/2017-08-28_59a37c4495707.png",
            "text": "what"
        }
    ],
    "skill_tips": "使用凋零冰晶使对方减速后再其移动方向的前方一小段距离使用禁锢寒霜。接着立刻贴近使用凛冬已至，配合被动对敌方打出成吨伤害",
    "hero_id": "40",
    "half_img": "http://pic.wankacn.com/2017-08-28_59a3840dd8625.png",
    "recommend_summoner_skill": [
        {
            "name": "闪现",
            "icon": "http://pictest.wankacn.com/2017-04-27_5901deac66009.jpeg",
            "description": "120秒CD：向指定方向位移一段距离"
        }
    ],
    "ticket_price": "588",
    "type": [
        "2"
    ],
    "big_img": "http://pic.wankacn.com/2017-08-28_59a38313260bb.png",
    "restrained_hero": [
        {
            "hero_id": "10",
            "name": "刘禅",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005ed4dfde6.png"
        },
        {
            "hero_id": "23",
            "name": "典韦",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005ee344db8.png"
        },
        {
            "hero_id": "48",
            "name": "亚瑟",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005f0e9459e.png"
        }
    ],
    "gold_price": "8888",
    "levels": {
        "attack": "3",
        "skill": "10",
        "survival": "2",
        "difficulty": "6"
    },
    "name": "王昭君",
    "hero_tips": "灵巧走位。尽量不要离敌方太近和太远，太近容易被贴身打击。太远冰冻住以后还没过去对方就解冻了。最好是等待别人与我方火并不能抽身离开时使用禁锢寒霜，给对方一个意想不到的绝望",
    "equip_choice": [
        {
            "title": "KPL职业出装",
            "description": "这是KPL职业联赛中AG超玩会.老帅的出装。暴力输出，需要注意入场时机。",
            "list": [
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166adc5c9.jpeg",
                    "equip_id": "40"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_59031675e2f15.jpeg",
                    "equip_id": "75"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166b10ebe.jpeg",
                    "equip_id": "41"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166b83498.jpeg",
                    "equip_id": "43"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166c6d0eb.jpeg",
                    "equip_id": "48"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166c96be0.jpeg",
                    "equip_id": "49",
                    "text2": "what"
                }
            ]
        },
        {
            "title": "KPL职业出装",
            "description": "这是KPL职业联赛中QGhappy.Cat的出装。团队收益装备，梦魇之牙克制地方回血英雄。",
            "list": [
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166ab272c.jpeg",
                    "equip_id": "39"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_59031676397b3.jpeg",
                    "equip_id": "76"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166adc5c9.jpeg",
                    "equip_id": "40"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166b10ebe.jpeg",
                    "equip_id": "41"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166b5c100.jpeg",
                    "equip_id": "42"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166c96be0.jpeg",
                    "equip_id": "49"
                }
            ]
        },
        {
            "title": "强力消耗装",
            "description": "这套装备靠减CD及回蓝，消耗对面英雄。冰霜法杖便宜、增加血量，可以让王昭君更稳健地对线，被动减速配合王昭君2技能很容易创造杀敌机会。",
            "list": [
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166c42ac0.jpeg",
                    "equip_id": "47"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_59031676397b3.jpeg",
                    "equip_id": "76"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166bda9f0.jpeg",
                    "equip_id": "45"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166b10ebe.jpeg",
                    "equip_id": "41"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166bb25f7.jpeg",
                    "equip_id": "44"
                },
                {
                    "icon": "http://pictest.wankacn.com/2017-04-28_5903166c96be0.jpeg",
                    "equip_id": "49"
                }
            ]
        }
    ],
    "waht": 10,
    "partner_hero": [
        {
            "hero_id": "2",
            "name": "小乔",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005ecad0a65.png"
        },
        {
            "hero_id": "5",
            "name": "妲己",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005ecec7ee2.png"
        },
        {
            "hero_id": "30",
            "name": "武则天",
            "icon": "http://pictest.wankacn.com/2017-04-26_59005eed6c76f.png"
        }
    ],
    "melee_tips": "在团战开始前期的迂回还没开始火并的时候跟在团后面用凋零冰晶对敌方进行骚扰和消耗，待开团开始后往人堆里放禁锢寒霜。总能冻住两个以上。接着使用凛冬已至再闪现过去。给对方一个沉重的打击。禁锢寒霜尽量瞄准输出类英雄那样才能凸显凛冬已至的爆炸伤害的效果",
    "history_intro": "昭君，西汉元帝时宫人。《汉书·元帝纪》记载：竟宁元年春，匈奴乎韩邪单于来朝，元帝赐单于待诏掖庭王樯为阏氏。《后汉书》又记王昭君，字嫱。她和亲匈奴后，号“宁胡阏氏”。",
    "background_story": "北方草原上，生活着凶悍的北夷部族，时常冲击长城进行掠夺。陷入内乱的诸侯们不得不送去粮食，布匹与和亲的公主换来停战协议。 北夷人将公主送往圣地——凛冬之海，献祭给神明作为新娘。久而久之，这演变成一项残忍神圣的传统。 然而数百年后，统治者们认为不再需要盟约，开始谋划残酷的阴谋：他们乘人们举行祭典毫无防备之际血洗草原，还想夺取蛮夷们献给神明的宝藏。 刽子手们如愿以偿。他们发出欢呼，忙碌着将成堆黄金带回中原。暴风雪突如其来，随之是浩大的雪崩。 是北夷人神明的愤怒吗？刚刚还不可一世的士兵哀嚎着逃窜。然而归去的路已被冰雪封锁。他们像琥珀中的小虫般挣扎，眼睁睁看着自己的身躯被冰封进透明的棺材。 幸存的北夷人从藏身之处走出来，簇拥着他们的公主——王昭君。她高雅，美丽，明亮的双眸饱含哀伤，纤长的手指拂过故乡来客们冰冷狰狞的脸庞。告诉我，故乡的梅花开了吗？",
    "skin_imgs": [
        {
            "skin_name": "冰雪之华",
            "big_img": "http://pic.wankacn.com/2017-08-29_59a4cf96438b3.jpeg"
        },
        {
            "skin_name": "精灵公主",
            "big_img": "http://pic.wankacn.com/2017-08-29_59a4cfaca937b.jpeg"
        },
        {
            "skin_name": "偶像歌手",
            "big_img": "http://pic.wankacn.com/2017-08-29_59a4cfc62223c.jpeg"
        },
        {
            "skin_name": "凤凰于飞",
            "big_img": "http://pic.wankacn.com/2017-08-29_59a4cfd3af958.jpeg"
        },
        {
            "skin_name": "幻想奇妙夜",
            "big_img": "http://pic.wankacn.com/2018-03-12_5aa63988e13e9.jpeg"
        }
    ],
    "title": "冰雪之华",
    "diamond_price": "0"
}

    a = find_path(dict1)
    in_value_path = a.in_value_path('基础伤害')  # 包含匹配，只要dict/list的元素中包含这个str，就能得到对应的path
    the_value_path = a.the_value_path('40')  # 完全匹配，只要dict/list的元素中就是这个 str，就能得到对应的path
    the_key_path = a.the_key_path('description')  # 只搜索dict的key，相同的就会得到对应的path

    print type(in_value_path)
    for i in in_value_path:
        print(i)
        print(eval('dict1' + i))