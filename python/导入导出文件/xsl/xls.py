import xlwt


dict_list = [
    {'_id': '5bf63a0fcb495b2b8cd01434', 'language': 'sl', 'num': 258},
    {'_id': '5bf63b47cb495b2b8cd0185f', 'language': 'az', 'num': 21},
    {'_id': '5bf63bf5cb495b2b8cd01a8a', 'language': 'ca', 'num': 166},
    {'_id': '5bf63c48cb495b2b8cd01b9c', 'language': 'cs', 'num': 69},
    {'_id': '5bf63cd7cb495b2b8cd01d7e', 'language': 'mt', 'num': 3079},
    {'_id': '5bf63ce0cb495b2b8cd01d9d', 'language': 'ro', 'num': 117},
    {'_id': '5bf63d00cb495b2b8cd01e11', 'language': 'lt', 'num': 1885},
    {'_id': '5bf63f30cb495b2b8cd0255f', 'language': 'sk', 'num': 364},
    {'_id': '5bf6437ccb495b2b8cd033a6', 'language': 'hu', 'num': 45},
    {'_id': '5bf6445acb495b2b8cd036b9', 'language': 'pt', 'num': 1428},
    {'_id': '5bf64848cb495b2b8cd043be', 'language': 'ga', 'num': 14},
    {'_id': '5bf64b18cb495b2b8cd04c83', 'language': 'lv', 'num': 37},
    {'_id': '5bf64bb6cb495b2b8cd04e9d', 'language': 'bg', 'num': 298},
    {'_id': '5bf64d20cb495b2b8cd0529e', 'language': 'sv', 'num': 1366},
    {'_id': '5bf64d69cb495b2b8cd05390', 'language': 'ko', 'num': 489},
    {'_id': '5bf64f98cb495b2b8cd05b0d', 'language': 'el', 'num': 31},
    {'_id': '5bf64feccb495b2b8cd05c29', 'language': 'he', 'num': 80},
    {'_id': '5bf651a3cb495b2b8cd0618d', 'language': 'id', 'num': 159},
    {'_id': '5bf652bccb495b2b8cd0650d', 'language': 'mg', 'num': 154},
    {'_id': '5bf66488cb495b2b8cd0985e', 'language': 'vi', 'num': 29},
    {'_id': '5bf67bdacb495b2b8cd11a2b', 'language': 'sr', 'num': 75},
    {'_id': '5bf67c0bcb495b2b8cd11ce2', 'language': 'sq', 'num': 38},
    {'_id': '5bf67c58cb495b2b8cd120ca', 'language': 'br', 'num': 615},
    {'_id': '5bf67c8ecb495b2b8cd12379', 'language': 'ja', 'num': 521},
    {'_id': '5bf67ce7cb495b2b8cd12879', 'language': 'ar', 'num': 7},
    {'_id': '5bf67ec2cb495b2b8cd1448a', 'language': 'ru', 'num': 2057},
    {'_id': '5bf68d13cb495b2b8cd1dc79', 'language': 'qu', 'num': 89},
    {'_id': '5bf68d2bcb495b2b8cd1dcd1', 'language': 'et', 'num': 361},
    {'_id': '5bf701f8cb495b2b8cd3144c', 'language': 'gl', 'num': 449},
    {'_id': '5bf70608cb495b2b8cd31a52', 'language': 'uk', 'num': 138},
    {'_id': '5bf7fe11cb495b2b8cd47946', 'language': 'vo', 'num': 4},
    {'_id': '5bf80665cb495b2b8cd49061', 'language': 'nb', 'num': 278},
    {'_id': '5bf81201cb495b2b8cd4ae53', 'language': 'eu', 'num': 114},
    {'_id': '5bf81e88cb495b2b8cd4cee2', 'language': 'ka', 'num': 3},
    {'_id': '5bf81f50cb495b2b8cd4d0f0', 'language': 'sw', 'num': 60},
    {'_id': '5bf82379cb495b2b8cd4dbc4', 'language': 'ms', 'num': 174},
    {'_id': '5bf83315cb495b2b8cd5030e', 'language': 'la', 'num': 28},
    {'_id': '5bf8f4e4cb495b2b8cd6e632', 'language': 'kk', 'num': 65},
    {'_id': '5bf8f6e0cb495b2b8cd6ebb8', 'language': 'ky', 'num': 7},
    {'_id': '5bfa5369cb495b2b8cda41ac', 'language': 'cy', 'num': 368},
    {'_id': '5bfaf774cb495b2b8cdbb3e3', 'language': 'eo', 'num': 41},
    {'_id': '5bfba06bcb495b2b8cdf3cba', 'language': 'hi', 'num': 6},
    {'_id': '5bfe6c76cb495b2b8cefbb14', 'language': 'is', 'num': 39},
    {'_id': '5bff70dbcb495b2b8cf27ef6', 'language': 'tl', 'num': 685},
    {'_id': '5c012b9fcb495b2b8cf63709', 'language': 'lb', 'num': 16},
    {'_id': '5c015fe8cb495b2b8cf6c00d', 'language': 'mk', 'num': 87},
    {'_id': '5c018582cb495b2b8cf6fa7e', 'language': 'an', 'num': 1},
    {'_id': '5c01f79acb495b2b8cf7ab2f', 'language': 'hr', 'num': 11},
    {'_id': '5c021bd5cb495b2b8cf7e1ce', 'language': 'th', 'num': 377},
    {'_id': '5c023caecb495b2b8cf8142e', 'language': 'nn', 'num': 93},
    {'_id': '5c0264a3cb495b2b8cf85438', 'language': 'rw', 'num': 30},
    {'_id': '5c026621cb495b2b8cf856c6', 'language': 'af', 'num': 12},
    {'_id': '5c03fa81cb495b2b8cfa61c7', 'language': 'be', 'num': 2},
    {'_id': '5c04a08dcb495b2b8cfc4e11', 'language': 'mn', 'num': 50},
    {'_id': '5c052f24cb495b2b8cff628b', 'language': 'ht', 'num': 10},
    {'_id': '5c0554fbcb495b2b8cffbc30', 'language': 'se', 'num': 6},
    {'_id': '5c05f8d0cb495b2b8c02fb23', 'language': 'zu', 'num': 1},
    {'_id': '5c06a489cb495b2b8c057e9d', 'language': 'ku', 'num': 2},
    {'_id': '5c08419bcb495b2b8c0becfc', 'language': 'xh', 'num': 20},
    {'_id': '5c0b46c3cb495b2b8c141f4b', 'language': 'am', 'num': 7},
    {'_id': '5c0b9198cb495b2b8c15a548', 'language': 'ta', 'num': 5},
    {'_id': '5c0bb96ecb495b2b8c1727cc', 'language': 'pa', 'num': 4},
    {'_id': '5c101cd7cb495b2b8c335049', 'language': 'hy', 'num': 2},
    {'_id': '5c1a0b2dcb495b2b8c585bdb', 'language': 'ml', 'num': 1},
]


def export_xsl(dict_list):
    header = ['_id', 'language', 'num']

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建一个Workbook对象，这就相当于创建了一个Excel文件
    sheet = book.add_sheet('test',
                           cell_overwrite_ok=True)  # # 其中的test是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False

    # 设置表头
    i = 0
    for k in header:
        sheet.write(0, i, k)
        i = i + 1

    # 数据写入excel
    row = 1
    for val in dict_list:
        print(val)
        sheet.write(row, 0, val['_id'])  # 第二行开始
        sheet.write(row, 1, val['language'])  # 第二行开始
        sheet.write(row, 2, val['num'])  # 第二行开始
        row = row + 1

    book.save('test1.xls')


if __name__ == '__main__':
    export_xsl(dict_list)
