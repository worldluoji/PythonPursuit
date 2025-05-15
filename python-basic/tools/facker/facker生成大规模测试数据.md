🛠️ **生成大规模测试数据的建议**：

1. **使用数据生成工具**：
   - 在线工具：Mockaroo、JSON Generator
   - Python脚本（使用Faker库）：
     ```python
     from faker import Faker
     import json

     fake = Faker()
     users = []

     for _ in range(1000):
         user = {
             "id": fake.random_int(),
             "name": fake.name(),
             "age": fake.random_int(18, 65),
             "email": fake.email(),
             "is_active": fake.boolean(),
             "registration_date": str(fake.date_this_decade()),
             "address": {
                 "street": fake.street_address(),
                 "city": fake.city(),
                 "zipcode": fake.zipcode()
             },
             "orders": []
         }
         users.append(user)

     print(json.dumps({"users": users}, indent=2))
     ```

2. **数据结构建议**：
   - 包含多层嵌套（对象嵌套数组嵌套对象）
   - 混合数据类型（字符串、数字、布尔值、日期）
   - 包含空值（测试异常处理）
   - 添加随机生成的特殊字符测试用例

3. **性能测试建议**：
   - 10,000条数据 ≈ 1-2MB
   - 100,000条数据 ≈ 10-15MB
   - 1,000,000条数据 ≈ 100-150MB

4. **验证工具**：
   - JSONLint（验证格式正确性）
   - jq（命令行处理JSON）
   - Postman（API测试）
