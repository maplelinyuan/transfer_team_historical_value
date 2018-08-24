import os

def push_redis():
    cmd = 'python compute_value_rate.py'
    os.system(cmd)

if __name__ == '__main__':
    push_redis()