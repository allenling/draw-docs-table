draw-docs-table
====================

This is a simple script to help you to draw a dot line style table.

Just test in  Linux env, not test for Windows.


**Maybe in your IDE`s console, like in my eclipse, the graphic might be wrong, and i suggest you to write the graphic into a file, open that file with Vim or just cat the file,
the graphic will be right. At least, my Ubuntu is find.**


Usage:

.. code-block:: python

    from doc_table import Table
    
    data = [['a', 'simple is good', 'simple is powerful'],
            ['e', 'struggle with the performance in a interview!', 'f'],
            ['g', 'why you do not read my projects when you will fucking interview me!', 'h']
            ]
    # just output string
    
    t.draw()
    
    # or wirte to a file
    with open('/tmp/test_gr', 'w') as f:
        Table(data).draw_to_fil(f)

And in output:
.. code-block::

    +---+---------------------------------------------------------------------+--------------------+
    |   +                                                                     +                    +
    | a + simple is good                                                      + simple is powerful +
    |   +                                                                     +                    +
    +---+---------------------------------------------------------------------+--------------------+
    |   +                                                                     +                    +
    | e + struggle with the performance in a interview!                       + f                  +
    |   +                                                                     +                    +
    +---+---------------------------------------------------------------------+--------------------+
    |   +                                                                     +                    +
    | g + why you do not read my projects when you will fucking interview me! + h                  +
    |   +                                                                     +                    +
    +---+---------------------------------------------------------------------+--------------------+


Also support unicode

like:

.. code-block:: python

    from doc_table import Table
    
    data1 = [['排序方法', '平均情况', '最坏情况', '最好情况', '空间复杂度', '稳定性', '复杂性'],
            ['直接插入排序', 'O(n^2)', 'O(n^2)', 'O(n)', 'O(1)', '稳定', '简单'],
            ['希尔排序', 'O(nlog2n)', 'O(nlog2n)', '', 'O(1)', '不稳定', '叫复杂']
            ]
    
    data2 = [['chúng tôi', '우리', 'մեզ'],
            ['chúng tôidgf', '我们', 'abc'],
            ]
    
    with open('/tmp/test_gr2', 'w') as f:
        Table(data1).draw_to_fil(f)
    
    with open('/tmp/test_gr1', 'w') as f:
        Table(data2).draw_to_fil(f)

.. code-block::

    +--------------+-----------+-----------+----------+------------+--------+--------+
    |              +           +           +          +            +        +        +
    | 排序方法     + 平均情况  + 最坏情况  + 最好情况 + 空间复杂度 + 稳定性 + 复杂性 +
    |              +           +           +          +            +        +        +
    +--------------+-----------+-----------+----------+------------+--------+--------+
    |              +           +           +          +            +        +        +
    | 直接插入排序 + O(n^2)    + O(n^2)    + O(n)     + O(1)       + 稳定   + 简单   +
    |              +           +           +          +            +        +        +
    +--------------+-----------+-----------+----------+------------+--------+--------+
    |              +           +           +          +            +        +        +
    | 希尔排序     + O(nlog2n) + O(nlog2n) +          + O(1)       + 不稳定 + 叫复杂 +
    |              +           +           +          +            +        +        +
    +--------------+-----------+-----------+----------+------------+--------+--------+

    +--------------+------+-----+
    |              +      +     +
    | chúng tôi    + 우리 + մեզ +
    |              +      +     +
    +--------------+------+-----+
    |              +      +     +
    | chúng tôidgf + 我们 + abc +
    |              +      +     +
    +--------------+------+-----+

