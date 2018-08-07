# 将500的中文队名转为transfermkt的英文名

def is_between(value, low, up=float('inf')):
    if value >= low and value < up:
        return True
    else:
        return False

class My_strategy:
    def __init__(self):
        self.strategy_league = ['德甲', '英超', '法甲', '法乙', '英冠', '俄超', '比甲', '德乙', '乌超', '丹超', '英甲', '英乙', '西甲', '丹甲', '捷甲', '意乙', '西乙', '波甲', '芬超', '奥乙', '奥甲', '土超', '爱甲', '爱超', 'K1联赛', '挪超']

    def get(self, league_name, value_ratio):
        if not league_name in self.strategy_league:
            return ''
        if league_name == '德甲':
            if is_between(value_ratio, 0.8, 0.9):
                return 1
        if league_name == '英超':
            if is_between(value_ratio, 0.8, 0.9):
                return 1
        if league_name == '法甲':
            if is_between(value_ratio, 1, 1.25):
                return 1
            elif is_between(value_ratio, 0.1, 0.2):
                return 0
        if league_name == '法乙':
            if is_between(value_ratio, 1.43, 1.67):
                return 3
            elif is_between(value_ratio, 0.2, 0.3):
                return 0
            elif is_between(value_ratio, 0.1, 0.2):
                return 1
        if league_name == '英冠':
            if is_between(value_ratio, 1.67, 2) or is_between(value_ratio, 10):
                return 3
        if league_name == '俄超':
            if is_between(value_ratio, 0.7, 0.8):
                return 0
            elif is_between(value_ratio, 1, 1.1) or is_between(value_ratio, 1.43, 1.67) or is_between(value_ratio, 2.5, 3.33):
                return 3
            elif is_between(value_ratio, 0.4, 0.5) or is_between(value_ratio, 2, 2.5):
                return 1
        if league_name == '比甲':
            if is_between(value_ratio, 2, 2.5):
                return 0
            elif is_between(value_ratio, 0.2, 0.3):
                return 1
            elif is_between(value_ratio, 5, 10):
                return 3
        if league_name == '德乙':
            if is_between(value_ratio, 2, 2.5):
                return 3
            elif is_between(value_ratio, 0.8, 0.9):
                return 1
        if league_name == '乌超':
            if is_between(value_ratio, 1.25, 1.43) or is_between(value_ratio, 3.33, 5):
                return 3
            elif is_between(value_ratio, 0.6, 0.7) or is_between(value_ratio, 1.43, 1.67):
                return 1
            elif is_between(value_ratio, 0.5, 0.6):
                return 0
        if league_name == '丹超':
            if is_between(value_ratio, 5, 10):
                return 3
            elif is_between(value_ratio, 0.9, 1):
                return 1
            elif is_between(value_ratio, 0.1, 0.2) or is_between(value_ratio, 1.1, 1.25):
                return 0
        if league_name == '英甲':
            if is_between(value_ratio, 10):
                return 3
        if league_name == '英乙':
            if is_between(value_ratio, 0, 0.1):
                return 0
        if league_name == '西甲':
            if is_between(value_ratio, 0.1, 0.2):
                return 3
            elif is_between(value_ratio, 0.2, 0.3):
                return 1
            elif is_between(value_ratio, 1.67, 2):
                return 0
        if league_name == '丹甲':
            if is_between(value_ratio, 0.3, 0.4):
                return 0
        if league_name == '捷甲':
            if is_between(value_ratio, 0.4, 0.5):
                return 1
            elif is_between(value_ratio, 5, 10):
                return 3
        if league_name == '意乙':
            if is_between(value_ratio, 3.33, 10):
                return 3
        if league_name == '西乙':
            if is_between(value_ratio, 0.3, 0.4) or is_between(value_ratio, 5, 10):
                return 1
            elif is_between(value_ratio, 0.1, 0.2):
                return 0
        if league_name == '波甲':
            if is_between(value_ratio, 2.5, 3.33):
                return 0
        if league_name == '芬超':
            if is_between(value_ratio, 5, 10):
                return 3
            elif is_between(value_ratio, 1.43, 1.67):
                return 0
        if league_name == '奥乙':
            if is_between(value_ratio, 2.5, 3.33):
                return 3
            elif is_between(value_ratio, 0.6, 0.7):
                return 0
        if league_name == '奥甲':
            if is_between(value_ratio, 0.4, 0.5):
                return 3
        if league_name == '土超':
            if is_between(value_ratio, 2.5, 3.33):
                return 3
        if league_name == '爱甲':
            if is_between(value_ratio, 2.5, 3.33):
                return 3
            elif is_between(value_ratio, 0.9, 1):
                return 0
        if league_name == '爱超':
            if is_between(value_ratio, 10):
                return 3
            elif is_between(value_ratio, 0, 0.1):
                return 0
        if league_name == 'K1联赛':
            if is_between(value_ratio, 0, 0.2) or is_between(value_ratio, 0.4, 0.5) or is_between(value_ratio, 10):
                return 1
            elif is_between(value_ratio, 0.5, 0.6):
                return 0
        if league_name == '挪超':
            if is_between(value_ratio, 0.2, 0.3):
                return 0
        return ''

