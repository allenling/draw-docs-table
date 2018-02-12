draw-docs-table
====================

python3.x

1. unicode中中文一般是三个byte, 但是在在ubuntu终端和Vim中, unicode显示是两个长度, 也就是如果你打印"我们"，其占的宽度是和四个横线(-)一样, 所以这里一个中文将会占两个位置.

2. 但是有些编辑器并不是这样显示的, 比如eclipse, 把所有的编码都设置成了utf-8, 不管在文件还是console中, 中英文始终无法对齐, 或许需要选择一些特别的字体把.

3. 所以, 如果你的显示设备是使用2个宽度来显示unicode的话, 是可以对齐的, 比如配置utf8支持的vim和配置了utf8的ubuntu的终端.

4. 有些设备unicode是不能和ascii对齐的, 两者宽度不一样(一般是3个汉字占5个位置, 也就是我们三这个3个汉字需要5个ascii字符才能对齐), 比如kubuntu中的kate编辑器, 2提到的eclipse. 需要对齐的话, 必须ascii也是utf-8编码才行, 也就是全角的字母, 这样和汉字是可以一一对齐的.

5. 所以注意一下你打印时候的终端是什么.

6. draw_align是补全列的

7. draw_no_align是不补全列的

8. 字符占位宽度: http://jkorpela.fi/chars/spaces.html


.. image:: https://github.com/allenling/draw-docs-table/blob/master/example_img/Selection_006.png

....

.. image:: https://github.com/allenling/draw-docs-table/blob/master/example_img/Selection_007.png

