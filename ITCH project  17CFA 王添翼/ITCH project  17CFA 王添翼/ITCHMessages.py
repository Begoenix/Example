import struct



class itchmessage(object):#定义字典以及所以str返回值的含义
    sysEventCodes = {
                        'O':'Start of Messages',
                        'S':'Start of System Hours',
                        'Q':'Start of Market Hours',
                        'M':'End of Market Hours',
                        'E':'End of System Hours',
                        'C':'End of Messages',
                    }
    exchanges = {
                        'N':'NYSE',
                        'A':'AMEX',
                        'P':'Arca',
                        'Q':'NASDAQ Global Select',
                        'G':'NASDAQ Global Market',
                        'S':'NASDAQ Capital Market',
                        'Z':'BATS Z  Exchange',
                        'V':'Investors’ Exchange, LLC',
                        ' ':'Not available'
                    }
    finStatusIndicators = {
                        'D':'Deficient',
                        'E':'Deliquent',
                        'Q':'Bankrupt',
                        'S':'Suspended',
                        'G':'Deficient and Bankrupt',
                        'H':'Deficient and Deliquent',
                        'J':'Delinquent and Bankrput',
                        'K':'Deficient, Delinquent and Bankrupt',
                        'C':'Creations and/or Redemptions Suspended for Exchange Traded Product ',
                        'N':'Normal (Default): Issuer Is NOT Deficient, Delinquent, or Bankrupt ',
                        ' ':'Not available'
                    }
    roundLotsOnly = {
                        'Y':'Nasdaq system only accepts round lots',
                        'N':'Nasdaq system does not have any order size restrictions for this security. Odd and mixed lot orders are allowed'
                    }
    authenticity = {
                        'P':'Live/Production ',
                        'T':'Test'
                    }
    shortSaleThresholdIndicator = {
                        'Y':'Issue is restricted under SEC Rule 203(b)(3) ',
                        'N':'Issue is not restricted ',
                        ' ': 'Threshold Indicator not available '
                    }
    IPOFlag = {
                        'Y':'Nasdaq listed instrument is set up as a new IPO security ',
                        'N':'Nasdaq listed instrument is not set up as a new IPO security ',
                        ' ':'Not available'
                    }
    LULDPriceTier = {
                        1:'Tier 1 NMS Stocks and select ETPs',
                        2:'Tier 2 NMS Stocks ',
                        ' ':'Not available'
                    }
    ETPFlag = {
                        'Y':'Instrument is an ETP ',
                        'N':'Instrument is not an ETP ',
                        ' ':'Not available'
                    }
    inverseIndicator = {
                        'Y':'ETP is an Inverse ETP',
                        'N':'ETP is not an Inverse ETP'
                    }
    tradingStates = {
                        'H':'Halted across all U.S. equity markets / SROs ',
                        'P':'Paused across all U.S. equity markets / SROs (Nasdaq-­­listed securities only) ',
                        'Q':'Quotation only period for cross SRO halt or pause',
                        'T':'Trading on NASDAQ'
                    }
    regSHOAction = {
                        '0':'No price test in place',
                        '1':'Reg SHO Short Sale Price Test Restriction in effect due to an intra--­day price drop in security',
                        '2':'Reg SHO Short Sale Price Test Restriction remains in effect'
                    }
    primaryMarketMaker = {
                        'Y':'primary market maker',
                        'N':'non primary market maker'
                    }
    marketMakerModes = {
                        'N':'Normal',
                        'P':'Passive',
                        'S':'Syndicate',
                        'R':'Pre-syndicate',
                        'L':'Penalty'
                    }
    marketParticipantStates = {
                        'A':'Active',
                        'E':'Excused',
                        'W':'Withdrawn',
                        'S':'Suspended',
                        'D':'Deleted'
                    }
    breachedLevel = {
                        '1':'Level1',
                        '2':'Level2',
                        '3':'Level3'
                    }
    IPOQuotationReleaseQualifier = {
                        'A':'Anticipated quotation',
                        'C':'IPO Release Canceled/Postponed'
                    }
    marketCode = {
                        'Q':'Nasdaq',
                        'B':'BX',
                        'X':'PSX'
                    }
    operationalHaltAction = {
                        'H':'Operationally Halted on the identified Market',
                        'T':'Operational Halt has been lifted and Trading resumed'
                    }
    buyAndSellIndicator = {
                        'B':'Buy Order',
                        'S':'Sell Order'
                    }
    printable = {
                        'N':'Non-Printable ',
                        'Y':'Printable'
                    }
    crossType = {
                        'O':'Nasdaq Opening Cross',
                        'C':'Nasdaq Closing Cross',
                        'H':'Cross for IPO and halted / paused securities',
                        'I':'Nasdaq Cross Network: Intraday Cross and Post Close Cross'
                    }
    priceVariationIndicator = {
                        'L':'Less than 1%',
                        '1':'1 to 1.99%',
                        '2':'2 to 2.99%',
                        '3':'3 to 3.99%',
                        '4':'4 to 4.99%',
                        '5':'5 to 5.99%',
                        '6':'6 to 6.99%',
                        '7':'7 to 7.99%',
                        '8':'8 to 8.99%',
                        '9':'9 to 9.99%',
                        'A':'10 to 19.99%',
                        'B':'20 to 29.99%',
                        'C':'30 or great',
                        ' ':'Cannot be calculated'
                    }
    interestFlag = {
                        'B':'RPI orders available on the buy side',
                        'S':'RPI orders available on the sell side',
                        'A':'RPI orders available on both sides (buy and sell)',
                        'N':'No RPI orders available'
                    }
    

#对指南手册中所有的message类型都定义了类并打包了解码方法以便于随时调用

    
class SystemEventMessage():
    def __init__(self, message):
        self.type = 'S'
        self.description = 'System Event Message'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack("!Q",messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.event) = struct.unpack('!3HIc',message[1:])

class StockDirectoryMessage():
    def __init__(self, message):
        self.type = 'R'
        self.description = 'Stock Directory Message'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
        self.adc,self.npc,self.stockcode,self.category,self.indicator,self.lotsize,
        self.lots,self.classification,self.issue,self.authenticity,self.shortsale,
        self.IPO,self.LULD,self.ETP,self.ETPleverage,self.ETPinverse) = struct.unpack('!3HI8s2cI2c2s5cIc',message[1:])

class StockTradingActionMessage():
    def __init__(self, message):
        self.type = 'H'
        self.description = "Stock Trading Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.stockcode,self.state,self.reserved,self.reason) = struct.unpack('!3HI8s2c4s',message[1:])

class RegSHOMessage():
    def __init__(self, message):
        self.type = 'Y'
        self.description = 'Reg SHO Short Sale Message'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.stockcode,self.action) = struct.unpack('!3HI8sc',message[1:])

class MarketParticipantPositionMessage():
    def __init__(self, message):
        self.type = 'L'
        self.description = 'Market Participant Message'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.MPID,self.stockcode,self.primary,self.mode,self.participant) = struct.unpack('!3HI4s8s3c',message[1:])
        
class MWCBDeclineLevelMessage():
    def __init__(self,message):
        self.type = 'V'
        self.description = 'MWCB Decline Level Message'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.price1,self.price2,self.price3) = struct.unpack('!3HI3Q',message[1:])
        
class MWCBStatusMessage():
    def __init__(self,message):
        self.type = 'W'
        self.description = 'MWCB Status Message '
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.breached) = struct.unpack('!3HIc',message[1:])

class  IPOQuotingPeriodUpdate():
    def __init__(self,message):
        self.type = 'K'
        self.description = ' IPO Quoting Period Update'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.stockcode,self.IPOtime,self.IPOqualifier,self.IPOprice) = struct.unpack('!3HI8sIcI',message[1:])

class LULDAuctionCollar():
    def __init__(self,message):
        self.type = 'J'
        self.description = 'Limit Up – Limit Down (LULD) Auction Collar'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.stockcode,self.refeprice,self.upprice,self.lowprice,self.extention) = struct.unpack('!3HI8s4I',message[1:])

class OperationalHalt():
    def __init__(self,message):
        self.type = 'h'
        self.description = 'Operational Halt'
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.stockcode,self.marketcode,self.haltaction) = struct.unpack('!3HI8s2c',message[1:])
        
class AddOrderMessage():
    def __init__(self, message):
        self.type = 'A'
        self.description = "Add Order Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.ordernumber,self.direction,self.shares,self.stockcode,self.price) = struct.unpack('!3HIQcI8sI',message[1:])
        
class AddOrderMPIDMessage():
    def __init__(self, message):
        self.type = 'F'
        self.description = "Add Order w/ MPID Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.ordernumber,self.direction,self.shares,self.stockcode,self.price,self.attribution) = struct.unpack('!3HIQcI8sI4s',message[1:])
        
class OrderExecutedMessage():
    def __init__(self, message):
        self.type = 'E'
        self.description = "Order Executed Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.ordernumber,self.exeshares,self.matchnumber) = struct.unpack('!3HIQIQ',message[1:])

class OrderExecutedPriceMessage():
    def __init__(self, message):
        self.type = 'C'
        self.description = "Order Executed w/ Price Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.ordernumber,self.exeshares,self.matchnumber,self.printable,self.exeprice) = struct.unpack('!3HIQIQcI',message[1:])

class OrderCancelMessage():
    def __init__(self, message):
        self.type = 'X'
        self.description = "Order Cancel Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.ordernumber,self.caclshares) = struct.unpack('!3HIQI',message[1:])

class OrderDeleteMessage():
    def __init__(self, message):
        self.type = 'D'
        self.description = "Order Delete Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.ordernumber) = struct.unpack('!3HIQ',message[1:])

class OrderReplaceMessage():
    def __init__(self, message):
        self.type = 'U'
        self.description = "Order Replaced Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.oldordernumber,self.newordernumber,self.shares,self.price) = struct.unpack('!3HI2Q2I',message[1:])

class TradeMessage():
    def __init__(self, message):
        self.type = 'P'
        self.description = "Trade Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.ordernumber,self.indicator,self.shares,self.stockcode,self.price,self.matchnumber) = struct.unpack('!3HIQcI8sIQ',message[1:])

class CrossTradeMessage():
    def __init__(self, message):
        self.type = 'Q'
        self.description = "Cross Trade Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.shares,self.stockcode,self.price,self.matchnumber,self.crosstype) = struct.unpack('!3HIQ8sIQc',message[1:])

class BrokenTradeMessage():
    def __init__(self, message):
        self.type = 'B'
        self.description = "Broken Trade Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.matchnumber) = struct.unpack('!3HIQ',message[1:])

class NoiiMessage():
    def __init__(self, message):
        self.type = 'I' 
        self.description = "NOII Message"
        messagetime = b'\x00\x00' + message[5:11]
        (self.timestamp,) = struct.unpack('!Q',messagetime)
        (self.stocklocal,self.trackingnumber,
         self.adc,self.npc,self.pairedshares, self.imbalance, self.imbalancedirection,
        self.ticker, self.farprice, self.nearprice, self.currentrefeprice,
        self.crosstype, self.pricevariationindicator) = struct.unpack('!3HI2Qc8s3I2c', message[1:])
#class RPII():
#    def __init__(self,message):
#        self.type = 'N'
#        self.description = 'Retail Price Improvement Indicato'
#        messagetime = b'\x00\x00' + message[5:11]
#        (self.timestamp,) = struct.unpack('!Q',messagetime)
#        (self.stocklocal,self.trackingnumber,
#         self.adc,self.npc,self.stockcode,self.interset) = struct.unpack('!3HI8sc',message[1:])

        
