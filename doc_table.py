
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
                tmp_dv += int(len(v.encode('utf-8')) / 1.5) if ord(v) > 256 else len(v)
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
        self.no_align_graph = ''
        self.rows = len(self.data)
        self.max_cols = max([len(i) for i in data])
        return

    def _cal_no_align_cells(self):
        cells = []
        row_index = 0
        row_height = [[] for _ in range(self.rows)]
        row_width = [[] for _ in range(self.rows)]
        while row_index < self.rows:
            row = self.data[row_index]
            row_cells = []
            col_index = 0
            while col_index < len(row) - 1:
                cell = Cell(row[col_index])
                row_cells.append(cell)
                row_width[row_index].append([col_index, cell.draw_width + 3])
                row_height[row_index].append(cell.draw_height)
                col_index += 1
            cell = Cell(row[-1])
            row_cells.append(cell)
            row_width[row_index].append([col_index, cell.draw_width + 4])
            row_height[row_index].append(cell.draw_height)
            cells.append(row_cells)
            row_index += 1
        max_row_width = max([sum([j[1] for j in i]) for i in row_width])
        max_row_height = [max(i) for i in row_height]
        row_index = 0
        # 尽可能平均分配大小
        while row_index < self.rows:
            tmp_max = max_row_width
            rest_cells = row_width[row_index]
            row_sum = 0
            last_cell = None
            while rest_cells:
                average = int(tmp_max / len(rest_cells))
                less_c = []
                for current_row in rest_cells:
                    last_cell = current_row
                    cl = current_row[1]
                    if cl >= average:
                        cells[row_index][current_row[0]].draw_width = cl
                        row_sum += cl
                        tmp_max -= cl
                    else:
                        less_c.append(current_row)
                if len(less_c) == len(rest_cells):
                    for i in less_c:
                        last_cell = i
                        cells[row_index][i[0]].draw_width = average
                        row_sum += average
                    break
                rest_cells = less_c
            if row_sum < max_row_width:
                cells[row_index][last_cell[0]].draw_width += (max_row_width - row_sum)
            row_index += 1
        row_index = 0
        while row_index < self.rows:
            row = cells[row_index]
            for cell in row:
                cell.draw_height = max_row_height[row_index]
                delta = cell.draw_height - cell.height
                if delta:
                    cell.value_lines.extend([' '] * delta)
                    cell.value_lines_len.extend([1] * delta)
            row_index += 1
        return cells

    def draw_no_align(self, redraw=False):
        if redraw is True:
            self.cells = []
            self.no_align_graph = ''
        if not self.no_align_graph:
            self.cells = self._cal_no_align_cells()
        else:
            return self.no_align_graph
        no_align_graph = ''
        # 封第一行顶部
        final_row_width = [[i.draw_width for i in j] for j in self.cells]
        for i in final_row_width[0][:-1]:
            no_align_graph += CELL_BOUNDARY + ROW_META * (i - 1)
        i = final_row_width[0][-1]
        no_align_graph += CELL_BOUNDARY + ROW_META * (i - 2) + CELL_BOUNDARY + ROW_BOUNDARY
        row_index = 0
        while row_index < self.rows:
            # 先画空隙
            row_cells = self.cells[row_index]
            bottom = ''
            col_space = ''
            for i in final_row_width[row_index][:-1]:
                col_space += COLUMN_META + PADDING * (i - 1)
                bottom += CELL_BOUNDARY + ROW_META * (i - 1)
            i = final_row_width[row_index][-1]
            col_space += COLUMN_META + PADDING * (i - 2) + COLUMN_META + ROW_BOUNDARY
            bottom += CELL_BOUNDARY + ROW_META * (i - 2) + CELL_BOUNDARY + ROW_BOUNDARY

            no_align_graph += col_space

            # 接着画每一行每一个cell和它的间隔
            # value一行一行画
            d_height = row_cells[0].draw_height
            hindex = 0
            while hindex < d_height:
                for cell in row_cells[:-1]:
                    no_align_graph += COLUMN_META + PADDING + cell.value_lines[hindex]
                    right_padding_count = cell.draw_width - 2 - cell.value_lines_len[hindex]
                    no_align_graph += PADDING * right_padding_count
                cell = row_cells[-1]
                no_align_graph += COLUMN_META + PADDING + cell.value_lines[hindex]
                right_padding_count = cell.draw_width - 4 - cell.value_lines_len[hindex]
                no_align_graph += PADDING * right_padding_count + PADDING + COLUMN_META + ROW_BOUNDARY
                hindex += 1
            no_align_graph += col_space
            no_align_graph += bottom
            row_index += 1
        self.no_align_graph = no_align_graph
        return no_align_graph

    def _cal_cells(self):
        cells = []
        # 补齐行数以及计算最大行宽和最大列高
        row_index = 0
        col_width = [[] for _ in range(self.max_cols)]
        row_height = [[] for _ in range(self.rows)]
        while row_index < self.rows:
            row = self.data[row_index]
            row_cells = []
            col_index = 0
            col_delta = self.max_cols - len(row)
            while col_index < self.max_cols:
                if self.max_cols - col_index <= col_delta:
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
            while col_index < self.max_cols:
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

    def draw_align(self, redraw=False):
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
    datas = [[['排序方法\n这是换行', '平均情况', '最坏情况', '最好情况', '空间复杂度', '稳定性', '复杂性'],
              ['直接插入排序', 'O(n^2)', 'O(n^2)', 'O(n)', 'O(1)', '稳定', '简单', '其他列'],
              ['希尔排序', 'O(nlog2n)', 'O(nlog2n)', '', 'O(1)', '不稳定', '叫复杂\n有三行\n第三行哦嘿嘿'],
              ],
             [['编译层负责把语法解析\n负责把语法解析成字节码, 然后提供字节码执行接口'],
              ['第一格', '第二格'],
              ],
             ]
    for data in datas:
        t = Table(data=data)
        print(t.draw_no_align())
        print(t.draw_align())
    with open('draw_doc_table_test', 'w') as f:
        t.draw_to_file(f)


if __name__ == '__main__':
    main()
