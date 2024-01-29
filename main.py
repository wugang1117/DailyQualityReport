
import decimal


qdata = [('BCLW35', '变形', '1'), ('BCLW35', '缺件', '2'), ('BCLW35', '漏焊', '3'), ('BCLW35', '极性反', '4'), ('BEAF05', '元件破损', '5'), ('BEAF05', '缺件', '6'), ('BEAF09', '元件破损', '7')]
print(qdata)
print(len(qdata))
quality_x1 = []
quality_x2 = []
quality_x3 = []
quality_y1 = []
quality_y2 = []
quality_y3 = []

item1=''
item2 = ''
item3 = ''


for i in range(0,len(qdata)):
    if i==0:
        item1 = qdata[0][0]
    if qdata[i][0] != item1 and item2=='':
        item2 = qdata[i][0]
    if (qdata[i][0] != item1) and (qdata[i][0] != item2):
        item3 = qdata[i][0]

print("$$$$$$$$$$$$$$")
print(item1,item2,item3)

for i in range(0,len(qdata)):
    if qdata[i][0] == item1:
        quality_x1.append(qdata[i][1])
        quality_y1.append(qdata[i][2])
    if qdata[i][0] == item2:
        quality_x2.append(qdata[i][1])
        quality_y2.append(qdata[i][2])
    if qdata[i][0] == item3:
        quality_x3.append(qdata[i][1])
        quality_y3.append(qdata[i][2])

print(quality_x1,quality_y1)
print(quality_x2,quality_y2)
print(quality_x3,quality_y3)