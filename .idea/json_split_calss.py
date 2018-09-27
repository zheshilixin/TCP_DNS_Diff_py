# -*- coding: utf-8 -*-
false = False
true  = True
class find_path():
    def find_value_path(self,target, value, tmp_list ):
        '''输入字典的值/列表的元素，以list返回所对应的key/posi，跟所在的字典/列表
                                          [key,dict,posi,list,key,dict........]
        '''
        if isinstance(target, dict):         #判断了它是字典
            dict1 = target
            for k,v in dict1.items():        #遍历字典
                if str(value)==str(v):       #如果某个value就是要找的，就把k，整个dict放进tmp_list
                    tmp_list.append(str([k]))
                    tmp_list.append(dict1)
                else:
                    self.find_value_path(v, value, tmp_list)#此value不是要找的，那么对这个value调用自身进行遍历

        elif isinstance(target, (list, tuple)):  #判断了它是列表
            var=target
            for each in var:                     #遍历列表
                 if str(each)==str(value):       #如果某个元素就是要找的，就把位置posi，整个list放进tmp_list
                    posi=var.index(each)
                    tmp_list.append(str([posi]))
                    tmp_list.append(var)
                 else:
                     self.find_value_path(each, value, tmp_list)#此元素不是要找的，那么对这个元素调用自身进行遍历
        return tmp_list

    def find_key_path(self,target, key, tmp_list):
        '''输入字典的key，以list返回所对应的key，所在的字典
                        [key,dict,key,dict........]'''
        if isinstance(target, dict):                     #跟find_value_path差不多，不过只当所查询的是key才会返回
            dict1 = target
            for k,v in dict1.items():
                if str(key)==str(k):
                    tmp_list.append(str([k]))
                    tmp_list.append(dict1)
                else:
                    self.find_key_path(v, key, tmp_list)

        elif isinstance(target, (list, tuple)):
            var=target
            for each in var:
                self.find_key_path(each, key, tmp_list)
        return tmp_list

    def get_path(self,target, objkey,path):
        '''以 (key所在的dict)作为查询目标，不断的以上一层(所在的list/dict)作为查询目标调用自身，
            直到查询的上一层就是整个文本时，就输出每次调用自身所对应的key/posi组成的path
        :param target: json_text
        :param objkey: key所在的dict
        :param path:  对应的key
        :return:      完整路径
        '''
        if objkey==target:
            return ''.join(path[::-1])  #因为是list，先翻转再join合并，
        else:
            list1=self.find_value_path(target,objkey,[])  #返回的list应该只有2个元素[key，小dict],也不可能是空[]
            print('要查找的value所在的字典/列表一模一样的有%d个呢！！' % (len(list1) / 2)) if len(list1) > 2 else None
            path.append(list1[0])
            return self.get_path(target, list1[1], path) #循环自身

    def remove_the_same(self,list):
        '''以[key,dict,posi,list,key,dict.....]形式传入
            去重(因为有些key所在的dict是一模一样的)
            返回[[key,dict],[posi,list],[key,dict]....]
        '''
        list1=[]
        for i in range(0, len(list), 2):
            r = list[i:i + 2]
            list1.append(r)
        list2 = []
        [list2.append(i) for i in list1 if not i in list2]
        return list2

    def print_all_path(self,target,find_list):
        '''步骤:1.remove_the_same()，去重，返回[[key,dict],[posi,list],[key,dict]....]
               2.循环[key,dict]，再find_value_path()判断，①如果还有重复，那么就对这些重复的循环，get_path()得出路径
                                                        ②没重复，直接get_path()得出路径
        :param target: json_text
        :param find_list: [key,dict,posi,list,key,dict.....]
        '''
        find_list = self.remove_the_same(find_list) #去重，返回[[key,dict],[posi,list],[key,dict]....]
        for key_dict in find_list:          # 循环各组key+小dict————[key,dict]
            second_dict = self.find_value_path(target, key_dict[1], [])#判断key所在的dict是否有一模一样的
            #整个dict作为要查询的，返回[posi(dict所在),大list，posi(dict所在),大list...]
            if len(second_dict) > 2:                              #判断出有多个相同的dict
                second_list = self.remove_the_same(second_dict)       #返回[[key,dict],[posi,list],[key,dict]....]
                for key_dict2 in second_list:                    #每个相同的dict分别求出路径
                    r = self.get_path(target, key_dict2[1], [key_dict[0], key_dict2[0]])  # 得出符合条件的path
                    print(r, '\n', eval('target' + r), '\n')             #第三个参数就是[key，上一层posi]
            else:
                r = self.get_path(target, key_dict[1], [key_dict[0]])  # key所在的dict独一无二，直接get_path
                print(r, '\n', eval('target' + r), '\n')


    def work(self,target, value):
        '''输入txt，需要查找的value，返回每个符合要求的path
        '''
        print('正在查找的是:%s'% value,'\n','*'*80)       #[key,dict,posi,list,key,dict.....]
        value_list = self.find_value_path(target, value, [])   #返回查找的value对应的key、所在dict组成的list
        key_list=   self.find_key_path(target, value, [])     #返回查找的key、            所在dict组成的list

        if value_list==[]:print('find_value_path——————这不是字典的值/列表的元素吧!找不到的！')
        else:print('find_value_path——————以《%s》为字典的值/列表的元素查到的具体路径在下面:'%value)#找不到！
        self.print_all_path(target, value_list)            #打印出key的路径，value值

        print('='*80)
        if key_list==[]:print('find_key_path————————这不是字典的key吧!找不到的！')
        else:print('find_key_path————————以《%s》为字典的key查到的具体路径跟value在下面:'%value)
        self.print_all_path(target, key_list)            #打印出key的路径，value值


if __name__ == '__main__':
    story1={
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
            "icon": "http://pic.wankacn.com/2017-08-28_59a37c4495707.png"
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
                    "equip_id": "49"
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

    json_check_disk = {
        "_shards": {
            "total": 20,
            "successful": 20,
            "failed": 0
        },
        "_all": {
            "primaries": {
                "docs": {
                    "count": 86404485,
                    "deleted": 0
                },
                "store": {
                    "size_in_bytes": 35285323041,
                    "throttle_time_in_millis": 0
                },
                "indexing": {
                    "index_total": 0,
                    "index_time_in_millis": 0,
                    "index_current": 0,
                    "index_failed": 0,
                    "delete_total": 0,
                    "delete_time_in_millis": 0,
                    "delete_current": 0,
                    "noop_update_total": 0,
                    "is_throttled": false,
                    "throttle_time_in_millis": 0
                },
                "get": {
                    "total": 0,
                    "time_in_millis": 0,
                    "exists_total": 0,
                    "exists_time_in_millis": 0,
                    "missing_total": 0,
                    "missing_time_in_millis": 0,
                    "current": 0
                },
                "search": {
                    "open_contexts": 0,
                    "query_total": 117967,
                    "query_time_in_millis": 4266334,
                    "query_current": 0,
                    "fetch_total": 0,
                    "fetch_time_in_millis": 0,
                    "fetch_current": 0,
                    "scroll_total": 0,
                    "scroll_time_in_millis": 0,
                    "scroll_current": 0,
                    "suggest_total": 0,
                    "suggest_time_in_millis": 0,
                    "suggest_current": 0
                },
                "merges": {
                    "current": 0,
                    "current_docs": 0,
                    "current_size_in_bytes": 0,
                    "total": 0,
                    "total_time_in_millis": 0,
                    "total_docs": 0,
                    "total_size_in_bytes": 0,
                    "total_stopped_time_in_millis": 0,
                    "total_throttled_time_in_millis": 0,
                    "total_auto_throttle_in_bytes": 209715200
                },
                "refresh": {
                    "total": 9,
                    "total_time_in_millis": 49,
                    "listeners": 0
                },
                "flush": {
                    "total": 9,
                    "total_time_in_millis": 0
                },
                "warmer": {
                    "current": 0,
                    "total": 19,
                    "total_time_in_millis": 8
                },
                "query_cache": {
                    "memory_size_in_bytes": 166307808,
                    "total_count": 642768,
                    "hit_count": 279708,
                    "miss_count": 363060,
                    "cache_size": 9999,
                    "cache_count": 14376,
                    "evictions": 4377
                },
                "fielddata": {
                    "memory_size_in_bytes": 45973192,
                    "evictions": 0
                },
                "completion": {
                    "size_in_bytes": 0
                },
                "segments": {
                    "count": 277,
                    "memory_in_bytes": 70499073,
                    "terms_memory_in_bytes": 40857059,
                    "stored_fields_memory_in_bytes": 12957832,
                    "term_vectors_memory_in_bytes": 0,
                    "norms_memory_in_bytes": 17728,
                    "points_memory_in_bytes": 11828538,
                    "doc_values_memory_in_bytes": 4837916,
                    "index_writer_memory_in_bytes": 0,
                    "version_map_memory_in_bytes": 0,
                    "fixed_bit_set_memory_in_bytes": 0,
                    "max_unsafe_auto_id_timestamp": -1,
                    "file_sizes": {}
                },
                "translog": {
                    "operations": 0,
                    "size_in_bytes": 817
                },
                "request_cache": {
                    "memory_size_in_bytes": 24818082,
                    "evictions": 1272,
                    "hit_count": 92602,
                    "miss_count": 23929
                },
                "recovery": {
                    "current_as_source": 0,
                    "current_as_target": 0,
                    "throttle_time_in_millis": 668313
                }
            },
            "total": {
                "docs": {
                    "count": 172808970,
                    "deleted": 0
                },
                "store": {
                    "size_in_bytes": 70570646073,
                    "throttle_time_in_millis": 0
                },
                "indexing": {
                    "index_total": 0,
                    "index_time_in_millis": 0,
                    "index_current": 0,
                    "index_failed": 0,
                    "delete_total": 0,
                    "delete_time_in_millis": 0,
                    "delete_current": 0,
                    "noop_update_total": 0,
                    "is_throttled": false,
                    "throttle_time_in_millis": 0
                },
                "get": {
                    "total": 0,
                    "time_in_millis": 0,
                    "exists_total": 0,
                    "exists_time_in_millis": 0,
                    "missing_total": 0,
                    "missing_time_in_millis": 0,
                    "current": 0
                },
                "search": {
                    "open_contexts": 0,
                    "query_total": 233672,
                    "query_time_in_millis": 6529008,
                    "query_current": 0,
                    "fetch_total": 0,
                    "fetch_time_in_millis": 0,
                    "fetch_current": 0,
                    "scroll_total": 0,
                    "scroll_time_in_millis": 0,
                    "scroll_current": 0,
                    "suggest_total": 0,
                    "suggest_time_in_millis": 0,
                    "suggest_current": 0
                },
                "merges": {
                    "current": 0,
                    "current_docs": 0,
                    "current_size_in_bytes": 0,
                    "total": 0,
                    "total_time_in_millis": 0,
                    "total_docs": 0,
                    "total_size_in_bytes": 0,
                    "total_stopped_time_in_millis": 0,
                    "total_throttled_time_in_millis": 0,
                    "total_auto_throttle_in_bytes": 419430400
                },
                "refresh": {
                    "total": 9,
                    "total_time_in_millis": 49,
                    "listeners": 0
                },
                "flush": {
                    "total": 9,
                    "total_time_in_millis": 0
                },
                "warmer": {
                    "current": 0,
                    "total": 29,
                    "total_time_in_millis": 8
                },
                "query_cache": {
                    "memory_size_in_bytes": 270341272,
                    "total_count": 1246008,
                    "hit_count": 539520,
                    "miss_count": 706488,
                    "cache_size": 17366,
                    "cache_count": 26114,
                    "evictions": 8748
                },
                "fielddata": {
                    "memory_size_in_bytes": 91940240,
                    "evictions": 0
                },
                "completion": {
                    "size_in_bytes": 0
                },
                "segments": {
                    "count": 554,
                    "memory_in_bytes": 140998146,
                    "terms_memory_in_bytes": 81714118,
                    "stored_fields_memory_in_bytes": 25915664,
                    "term_vectors_memory_in_bytes": 0,
                    "norms_memory_in_bytes": 35456,
                    "points_memory_in_bytes": 23657076,
                    "doc_values_memory_in_bytes": 9675832,
                    "index_writer_memory_in_bytes": 0,
                    "version_map_memory_in_bytes": 0,
                    "fixed_bit_set_memory_in_bytes": 0,
                    "max_unsafe_auto_id_timestamp": -1,
                    "file_sizes": {}
                },
                "translog": {
                    "operations": 0,
                    "size_in_bytes": 1247
                },
                "request_cache": {
                    "memory_size_in_bytes": 46438156,
                    "evictions": 5155,
                    "hit_count": 183446,
                    "miss_count": 47786
                },
                "recovery": {
                    "current_as_source": 0,
                    "current_as_target": 0,
                    "throttle_time_in_millis": 1305926
                }
            }
        },
        "indices": {
            "tcp-2018-09-01": {
                "primaries": {
                    "docs": {
                        "count": 86404485,
                        "deleted": 0
                    },
                    "store": {
                        "size_in_bytes": 35285323041,
                        "throttle_time_in_millis": 0
                    },
                    "indexing": {
                        "index_total": 0,
                        "index_time_in_millis": 0,
                        "index_current": 0,
                        "index_failed": 0,
                        "delete_total": 0,
                        "delete_time_in_millis": 0,
                        "delete_current": 0,
                        "noop_update_total": 0,
                        "is_throttled": false,
                        "throttle_time_in_millis": 0
                    },
                    "get": {
                        "total": 0,
                        "time_in_millis": 0,
                        "exists_total": 0,
                        "exists_time_in_millis": 0,
                        "missing_total": 0,
                        "missing_time_in_millis": 0,
                        "current": 0
                    },
                    "search": {
                        "open_contexts": 0,
                        "query_total": 117967,
                        "query_time_in_millis": 4266334,
                        "query_current": 0,
                        "fetch_total": 0,
                        "fetch_time_in_millis": 0,
                        "fetch_current": 0,
                        "scroll_total": 0,
                        "scroll_time_in_millis": 0,
                        "scroll_current": 0,
                        "suggest_total": 0,
                        "suggest_time_in_millis": 0,
                        "suggest_current": 0
                    },
                    "merges": {
                        "current": 0,
                        "current_docs": 0,
                        "current_size_in_bytes": 0,
                        "total": 0,
                        "total_time_in_millis": 0,
                        "total_docs": 0,
                        "total_size_in_bytes": 0,
                        "total_stopped_time_in_millis": 0,
                        "total_throttled_time_in_millis": 0,
                        "total_auto_throttle_in_bytes": 209715200
                    },
                    "refresh": {
                        "total": 9,
                        "total_time_in_millis": 49,
                        "listeners": 0
                    },
                    "flush": {
                        "total": 9,
                        "total_time_in_millis": 0
                    },
                    "warmer": {
                        "current": 0,
                        "total": 19,
                        "total_time_in_millis": 8
                    },
                    "query_cache": {
                        "memory_size_in_bytes": 166307808,
                        "total_count": 642768,
                        "hit_count": 279708,
                        "miss_count": 363060,
                        "cache_size": 9999,
                        "cache_count": 14376,
                        "evictions": 4377
                    },
                    "fielddata": {
                        "memory_size_in_bytes": 45973192,
                        "evictions": 0
                    },
                    "completion": {
                        "size_in_bytes": 0
                    },
                    "segments": {
                        "count": 277,
                        "memory_in_bytes": 70499073,
                        "terms_memory_in_bytes": 40857059,
                        "stored_fields_memory_in_bytes": 12957832,
                        "term_vectors_memory_in_bytes": 0,
                        "norms_memory_in_bytes": 17728,
                        "points_memory_in_bytes": 11828538,
                        "doc_values_memory_in_bytes": 4837916,
                        "index_writer_memory_in_bytes": 0,
                        "version_map_memory_in_bytes": 0,
                        "fixed_bit_set_memory_in_bytes": 0,
                        "max_unsafe_auto_id_timestamp": -1,
                        "file_sizes": {}
                    },
                    "translog": {
                        "operations": 0,
                        "size_in_bytes": 817
                    },
                    "request_cache": {
                        "memory_size_in_bytes": 24818082,
                        "evictions": 1272,
                        "hit_count": 92602,
                        "miss_count": 23929
                    },
                    "recovery": {
                        "current_as_source": 0,
                        "current_as_target": 0,
                        "throttle_time_in_millis": 668313
                    }
                },
                "total": {
                    "docs": {
                        "count": 172808970,
                        "deleted": 0
                    },
                    "store": {
                        "size_in_bytes": 70570646073,
                        "throttle_time_in_millis": 0
                    },
                    "indexing": {
                        "index_total": 0,
                        "index_time_in_millis": 0,
                        "index_current": 0,
                        "index_failed": 0,
                        "delete_total": 0,
                        "delete_time_in_millis": 0,
                        "delete_current": 0,
                        "noop_update_total": 0,
                        "is_throttled": false,
                        "throttle_time_in_millis": 0
                    },
                    "get": {
                        "total": 0,
                        "time_in_millis": 0,
                        "exists_total": 0,
                        "exists_time_in_millis": 0,
                        "missing_total": 0,
                        "missing_time_in_millis": 0,
                        "current": 0
                    },
                    "search": {
                        "open_contexts": 0,
                        "query_total": 233672,
                        "query_time_in_millis": 6529008,
                        "query_current": 0,
                        "fetch_total": 0,
                        "fetch_time_in_millis": 0,
                        "fetch_current": 0,
                        "scroll_total": 0,
                        "scroll_time_in_millis": 0,
                        "scroll_current": 0,
                        "suggest_total": 0,
                        "suggest_time_in_millis": 0,
                        "suggest_current": 0
                    },
                    "merges": {
                        "current": 0,
                        "current_docs": 0,
                        "current_size_in_bytes": 0,
                        "total": 0,
                        "total_time_in_millis": 0,
                        "total_docs": 0,
                        "total_size_in_bytes": 0,
                        "total_stopped_time_in_millis": 0,
                        "total_throttled_time_in_millis": 0,
                        "total_auto_throttle_in_bytes": 419430400
                    },
                    "refresh": {
                        "total": 9,
                        "total_time_in_millis": 49,
                        "listeners": 0
                    },
                    "flush": {
                        "total": 9,
                        "total_time_in_millis": 0
                    },
                    "warmer": {
                        "current": 0,
                        "total": 29,
                        "total_time_in_millis": 8
                    },
                    "query_cache": {
                        "memory_size_in_bytes": 270341272,
                        "total_count": 1246008,
                        "hit_count": 539520,
                        "miss_count": 706488,
                        "cache_size": 17366,
                        "cache_count": 26114,
                        "evictions": 8748
                    },
                    "fielddata": {
                        "memory_size_in_bytes": 91940240,
                        "evictions": 0
                    },
                    "completion": {
                        "size_in_bytes": 0
                    },
                    "segments": {
                        "count": 554,
                        "memory_in_bytes": 140998146,
                        "terms_memory_in_bytes": 81714118,
                        "stored_fields_memory_in_bytes": 25915664,
                        "term_vectors_memory_in_bytes": 0,
                        "norms_memory_in_bytes": 35456,
                        "points_memory_in_bytes": 23657076,
                        "doc_values_memory_in_bytes": 9675832,
                        "index_writer_memory_in_bytes": 0,
                        "version_map_memory_in_bytes": 0,
                        "fixed_bit_set_memory_in_bytes": 0,
                        "max_unsafe_auto_id_timestamp": -1,
                        "file_sizes": {}
                    },
                    "translog": {
                        "operations": 0,
                        "size_in_bytes": 1247
                    },
                    "request_cache": {
                        "memory_size_in_bytes": 46438156,
                        "evictions": 5155,
                        "hit_count": 183446,
                        "miss_count": 47786
                    },
                    "recovery": {
                        "current_as_source": 0,
                        "current_as_target": 0,
                        "throttle_time_in_millis": 1305926
                    }
                }
            }
        }
    }

    json_sip_dip = {
  "took": 240,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "failed": 0
  },
  "hits": {
    "total": 1493663,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 4226,
      "sum_other_doc_count": 550449,
      "buckets": [
        {
          "3": {
            "doc_count_error_upper_bound": 2886,
            "sum_other_doc_count": 367438,
            "buckets": [
              {
                "key": "202.102.94.125",
                "doc_count": 7745
              },
              {
                "key": "180.97.245.254",
                "doc_count": 6583
              },
              {
                "key": "180.97.245.253",
                "doc_count": 6543
              },
              {
                "key": "188.172.219.132",
                "doc_count": 4465
              },
              {
                "key": "180.97.33.107",
                "doc_count": 3719
              }
            ]
          },
          "key": "192.168.4.100",
          "doc_count": 396493
        },
        {
          "3": {
            "doc_count_error_upper_bound": 1801,
            "sum_other_doc_count": 281838,
            "buckets": [
              {
                "key": "180.97.33.107",
                "doc_count": 10874
              },
              {
                "key": "180.97.33.108",
                "doc_count": 4578
              },
              {
                "key": "101.226.211.101",
                "doc_count": 2276
              },
              {
                "key": "61.129.248.209",
                "doc_count": 2154
              },
              {
                "key": "223.252.199.69",
                "doc_count": 1581
              }
            ]
          },
          "key": "192.168.3.100",
          "doc_count": 303301
        },
        {
          "3": {
            "doc_count_error_upper_bound": 212,
            "sum_other_doc_count": 20066,
            "buckets": [
              {
                "key": "8.8.8.8",
                "doc_count": 22686
              },
              {
                "key": "114.114.114.114",
                "doc_count": 22660
              },
              {
                "key": "221.13.30.242",
                "doc_count": 22606
              },
              {
                "key": "45.33.52.101",
                "doc_count": 2671
              },
              {
                "key": "121.156.123.249",
                "doc_count": 2573
              }
            ]
          },
          "key": "192.168.0.201",
          "doc_count": 93262
        },
        {
          "3": {
            "doc_count_error_upper_bound": 1184,
            "sum_other_doc_count": 58964,
            "buckets": [
              {
                "key": "180.97.33.107",
                "doc_count": 8040
              },
              {
                "key": "180.97.33.108",
                "doc_count": 7509
              },
              {
                "key": "74.125.204.101",
                "doc_count": 3470
              },
              {
                "key": "74.125.204.100",
                "doc_count": 3468
              },
              {
                "key": "74.125.204.102",
                "doc_count": 3466
              }
            ]
          },
          "key": "192.168.1.17",
          "doc_count": 84917
        },
        {
          "3": {
            "doc_count_error_upper_bound": 1072,
            "sum_other_doc_count": 49795,
            "buckets": [
              {
                "key": "74.125.204.138",
                "doc_count": 3152
              },
              {
                "key": "74.125.204.102",
                "doc_count": 3090
              },
              {
                "key": "74.125.204.101",
                "doc_count": 3081
              },
              {
                "key": "74.125.204.139",
                "doc_count": 3067
              },
              {
                "key": "74.125.204.100",
                "doc_count": 3056
              }
            ]
          },
          "key": "192.168.1.58",
          "doc_count": 65241
        }
      ]
    }
  },
  "status": 200
}

    json_sip = {
  "took": 88,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "hits": {
    "total": 184541,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 129679,
      "buckets": [
        {
          "key": "23.92.24.244",
          "doc_count": 14206
        },
        {
          "key": "192.168.0.66",
          "doc_count": 7108
        },
        {
          "key": "180.97.33.107",
          "doc_count": 6119
        },
        {
          "key": "180.97.33.108",
          "doc_count": 4574
        },
        {
          "key": "74.125.204.113",
          "doc_count": 3865
        },
        {
          "key": "74.125.204.101",
          "doc_count": 3849
        },
        {
          "key": "74.125.204.138",
          "doc_count": 3847
        },
        {
          "key": "74.125.204.102",
          "doc_count": 3776
        },
        {
          "key": "74.125.204.139",
          "doc_count": 3764
        },
        {
          "key": "74.125.204.100",
          "doc_count": 3754
        }
      ]
    }
  },
  "status": 200
}

    json_http = {
  "took": 25,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "hits": {
    "total": 3738,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "2": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 352,
      "buckets": [
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 333,
            "buckets": [
              {
                "key": "minigame.qq.com/appdir/avatar/element/76.zip",
                "doc_count": 1745
              },
              {
                "key": "dldir3.qq.com/minigamefile/face/30126.7z",
                "doc_count": 35
              },
              {
                "key": "dldir3.qq.com/minigamefile/face/30036.7z",
                "doc_count": 34
              },
              {
                "key": "get.sogou.com/q",
                "doc_count": 15
              },
              {
                "key": "180.96.2.71/download",
                "doc_count": 14
              }
            ]
          },
          "key": "192.168.3.100",
          "doc_count": 2176
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 397,
            "buckets": [
              {
                "key": "cntr.wps.cn/flow",
                "doc_count": 25
              },
              {
                "key": "helpdubaclient.ksmobile.com/nep/v1/",
                "doc_count": 14
              },
              {
                "key": "117.48.124.186/query3",
                "doc_count": 10
              },
              {
                "key": "120.52.183.150/",
                "doc_count": 8
              },
              {
                "key": "122.193.207.52/",
                "doc_count": 8
              }
            ]
          },
          "key": "192.168.4.100",
          "doc_count": 462
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 208,
            "buckets": [
              {
                "key": "192.168.0.118:5602/ui/favicons/favicon-32x32.png",
                "doc_count": 36
              },
              {
                "key": "192.168.0.118:5602/ui/favicons/favicon-16x16.png",
                "doc_count": 29
              },
              {
                "key": "180.96.2.51/download",
                "doc_count": 26
              },
              {
                "key": "192.168.0.118:5602/es_admin/_mget",
                "doc_count": 26
              },
              {
                "key": "192.168.0.118:5601/ui/favicons/favicon-32x32.png",
                "doc_count": 22
              }
            ]
          },
          "key": "192.168.1.18",
          "doc_count": 347
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 92,
            "buckets": [
              {
                "key": "23.92.24.244:5608/ui/favicons/favicon-32x32.png",
                "doc_count": 48
              },
              {
                "key": "23.92.24.244:5608/ui/favicons/favicon-16x16.png",
                "doc_count": 46
              },
              {
                "key": "23.92.24.244:5608/es_admin/_mget",
                "doc_count": 41
              },
              {
                "key": "23.92.24.244:5608/elasticsearch/_msearch",
                "doc_count": 30
              },
              {
                "key": "23.92.24.244:5608/elasticsearch/.dashboardgroup/dashboardgroup/_search",
                "doc_count": 15
              }
            ]
          },
          "key": "192.168.1.15",
          "doc_count": 272
        },
        {
          "3": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 122,
            "buckets": [
              {
                "key": "qd-update.qq.com:8080/",
                "doc_count": 2
              },
              {
                "key": "www.eclipse.org/downloads/download.php",
                "doc_count": 2
              },
              {
                "key": "101.110.118.66/ftp.yz.yamagata-u.ac.jp/pub/eclipse/releases/oxygen/201804111000/plugins/org.eclipse.cdt.core.native_5.10.0.201802261533.jar.pack.gz",
                "doc_count": 1
              },
              {
                "key": "101.110.118.70/ftp.yz.yamagata-u.ac.jp/pub/eclipse/releases/oxygen/201804111000/features/org.eclipse.cdt.native_9.4.3.201802261533.jar",
                "doc_count": 1
              },
              {
                "key": "113.96.231.11:443/",
                "doc_count": 1
              }
            ]
          },
          "key": "192.168.1.14",
          "doc_count": 129
        }
      ]
    }
  },
  "status": 200
}
    d=find_path()
    #d.work(story1,'name')
    #d.work(json_check_disk,70570646073)
    d.work(json_http,"minigame.qq.com/appdir/avatar/element/76.zip")

