# 将500的中文队名转为transfermkt的英文名

def is_between(value, low, up=float('inf')):
    if value >= low and value < up:
        return True
    else:
        return False

class My_strategy:
    def __init__(self):
        self.strategy_league = ['德甲', '英超', '法甲', '法乙', '英冠', '俄超', '比甲', '德乙', '乌超', '丹超', '英甲', '英乙', '西甲', '丹甲', '捷甲', '意乙', '西乙', '波甲', '芬超', '奥乙', '奥甲',
                                '土超', '爱甲', '爱超', 'K1联赛', '挪超', '荷甲', '挪甲', 'K2联赛', 'J1联赛', '澳超', '中超', 'J2联赛', '瑞典超', '瑞典甲', '俄甲', '苏超', '瑞士超', '瑞士甲', '荷乙', '冰岛超',
                                '葡超', '巴西甲', '墨超', '巴西乙', '葡甲', '阿甲']
        self.elimilated_league = ['挪甲', '瑞典甲', '英乙', '爱超', '爱甲', '中超', '英冠']
        self.no_draw_league = ['荷甲', '俄超', 'J1联赛', 'J2联赛', '墨超', '巴西甲', '丹超', '丹甲', '英超', '捷甲', '奥甲', 'K1联赛', 'K2联赛', '澳超', '冰岛超', '阿甲']

    def get(self, league_name, value_ratio, home_odd, draw_odd, away_odd, home_value, away_value):
        if league_name in self.elimilated_league:
            return ''

        if is_between(value_ratio, 3.5, 4.5):
            cur_max_odd = 2
            if home_odd >= 1.63 and home_odd <= cur_max_odd:
                return 3
        elif is_between(value_ratio, 1.43, 1.5) and league_name not in self.no_draw_league:
            if draw_odd >= 3 and draw_odd <= 3.9:
                return 1
        elif is_between(value_ratio, 0.3, 0.36):
            if away_odd >= 1.8 and away_odd <= 2.1:
                return 0

        return ''

