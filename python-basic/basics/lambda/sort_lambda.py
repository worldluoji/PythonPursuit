import operator

# Define the list of records
list_records = [
    ('Financial', '张三', 6000),
    ('IT', '丁一', 8000),
    ('Marketing', '李四', 8000),
    ('IT', '王二', 7000)
]

# Sort the list first by department, then by salary in descending order
list_records.sort(key=operator.itemgetter(0, 2), reverse=True)

print(list_records)

# Define dictionary of ages
dictionary_age = {
    '张三': 30,
    '丁一': 35,
    '李四': 18,
    '王二': 25,
}

# Sort the list by department and then by age in ascending order
list_records.sort(key=lambda x: (x[0], dictionary_age[x[1]]))

print(list_records)