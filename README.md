# Tabler

Easy text table generation with Python.
Supports [sparse tables](#sparse-tables)


## Installation

At this point, just copy `tabler` folder to the folder with your script or anywhere in the python path.
Pypi and setup.py would be available later.

## Basic usage

```python
from tabler import Table

table = Table.from_list([
    ["Number", "Square"],
    *[[x, x ** 2] for x in range(2, 6)]
])

print(table)

result = """
┏━━━━━━┳━━━━━━┓
┃Number┃Square┃
┣━━━━━━╋━━━━━━┫
┃  2   ┃  4   ┃
┣━━━━━━╋━━━━━━┫
┃  3   ┃  9   ┃
┣━━━━━━╋━━━━━━┫
┃  4   ┃  16  ┃
┣━━━━━━╋━━━━━━┫
┃  5   ┃  25  ┃
┗━━━━━━┻━━━━━━┛
"""

```

## Sparse tables

You can omit values:

```python
from tabler import Table

table = Table.from_list([
    [i] * i
    for i in range(5)
])

print(table)

result = """
┏━┳━┳━┳━┓
┃ ┃ ┃ ┃ ┃
┣━╋━╋━╋━┫
┃1┃ ┃ ┃ ┃
┣━╋━╋━╋━┫
┃2┃2┃ ┃ ┃
┣━╋━╋━╋━┫
┃3┃3┃3┃ ┃
┣━╋━╋━╋━┫
┃4┃4┃4┃4┃
┗━┻━┻━┻━┛
"""

```

Or fill in specific cells:

```python
from tabler import Table

table = Table()

table[0, 0] = "Here"
table[2, 2] = "And Here"

print(table)

result = """
┏━━━━┳┳━━━━━━━━┓
┃Here┃┃        ┃
┣━━━━╋╋━━━━━━━━┫
┃    ┃┃        ┃
┣━━━━╋╋━━━━━━━━┫
┃    ┃┃And Here┃
┗━━━━┻┻━━━━━━━━┛
"""

```

## Align

Previous example didn't look nice because of the empty column, let's widen it a bit:     

```python
from tabler import Table

table = Table()

table[0, 0] = "Here"
table[2, 2] = "And Here"

print(table.to_string(even_columns=True))

result = """
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃  Here  ┃        ┃        ┃
┣━━━━━━━━╋━━━━━━━━╋━━━━━━━━┫
┃        ┃        ┃        ┃
┣━━━━━━━━╋━━━━━━━━╋━━━━━━━━┫
┃        ┃        ┃And Here┃
┗━━━━━━━━┻━━━━━━━━┻━━━━━━━━┛
"""

```

Same goes for `even_rows` parameter, which aligns rows the same way

## Stretching

If you want the table to be stretched, you can use `stretch_to` parameter    

```python
from tabler import Table

table = Table()

table[0, 0] = "Here"
table[2, 2] = "And Here"

print(
    table.to_string(
        even_columns=True, 
        stretch_to=(37, 25)
    )
)

result = """
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃   Here    ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━┫
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━┫
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃ And Here  ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┃           ┃           ┃           ┃
┗━━━━━━━━━━━┻━━━━━━━━━━━┻━━━━━━━━━━━┛
"""

```


## Slicing

You can retrieve a slice of the table like this:

```python

from tabler import Table

table = Table()

table[0, 0] = "Here"
table[2, 2] = "And Here"

print(
    table[(0, 0):(2, 2)]
)

result = """
┏━━━━┓
┃Here┃
┗━━━━┛
"""
```

## Custom borders

If you need to use other characters as borders, just change `table.tablechars`:

```python
from tabler import Table

table = Table()

table[0, 0] = "Here"
table[1, 0] = "There"

print(
    table
)

result = """
┏━━━━┳━━━━━┓
┃Here┃There┃
┗━━━━┻━━━━━┛
"""

table.tablechars = " " * 11 # using spaces as separators

print(
    table
)

result = """
            
 Here There 
            
"""

```

Also, there are predefined sets of chars:

```python
from tabler import tablechars

print(tablechars)

"""
{
    "default": "┏┓┗┛┃━┣┫┳┻╋",
    "double":  "╔╗╚╝║═╠╣╦╩╬",
    "dots":    "····  ·····",
    "simple":  "    |-     ",
    "dots2":   "····|-·····",
    "empty":   " " * 11,
}
"""
```