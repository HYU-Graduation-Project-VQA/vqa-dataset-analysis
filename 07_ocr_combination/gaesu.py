import json

while(True):
    a, b, c, d, e = map(int, input().split())

    print((a * 0 + b * 0.3 + c * 0.6 + d * 0.9 + e)/(a+b+c+d+e))