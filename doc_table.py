
CELL_BOUNDARY = '+'
ROW_BOUNDARY = '\n'

PADDING = ' '
LEN_PADDING = 1

ROW_META = '-'
COLUMN_META = '|'

VALUE_PADDING = ' '


class Cell(object):

    def __init__(self, value):
        self.value = str(value)
        self.value = ' ' if not self.value else self.value
        self.value_lines = self.value.splitlines()
        self.height = len(self.value_lines)
        self.value_lines_len = []
        # 每一个cell的每一段的长度
        for vl in self.value_lines:
            tmp_dv = 0
            for v in vl:
                tmp_dv += int(len(str(v).encode('utf-8')) / 1.5) if ord(v) > 256 else len(v)
            self.value_lines_len.append(tmp_dv)
        self.width = max(self.value_lines_len)
        # 画图时候的长宽
        self.draw_width = self.width
        self.draw_height = self.height
        return

    def __str__(self):
        return 'Cell: <%s, %s, %s>' % (self.value, self.draw_width, self.draw_height)

    def __repr__(self):
        return self.__str__()


class Table(object):
    def __init__(self, data, name='table'):
        self.name = name
        self.data = data
        self.cells = []
        self.graph = ''
        self.rows = len(self.data)
        self.cols = max([len(i) for i in data])
        return

    def _cal_cells(self):
        cells = []
        # 补齐行数以及计算最大行宽和最大列高
        row_index = 0
        col_width = [[] for _ in range(self.cols)]
        row_height = [[] for _ in range(self.rows)]
        while row_index < self.rows:
            row = self.data[row_index]
            row_cells = []
            col_index = 0
            delta = self.cols - len(row)
            while col_index < self.cols:
                if self.cols - col_index <= delta:
                    cell = Cell(' ')
                else:
                    cell = Cell(row[col_index])
                row_cells.append(cell)
                col_width[col_index].append(cell.draw_width)
                row_height[row_index].append(cell.draw_height)
                col_index += 1
            row_index += 1
            cells.append(row_cells)
        # 第二个参数是加上间隙
        max_row_height = [(max(i), max(i) + 2) for i in row_height]
        max_col_width = [(max(i), max(i) + 2) for i in col_width]
        row_index = col_index = 0
        while row_index < self.rows:
            col_index = 0
            while col_index < self.cols:
                cell = cells[row_index][col_index]
                cell.draw_width = max_col_width[col_index][0]
                cell.draw_height = max_row_height[row_index][0]
                delta = cell.draw_height - cell.height
                if delta:
                    cell.value_lines.extend([' '] * delta)
                    cell.value_lines_len.extend([1] * delta)
                col_index += 1
            row_index += 1
        return cells, max_col_width, max_row_height

    def draw(self, redraw=False):
        if redraw is True:
            self.cells = []
            self.graph = ''
        if not self.graph:
            self.cells, self.max_col_width, self.max_row_height = self._cal_cells()
        else:
            return self.graph
        col_row_width = [i[1] for i in self.max_col_width]
        col_space = COLUMN_META
        up_down_line = CELL_BOUNDARY
        for ar in col_row_width:
            up_down_line += ROW_META * ar + CELL_BOUNDARY
            col_space += PADDING * ar + COLUMN_META
        up_down_line += ROW_BOUNDARY
        col_space += ROW_BOUNDARY
        graph = ''
        for row_cells in self.cells:
            # 一行一行画
            # 先画封顶的那一段和上空隙 +-----+-----+--------+\n
            graph += up_down_line

            # 然后是空隙             |     |     |        |\n
            graph += col_space

            # 接着画每一行每一个cell和它的间隔
            # value一行一行画
            d_height = row_cells[0].draw_height
            hindex = 0
            while hindex < d_height:
                for cell in row_cells:
                    graph += COLUMN_META + PADDING + cell.value_lines[hindex]
                    right_padding_count = cell.draw_width - cell.value_lines_len[hindex]
                    graph += PADDING * right_padding_count + PADDING
                graph += COLUMN_META + ROW_BOUNDARY
                hindex += 1
            # 画下面的空隙
            graph += col_space
        graph += up_down_line
        self.graph = graph
        return graph

    def draw_to_file(self, f):
        f.write(self.draw())
        return


def main():
    tt = Table(data=[['''编译层负责把语法解析\n负责把语法解析成字节码, 然后提供字节码执行接口''']])
    print(tt.draw())
    data = [['排序方法\n这是换行', '平均情况', '最坏情况', '最好情况', '空间复杂度', '稳定性', '复杂性'],
            ['直接插入排序', 'O(n^2)', 'O(n^2)', 'O(n)', 'O(1)', '稳定', '简单', '其他列'],
            ['希尔排序', 'O(nlog2n)', 'O(nlog2n)', '', 'O(1)', '不稳定', '叫复杂\n有三行\n第三行哦嘿嘿']
            ]
    t = Table(data=data)
    print(t.draw())
    with open('draw_doc_table_test', 'w') as f:
        t.draw_to_file(f)


if __name__ == '__main__':
    main()
