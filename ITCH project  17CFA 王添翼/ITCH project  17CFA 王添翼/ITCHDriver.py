import os
import sys
import struct
import ITCHMessages
from threading import Thread
from multiprocess import Process, Queue


class ITCHDriver(Process):
    def __init__(self,queue = 2048000):
        super(ITCHDriver,self).__init__()
        self.engine = {}
        self.messagequeue = Queue(queue)#设置队列，但由于对此包不甚了解，故用处不大，有关内容待优化



#定义转换器函数，对不同类型的信息，提供不同的解码方法
    def gear(self,message):

        msgtype = str(message[0:1],encoding = 'gbk')
        if msgtype == 'S':
            return ITCHMessages.SystemEventMessage(message)
        elif msgtype == 'R':
            return ITCHMessages.StockDirectoryMessage(message)
        elif msgtype == 'H':
            return ITCHMessages.StockTradingActionMessage(message)
        elif msgtype == 'Y':
            return ITCHMessages.RegSHOMessage(message)
        elif msgtype == 'L':
            return ITCHMessages.MarketParticipantPositionMessage(message)
        elif msgtype == 'V':
            return ITCHMessages.MWCBDeclineLevelMessage(message)
        elif msgtype == 'W':
            return ITCHMessages.MWCBStatusMessage(message)
        elif msgtype == 'K':
            return ITCHMessages.IPOQuotingPeriodUpdate(message)
        elif msgtype == 'J':
            return ITCHMessages.LULDAuctionCollar(message)
        elif msgtype == 'h':
            return ITCHMessages.OperationalHalt(message)
        elif msgtype == 'A':
            return ITCHMessages.AddOrderMessage(message)
        elif msgtype == 'F':
            return ITCHMessages.AddOrderMPIDMessage(message)
        elif msgtype == 'E':
            return ITCHMessages.OrderExecutedMessage(message)
        elif msgtype == 'C':
            return ITCHMessages.OrderExecutedPriceMessage(message)
        elif msgtype == 'X':
            return ITCHMessages.OrderCancelMessage(message)
        elif msgtype == 'D':
            return ITCHMessages.OrderDeleteMessage(message)
        elif msgtype == 'U':
            return ITCHMessages.OrderReplaceMessage(message)
        elif msgtype == 'P':
            return ITCHMessages.TradeMessage(message)
        elif msgtype == 'Q':
            return ITCHMessages.CrossTradeMessage(message)
        elif msgtype == 'B':
            return ITCHMessages.BrokenTradeMessage(message)
        elif msgtype == 'I':
            return ITCHMessages.NoiiMessage(message)
        elif msgtype == 'N':
            return ITCHMessages.RPII(message)




#输出器添加，将需要用到的输出工具与相应的解码器匹配
    def AddEngine(self,messagetype,engine):

        self.engine[messagetype] = engine


#程序运行点火
    def run(self):
        if self.messagequeue.empty() != True:
            messageData = self.messagequeue.get()
            itch = self.gear(messageData)
            if type(itch) in self.engine:
                return self.engine[type(itch)](itch)
                
        else:
            return None
    
        
    
