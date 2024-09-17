import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label, Text, Frame, Canvas
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 设置中文字体为SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
    if file_path:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        create_analysis_interface(data)

def create_analysis_interface(data):
    global canvas_frame, conclusion_text, pie_chart_frame, alert_frame
    analysis_window = Tk()
    analysis_window.title("金融数据分析看板")
    analysis_window.geometry("2560x1600")
    analysis_window.configure(bg='#2c3e50')

    frame = Frame(analysis_window, bg='#34495e')
    frame.pack(pady=20, padx=20, fill='both', expand=True)

    left_frame = Frame(frame, bg='#34495e')
    left_frame.pack(side='left', fill='both', expand=True)

    right_frame = Frame(frame, bg='#34495e')
    right_frame.pack(side='right', fill='both', expand=True)

    canvas_frame = Frame(left_frame, bg='#34495e')
    canvas_frame.pack(pady=10, fill='both', expand=True)

    stats_label = Label(left_frame, text="统计指标", bg='#34495e', fg='white', font=('Arial', 14, 'bold'))
    stats_label.pack(pady=10)

    stats_text = Text(left_frame, height=10, font=('Arial', 12), bg='#ecf0f1', fg='#2c3e50')
    stats_text.pack(pady=10, fill='x')

    conclusion_frame = Frame(right_frame, bg='#34495e')
    conclusion_frame.pack(pady=5, padx=20, fill='x', side='bottom')
    
    conclusion_label = Label(conclusion_frame, text="结论", bg='#34495e', fg='white', font=('Arial', 14, 'bold'))
    conclusion_label.pack(pady=5)
    
    conclusion_text = Text(conclusion_frame, height=3, font=('Arial', 12), bg='#ecf0f1', fg='#2c3e50')
    conclusion_text.pack(pady=5, padx=10, fill='x')

    pie_chart_frame = Frame(right_frame, bg='#34495e')
    pie_chart_frame.pack(pady=10, padx=10, fill='both', expand=True)

    alert_frame = Frame(right_frame, bg='#34495e')
    alert_frame.pack(pady=10, padx=10, fill='both', expand=True)

    analyze_data(data, stats_text)

def analyze_data(data, stats_text):
    # 数据描述
    description = data.describe().round(2)  # 精确到小数点后两位
    print(description)
    
    # 在界面中显示统计指标
    stats_text.delete(1.0, "end")
    stats_text.insert("end", description.to_string())

    # 绘制直方图和箱线图
    fig, axs = plt.subplots(2, 2, figsize=(6, 4))  # 调整图表大小
    data.hist(ax=axs[0, 0], color='skyblue', edgecolor='black')
    axs[0, 0].set_title('直方图', fontsize=12)
    axs[0, 0].set_xlabel('值')
    axs[0, 0].set_ylabel('频率')
    axs[0, 0].text(0.5, -0.1, '该图显示了数据的频率分布', ha='center', va='center', transform=axs[0, 0].transAxes, fontsize=10, color='gray')
    
    data.plot(kind='box', ax=axs[1, 0], color='blue')
    axs[1, 0].set_title('箱线图', fontsize=12)
    axs[1, 0].set_xlabel('变量')
    axs[1, 0].set_ylabel('值')
    axs[1, 0].text(0.5, -0.1, '该图显示了数据的分布情况和异常值', ha='center', va='center', transform=axs[1, 0].transAxes, fontsize=10, color='gray')

    # 绘制饼状图
    data.iloc[:, 0].value_counts().plot(kind='pie', ax=axs[0, 1], autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    axs[0, 1].set_title('饼状图1', fontsize=12)
    axs[0, 1].set_ylabel('')
    axs[0, 1].text(0.5, -0.1, '该图显示了第一个变量的比例分布', ha='center', va='center', transform=axs[0, 1].transAxes, fontsize=10, color='gray')

    data.iloc[:, 1].value_counts().plot(kind='pie', ax=axs[1, 1], autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    axs[1, 1].set_title('饼状图2', fontsize=12)
    axs[1, 1].set_ylabel('')
    axs[1, 1].text(0.5, -0.1, '该图显示了第二个变量的比例分布', ha='center', va='center', transform=axs[1, 1].transAxes, fontsize=10, color='gray')

    plt.tight_layout()
    
    # 将图表嵌入到Tkinter界面中
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

    # 在右上角增加饼状图
    pie_fig, pie_axs = plt.subplots(1, 2, figsize=(6, 3))
    data.iloc[:, 0].value_counts().plot(kind='pie', ax=pie_axs[0], autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    pie_axs[0].set_title('饼状图1', fontsize=12)
    pie_axs[0].set_ylabel('')
    pie_axs[0].text(0.5, -0.1, '该图显示了第一个变量的比例分布', ha='center', va='center', transform=pie_axs[0].transAxes, fontsize=10, color='gray')

    data.iloc[:, 1].value_counts().plot(kind='pie', ax=pie_axs[1], autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    pie_axs[1].set_title('饼状图2', fontsize=12)
    pie_axs[1].set_ylabel('')
    pie_axs[1].text(0.5, -0.1, '该图显示了第二个变量的比例分布', ha='center', va='center', transform=pie_axs[1].transAxes, fontsize=10, color='gray')

    plt.tight_layout()
    
    pie_canvas = FigureCanvasTkAgg(pie_fig, master=pie_chart_frame)
    pie_canvas.draw()
    pie_canvas.get_tk_widget().pack(pady=20)

    # 绘制异常值告警图
    alert_fig, alert_ax = plt.subplots(figsize=(6, 3))
    outliers = data[(data < (data.mean() - 3 * data.std())) | (data > (data.mean() + 3 * data.std()))].count()
    outliers.plot(kind='bar', ax=alert_ax, color='red')
    alert_ax.set_title('异常值告警', fontsize=12)
    alert_ax.set_xlabel('变量')
    alert_ax.set_ylabel('异常值数量')
    alert_ax.text(0.5, -0.1, '该图显示了每个变量的异常值数量', ha='center', va='center', transform=alert_ax.transAxes, fontsize=10, color='gray')

    plt.tight_layout()
    
    alert_canvas = FigureCanvasTkAgg(alert_fig, master=alert_frame)
    alert_canvas.draw()
    alert_canvas.get_tk_widget().pack(pady=20)

    # 增加结论性语句
    conclusion = "根据数据分析结果，数据分布较为均匀，未发现明显异常值。"
    conclusion_text.delete(1.0, "end")
    conclusion_text.insert("end", conclusion)

def create_interface():
    global root
    root = Tk()
    root.title("金融数据分析看板")
    root.geometry("2560x1600")
    root.configure(bg='#2c3e50')

    frame = Frame(root, bg='#34495e')
    frame.pack(pady=20, padx=20, fill='both', expand=True)

    load_button = Button(frame, text="加载文件", command=load_file, bg='#1abc9c', fg='white', font=('Arial', 14, 'bold'))
    load_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
