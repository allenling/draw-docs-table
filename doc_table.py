
CELL_BOUNDARY = '+'
ROW_BOUNDARY = '\n'

PADDING_TOP = ' '
PADDING_BOTTOM = ' '

PADDING_LEFT = ' '
PADDING_RIGHT = ' '

LEN_PADDING_LEFT = len(PADDING_LEFT)
LEN_PADDING_RIGHT = len(PADDING_RIGHT)

ROW_META = '-'
COLUMN_META = '|'

VALUE_PADDING = ' '


class Cell(object):

    def __init__(self, value):
        self.value = str(value)
        self.width = 0
        for v in self.value:
            self.width += int(len(str(v).encode('utf-8')) / 1.5) if ord(v) > 256 else len(v)
        return


class Table(object):
    def __init__(self, data):
        self.data = data
        self.cells = []
        return

    def draw_cells(self):
        cells = []
        for d in self.data:
            tmp = []
            for value in d:
                tmp.append(Cell(value))
            cells.append(tmp)
        self.column_max_width = [0 for _ in self.data[0]]
        for row_index in range(len(cells)):
            for column_index in range(len(cells[row_index])):
                cell = cells[row_index][column_index]
                self.column_max_width[column_index] = max([self.column_max_width[column_index], cell.width])
        self.cells = cells
        return

    def draw(self, redraw=False):
        if redraw is True:
            self.cells = []
        if not self.cells:
            self.draw_cells()
        graph = ''
        row_extra_len = LEN_PADDING_LEFT + LEN_PADDING_RIGHT
        for row_index in range(len(self.cells)):
            row_graphic = CELL_BOUNDARY
            # draw row top lines
            for column_width in self.column_max_width:
                row_graphic += ROW_META * (column_width + row_extra_len) + CELL_BOUNDARY
            row_graphic += ROW_BOUNDARY + COLUMN_META

            # draw row padding top spaces
            for column_width in self.column_max_width:
                row_graphic += PADDING_TOP * (column_width + row_extra_len) + CELL_BOUNDARY
            row_graphic += ROW_BOUNDARY + COLUMN_META

            # draw row value
            for column_index in range(len(self.column_max_width)):
                column_width = self.column_max_width[column_index]
                cell = self.cells[row_index][column_index]
                diff_len = column_width - cell.width
                row_graphic += PADDING_LEFT + cell.value + VALUE_PADDING * diff_len + PADDING_RIGHT + CELL_BOUNDARY
            row_graphic += ROW_BOUNDARY + COLUMN_META

            # draw row padding bottom spaces
            for column_width in self.column_max_width:
                row_graphic += PADDING_BOTTOM * (column_width + 2) + CELL_BOUNDARY
            row_graphic += ROW_BOUNDARY
            graph += row_graphic
        # finally, close table
        graph += CELL_BOUNDARY
        for column_width in self.column_max_width:
            graph += ROW_META * (column_width + row_extra_len) + CELL_BOUNDARY
        graph += ROW_BOUNDARY
        return graph

    def draw_to_fil(self, f):
        f.write(self.draw())
        return


def main():
    data = [['排序方法', '平均情况', '最坏情况', '最好情况', '空间复杂度', '稳定性', '复杂性'],
            ['直接插入排序', 'O(n^2)', 'O(n^2)', 'O(n)', 'O(1)', '稳定', '简单'],
            ['希尔排序', 'O(nlog2n)', 'O(nlog2n)', '', 'O(1)', '不稳定', '叫复杂']
            ]
    t = Table(data)
    print(t.draw())
    with open('/tmp/gr', 'w') as f:
        t.draw_to_fil(f)


if __name__ == '__main__':
    main()
