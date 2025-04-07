# Selenium
所谓的无头浏览器，指的是没有界面的浏览器。我们依然可以借助火狐，谷歌等浏览器进行数据的抓取，但不会产生界面。

这项技术有一个比较常用的框架，叫做 Selenium，它是一个自动化测试和浏览器自动化的开源框架。它允许开发人员编写脚本，并借助浏览器和浏览器的驱动，来模拟在浏览器中的行为，自动执行一些列的操作，比如点击按钮、填写表单、导航到不同的页面等。

---

## 安装Selenium库
```
uv init selenium-demo
cd selenium-demo
uv add selenium
```

---

## Selenium 4 的自动化驱动管理
1. **自动检测浏览器版本并下载驱动**  
   Selenium 4 新增了自动检测本地浏览器版本的功能，并会尝试从官方源下载匹配的驱动程序。例如，使用 `webdriver.Chrome()` 时，若未指定驱动路径，Selenium 会通过内置逻辑自动寻找浏览器版本并下载对应的驱动。

   **示例代码（无需手动指定路径）：**
   ```python
   from selenium import webdriver
   driver = webdriver.Chrome()  # 自动检测浏览器版本并下载驱动
   ```

2. **推荐使用 `webdriver-manager` 库**  
   为解决自动下载可能因网络问题失败的情况（尤其是国内环境），官方推荐使用第三方库 `webdriver-manager`。该库能自动管理驱动的下载、版本匹配和路径配置，进一步简化流程。

   **示例代码：**
   ```python
   from selenium import webdriver
   from selenium.webdriver.chrome.service import Service
   from webdriver_manager.chrome import ChromeDriverManager

   service = Service(executable_path=ChromeDriverManager().install())
   driver = webdriver.Chrome(service=service)
   ```

---

### 二、仍需手动指定路径的场景
1. **需要特定版本的驱动**  
   若需使用非当前浏览器版本的驱动（如测试旧版本浏览器），仍需手动下载驱动并通过 `Service` 对象指定路径。

   **示例代码：**
   ```python
   from selenium import webdriver
   from selenium.webdriver.chrome.service import Service

   service = Service(executable_path="/path/to/custom/chromedriver")
   driver = webdriver.Chrome(service=service)
   ```

2. **国内网络环境限制**  
   Selenium 自动下载依赖的官方源可能在国内访问不稳定，此时建议手动下载驱动并指定路径，或使用 `webdriver-manager` 的国内镜像源。

3. **非主流浏览器或特殊配置**  
   如使用 Firefox、Edge 等浏览器，或需配置代理、无头模式等参数时，可能需要结合 `Service` 和 `Options` 对象进行更精细的控制。

---

## reference
- https://www.selenium.dev/zh-cn/documentation/webdriver/elements/finders/
- https://www.selenium.dev/zh-cn/documentation/webdriver/elements/locators/