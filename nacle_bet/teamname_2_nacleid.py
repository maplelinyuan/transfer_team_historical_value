# 将500的中文队名转为transfermkt的英文名

class teamname_2_id:
    def __init__(self):
        self.teamname_2_id_dict = {
            '瑞典甲': '2476',
            '英锦赛': '197559',
            '巴乙': '1835',
            '巴甲': '1834',
            '墨西杯': '5778',
            '美职': '2663',
            '新加联': '9427',
            '罗乙1': '199710',
            '意丙杯': '10806',
            '阿尔及甲': '8667',
            '女世外欧': '198974',
            '法丙': '2027',
            '英北超': '11693',
            '英依超': '11697',
            '英足总杯': '1979',
            '哥甲': '5591',
    }

    def get(self, name):
        try:
            return self.teamname_2_id_dict[name]
        except Exception as err:
            print('尚无该联赛名称: %s' % name)
            return -1

