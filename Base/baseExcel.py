import xlrd
import xlwt


class ExcelRead:
    """
    对excel文件进行操作
    """

    def __init__(self, excel_path, sheet_name="Sheet1"):
        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheet_by_name(sheet_name)
        # 获取第一行为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols

    def dict_date(self):
        """
        读取excel里的所有数据，格式为[{}]
        """
        if self.rowNum <= 1:
            print("总行数小于1")
            return None
        else:
            r = []
            j = 1
            for i in range(self.rowNum - 1):
                s = {}
                # 从第二行取对应的values值
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r

    def get_rowinfo(self, row):
        """
        获取exl中行信息,row--行数
        """
        if row <= 1:
            rowdata = None
        else:
            testdates = self.dict_date()
            rowdata = testdates[row - 2]
        return rowdata

    def get_colinfo(self, name):
        """
        获取exl中列信息
        """
        name_data = []
        testdates = self.dict_date()
        for data in testdates:
            name_data.append(data[name])
        return name_data

    def get_cellinfo(self, row, name):
        """
        获取exl中某一单元格信息，row--行数（int）；name--列名(char)
        """
        if row <= 1:
            rowdata = None
        else:
            testdates = self.dict_date()
            rowdata = testdates[row - 2][name]
        return rowdata


class ExcelWrite:
    """
    对exl进行写操作
    """
    def __init__(self, sheet_name="Sheet1"):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        # 获取工作表对象Worksheet
        self.worksheet = self.workbook.add_sheet(sheet_name)

    def set_header(self, list_data):
        """
        给exl表写入标题
        """
        if not isinstance(list_data, list):
            raise TypeError("数据必须是列表")
        keys_data = list(list_data[0].keys())
        num = len(keys_data)
        for c in range(num):
            self.worksheet.write(0, c, label=keys_data[c])

    def excl_write(self, list_data, excel_path):
        """
        表格写入全部数据,格式为：[{}]
        """
        if not isinstance(list_data, list):
            raise TypeError("数据必须是列表")
        # 获取每行列表
        self.set_header(list_data)
        rows_num = len(list_data)
        for r in range(rows_num):
            values_data = list(list_data[r].values())
            cows_num = len(values_data)
            for c in range(cows_num):
                self.worksheet.write(r + 1, c, values_data[c])
        # 保存数据到硬盘
        self.workbook.save(excel_path)


if __name__ == "__main__":
    path = r'D:\code\python_code\TestFramework_po\Data\DataDriver\ExcelDriver\project02\Excel数据驱动-登录.xlsx'
    sheet = 'Sheet1'
    excel = ExcelRead(path, sheet)
    res = excel.dict_date()
    print(res)
