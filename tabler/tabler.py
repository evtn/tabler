from typing import List, Union, Tuple, Any, overload, Dict

tablechars = {
    "default": "┏┓┗┛┃━┣┫┳┻╋",
    "double":  "╔╗╚╝║═╠╣╦╩╬",
    "dots":    "····  ·····",
    "simple":  "    |-     ",
    "dots2":   "····|-·····",
    "empty":   " " * 11,
}

class Table:
    tablechars = tablechars["default"]
    def __init__(self, data=None):
        self.data: Dict[Tuple[int, int], Any] = data or {}
        self.recalc_dimensions()

    @staticmethod
    def from_list(list_: List) -> "Table":
        """Builds a Table from a list"""
        table = Table()
        for y, row in enumerate(list_):
            for x, column in enumerate(row):
                table[x, y] = column
        return table

    def reverse(self, columns: bool = True, rows: bool = True) -> "Table":
        """Returns a reversed table, where specified dimensions are reversed"""
        new = Table()
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if (x, y) in self.data:
                    column_index = self.dimensions[0] - 1 - x if columns else x
                    row_index = self.dimensions[1] - 1 - y if rows else y
                    new[column_index, row_index] = self.data[x, y]
        return new

    @overload
    def __getitem__(self, index: Tuple[int, int]) -> str:
        pass

    @overload
    def __getitem__(self, index: slice) -> "Table":
        pass

    def __getitem__(self, index: Union[slice, Tuple[int, int]]) -> Union["Table", str]:
        """
            If index is a tuple, returns a string of element on specific position (or '', if there's no element)
            If index is a slice of tuples, new table is returned.
        """
        if isinstance(index, slice):
            if index.step:
                is_negative = [step < 0 for step in index.step]
                if any(is_negative):
                    return self.reverse(*is_negative)[index.stop:index.start:tuple(abs(step) for step in index.step)]
            new = Table()
            index = slice(
                index.start or (0, 0),
                index.stop or self.dimensions,
                index.step or (1, 1)
            )
            for x in range(index.start[0], index.stop[0], index.step[0]):
                for y in range(index.start[1], index.stop[1], index.step[1]):
                    if (x, y) in self.data:
                        new[x, y] = self.data[x, y]
            return new
        if all(self.dimensions):
            index = tuple(
                x % self.dimensions[i] if x < 0 else x
                for i, x in enumerate(index)
            )
        if index in self.data:
            return str(self.data[index])
        return ""

    def __setitem__(self, index: Tuple[int, int], value) -> Any:
        """Sets item at specific position."""
        if all(self.dimensions):
            index = tuple(
                x % self.dimensions[i] if x < 0 else x
                for i, x in enumerate(index)
            )
        self.data[index] = value
        self.recalc_dimensions(index)
        return value

    def pop(self, index: Tuple[int, int]) -> Any:
        """Removes item from table and returns it"""
        elem = self.data.pop(index)
        self.recalc_dimensions()
        return elem

    def recalc_dimensions(self, index=None):
        """Recalculates table dimensions. index is used if an element was added on that index"""
        if index:
            self.dimensions = [
                max(index[i] + 1, self.dimensions[i])
                for i in range(2)
            ]
        if not self.data:
            self.dimensions = [0, 0]
            return
        self.dimensions = [
            max(x[i] for x in self.data) + 1
            for i in range(2)
        ]

    def column_width(self, column: int, table_height: int) -> int:
        """Returns column width, in symbols"""
        return max(
            max(len(x) for x in self[column, y].split("\n"))
            for y in range(table_height)
        )

    def max_column(self) -> int:
        """Returns the widest column width, in symbols"""
        return max(
            self.column_width(column, self.dimensions[1]) for column in range(self.dimensions[0])
        )

    def row_height(self, row: int, table_width: int) -> int:
        """Returns row height, in lines"""
        return max(
            len(self[x, row].split("\n"))
            for x in range(table_width)
        )

    def max_row(self) -> int:
        """Returns the tallest row height, in lines"""
        return max(
            self.row_height(row, self.dimensions[0]) for row in range(self.dimensions[1])
        )

    def build_cell(self, coords: Tuple[int, int], height: int, width: int) -> List[str]:
        """Builds a list of lines for a specific cell."""
        empty_row = " " * width

        cell = ["{0:^{width}}".format(sr, width=width) for sr in self[coords].split("\n")]
        top = (height - len(cell)) // 2
        bottom = height - len(cell) - top
        
        cell = [
            *([empty_row] * top),
            *cell,
            *([empty_row] * bottom)
        ]

        return ["".join(cellrow) for cellrow in cell]

    def build_row(self, y: int, height: int, widths: List[int]) -> str:
        """Builds a string representing one row"""
        cellrows: List[List[str]] = [[] for _ in range(height)]
        for x in range(self.dimensions[0]):
            cell = self.build_cell((x, y), height, widths[x])
            for i, cellrow in enumerate(cell):
                cellrows[i].append(cellrow)
        return "\n".join(
            "".join(
                [self.edge(False), self.edge(False).join(cellrow), self.edge(False)]
            )
            for cellrow in cellrows
        )

    def __str__(self) -> str:
        """Builds a default table string"""
        return self.to_string()

    def __repr__(self) -> str:
        """Returns info string on Table"""
        return "Table[{}x{}], elements: {}".format(*self.dimensions, len(self.data))

    def stretch(self, target, sizes, is_even):
        """Calculates sizes for stretched dimensions"""
        size_count = len(sizes)
        target = target - size_count - 1
        if not is_even:
            k = target / sum(sizes)
            if k > 1:
                for i in range(size_count):
                    sizes[i] = round((sizes[i] * k) // 1)
                return sizes
        else:
            max_size = max(sizes)
            if max_size * len(sizes) < target:
                size = target // size_count
                diff = target - size * size_count
                return [size + (i < diff) for i in range(size_count)]


    def column_widths(self, is_even=False, stretch_to=None):
        """
        returns a list of widths for every column. 
        if `is_even=True`, columns would have same width.
        if `stretch_to` is used, table would be stretched to specified width (if possible)
        """
        column_widths = [self.column_width(x, self.dimensions[1]) for x in range(self.dimensions[0])]
        column_count = len(column_widths)
        if stretch_to:
            column_widths_ = self.stretch(stretch_to, column_widths, is_even)
            if column_widths_:
                return column_widths_
        if is_even:
            return [max(column_widths)] * self.dimensions[0]
        return column_widths

    def row_heights(self, is_even=False, stretch_to=None):
        """
        returns a list of heights for every row. 
        if `is_even=True`, row would have same height.
        if `stretch_to` is used, table would be stretched to specified height (if possible)
        """
        row_heights = [self.row_height(y, self.dimensions[0]) for y in range(self.dimensions[1])]
        row_count = len(row_heights)
        if stretch_to:
            row_heights_ = self.stretch(stretch_to, row_heights, is_even)
            if row_heights_:
                return row_heights_
        if is_even:
            return [max(row_heights)] * self.dimensions[0]
        return row_heights
            

    def to_string(self, even_columns: bool = False, even_rows: bool = False, stretch_to=(None, None)) -> str:
        """
            Builds a table string. 
            Use `even_columns=True` to build a table with even column width
            Use `even_rows=True` to build a table with even row height
        """
        if not len(self.data):
            return Table({(0, 0): " "}).to_string(even_columns, even_rows)
        
        column_widths = self.column_widths(even_columns, stretch_to[0])
        row_heights = self.row_heights(even_rows, stretch_to[1])

        result = [self.full_horizontal_edge(column_widths, False)]
        
        for y in range(self.dimensions[1]):
            result.append(
                self.build_row(y, row_heights[y], column_widths)
            )
            if y + 1 != self.dimensions[1]:
                result.append(
                    self.full_horizontal_edge(column_widths, False, True)
                )
        result.append(
            self.full_horizontal_edge(column_widths, True)
        )

        return "\n".join(result)

    def full_horizontal_edge(self, widths: List[int], is_bottom: bool, is_middle: bool = False) -> str:
        column_gaps = [self.edge(True) * width for width in widths]
        if is_middle:
            frames = [self.cross(False, False, bool(i)) for i in [0, 1]]
        else:
            frames = [self.corner(is_bottom, bool(i)) for i in [0, 1]]
        return "".join([
            frames[0],
            self.cross(is_middle, True, is_bottom).join(column_gaps),
            frames[1],
        ])
        
    def corner(self, is_bottom: bool, is_right: bool) -> str:
        return self.tablechars[is_bottom * 2 + is_right]

    def edge(self, is_horizontal: bool) -> str:
        return self.tablechars[4 + is_horizontal]

    def cross(self, full: bool = True, is_horizontal: bool = False, is_ending: bool = False) -> str:
        if full:
            return self.tablechars[-1]
        return self.tablechars[6 + is_horizontal * 2 + is_ending]
