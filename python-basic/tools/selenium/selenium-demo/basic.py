from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

def test():
    # '--verbose',  log_output=sys.stdout,
    service = Service( service_args=['--headless=new','--no-sandbox',
                                    '--disable-dev-shm-usage',
                                    '--disable-gpu',
                                    '--ignore-certificate-errors',
                                    '--ignore-ssl-errors',
                    ])

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    driver = webdriver.Edge(options=options,service=service)

    driver.get("https://modelscope.cn/my/overview")
    print(driver.title)

    driver.quit()


if __name__ == "__main__":
    test()