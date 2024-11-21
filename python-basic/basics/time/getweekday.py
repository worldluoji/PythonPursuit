import datetime

# 获取当前的日期和时间
now = datetime.datetime.now()

# 输出当前时间
print("当前时间:", now)

# 获取当前是星期几
# weekday()方法返回的是0（周一）到6（周日），isoweekday()方法返回1（周一）到7（周日）
weekday_number = now.isoweekday()

# 将数字转换成对应的星期几文本
weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
current_weekday = weekdays[weekday_number - 1]

# 输出当前是星期几
print("今天是:", current_weekday)