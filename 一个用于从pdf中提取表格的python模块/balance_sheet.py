# coding by Begoenix
# last edit Jun 15, 2022
# in St.Louis, MO, USA

import requests
import random
import time
import datetime as dt
import requests as rt
import fitz as ft
import cv2 as cv
import numpy as np
import pdfplumber as pdfer
import pandas as pd
import os



user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
    ]

#dict_news_type = {"年度报告全文":"10k"}

class PDF_receiver:
    def __init__(self):
        self.notices_url = "https://np-anotice-stock.eastmoney.com/api/security/ann?cb=jQuery0_{}&sr=-1&page_size=100&page_index={}&ann_type=A&client_source=web&stock_list={}&f_node=0&s_node=0"
        self.noticesdownload_url = "https://pdf.dfcfw.com/pdf/H2_{}_1.pdf"
        self.reports_url = "https://reportapi.eastmoney.com/report/list?cb=datatable8680457&pageNo={}&pageSize=100&code={}&industryCode=*&industry=*&rating=*&ratingchange=*&beginTime={}&endTime={}&fields=&qType=0&_="
        self.reportsdownload_url = "https://pdf.dfcfw.com/pdf/H3_{}_1.pdf"
        pass

    def get_user_agent(self):
        rdnum = random.randint(0,len(user_agents)-1)

        return user_agents[rdnum]

    def get_stock_notices_page(self,page,stock_code):
        time_st = int(round(time.time() * 1000))
        url = self.notices_url.format(time_st, page, stock_code)
        notices_outcome = rt.get(url, headers = {"user_agent": self.get_user_agent()})
        time.sleep(1 + random.randint(1,11)/10 + random.randint(1,11)/100)
        return notices_outcome.text

    def get_stock_reports_page(self, page, stock_code, start_date, end_date):
        time_st = int(round(time.time() * 1000))
        url = self.reports_url.format(page, stock_code, start_date, end_date)
        reports_outcome = rt.get(url, headers = {"user_agent": self.get_user_agent()})
        time.sleep(1 + random.randint(1,11)/10 + random.randint(1,11)/100)
        return reports_outcome.text


    def get_required_notices(self, start_time, end_time, stock_code, news_type = "all"):

        '''get the required news, can change type of news
        '''

        start_time = dt.datetime.strptime(start_time, "%Y-%m-%d")
        end_time = dt.datetime.strptime(end_time, "%Y-%m-%d")
        time_tem = start_time
        start_time = end_time
        end_time = time_tem
        data_reports = pd.DataFrame()
        page_start = 1
        text_0 = self.get_stock_notices_page(1, stock_code)
        dict_index = text_0.index("(")
        text_0 = text_0[dict_index + 1: -1]
        time_0 = eval(text_0)["data"]["list"][0]["eiTime"].split(" ")[0]
        time_0 = dt.datetime.strptime(time_0, "%Y-%m-%d")
        time_0n = eval(text_0)["data"]["list"][-1]["eiTime"].split(" ")[0]
        time_0n = dt.datetime.strptime(time_0n, "%Y-%m-%d")
        length_tem = len((eval(text_0))["data"]["list"])

        while start_time < time_0n and length_tem > 3 :
            page_start += 1
            text_0 = self.get_stock_notices_page(page_start, stock_code)
            dict_index = text_0.index("(")
            text_0 = text_0[dict_index + 1: -1]
            length_tem = len((eval(text_0))["data"]["list"])
            if length_tem < 3:
                return None
            else:
                continue
            time_0 = eval(text_0)["data"]["list"][0]["eiTime"].split(" ")[0]
            time_0 = dt.datetime.strptime(time_0, "%Y-%m-%d")
            time_0n = eval(text_0)["data"]["list"][-1]["eiTime"].split(" ")[0]
            time_0n = dt.datetime.strptime(time_0n, "%Y-%m-%d")
            length_tem = len((eval(text_0))["data"]["list"])


        text_tem = eval(text_0)["data"]["list"]
        start_note = 0
        for i in range(1, length_tem):
            time_tem = eval(text_0)["data"]["list"][length_tem - 1 - i]["eiTime"].split(" ")[0]
            time_tem = dt.datetime.strptime(time_tem, "%Y-%m-%d")
            if time_tem > start_time and i < length_tem - 1:
                start_note = length_tem - i
                break
            elif i == length_tem - 1:
                start_note = 0
                break


        page_end = 1
        text_0 = self.get_stock_notices_page(1, stock_code)
        dict_index = text_0.index("(")
        text_0 = text_0[dict_index + 1: -1]
        time_0 = eval(text_0)["data"]["list"][0]["eiTime"].split(" ")[0]
        time_0 = dt.datetime.strptime(time_0, "%Y-%m-%d")
        time_0n = eval(text_0)["data"]["list"][-1]["eiTime"].split(" ")[0]
        time_0n = dt.datetime.strptime(time_0n, "%Y-%m-%d")
        length_tem = len((eval(text_0))["data"]["list"])
        while end_time < time_0n and length_tem > 3:
            page_end += 1
            text_0 = self.get_stock_notices_page(page_end, stock_code)
            dict_index = text_0.index("(")
            text_0 = text_0[dict_index + 1: -1]
            length_tem = len((eval(text_0))["data"]["list"])
            if length_tem < 3:
                break
            else:
                pass
            time_0 = eval(text_0)["data"]["list"][0]["eiTime"].split(" ")[0]
            time_0 = dt.datetime.strptime(time_0, "%Y-%m-%d")
            time_0n = eval(text_0)["data"]["list"][-1]["eiTime"].split(" ")[0]
            time_0n = dt.datetime.strptime(time_0n, "%Y-%m-%d")


        text_tem = eval(text_0)["data"]["list"]
        end_note = 0
        for i in range(length_tem):
            time_tem = eval(text_0)["data"]["list"][i]["eiTime"].split(" ")[0]
            time_tem = dt.datetime.strptime(time_tem, "%Y-%m-%d")
            if time_tem < end_time and i < length_tem - 1:
                end_note = i
                break
            elif i == length_tem - 1:
                end_note = length_tem - 1
                break
        news_numb = 1
        for i in range(page_start, page_end + 1):
            text_tem = self.get_stock_notices_page(i, stock_code)
            index_tem = text_tem.index("(")
            text_tem = text_tem[index_tem + 1: -1]
            text_tem = eval(text_tem)["data"]["list"]
            if i == page_start:
                text_tem = text_tem[start_note:]
            else:
                pass
            if i == page_end:
                text_tem = text_tem[:end_note]
            for j in range(len(text_tem)):
                art_code = text_tem[j]["art_code"]
                stock_code = stock_code
                art_type = text_tem[j]["columns"][0]["column_name"]
                title = text_tem[j]["title_ch"]
                retime = text_tem[j]["eiTime"].split(" ")[0]
                if news_type == "all":
                    pass
                elif art_type == news_type:
                    pass
                else:
                    continue
                data_tem = pd.DataFrame([[stock_code, title, art_type, art_code, retime]], index = [news_numb],
                                        columns = ["stock_code", "title", "report_type", "report_code", "report_time"])
                data_reports = pd.concat([data_reports, data_tem], axis = 0)
                news_numb += 1

        return data_reports


    def get_required_reports(self, start_time, end_time, stock_code):

        '''get the required reports
        '''

        str_reports = self.get_stock_reports_page(1, stock_code, start_time, end_time)
        dict_reports = eval(str_reports[str_reports.index("hits")-2:-1])
        hits = dict_reports["hits"]
        if hits <= 100:
            pages = 1
        else:
            pages = int(hits/100) + 1

        data_reports = pd.DataFrame()
        for page in range(1, pages+1):
            str_reports_tem = self.get_stock_reports_page(page, stock_code, start_time, end_time)
            dict_reports_tem = eval(str_reports_tem[str_reports_tem.index("hits")-2:-1])["data"]
            for item in dict_reports_tem:
                orgsname = item["orgSName"]
                publishdate = item["publishDate"]
                infocode = item["infoCode"]
                oneeps = item["predictNextYearEps"]
                onepe = item["predictNextYearPe"]
                twoeps = item["predictNextTwoYearEps"]
                twope = item["predictNextTwoYearPe"]
                indus = item["indvInduName"]
                rating = item["emRatingName"]
                data_tem = pd.DataFrame([[orgsname, publishdate, infocode, oneeps, onepe, twoeps, twope,
                                         indus, rating]], index = [0], columns = ["issuer", "publishdate", "infocode",
                                                                                 "1_eps", "1_pe", "2_eps", "2_pe",
                                                                                 "industry", "rating"])
                data_reports = pd.concat([data_reports, data_tem], axis = 0)

        return data_reports


    def download_notices(self, art_code):
        url = self.noticesdownload_url.format(art_code)
        pdf = rt.get(url, headers = {"user_agent": self.get_user_agent()}).content
        with open("temp.pdf", "wb") as file:
            file.write(pdf)
        return None

    def download_reports(self, report_code):
        url = self.reportsdownload_url.format(report_code)
        pdf = rt.get(url, headers = {"user_agent": self.get_user_agent()}).content
        with open("temp.pdf", "wb") as file:
            file.write(pdf)
        return None

    def table_reader(self, pdf, page_list, filename, x_zoom = 1.5, y_zoom = 2):
        '''用于提取pdf中的表格
            参数从左到右分别为
            pdf文件位置
            页码列表
            输出表格储存的位置
            对每一页图片化后x轴的放大倍数，default为1.5倍
            对每一页图片化后y轴的放大倍数，default为2倍
            注意，当表格提取不完整时，可适当提高后两个参数，但不推荐超过4或5
        '''
        if not os.path.exists(filename):
            os.makedirs(filename)
        else:
            pass
        pdf1 = ft.open(pdf)
        cross_page_code = 0
        data_crosspage = pd.DataFrame()
        file = pdfer.open(pdf)
        loading_code = 0
        # 加载对象
        for page in page_list:
            print("processing page {}".format(page))
            #加载该页的文本的内容
            content = file.pages[page]
            table_businessdata = content.extract_words()
            #将需要处理的pdf页转化成image，格式为jpg；只会占用一次空间，使用结束后可删除，现阶段由于debug还未上线自动删除
            page1 = pdf1.load_page(page)
            zoomx = x_zoom
            zoomy = y_zoom
            mat = ft.Matrix(zoomx, zoomy)
            pix = page1.get_pixmap(matrix=mat)
            pix.save("temps.jpg")
            image = cv.imread("temps.jpg", 1)

            #图片灰度化并二项化
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            binary = cv.adaptiveThreshold(~gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 35, -5)

            #提取列线
            scale = 40
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (scale, 1))
            eroded = cv.erode(binary, kernel, iterations=1)
            dilatedcol = cv.dilate(eroded, kernel, iterations=1)

            #提取行线
            scale = 20
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, scale))
            eroded = cv.erode(binary, kernel, iterations=1)
            dilatedrow = cv.dilate(eroded, kernel, iterations=1)

            #获得交点图
            bitwiseAnd = cv.bitwise_and(dilatedcol, dilatedrow)
            cv.imwrite("temps2.jpg",bitwiseAnd)
            cv.imwrite("temps3.jpg", dilatedrow)

            #获取该页内可能存在表格的区域，判定方法为图片左侧存在大于20个单位的列线
            list_range = []
            now = 0
            for y in range(len(dilatedrow) - 1):
                if y < now:
                    continue
                else:
                    pass
                for x in range(int(len(dilatedrow) / 2)):
                    if y < now:
                        break
                    else:
                        pass
                    if dilatedrow[y][x] > 0 and dilatedrow[y + 1][x] > 0:
                        start = y / zoomy
                        for k in range(y + 1, len(dilatedrow)-1):
                            if dilatedrow[k][x] > 0 and dilatedrow[k + 1][x] > 0:
                                continue
                            else:
                                end = k / zoomy
                                if end - start > 20:
                                    list_range += [(int(start) - 2, int(end) + 2)]
                                else:
                                    pass
                                now = k
                                break

            #获取图片内所有点的像素位置，无论如何，同一个视觉点都会存在一个及以上的像素点，因此list_points是原始点集
            list_points = []
            for i in range(len(bitwiseAnd)):
                if bitwiseAnd[i].any() > 0:
                    for j in range(len(bitwiseAnd[i])):
                        if bitwiseAnd[i][j] > 0:
                            list_points += [(i / zoomy, j / zoomx)]
                        else:
                            continue
                else:
                    continue

            #基于原始点集，获取集合后的统一点集，即把临近的点整合为同一个点，临近的判定标准为8像素单位
            list_points_new = []
            ys, xs = np.where(bitwiseAnd > 1)
            ys = np.sort(ys / y_zoom)
            xs = np.sort(xs / x_zoom)
            if not len(ys) or not len(xs):
                continue
            list_ys = [ys[0]]
            list_xs = [xs[0]]
            for i in range(1, len(ys)):
                if ys[i] - ys[i - 1] > 8:
                    list_ys.append(ys[i])
            for i in range(1, len(xs)):
                if xs[i] - xs[i - 1] > 8:
                    list_xs.append(xs[i])
            for i in list_ys:
                for j in list_xs:
                    for k in range(len(list_points)):
                        if int(list_points[k][0]) in range(int(i) - 8, int(i) + 8) and int(list_points[k][1]) in range(int(j) - 8, int(j) + 8):
                            if (i, j) not in list_points_new:
                                list_points_new.append((i, j))
                                del list_points[k]
                                break
                            else:
                                pass

            #对于图片范围内存在的每一个表格区域，分别提取属于该区域的点，表现为该区域适配的横纵坐标，并获取表格的最大行列数，写入中间变量data_tables
            data_tables = pd.DataFrame(index=[i for i in range(len(list_range))], columns=["ys", "xs", "row", "col"])

            for i in range(len(list_range)):
                ran = list_range[i]
                list_y_tem = []
                list_x_tem = []
                for j in list_points_new:
                    if int(j[0]) in range(ran[0], ran[1]):
                        list_y_tem += [j[0]]
                        list_x_tem += [j[1]]
                    else:
                        pass
                if len(list_y_tem) == 0 or len(list_x_tem) == 0:
                    data_tables.iloc[i, 2] = 0
                    data_tables.iloc[i, 3] = 0
                    data_tables.iloc[i, 0] = []
                    data_tables.iloc[i, 1] = []
                    continue
                else:
                    pass
                row = list_y_tem.count(list_y_tem[0])
                col = list_x_tem.count(list_x_tem[0])
                list_y_tem2 = []
                list_x_tem2 = []
                for j in list_y_tem:
                    count = list_y_tem.count(j)
                    if count > row:
                         row = count
                    if j not in list_y_tem2:
                        list_y_tem2.append(j)
                for j in list_x_tem:
                    count = list_x_tem.count(j)
                    if count > col:
                        col = count
                    if j not in list_x_tem2:
                        list_x_tem2.append(j)
                data_tables.iloc[i, 2] = col - 1
                data_tables.iloc[i, 3] = row - 1
                data_tables.iloc[i, 0] = sorted(list_y_tem2)
                data_tables.iloc[i, 1] = sorted(list_x_tem2)

            #根据中间变量，对每个表，使用横纵坐标划分单元格区域，并根据交点的存在与否判断该单元格是否存在，将存在的写入中间变量list_mess
            #list_mess的格式为：[左横坐标，右横坐标，上纵坐标，下纵坐标，文本，在输出dataframe中的相对位置]
            list_mess = []
            for i in range(len(list_range)):
                ys_tem = data_tables.iloc[i, 0]
                xs_tem = data_tables.iloc[i, 1]
                list_tem = []
                for j in range(len(ys_tem) - 1):
                    x_code = 0
                    for k in range(len(xs_tem) - 1):
                        for m in range(k+1, len(xs_tem)):
                            if (ys_tem[j], xs_tem[k]) in list_points_new and (ys_tem[j+1], xs_tem[m]) in list_points_new and (ys_tem[j], xs_tem[m]) in list_points_new and (ys_tem[j+1], xs_tem[k]) in list_points_new:
                                list_now = [xs_tem[k], xs_tem[m], ys_tem[j], ys_tem[j + 1], "", (j,x_code)]
                                list_tem += [list_now]
                                x_code += 1
                                break
                list_mess += [list_tem]

            #根据pdf中文本的坐标位置，选择刚好能容纳其的单元格并写入对应的文本，支持跨页表格的合并
            count = 0
            for j in table_businessdata[:-1]:
                for k in range(len(list_range)):
                    if len(list_mess[k]) == 0:
                        continue
                    else:
                        pass
                    ran = list_range[k]
                    if int(j["top"]) in range(ran[0], ran[1]):
                        for m in list_mess[k]:
                            if j["x0"] > m[0] and j["x1"] < m[1] and j["top"] > m[2] and j["bottom"] < m[3]:
                                m[4] += j["text"]
                                if count == 0:
                                    cross_page_code = 1
                                elif count == len(table_businessdata)-2:
                                    loading_code = 1
                                break
                count += 1

            #根据写入的文本与输出坐标，写入输出表格的对应位置
            for i in range(len(list_range)):
                row = data_tables.iloc[i, 2]
                col = data_tables.iloc[i, 3]
                data_tem = pd.DataFrame(index=[j for j in range(row)],
                                        columns=[j for j in range(col)])
                for j in range(len(list_mess[i])):
                    rs = list_mess[i][j][-1][0]
                    cs = list_mess[i][j][-1][1]
                    data_tem.iloc[rs, cs] = list_mess[i][j][4]
                if len(data_crosspage) and cross_page_code and (i == 0):
                    data_tem = pd.concat([data_crosspage, data_tem], axis = 0)
                else:
                    pass
                cross_page_code = 0
                data_crosspage = pd.DataFrame()
                if loading_code and (i==len(list_range)-1):
                    data_crosspage = data_tem
                    loading_code = 0
                    if page_list.index(page) == len(page_list)-1:
                        pass
                    else:
                        continue
                data_tem.to_csv("{}\\{}_{}.csv".format(filename, page, i), encoding="utf-8-sig")

        file.close()
        return None

    def extact_title(self, pdf):
        outcome = ""
        with pdfer.open("temp.pdf") as pdf:
            for page in pdf.pages:
                text_tem = page.extract_text()
                if "目录" in text_tem:
                    outcome = text_tem
                    break
                else:
                    pass
            pdf.close()
        list1 = outcome.split("\n")
        page_code1 = ""
        page_code2 = ""
        page_code3 = ""
        for line in list1:
            if "公司业务概要" in line:
                for num in line:
                    if ord(num) >= 48 and ord(num) <= 57:
                        page_code1 += num
            elif "经营情况讨论与分析" in line:
                for num in line:
                    if ord(num) >= 48 and ord(num) <= 57:
                        page_code2 += num
            elif "重要事项" in line:
                for num in line:
                    if ord(num) >= 48 and ord(num) <= 57:
                        page_code3 += num
        page_numb = 0
        drift = 0
        page_target = [i for i in range(int(page_code1) - 2, int(page_code1) + 2)]
        text_business = ""
        table_business = []
        ima_business = []
        text_businessdata = ""
        table_businessdata = []
        ima_businessdata = []
        with pdfer.open("temp.pdf") as pdf:
            for page in pdf.pages:
                page_numb += 1
                if page_numb in page_target:
                    text_tem = page.extract_text()
                    if "公司业务概要" in text_tem:
                        drift = page_numb - int(page_code1)
                        break
            page_code1 = int(page_code1) + drift
            page_code2 = int(page_code2) + drift
            page_code3 = int(page_code3) + drift
            page_numb = 0











# 1.1.1 修改了table_reader Jun-5-2022
# 1.1.2 增加了爬取券商研报的功能:get_stock_reports_page()与get_required_reports() Jun-15-2022