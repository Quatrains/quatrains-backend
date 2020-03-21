# -*- coding:utf8 -*-
'''
Function:
    Recommend poem for user.
Parameters:
    infomation_path: 'dict_SimilariyPopularityType.json' 的路径；
    user_choose_type: list, ['悼亡', ’月‘, ...]，用户初入程序时选择的喜爱类型；
    user_favorite_poem: list, 用户标记为喜爱的诗，idx；
    user_recommended_poem: list, 最近30天给用户推荐过的诗，idx。
代码运行说明：
    需要下载 data/dict_SimilariyPopularityType.json；
    需要本代码，以及 utils/utils.py.
'''
import random
import json


class Predict:
    def __init__(self, infomation_path):
        self.infomation_path = infomation_path
        self.loadData()

    def loadData(self):
        with open(self.infomation_path, encoding='utf8') as f:
            info = json.load(f)
        self.idx_likescount_list = info['popularity']
        self.type_idx_dict = info['type']
        self.idx_mostsimiliar_dict = {}
        for _idx, _similars in info['similarity'].items():
            self.idx_mostsimiliar_dict[int(_idx)] = _similars

    def _randomSelectPoem(self, user_choose_type, user_favorite_poem, user_recommended_poem):
        # self.idx_likescount_list - self.user_favorite_poem - self.recommend_poem
        to_be_choosed = []
        if user_choose_type:
            _type = random.sample(user_choose_type, len(user_choose_type)//2) 
            for _t in _type:
                to_be_choosed += self.type_idx_dict[_t]
            to_be_choosed = list(set(to_be_choosed).difference(set(user_favorite_poem)).difference(user_recommended_poem))
            if to_be_choosed:
                return random.choice(to_be_choosed)
        to_be_choosed = list(set(self.idx_likescount_list).difference(set(user_favorite_poem)).difference(user_recommended_poem))
        return random.choice(to_be_choosed)

    def predict(self, user_choose_type, user_favorite_poem, user_recommended_poem):
        # 第一次进入系统
        if not user_favorite_poem and not user_recommended_poem: 
            # 未选择喜爱类型
            if not user_choose_type: 
                return random.choice(self.idx_likescount_list)
            # 选择喜爱类型
            else:
                _type = random.choice(user_choose_type)
                return random.choice(self.type_idx_dict[_type])

        # 非第一次进入系统
        else:
            # 用户有标记喜爱的诗词
            if user_favorite_poem:
                idx = random.choice(user_favorite_poem)
                to_be_choosed = list(set(self.idx_mostsimiliar_dict[idx]).difference(set(user_recommended_poem)))
                if to_be_choosed:
                    return random.choice(to_be_choosed)
                else:
                    return self._randomSelectPoem(user_choose_type, user_favorite_poem, user_recommended_poem)
            # 用户未标记喜爱的诗词
            else:
                return self._randomSelectPoem(user_choose_type, user_favorite_poem, user_recommended_poem)


# infomation_path = 'dict_SimilariyPopularityType.json'
# s = Predict(infomation_path)
# idx = s.predict(["悼亡", "月"], [], [])
# print(idx)



