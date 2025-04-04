# Selenium
所谓的无头浏览器，指的是没有界面的浏览器。我们依然可以借助火狐，谷歌等浏览器进行数据的抓取，但不会产生界面。

这项技术有一个比较常用的框架，叫做 Selenium，它是一个自动化测试和浏览器自动化的开源框架。它允许开发人员编写脚本，并借助浏览器和浏览器的驱动，来模拟在浏览器中的行为，自动执行一些列的操作，比如点击按钮、填写表单、导航到不同的页面等。

以下是使用Selenium进行网页自动化的基本步骤：

1. 安装Selenium库
你可以通过pip安装Selenium：
```
pip install selenium
```

2. 下载WebDriver
根据你想要自动化的浏览器[下载对应的WebDriver](https://www.selenium.dev/downloads/#Platforms%20Supported%20by%20Selenium)。

Selenium 4 引入了对 WebDriver Manager 的内置支持，这意味着在某些情况下，你不再需要手动下载和管理浏览器驱动程序（如ChromeDriver或GeckoDriver）。这项改进简化了设置过程，因为Selenium现在可以自动处理驱动程序的下载和配置。

尽管Selenium 4提供了内置的WebDriver管理功能，但有时你可能仍然需要手动配置WebDriver，特别是在以下几种情况下：
- 当你需要使用特定版本的WebDriver时。
- 在企业环境中，由于网络限制无法直接从互联网下载驱动程序。
- 需要支持的浏览器或版本尚未被Selenium内置管理器所涵盖。


3. 编写Python脚本
下面是一个简单的例子，展示如何使用Selenium打开一个网站并模拟点击操作：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  # 导入 Chrome Service 类
import time

# 设置ChromeDriver的路径
driver_path = '/path/to/chromedriver'

# 创建 Service 对象，指定驱动程序的路径
s = Service('/path/to/chromedriver')
# 使用 Service 对象创建 WebDriver 实例
driver = webdriver.Chrome(service=s)

try:
    # 打开目标网站
    driver.get('http://example.com')

    # 等待页面加载完成
    time.sleep(5)  # 可以用更智能的方式等待元素出现

    # 找到需要点击的元素并点击它
    element = driver.find_element(By.ID, 'element_id')  # 使用合适的定位方式
    element.click()

    # 模拟更多交互...

finally:
    # 关闭浏览器
    driver.quit()
```

4. 运行脚本
确保你在运行脚本之前已经正确设置了环境变量或者指定了WebDriver的完整路径。

除了Selenium之外，还有其他一些工具也可以用于网页自动化，比如Puppeteer（主要用于Node.js环境），但如果你已经在使用Python，那么Selenium通常是首选。

请注意，随着技术的发展，新的工具和方法不断涌现，所以在开始项目前检查最新的工具和技术是很重要的。此外，对于一些现代化的单页应用(SPA)，可能还需要处理JavaScript生成的内容，这时可以考虑使用像Playwright这样的工具，它也支持Python，并且对现代Web应用程序有更好的支持。


## 查询元素
```html
<ol id="vegetables">
 <li class="potatoes">…
 <li class="onions">…
 <li class="tomatoes"><span>Tomato is a Vegetable</span>…
</ol>
<ul id="fruits">
  <li class="bananas">…
  <li class="apples">…
  <li class="tomatoes"><span>Tomato is a Fruit</span>…
</ul>
```
通过如下方法，可以找到tomatoes元素：
```python
fruits = driver.find_element(By.ID, "fruits")
tomatoes = fruits.find_element(By.CLASS_NAME,"tomatoes")
```

## reference
- https://www.selenium.dev/zh-cn/documentation/webdriver/elements/finders/
- https://www.selenium.dev/zh-cn/documentation/webdriver/elements/locators/