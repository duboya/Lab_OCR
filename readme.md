# Q & A


### 说明：
1. 中间含灰色widget： 
	img_char：			width：212		height：12				column_white_num_max：9		column_black_num_max：12
	img_row:			width: 212		image_height：345		row_white_num_max：81		row_black_num_max：212
	列起始判定条件：column_white_num[column_mark] > column_white_num_max：9 * 0.05 = 0.4 即出现白色像素点即可
	列终止判定条件：column_black_num[m] > column_black_num_max ：12 * 0.95 = 11.4 即全为背景像素点
	行起始判定条件：row_white_num[row_mark] > row_white_num_max * 0.1 = 8.1 
	行终止判定条件：row_black_num[m] > row_black_num_max * 0.9 = 190.8
	. 虽然淡蓝与灰色也不易通过亮度区分，但是因为不存在淡蓝与灰色共存状态，故而暂不进行处理。	
3. 亮度阈值： 白色：180，  黄色：130  浅蓝：100   红色：65
4. 终究还是二值化gen_gray function上出了问题，解决思路是先用红色进行过滤一下原图，再进行二值化（前面用红色过滤只是为了检测待检测行的颜色，只做判定，并未做操作）
5. 只需对红色、淡蓝进行特殊处理，因为这两种颜色进行二值化，选定的亮度阈值分别为65,100。这个亮度阈值不能将灰色过滤，对于绿色与白色，亮度阈值足以过滤到灰色。


### 待解决：
1. 小数点不能检测     开始位置都没找到，存在这个情况。（已解决）
2. 出现数字1不能检测（原因是字符列切割时候限制必须在2列以上，以确保过滤直线，反倒成了问题）（已解决）
3. 可能会出现黄色与白色（目前没有看到红色与其他颜色共同出现的情况，暂不考虑）
4. 会将灰色区域检测出来（已解决）
5. 带框数字检测(已解决)
6. 断裂字符被当做两字符处理了：因为目前处理粒度比较小，单像素级别，造成如果二值化后的图像出现中间断裂会当做双字符进行处理。（已解决）
7. 处理右下角字符切割时，字符显示不好。(已解决)
8. 中上方仪表盘中数字识别（已解决）
9. 右下角文本块切成两块，很难做一个规则判定中间切点

### 解决思路：
1. 对于数字1，列分割时候，检测当列出现像素点高于一定阈值后，如果其实列到结束列的列宽不满足>2，但是如果列中像素大于某设定阈值则视为数字1看待。
2. 对于daunt这种情况下可通过尽大可能地让图像灰度更饱满一些，虽然会造成列区分度降低，但目前这应该是比较好的方案
3. 中上方仪表盘初步方案首先以仪表盘开始点作为固定点，利用该固定点做上下左右区域切割（以像素点做，写死），得到待识别字符区域，依据该字符区域有么有字符进行判定（无需判定识别出具体问题）
   上述思路不好实行，因为不容易知道另一像素点的行信息。不如换个思路，先处理带框数据，先找框，在依据框的信息，确定哪些点的位置信息，依旧是直接确定像素平移。
9. 采用先判定文本块起始点与文本块终点列，在中间找到一列满足其左右两边具有足够空隙（0值列）

### 已解决：
1. 字符黏连问题，目前扩展到3字符黏连判定。
2. 红色、灰色区分问题，通过转换到LAB空间，再转换到HSV空间，依据亮度进行区分。
3. 已解决检测到灰色区域，通过将detect_row_img_color中不符合判定颜色，则一律依照黄色亮度阈值进行划分（之前设定是红色阈值65，现在设置为黄色阈值130）
4. 小数点问题，通过设定单个像素点及两个像素点检测规则
    elif column_white_num[column_mark] / column_white_num_max < 0.34:
    elif column_white_num[column_mark] / column_white_num_max and column_white_num[column_mark+1] / column_white_num_max < 0.34:
    阈值设到0.34保证能承受大约3个像素点；
5. 灰色区域检测出来，行检测出来无所谓，当成背景图像直接处理一遍，得不到字符识别结果输出即可
6. 带框解决方案，先去框，由于带框数字检测只有一行，以及框中部分内容包含全为虚直线的情况，采用先上下去边框线（只去一次），以保证即便是内容只有直虚线也依旧能够将其视作完整一行来处理。
   横框线利用两行间距大于5限定直接去掉，列框线利用列长像素比行高像素长度相差在1之内的一律视为列线。
7. 对于断裂字符，目前采用在产生对应颜色二值图时候，降低亮度阈值，以使得图像显示更清晰。
8. 对于仪表盘数字判定，为了避开指针带来的影响，采用列平均字符判定，经过测试选定列平均阈值范围为：无字符：0 ~ 2.45；一行字符：2.45 ~ 4.5 两行字符：4.7 ~ 
9. 针对框线边上多出的1个像素点被判定为小数点情况，进一步细化判定框线条件，将检测到的框线前后两步及自身都变为0.

### Sample:
1. 完成字符切割，先初步识别，再将识别进行单字符分类，完成初步训练样本收集整理；
2. 完成CNN模型初步调优；