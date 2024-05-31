"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:788392508
在线反馈:https://support.qq.com/product/618914
"""
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_frame_main = self.__tk_frame_main(self)
        self.tk_label_frame_setting = self.__tk_label_frame_setting( self.tk_frame_main) 
        self.tk_select_box_csvfile = self.__tk_select_box_csvfile( self.tk_label_frame_setting) #选择阻值体系csv的下拉框
        self.tk_label_1 = self.__tk_label_1( self.tk_label_frame_setting) 
        self.tk_input_percision = self.__tk_input_percision( self.tk_label_frame_setting) #设置“精度要求”的输入框
        self.tk_check_button_no_replacement = self.__tk_check_button_no_replacement( self.tk_label_frame_setting) #设置“同阻值只能用一个”的复选框
        self.tk_select_box_num_component = self.__tk_select_box_num_component( self.tk_label_frame_setting) #设置“能用1 2or3个电阻”的下拉框
        self.tk_button_run = self.__tk_button_run( self.tk_label_frame_setting) #“计算”按钮
        self.tk_label_label2 = self.__tk_label_label2( self.tk_label_frame_setting) 
        self.tk_input_target = self.__tk_input_target( self.tk_label_frame_setting) #设置“目标阻值”的输入框
        self.tk_label_frame_schematic = self.__tk_label_frame_schematic( self.tk_frame_main) 
        self.tk_canvas_schematic = self.__tk_canvas_schematic( self.tk_label_frame_schematic) #显示“连接示意图”的画布
        self.tk_label_frame_values = self.__tk_label_frame_values( self.tk_frame_main) 
        self.tk_text_values = self.__tk_text_values( self.tk_label_frame_values) #显示“阻值预览”的文本框
        self.tk_label_frame_output = self.__tk_label_frame_output( self.tk_frame_main) 
        self.tk_table_results = self.__tk_table_results( self.tk_label_frame_output) #显示阻值的输出列表
    def __win(self):
        self.title("阻值计算器")
        # 设置窗口大小、居中
        width = 800
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.minsize(width=width, height=height)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_frame_main(self,parent):
        frame = Frame(parent,)
        frame.place(relx=0.00, rely=0.00, relwidth=1.00, relheight=1.00)
        return frame
    def __tk_label_frame_setting(self,parent):
        frame = LabelFrame(parent,text="设置",)
        frame.place(relx=0.03, rely=0.04, relwidth=0.25, relheight=0.50)
        return frame
    def __tk_select_box_csvfile(self,parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("自定义阻值")
        cb.place(relx=0.13, rely=0.03, relwidth=0.75, relheight=0.10)
        return cb
    def __tk_label_1(self,parent):
        label = Label(parent,text="精度要求(%)：",anchor="center", )
        label.place(relx=0.13, rely=0.30, relwidth=0.40, relheight=0.10)
        return label
    def __tk_input_percision(self,parent):
        ipt = Entry(parent, )
        ipt.place(relx=0.50, rely=0.30, relwidth=0.38, relheight=0.10)
        return ipt
    def __tk_check_button_no_replacement(self,parent):
        self.var_check_button_no_replacement = BooleanVar()######################
        cb = Checkbutton(parent,text="同阻值电阻只能用一个",variable=self.var_check_button_no_replacement)
        cb.place(relx=0.13, rely=0.17, relwidth=0.75, relheight=0.10)
        return cb
    def __tk_select_box_num_component(self,parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = ("使用1个电阻","使用1-2个电阻","使用1-3个电阻")
        cb.place(relx=0.13, rely=0.43, relwidth=0.75, relheight=0.10)
        return cb
    def __tk_button_run(self,parent):
        btn = Button(parent, text="计算", takefocus=False,)
        btn.place(relx=0.13, rely=0.70, relwidth=0.70, relheight=0.17)
        return btn
    def __tk_label_label2(self,parent):
        label = Label(parent,text="目标阻值：",anchor="center", )
        label.place(relx=0.13, rely=0.57, relwidth=0.35, relheight=0.10)
        return label
    def __tk_input_target(self,parent):
        ipt = Entry(parent, )
        ipt.place(relx=0.45, rely=0.57, relwidth=0.42, relheight=0.10)
        return ipt
    def __tk_label_frame_schematic(self,parent):
        frame = LabelFrame(parent,text="连接示意图",)
        frame.place(relx=0.03, rely=0.58, relwidth=0.25, relheight=0.33)
        return frame



    def __tk_canvas_schematic(self,parent):
        canvas = Canvas(parent,bg="#aaa")
        canvas.place(relx=0.05, rely=0.05, relwidth=0.88, relheight=0.75)
        return canvas
    def __tk_label_frame_values(self,parent):
        frame = LabelFrame(parent,text="阻值预览",)
        frame.place(relx=0.31, rely=0.04, relwidth=0.63, relheight=0.25)
        return frame
    def __tk_text_values(self,parent):
        text = Text(parent)
        text.place(relx=0.04, rely=0.07, relwidth=0.92, relheight=0.67)
        self.create_bar(parent, text,True, False, 20, 10, 460,100,500,150)
        return text
    def __tk_label_frame_output(self,parent):
        frame = LabelFrame(parent,text="结果输出",)
        frame.place(relx=0.31, rely=0.33, relwidth=0.63, relheight=0.58)
        return frame
    def __tk_table_results(self,parent):
        # 表头字段 表头宽度
        columns = {"序号":45,"误差":119,"R1":97,"R2":97,"R3":97}
        tk_table = Treeview(parent, show="headings", columns=list(columns),)
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸
        
        tk_table.place(relx=0.04, rely=0.01, relwidth=0.92, relheight=0.86)
        return tk_table
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_select_box_csvfile.bind('<<ComboboxSelected>>',self.ctl.env_csv_select)
        self.tk_check_button_no_replacement.bind('<Button-1>',self.ctl.env_replacement)
        self.tk_select_box_num_component.bind('<<ComboboxSelected>>',self.ctl.env_ncomponent_select)
        self.tk_button_run.bind('<Button-1>',self.ctl.env_run)
        self.tk_table_results.bind('<ButtonRelease-1>',self.ctl.env_select_result)

        self.tk_canvas_schematic.bind("<Configure>", self.ctl.on_canvas_resize)# 绑定画布大小变化事件
        pass
    def __style_config(self):
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()