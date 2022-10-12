import balance_sheet as bs

# 调用pdf处理器的类
pdf = bs.PDF_receiver()

# 设置你需要提取的页码范围，格式为list且推荐为连续页（涉及到跨页合并表格的问题）
list_page = [i for i in range(27,34)]
#该页码范围选取了最典型的实线表，对于没有实线边界的表格无法提取
#对于最传统的实线表格，提取准确性高于常用的pdfplumber/camelot等工具

#获取中国国航2021年年度报告的相关信息，信息来源为东方财富
outcome = pdf.get_required_notices("2021-12-31", "2022-06-01", "601111", news_type = "年度报告全文")
#获取中国国航2021年年度报告全文pdf
notice_code = outcome.report_code.iloc[0]
#下载报表
pdf.download_notices(notice_code)
#提取表格并存在相对路径中的601111文件夹下
pdf.table_reader("temp.pdf", list_page, "601111", x_zoom=2, y_zoom=2)