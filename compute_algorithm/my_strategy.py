# 将500的中文队名转为transfermkt的英文名

def is_between(value, low, up=float('inf')):
    if value >= low and value < up:
        return True
    else:
        return False

class My_strategy:
    def __init__(self):
        self.all_league = ['德甲', '英超', '法甲', '法乙', '英冠', '俄超', '比甲', '德乙', '乌超', '丹超', '英甲', '英乙', '西甲', '丹甲', '捷甲', '意乙', '西乙', '波甲', '芬超', '奥乙', '奥甲',
                                '土超', '爱甲', '爱超', 'K1联赛', '挪超', '荷甲', '挪甲', 'K2联赛', 'J1联赛', '澳超', '中超', 'J2联赛', '瑞典超', '瑞典甲', '俄甲', '苏超', '瑞士超', '瑞士甲', '荷乙', '冰岛超',
                                '葡超', '巴西甲', '墨超', '巴西乙', '葡甲', '阿甲', '罗甲', '克罗甲', '塞甲联', '以超', '保超', '哥甲']
        self.elimilated_league = ['爱甲', '爱超']
        self.no_draw_league = []

        self.strategy2_league_arr = ['德甲', '英超', '法甲', '俄超', '丹超', '西甲', '捷甲', '土超', '俄甲', '瑞士超', '荷乙',
                           '巴乙', '阿甲', '保超', '哥甲']

    def get(self, league_name, value_ratio, home_odd, draw_odd, away_odd, home_value, away_value):
        if league_name in self.elimilated_league:
            return ''

        if is_between(value_ratio, 0.6, 0.7) and home_odd <= 1.5:
            return 3

        if is_between(value_ratio, 0.1, 0.2) and home_odd <= 3.05:
            return 1
        if is_between(value_ratio, 0.2, 0.3) and home_odd <= 3:
            return 1
        if is_between(value_ratio, 0.4, 0.5) and home_odd <= 2.9:
            return 1
        if is_between(value_ratio, 0.5, 0.6) and home_odd <= 2.85:
            return 1
        if is_between(value_ratio, 1, 1.25) and home_odd <= 2.9:
            return 1
        if is_between(value_ratio, 1.67, 2) and home_odd <= 3.1:
            return 1
        if is_between(value_ratio, 2.5, 3.33) and home_odd <= 3.15:
            return 1
        if is_between(value_ratio, 10, 99) and home_odd <= 5:
            return 1

        if is_between(value_ratio, 0.8, 0.9) and home_odd <= 1.7:
            return 0

        # 前策略
        # if league_name in self.strategy2_league_arr:
        #     if is_between(value_ratio, 0.01, 0.18) and home_odd >= 2.8 and home_odd <= 9:
        #         return 0
        #
        # if is_between(value_ratio, 3.8, 4.5):
        #     cur_max_odd = 2.1
        #     if home_odd >= 1.4 and home_odd <= cur_max_odd:
        #         return 3
        # elif is_between(value_ratio, 1.8, 1.9) and league_name not in self.no_draw_league:
        #     if draw_odd >= 2.5 and draw_odd <= 3.8:
        #         return 1
        # elif is_between(value_ratio, 0, 0.1) or is_between(value_ratio, 1.1, 1.3):
        #     if away_odd >= 1.4 and away_odd <= 2.3:
        #         return 0

        return ''

