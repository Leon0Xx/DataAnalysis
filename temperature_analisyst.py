from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

cities_location = {
    "Beijing": (116.41667, 39.91667),
    "Shanghai": (121.43333, 34.50000),
    "Tianjin": (117.20000, 39.13333),
    "Hong Kong": (114.10000, 22.20000),
    "Guangzhou": (113.23333, 23.16667),
    "Zhuhai": (113.51667, 22.30000),
    "Shenzhen": (114.06667, 22.61667),
    "Hangzhou": (120.20000, 30.26667),
    "Chongqing": (106.45000, 29.56667),
    "Qingdao": (120.33333, 36.06667),
    "Xiamen": (118.10000, 24.46667),
    "Fuzhou": (119.30000, 26.08333),
    "Lanzhou": (103.73333, 36.03333),
    "Guiyang": (106.71667, 26.56667),
    "Changsha": (113.00000, 28.21667),
    "Nanjing": (118.78333, 32.05000),
    "Nanchang": (115.90000, 28.68333),
    "Shenyang": (123.38333, 41.80000),
    "Taiyuan": (112.53333, 37.86667),
    "Chengdu": (104.06667, 30.66667),
    "Lhasa": (91.00000, 29.60000),
    "Urumqi": (87.68333, 43.76667),
    "Kunming": (102.73333, 25.05000),
    "Xi'an": (108.95000, 34.26667),
    "Xining": (101.75000, 36.56667),
    "Yinchuan": (106.26667, 38.46667),
    "Changchun": (125.35000, 43.88333),
    "Wuhan": (114.31667, 30.51667),
    "Zhengzhou": (113.65000, 34.76667),
    "Shijiazhuang": (114.48333, 38.03333),
    "Sanya": (109.50000, 18.20000),
    "Haikou": (110.35000, 20.01667),
    "Aomen": (113.50000, 22.20000),
    "Nanjing": (118.80000, 32.05000),
}

# 添加中英文城市名称映射
city_name_mapping = {
    "Beijing": "北京",
    "Shanghai": "上海",
    "Tianjin": "天津",
    "Hong Kong": "香港",
    "Guangzhou": "广州",
    "Zhuhai": "珠海",
    "Shenzhen": "深圳",
    "Hangzhou": "杭州",
    "Chongqing": "重庆",
    "Qingdao": "青岛",
    "Xiamen": "厦门",
    "Fuzhou": "福州",
    "Lanzhou": "兰州",
    "Guiyang": "贵阳",
    "Changsha": "长沙",
    "Nanjing": "南京",
    "Nanchang": "南昌",
    "Shenyang": "沈阳",
    "Taiyuan": "太原",
    "Chengdu": "成都",
    "Lhasa": "拉萨",
    "Urumqi": "乌鲁木齐",
    "Kunming": "昆明",
    "Xi'an": "西安",
    "Xining": "西宁",
    "Yinchuan": "银川",
    "Changchun": "长春",
    "Wuhan": "武汉",
    "Zhengzhou": "郑州",
    "Shijiazhuang": "石家庄",
    "Sanya": "三亚",
    "Haikou": "海口",
    "Aomen": "澳门",
    "Nanjing": "南京"
}

# 定义主要城市和坐标（可扩展）
cities = ["Changsha", "Nanchang", "Wuhan", "Chengdu", "Chongqing", "Nanjing", "Fuzhou", "Hangzhou"]

def get_temp_desc(temp):
    # print(111, temp, type(temp))
    if temp < 10:
        return "寒冷"
    elif temp < 18:
        return "凉爽"
    elif temp < 25:
        return "舒适"
    elif temp < 30:
        return "偏热"
    else:
        return "炎热"

# 时间范围（过去5年）
start = datetime(2020, 1, 1)
end = datetime(2024, 12, 31)

results = []
desc_stats = []

# 定义desc的显示顺序
desc_order = ["寒冷", "凉爽", "舒适", "偏热", "炎热"]

# 为desc_order定义颜色，越靠后颜色越深，舒适和凉爽使用冷色调
colors = ["#1A07F0", "#6593F0", "#3DE03D", "#FFA07ADC", "#FF4400C6"]

for city in cities:
    coords = cities_location[city]
    # 获取气象点
    location = Point(coords[1], coords[0])  # coords[1]是纬度，coords[0]是经度，符合Point类的要求

    # 获取逐日数据
    data = Daily(location, start, end)
    data = data.fetch()
    data = data[data['tavg'].notna()]
    data['desc'] = data['tavg'].apply(get_temp_desc)
    # print(type(data))
    # print(data.head(10))

    # 计算舒适度天数（18~25℃）
    comfortable_days = ((data['tavg'] >= 18) & (data['tavg'] <= 25)).sum()
    total_days = data.shape[0]
    comfort_ratio = comfortable_days / total_days * 100

    # 统计各desc字段的天数百分比，并按指定顺序排列
    desc_counts = data['desc'].value_counts()
    desc_percentages = (desc_counts / total_days * 100).round(2)
    
    # 按照指定顺序添加数据
    for desc in desc_order:
        if desc in desc_percentages:
            percentage = desc_percentages[desc]
        else:
            percentage = 0.0
        desc_stats.append({
            "city": city_name_mapping[city],  # 使用中文城市名
            "description": desc,
            "percentage": percentage
        })

# 转为DataFrame
df = pd.DataFrame(results)
print(df)

# 新增：统计desc字段各情况下的天数百分比并输出表格和条形图
desc_df = pd.DataFrame(desc_stats)
print("\ndesc字段统计:")
print(desc_df)

# 创建透视表用于绘图，确保列的顺序正确
pivot_df = desc_df.pivot(index='city', columns='description', values='percentage')
# 按照指定顺序重新排列列
pivot_df = pivot_df[desc_order]
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
