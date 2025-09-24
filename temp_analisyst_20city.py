from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from meteostat import Point, Daily, Stations, Hourly

"""
全国主要城市气温，宜居度排行

参考数据:
ASHRAE（美国采暖、制冷与空调工程师学会）标准
一般舒适温度范围：约 18–27℃
湿度要求：30–60% 相对湿度
"""

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

cities_location = {
    "北京": (116.41667, 39.91667),
    "上海": (121.43333, 31.23040),
    "广州": (113.23333, 23.16667),
    "天津": (117.20000, 39.13333),
    "香港": (114.10000, 22.20000),
    "珠海": (113.51667, 22.30000),
    "深圳": (114.06667, 22.61667),
    "杭州": (120.20000, 30.26667),
    "重庆": (106.45000, 29.56667),
    "青岛": (120.33333, 36.06667),
    "厦门": (118.10000, 24.46667),
    "福州": (119.30000, 26.08333),
    "兰州": (103.73333, 36.03333),
    "贵阳": (106.71667, 26.56667),
    "长沙": (113.00000, 28.21667),
    "南京": (118.78333, 32.05000),
    "南昌": (115.90000, 28.68333),
    "沈阳": (123.38333, 41.80000),
    "太原": (112.53333, 37.86667),
    "成都": (104.06667, 30.66667),
    "拉萨": (91.00000, 29.60000),
    "乌鲁木齐": (87.68333, 43.76667),
    "昆明": (102.73333, 25.05000),
    "西安": (108.95000, 34.26667),
    "西宁": (101.75000, 36.56667),
    "银川": (106.26667, 38.46667),
    "长春": (125.32357, 43.81684),
    "武汉": (114.31667, 30.51667),
    "郑州": (113.65000, 34.76667),
    "石家庄": (114.48333, 38.03333),
    "三亚": (109.50000, 18.20000),
    "海口": (110.35000, 20.01667),
    "澳门": (113.50000, 22.20000),
    "南京": (118.80000, 32.05000),
}

# 定义desc的显示顺序
desc_order = ["寒冷", "凉爽", "舒适", "偏热", "炎热"]

# 为desc_order定义颜色，越靠后颜色越深，舒适和凉爽使用冷色调
colors = ["#1A07F0", "#6593F0", "#3DE03D", "#FFA07ADC", "#FF4400C6"]

def get_temp_desc(temp):
    # print(111, temp, type(temp))
    if temp < 10:
        return "寒冷"
    elif temp < 18:
        return "凉爽"
    elif temp <= 25:
        return "舒适"
    elif temp < 30:
        return "偏热"
    else:
        return "炎热"


# 时间范围（过去5年）
start = datetime(2023, 1, 1)
end = datetime(2024, 12, 31)

desc_stats = []

# 定义desc的显示顺序
desc_order = ["寒冷", "凉爽", "舒适", "偏热", "炎热"]

# 为desc_order定义颜色，越靠后颜色越深，舒适和凉爽使用冷色调
colors = ["#1A07F0", "#6593F0", "#3DE03D", "#FFA07ADC", "#FF4400C6"]

for city in cities_location.keys():
    lon, lat = cities_location[city]
    # 获取气象点
    location = Point(lat, lon)  # coords[1]是纬度，coords[0]是经度，符合Point类的要求
    
    # 获取逐日数据
    # print(111, city, lon, lat)
    data = Daily(location, start, end)
    # data = Hourly(location, start, end)
    data = data.fetch()
    # print(111, city)
    # print(data.head(10))

    # 过滤掉温度为空的数据
    data = data[data['tavg'].notna()]
    
    data['desc'] = data['tavg'].apply(get_temp_desc)
    # print(111, city)
    # print(data.head(10))
    # 统计各desc字段的天数百分比，并按指定顺序排列
    total_days = data.shape[0]
    comfortable_count = int((data['desc'] == '舒适').sum())
    comfort_ratio = comfortable_count / total_days * 100
    desc_counts = data['desc'].value_counts()
    desc_percentages = (desc_counts / total_days * 100).round(2)

    # 按照指定顺序添加数据
    for desc in desc_order:
        if desc in desc_percentages:
            percentage = desc_percentages[desc]
        else:
            percentage = 0.0
        desc_stats.append({
            "city": city,  # 使用中文城市名
            "description": desc,
            "percentage": percentage
        })

# 新增：统计desc字段各情况下的天数百分比并输出表格和条形图
desc_df = pd.DataFrame(desc_stats)
# print("\ndesc字段统计:")
# print(desc_df)

# 创建透视表用于绘图，确保列的顺序正确
pivot_df = desc_df.pivot(index='city', columns='description', values='percentage')
# 按照指定顺序重新排列列
pivot_df = pivot_df[desc_order]
# pivot_df.sort_values(by='舒适', ascending=False, inplace=True)
pivot_df.sort_values(by='炎热', ascending=False, inplace=True)
print("\n透视表:")
print(pivot_df)

# 绘制堆叠条形图，使用指定颜色
ax = pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), color=colors)
plt.ylabel("百分比 (%)")
plt.xlabel("城市")
plt.title("各城市温度描述分布")
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[::-1], labels[::-1], title="温度描述")  # 反转顺序
# plt.legend(title="温度描述")
plt.xticks(rotation=45)
plt.tight_layout()

# 在每个堆叠部分添加数据标签
for container in ax.containers:
    labels = [f'{v:.1f}%' if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center', fontsize=8)

plt.show()