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
            '意青杯': '10448',
            '意丙1C': '199868',
            '意丙1B': '199868',
            '阿尔及甲': '8667',
            '女世外欧': '198974',
            '法丙': '2027',
            '英北超': '11693',
            '英依超': '11697',
            '英足总杯': '1979',
            '哥甲': '5591',
            '沙特甲': '10600',
            '北联杯': '4996',
            '日联杯': '4995',
            '俄杯': '2409',
            '德丙联': '1844',
            '巴西杯': '1833',
            '友谊赛': '2117',
            '捷克杯': '1898',
            '巴拉联': '2359',
            '非洲杯': '1713',
            '欧U19': '5983',
            '丹麦杯': '1908',
            '球会友谊': ['1863', '187737'],
            '哥斯甲': '9531',
            '欧U21外': '5982',
            '捷克乙': '9441',
            '西乙': '2432',
            '哥伦杯': '1867',
            '葡联杯': '4997',
            '荷乙': '1929',
            '苏挑杯': '2420',
            '爱超': '2120',
            '英乙': '1958',
            '德北联': '2048',
            '厄甲': '5598',
            '以甲': '2133',
            '西丙1': '2464',
            '西丙2': '2465',
            '西丙3': '2466',
            '丹乙A': '191393',
            '丹乙B': '191393',
            '荷女甲': '192784',
            '爱甲': '2123',
            '日女甲': '202439',
            '俄甲': '35174',
            '日足联': '201838',
            'K2联赛': '9097',
            '日职乙': '2159',
            '英甲': '1957',
            '德巴联': '6546',
            '德南联': '6543',
            '德西联': '2050',
            '苏冠': '2417',
            '苏乙': '2419',
            '波乙': '6633',
            '北爱超': '2259',
            '英非联': '1978',
            '比乙': '1818',
            '瑞典乙北': '2510',
            '瑞典乙南': '2513',
            '英非南': '1952',
            '英非北': '1951',
            '西女超': '2468',
            '智利杯': '1856',
            '阿根廷杯': '1741',
            '阿乙': '1739',
            '乌拉超': '5593',
            '智乙': '10279',
            '秘鲁甲': '2366',
            '欧国联': ['200719', '200721', '200726', '200727']
    }

    def get(self, name):
        try:
            return self.teamname_2_id_dict[name]
        except Exception as err:
            print('尚无该联赛名称: %s' % name)
            return -1

