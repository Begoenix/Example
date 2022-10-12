from ITCHDriver import ITCHDriver
import ITCHMessages
from multiprocess import Process, Queue
import pandas as pd


#设置储存结果DataFrame，其元素格式是list，list[0]储存加权均价，list[1]储存成交股数
VWAP = pd.DataFrame(index = ['try'],columns = ['former',9,10,11,12,13,14,15,'later'])



#股票撮合成功信息的输出器，输出成交时间，股票代码，成交价格与股数，这里用到的是TradeMessage信息
def tradeengine(message):
    a = ()
    timestamp = int(str(message.timestamp)[:-9])
    time = int(timestamp/3600)
    stock_code = str(message.stockcode,encoding = 'gbk')
    priceint = float(str(message.price)[:-4])
    pricefloat = float(str(message.price)[-4:])/10000
    price = priceint + pricefloat
    shares = message.shares
    judge = 'y'
    a = (time,stock_code,price,shares,judge)
    return a
  

#事件输出器，输出反映市场动态的信息，诸如系统开机，开始交易等
def eventengine(message):
    if message.event == b'O':
        print('Messages start')
    elif message.event == b'S':
        print('System start')
    elif message.event == b'Q':
        print('Market start')
    elif message.event == b'M':
        print('Market end')
    elif message.event == b'E':
        print('Syetem end')
    elif message.event == b'C':
        print('Messages end')
    judge = 'n'
    a = ('n',judge)
    return a

#定义运行任务并匹配输出器与解码器
task = ITCHDriver()
task.AddEngine(ITCHMessages.TradeMessage,tradeengine)
task.AddEngine(ITCHMessages.SystemEventMessage,eventengine)
if __name__ == '__main__':
    task.start()

#开始运行，分批读取文件
file = '01302019.NASDAQ_ITCH50'
cachesize = 1024*4
data = open(file,'rb')
going = True
now = 0
buflen = 0
data_tem = data.read(cachesize)
buflen = len(data_tem)
while going is True :
    byte = data_tem[now:now+1]
    now += 1
    if going is False:
        print('np')
    else:
        if byte == b'\x00' and now != buflen:#信息以b'\x00'开头
            try:
                length = ord(data_tem[now:now+1])
                now += 1
            except:
                TypeError
                print(now,buflen)
                break
            if (now + length) > buflen:
                tem = data_tem[now:buflen]
                data_tem = tem + data.read(cachesize)
                buflen = len(data_tem)
                now = 0
            message = data_tem[now:now + length]
            now += length
            task.messagequeue.put(message)
            mes = task.run()
            try:#添加到结果VWAP里
                if mes[-1] == 'y':
                    time = mes[0]
                    stock_code = mes[1]
                    price = mes[2]
                    shares = mes[3]
                    if stock_code in VWAP.index:
                        if time < 9:
                            VWAP.loc[stock_code,'former'][0] = (VWAP.loc[stock_code,'former'][0]*VWAP.loc[stock_code,'former'][1] + price*shares)/(VWAP.loc[stock_code,'former'][1] + shares)
                            VWAP.loc[stock_code,'former'][1] += shares
                        elif time > 15:
                            VWAP.loc[stock_code,'later'][0] = (VWAP.loc[stock_code,'later'][0]*VWAP.loc[stock_code,'later'][1] + price*shares)/(VWAP.loc[stock_code,'later'][1] + shares)
                            VWAP.loc[stock_code,'later'][1] += shares
                        else:
                            VWAP.loc[stock_code,time][0] = (VWAP.loc[stock_code,time][0]*VWAP.loc[stock_code,time][1] + price*shares)/(VWAP.loc[stock_code,time][1] + shares)
                            VWAP.loc[stock_code,time][1] += shares
                    else:
                        data_s = pd.DataFrame(index = [stock_code], columns = ['former',9,10,11,12,13,14,15,'later'])
                        if time < 9:
                            data_s.loc[stock_code,'former'] = [price,shares]
                        elif time > 15:
                            data_s.loc[stock_code,'later'] = [price,shares]
                        else:
                            data_s.loc[stock_code,time] = [price,shares]
                        VWAP = pd.concat([VWAP,data_s],axis = 0)
                    mes = None
            except:
                TypeError

            if now == buflen:
                now = 0
                data_tem = data.read(cachesize)
                buflen = len(data_tem)
        elif byte == b'\x00' and now == buflen:#当b'x\00'正好是该批次读取的文件的最后一字节时的解决方法
            now = 0
            data_tem = data.read(cachesize)
            buflen = len(data_tem)
            length = ord(data_tem[now:now+1])
            now += 1
            message = data_tem[now:now + length]
            now += length
            task.messagequeue.put(message)
            mes = task.run()
            try:
                if mes[-1] == 'y':
                    time = mes[0]
                    stock_code = mes[1]
                    price = mes[2]
                    shares = mes[3]
                    if stock_code in VWAP.index:
                        if time < 9:
                            VWAP.loc[stock_code,'former'][0] = (VWAP.loc[stock_code,'former'][0]*VWAP.loc[stock_code,'former'][1] + price*shares)/(VWAP.loc[stock_code,'former'][1] + shares)
                            VWAP.loc[stock_code,'former'][1] += shares
                        elif time > 15:
                            VWAP.loc[stock_code,'later'][0] = (VWAP.loc[stock_code,'later'][0]*VWAP.loc[stock_code,'later'][1] + price*shares)/(VWAP.loc[stock_code,'later'][1] + shares)
                            VWAP.loc[stock_code,'later'][1] += shares
                        else:
                            VWAP.loc[stock_code,time][0] = (VWAP.loc[stock_code,time][0]*VWAP.loc[stock_code,time][1] + price*shares)/(VWAP.loc[stock_code,time][1] + shares)
                            VWAP.loc[stock_code,time][1] += shares
                    else:
                        data_s = pd.DataFrame(index = [stock_code], columns = ['former',9,10,11,12,13,14,15,'later'])
                        if time < 9:
                            data_s.loc[stock_code,'former'] = [price,shares]
                        elif time > 15:
                            data_s.loc[stock_code,'later'] = [price,shares]
                        else:
                            data_s.loc[stock_code,time] = [price,shares]
                        VWAP = pd.concat([VWAP,data_s],axis = 0)
                    mes = None
            except:
                TypeError

            

        else:
            print('Byte was {}'.format(ord(byte)))



        


            
