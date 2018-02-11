draw-docs-table
====================

python3.x

1. unicode是三个byte, 但是在在终端和Vim中, unicode显示是两个长度, 也就是如果你打印"我们"，则下一行也要四个横线(-)才能和"我们"对齐

2. 但是有些编辑器并不是这样显示的, 比如eclipse, 把所有的编码都设置成了utf-8, 不管在文件还是console中, 中英文始终无法对齐, 或许需要选择一些特别的字体把.

3. chrome中，网页转成unicode编码之后, 也是使用两个长度来显示unicode, 所以是可以正确显示点线风格的表格的.

4. vim在设置utf-8编码的情况下显示也是正常的.

5. 所以注意一下你打印时候的终端是什么.

6. 自动补全列.

7. draw_align是补全列的

8. draw_no_align是不补全列的


.. image:: https://github.com/allenling/draw-docs-table/blob/master/example_img/Selection_006.png

....

.. image:: https://github.com/allenling/draw-docs-table/blob/master/example_img/Selection_007.png

