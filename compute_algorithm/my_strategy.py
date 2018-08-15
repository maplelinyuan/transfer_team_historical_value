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

    def get(self, league_name, value_ratio, home_odd, draw_odd, away_odd):
        if is_between(value_ratio, 2, 5):
            if home_odd >= 1.64:
                return 3
        elif is_between(value_ratio, 0.8, 1.67):
            if draw_odd >= 2.75 and draw_odd <= 4:
                return 1
        elif is_between(value_ratio, 0.1, 0.3):
            if away_odd <= 2.9:
                return 0

        return ''

