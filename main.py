import tkinter as tk
import csv
import os
import layout as GUI  # 使用英文取代中文作为GUI实现部分
import re
import bisect
from PIL import Image, ImageTk
import itertools


csv_path = r'./data'


def list_csv_files(directory):
    file_list = []
    # 遍历指定目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件的后缀是否匹配
            if file.endswith(r'.csv'):
                # 构造文件的完整路径
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


def csv2char(csv_filename):
    data_txt = []
    if csv_filename != None:
        with open(csv_filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data_txt.extend(row)
                pass
            pass
        pass
    # 此时字符串中含有空字符串，有碍观瞻
    data_txt = [s for s in data_txt if s]
    return data_txt


def char2float(input_list):
    output_list = []
    for s in input_list:
        try:
            num = float(s)
            output_list.append(num)
        except ValueError:
            pass
        pass
    output_list.sort(reverse=False)
    return output_list


class Outcome:
    def __init__(self, R1, R2, R3, type, err):
        self.R1 = R1
        self.R2 = R2#根据type的不同，如果不使用，则设为-1
        self.R3 = R3#根据type的不同，如果不使用，则设为-1
        self.type = type  # type1 23 4567
        '''
        type1:R1
        type2:(R1 p R2)
        type3:(R1 s R2)
        type4:(R1 p R2 p R3)
        type5:(R1 s R2 s R3)
        type6:((R1 p R2) s R3)
        type7:((R1 s R2) p R3)
        '''
        self.err = err  # pos or neg or zero, -99.9 to 99.9,=(outcome-target)/target
        pass

    pass


def find_best_1r(input_list, target,percision, replacement=True):  #
    '''
    由于只用一个，所以不必考虑放回的问题
    :param input_list:  输入的数组，
    :param target: 想接近的目标值，
    :param percision: percision【0-0.999】，
    :param replacement: 是否放回
    :return: list【class：Outcome】
    '''
    target_max=target*(1+percision)
    target_min = target * (1 - percision )
    #print("max,min",target_max,target_min)
    index = bisect.bisect_left(input_list, target)-1
    #如果找得到多个正好相等的数，则输出最左边的数的下标+1；如果没有正好相等的数，则输出间隙左边的数的下标+1;如果小于最小的那个数，则输出0
    ret = []
    #先从中点向下寻找
    i=index
    while True:
        if i <0:#如果已经取到头了，则停止
            break
        if input_list[i]<target_min:#如果这次取到的已经超过了下限
            break
        else:
            ret.append(Outcome(input_list[i], -1, -1, 1, (input_list[i] - target)/target))#记录目前这个可用的组合
            #print('-',input_list[i])
        i-=1
    i=index+1
    # 再从中点向上寻找
    while True:
        if i>=len(input_list):#如果已经取到头了，则停止
            break
        if input_list[i]>target_max:
            break
        else:
            ret.append(Outcome(input_list[i], -1, -1, 1, (input_list[i] - target)/target))  # 记录目前这个可用的组合
            #print('+', input_list[i])
        i += 1

    return ret#如果输入的数组有重复，那么结果也可能会有重复


def find_best_2r(input_list, target,percision, replacement=True):
    target_max = target * (1 + percision)
    target_min = target * (1 - percision)
    ret = []
    #type2:(R1 p R2)
    for i in range(len(input_list)):
        R1=input_list[i]
        # remain_list=input_list.remove(input_list[i])#replacement=F
        if R1<target_min or R1==target:#如果选出的R1已经比可接受的最小值小，那么并联R2后一定更小；如果选出的R1与目标相等，那么根本用不着两个电阻
            continue
        index = bisect.bisect_left(input_list, (target*R1)/(R1-target)) - 1#寻找R2理想值
        if index<0:
            index=0
        j = min(index,i)
        while True:#由于R1 R2可以互换，因此R2取值范围为min-R1，包含端点
            if j < 0:  # 防止精度要求过于宽泛导致的下标溢出
                break
            R2=input_list[j]
            Rout=R1*R2/(R1+R2)
            if Rout < target_min:  # 如果这次取到的结果已经超过了下限，那么j继续变小之后结果只会更小
                break
            elif Rout<target_max:
                ret.append(Outcome(R1, R2, -1, 2, (Rout - target) / target))  # 记录目前这个可用的组合
                #print('-',input_list[i],(Rout - target) / target)
            j -= 1
        j = index+1
        while True:  # 由于R1 R2可以互换，因此R2取值范围为min-R1，包含端点
            if j >=len(input_list) or j>i:  # 防止精度要求过于宽泛导致的下标溢出,防止j大于i导致的重复搜索
                break
            R2 = input_list[j]
            Rout = R1 * R2 / (R1 + R2)
            if Rout > target_max:  # 如果这次取到的结果已经超过了下限，那么j继续变小之后结果只会更小
                break
            elif Rout > target_min:# 串联之后，即使R1大于target min，也可能在并联了默认的R2后整体低于target min
                ret.append(Outcome(R1, R2, -1, 2, (Rout - target) / target))  # 记录目前这个可用的组合
                #print('+',input_list[i],(Rout - target) / target)
            j += 1
    #type3:(R1 s R2)
    for i in range(len(input_list)):
        R1=input_list[i]
        # remain_list=input_list.remove(input_list[i])#replacement=F
        if R1>target_max or R1==target:#如果选出的R1已经比可接受的最小值大，那么串联R2后一定更大；如果选出的R1与目标相等，那么根本用不着两个电阻
            continue
        index = bisect.bisect_left(input_list, target-R1) - 1#寻找R2理想值
        if index<0:
            index=0
        j = min(index,i)
        while True:#由于R1 R2可以互换，因此R2取值范围为min-R1，包含端点
            if j < 0:  # 防止精度要求过于宽泛导致的下标溢出
                break
            R2 = input_list[j]
            Rout = R1 + R2
            if Rout < target_min:  # 如果这次取到的结果已经超过了下限，那么j继续变小之后结果只会更小
                break
            elif Rout > target_min:##################???????????????????????????????????????
                ret.append(Outcome(R1, R2, -1, 3, (Rout - target) / target))  # 记录目前这个可用的组合
                #print('-',input_list[i],(Rout - target) / target)
            j -= 1
        j = index+1
        while True:  # 由于R1 R2可以互换，因此R2取值范围为min-R1，包含端点
            if j >=len(input_list) or j>i:  # 防止精度要求过于宽泛导致的下标溢出,防止j大于i导致的重复搜索
                break
            R2 = input_list[j]
            Rout=R1+R2
            if Rout > target_max:  # 如果这次取到的结果已经超过了下限，那么j继续变小之后结果只会更小
                break
            elif Rout > target_min:
                ret.append(Outcome(R1, R2, -1, 3, (Rout - target) / target))  # 记录目前这个可用的组合
                #print('+',input_list[i],(Rout - target) / target)
            j += 1
    # 首先要分串并联两种情况讨论
    # 其次每种情况中，需要遍历R1的值找出最合适的R2的值，对于每个确定的R1，对应R2的结果有1-2个
    # 还可以利用R1和R2完全等价的特性减少一半的工作量
    # serial R1》=R2
    return ret
    pass

def find_best_3r(input_list, target,percision, replacement=True):
    target_max = target * (1 + percision)
    target_min = target * (1 - percision)
    ret = []
    combinations=list(itertools.combinations_with_replacement(input_list, 2))#先挑选两个数，每个都是（i，j）结构，其中j不小于i，要求k不小于j
    '''
    选取第三个数的规则：
    1 结构退化：如果已选出的两个电阻符合要求，则不需要第三个电阻
    2 串并联引起的变化： 如果已经选出的两个电阻的等效阻值已经小于可接受的最小值，则并联第三个电阻也一定会更小，此时无论向上或向下搜索都没有意义，串联同理
    3 避免组合重复：第三个阻值一定大于等于前两个阻值中的最大者（理想值选的比两者小不代表向上搜索后也一定小）
    4 单调性：在向下搜索时，如果结果已经小于可接受的最小值，则停止此次搜索，向上同理
    5 避免溢出：如果确定的理想值超过了input list的边界，则停止此次向上或向下搜索
    6 意外情况：在向上搜索时，实际值也可能低于可接受的最小值；向下同理，这可能是理想值选取算法的舍入问题导致的
    '''
    # type4:3p
    for combo in combinations:
        R1,R2=combo[0],combo[1]
        R1p2=(R1*R2)/(R1+R2)
        if R1p2<target_min or R1p2==target:#规则1和2
            continue
        index = bisect.bisect_left(input_list, (target * R1p2) / (R1p2 - target))  # 寻找R2理想值
        index=min(index,len(input_list))
        #向下寻找
        #j = min(index, i)
        j=index-1
        while True:  #
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1p2*R3/(R1p2+R3)
            if Rout < target_min or R3<max(R1,R2):  # 规则3 4
                break
            elif Rout < target_max:# 规则6
                ret.append(Outcome(R1, R2, R3, 4, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j -= 1
            pass
        #向上寻找
        j = index
        while True:
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1p2*R3/(R1p2+R3)
            if Rout > target_max:  # 规则4
                break
            elif R3>=max(R1,R2)and Rout>target_min: # 规则3 6
                ret.append(Outcome(R1, R2, R3, 4, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j += 1
            pass
        pass
    # type5:3s
    for combo in combinations:
        R1,R2=combo[0],combo[1]
        R1s2=R1+R2
        if R1s2>target_max or R1s2==target:#规则1和2
            continue
        index = bisect.bisect_left(input_list, (target - R1s2))  # 寻找R2理想值,目标值可能是负数但也没关系
        index=min(index,len(input_list))
        # 向下寻找
        j = index - 1
        while j >= max(R1, R2):  # 规则3
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1s2 + R3
            if Rout < target_min or R3<max(R1,R2):  # 规则3 4
                break
            elif Rout < target_max:  # 规则6
                ret.append(Outcome(R1, R2, R3, 5, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j -= 1
            pass
        # 向上寻找
        j = index
        while True:
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1s2 + R3
            if Rout > target_max:  # 规则4
                break
            elif R3 >= max(R1, R2) and Rout>target_min:  # 规则3 6
                ret.append(Outcome(R1, R2, R3, 5, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j += 1
            pass
    #type6 (p)s
    for combo in combinations:
        R1,R2=combo[0],combo[1]
        R1p2=(R1*R2)/(R1+R2)
        if R1p2>target_max or R1p2==target:#规则1和2
            continue
        index = bisect.bisect_left(input_list, (target - R1p2))  # 寻找R3想值
        index=min(index,len(input_list))
        #向下寻找
        j=index-1
        while j>=max(R1,R2):  # 规则3
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1p2+R3
            if Rout < target_min or R3<max(R1,R2):  # 规则3 4
                break
            elif Rout < target_max:# 规则6
                ret.append(Outcome(R1, R2, R3, 6, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j -= 1
            pass
        #向上寻找
        j = index
        while True:
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1p2+R3
            if Rout > target_max:  # 规则4
                break
            elif R3>=max(R1,R2)and Rout>target_min: # 规则3 6
                ret.append(Outcome(R1, R2, R3, 6, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j += 1
            pass
        pass
    #type7 (s)p
    for combo in combinations:
        R1,R2=combo[0],combo[1]
        R1s2=R1+R2
        if R1s2<target_min or R1s2==target:#规则1和2
            continue
        index = bisect.bisect_left(input_list, (target * R1s2) / (R1s2 - target))  # 寻找R2理想值,目标值可能是负数但也没关系
        index=min(index,len(input_list))
        # 向下寻找
        j = index - 1
        while j >= max(R1, R2):  # 规则3
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1s2 * R3/(R1s2 + R3)
            if Rout < target_min or R3<max(R1,R2):  # 规则3 4
                break
            elif Rout < target_max:  # 规则6
                ret.append(Outcome(R1, R2, R3, 7, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j -= 1
            pass
        # 向上寻找
        j = index
        while True:
            if j < 0 or j>=len(input_list):  # 规则5
                break
            R3 = input_list[j]
            Rout = R1s2 * R3/(R1s2 + R3)
            if Rout > target_max:  # 规则4
                break
            elif R3 >= max(R1, R2) and Rout>target_min:  # 规则3 6
                ret.append(Outcome(R1, R2, R3, 7, (Rout - target) / target))  # 记录目前这个可用的组合
                # print('-',input_list[i],(Rout - target) / target)
            j += 1
            pass
    # 首先要分串并联两种情况讨论
    # 其次每种情况中，需要遍历R1的值找出最合适的R2的值，对于每个确定的R1，对应R2的结果有1-2个
    # 还可以利用R1和R2完全等价的特性减少一半的工作量
    # serial R1》=R2
    return ret
    pass

class Controller():
    win = None  # 用于在init时读取控件
    csv_list = None  # 初始化时扫描csv文件列表并存在这里
    r_values = None  # 如果使用配置文件，则在点击下拉框时阻值列表写入此处，否则在run时读取文本框并写入此处
    resultlist=[]
    selected_type=0#当前列表选中的连接方式
    def __init__(self):  # 在创建之初被调用，第一个调用
        self.csv_list = list_csv_files(csv_path)
        pass

    def init(self, para: 'GUI.WinGUI'):  # 在被传入win时调用，第二个调用,type(para)=class 'layout.Win'
        self.win = para  # 使用类型注解para: 来标注变量的类型,这样就可以进行自动代码补全了
        csv_file_names = [os.path.basename(file_path) for file_path in self.csv_list]  # 配置下拉框的内容
        self.win.tk_select_box_csvfile['values'] = ["自定义阻值"] + csv_file_names
        self.win.var_check_button_no_replacement.set(False)  # 配置“是否每种电阻只允许用一次”的选项
        self.win.tk_input_percision.insert(0, "5")  # 设置精度要求%
        self.win.tk_select_box_num_component.set("使用1-2个电阻")
        self.win.tk_select_box_csvfile.set("自定义阻值")
        pass

    def env_csv_select(self, para):
        #print("env_csv_select")
        if self.win.tk_select_box_csvfile.current() == 0:  # 使用自定义阻值表
            # TBD 清空预览窗口
            self.win.tk_text_values.config(state='normal')
            pass
        else:  # 用配置文件覆盖阻值表
            c = csv2char(self.csv_list[self.win.tk_select_box_csvfile.current() - 1])
            d = char2float(c)
            self.r_values = d
            self.win.tk_text_values.delete(1.0, tk.END)
            self.win.tk_text_values.insert(tk.END, ",".join(c))
            self.win.tk_text_values.config(state='disabled')  # 选择csv提供的阻值时，禁止用户编辑
            pass
        pass

    def env_percision_change(self, para):
        #print("env_percision_change")

        pass

    def env_replacement(self, para):  # unused function
        # print("env_replacement")
        pass

    def env_input_complete(self, para):  # unused function
        # print("env_input_complete")
        pass

    def env_ncomponent_select(self, para):  # unused function
        # print("env_ncomponent_select")
        pass

    def load_and_display_image(self, imagenum):
        # 打开图像文件
        if imagenum>7 or imagenum<0:
            imagenum=0
        image_path=r'./data/图片'+str(imagenum)+'.png'
        try:
            image = Image.open(image_path)
        except:
            return

        # 获取画布的宽度和高度
        canvas_width = self.win.tk_canvas_schematic.winfo_width()
        canvas_height = self.win.tk_canvas_schematic.winfo_height()

        # 调整图像大小以适应画布
        resized_image = image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        # 将图像转换为 PhotoImage 对象
        self.image_tk = ImageTk.PhotoImage(resized_image)

        # 在 Canvas 上显示图像
        self.win.tk_canvas_schematic.create_image(0, 0, anchor="nw", image=self.image_tk)

    def on_canvas_resize(self, event):
        # 重新加载和显示图像以适应新的画布大小
        self.load_and_display_image(self.selected_type)
    def env_select_result(self, para):#选中了输出列表中的某个行，需要给出对应的连接方式
        #print("env_select_result")
        selected_item = self.win.tk_table_results.selection()
        if selected_item:
            row_index = self.win.tk_table_results.index(selected_item[0])  # 获取行号
            self.selected_type=self.resultlist[row_index].type
            #print("conn:",self.selected_type)
            self.load_and_display_image(self.selected_type)
        else:
            print("错误：发现鼠标抬起但未选中任何行")
        pass

    def env_run(self, para):
        '''
        点击按钮对应的函数
        1判断是否使用预设组织表，如果是则需要重新载入阻值
        2读取配值目标/允许误差/可用几个电阻/是否允许重复使用
        3根据可用几个电阻分情况讨论，所有得出的结果均追加到一个列表中
        4在允许使用n个电阻的情况中，先使用枚举工具枚举n-1个电阻的值，再根据公式求出最后一个电阻应该是多少，然后以此为中心搜索表中有几个符合精度要求
        5将所有结果按照精度的绝对值进行排序并输出到表格中
        :param para:
        :return:
        '''
        if self.win.tk_select_box_csvfile.current() == 0:  # 如果使用自定义阻值表，则重新载入阻值
            custom_val_str = self.win.tk_text_values.get(1.0, tk.END)
            custom_val_str = re.sub(r'[^0-9.,]', '', custom_val_str)  # 清洗输入字符串，仅保留有用的信息
            custom_val_str_arr = custom_val_str.split(',')
            self.r_values = char2float(custom_val_str_arr)
            pass
        if len(self.r_values)<3:#如果没有足够多的备选阻值
            print('错误！备选电阻数量需大于3个')
            return
        #r values不需要按照从小到大的顺序排列，因为char2float中已经实现了这一功能
        no_replacement = self.win.var_check_button_no_replacement.get()  # 读取“是否每种电阻只允许用一次”的选项
        n_component = self.win.tk_select_box_num_component.current() + 1  # 读取 允许使用的元件的个数,1-3
        percision_str = self.win.tk_input_percision.get()#精度（str类型，0-100）
        target_str = self.win.tk_input_target.get()#目标值（str类型）
        # 获取精度限制（如果用户没有指定就忽略）
        try:
            percision = float(percision_str) / 100
            if percision<0 or percision>100:
                print('错误！精度不符合要求，请指定0-100之内的精度')
                return
        except ValueError:
            percision = float('inf')  # 如果没有指定精度，就不考虑精度限制
            print('错误！未指定精度')
            return
        # 获取目标阻值（如果没有指定就结束运行）
        try:
            target = float(target_str)
            if target<=0:
                print('错误！目标阻值必须为正数')
                return
        except ValueError:
            print('错误！请指定目标值')
            return
        # 新建一个对象数组，对象继承于Outcome类，用于记录每个输出结果的阻值 连接方式 精度
        self.resultlist = []
        # 检索单电阻
        self.resultlist.extend(find_best_1r(self.r_values, target,percision, True))   #########TBD：没有考虑不放回的情况
        if n_component > 1:
            self.resultlist.extend(find_best_2r(self.r_values, target,percision, True))
            pass
            # 检索2电阻
        if n_component > 2:
            self.resultlist.extend(find_best_3r(self.r_values, target,percision, True))
            pass
            # 检索3电阻

        #排序
        self.resultlist.sort(key=lambda obj: abs(obj.err))
        #视情况剔除内部重复的项
        if(no_replacement):
            self.resultlist = [
                obj for obj in self.resultlist
                if len({obj.R1, obj.R2, obj.R3}) == 3
            ]
        #清空显示
        ch=self.win.tk_table_results.get_children('')
        for chn in ch:
            self.win.tk_table_results.delete(chn)
        # 显示输出
        for i in range(len(self.resultlist)):
            values=[f"{i+1}",f"{(self.resultlist[i].err*100):.2f}%({(target*self.resultlist[i].err+target):.2f})",f"{self.resultlist[i].R1}",f"{self.resultlist[i].R2}",f"{self.resultlist[i].R3}"]
            if values[-2]=="-1":
                values[-2] = "不需要"
            if values[-1]=="-1":
                values[-1] = "不需要"
            self.win.tk_table_results.insert("","end",values=values)
            pass
        print('总条目数', len(self.resultlist))
        self.load_and_display_image(self.selected_type)
        pass
'''
self.R1 = R1
        self.R2 = R2#根据type的不同，如果不使用，则设为-1
        self.R3 = R3#根据type的不同，如果不使用，则设为-1
        self.type = type  # type1 23 4567
        self.err = err  # pos or neg or zero, -99.9 to 99.9,=(outcome-target)/target
'''

if __name__ == "__main__":
    crtl = Controller()
    win = GUI.Win(crtl)  # GUI就是旁边的layout.py文件，Win是其中定义的一个class，ctrl被传入，并在win初始化的时候调用ctrl中的init（）方法
    win.mainloop()
    pass
