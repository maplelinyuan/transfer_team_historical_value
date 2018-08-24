import os

def push_redis():
    cmd = 'python match_result_and_avgOdd.py'
    os.system(cmd)

if __name__ == '__main__':
    push_redis()