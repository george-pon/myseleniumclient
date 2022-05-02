#!/usr/bin/python3
#
# 指定されたURLにアクセスしてスクリーンショットを撮影する
#   Web サイトの document title も 取得する
#   スクリーンショットも採取する
#
# 結果はJSON型文字列として標準出力に出力する。
#   title : document title
#   screenshot : base64 encoded screenshot (PNG format)
#
# 環境変数 SELENIUM_URL または 起動オプション --seleniumurl に指定がある場合は、ネットワーク経由のselenium driverに接続する。
# 指定が無い場合は local にある chromium コマンドを起動する。
#
# https://www.selenium.dev/documentation/webdriver/  Web Driver のドキュメント
# 
# https://qiita.com/DisneyAladdin/items/431e9fd0c1cf709347da 【Python】Seleniumでスクリーンショットを撮る - Qiita
#
# https://github.com/SeleniumHQ/docker-selenium SeleniumHQ/docker-selenium: Docker images for the Selenium Grid Server
#     SeleniumHQ さんが作った Dockerimage https://hub.docker.com/u/selenium
#     これを使えば selenium docker image を自作しなくて済む
#     helm chart 版もある模様 https://github.com/SeleniumHQ/docker-selenium/blob/trunk/chart/selenium-grid/README.md
#     内部にVNCのX Serverを起動しているので、画面はあるからスクリーンショットも撮影可能。
# 
# https://qiita.com/ryoheiszk/items/93b2d52eec370c09a22e DockerでPython-Seleniumスクレイピング環境を立てた - Qiita
#     上のSeleniumHQを使ったサンプルアプリ
#
# 2022.04.10
#
import os
import sys
import argparse
import json
import base64
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def browser_fetch(url, verbose, screenshot, fullscreenshot, cmdscreenshot, waitsec, seleniumurl):

    # デフォルトの待機秒数は 5
    if not waitsec:
        waitsec = 5

    # 出力用の辞書型を作成
    result_dict = {}

    if verbose:
        print("url="+url)

    # output file name
    # filename =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot.png")
    filename =  "screenshot.png"

    # 引数で seleniumurl が指定された場合は、それを使う
    # 指定が無い場合は、環境変数 SELENIUM_URL を読み取ってみる
    if not seleniumurl:
        seleniumurl = os.environ["SELENIUM_URL"]

    # seleniumurl の指定が無い場合は、localにあるchoromiumコマンドを起動してみる
    if not seleniumurl:
        # 起動オプション設定 (普通にlocalにあるchromiumコマンドを起動する場合)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # ヘッドレスで起動するオプションを指定
        options.add_argument("--disable-gpu") # GPU使用しない
        options.add_argument('--disable-extensions')       # すべての拡張機能を無効にする。ユーザースクリプトも無効にする
        options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
        options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
        # options.add_argument('--start-maximized')          # 起動時にウィンドウを最大化する
        # create driver (普通にlocalにあるchromiumを起動する場合)
        driver = webdriver.Chrome(options=options)
    else:
        # ネットワーク上にあるchrome driverに接続する場合
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(
            command_executor=os.environ["SELENIUM_URL"],
            options=options
        )

    # 要素指定時の最大待機秒数を設定
    driver.implicitly_wait(5)

    # access web site
    driver.get(url)

    # timer 強制的にwait
    time.sleep(waitsec)

    # get title of the page
    title = driver.execute_script("return document.title;")
    result_dict["title"] = title
    if verbose:
        print("document title is "+title)

    # chromium コマンドを直接使ってスクリーンショットをとるｗｗ
    if cmdscreenshot:
        # chromium --headless --disable-gpu --screenshot URL
        subprocess.run(["/usr/bin/chromium", "--headless", "--disable-gpu", "--screenshot", url])

        # Read Screen Shot file
        f = open(filename, "rb")
        data = f.read()
        data64 = base64.b64encode(data)
        str64 = data64.decode('utf-8')
        result_dict["screenshot"] = str64
        f.close()

    # 画面サイズはdoumentのサイズに応じて変更しない
    if screenshot:
        # Get Screen Shot
        driver.save_screenshot(filename)

        # Read Screen Shot file
        f = open(filename, "rb")
        data = f.read()
        data64 = base64.b64encode(data)
        str64 = data64.decode('utf-8')
        result_dict["screenshot"] = str64
        f.close()
        if verbose:
            print("screen shot save to "+filename)

    # 画面サイズはdocumentのサイズに応じて変更。webpage全体を撮影する。
    if fullscreenshot:
        # get width and height of the page
        w = driver.execute_script("return document.body.scrollWidth;")
        h = driver.execute_script("return document.body.scrollHeight;")

        # set window size
        driver.set_window_size(w,h)

        # Get Screen Shot
        driver.save_screenshot(filename)

        # Read Screen Shot file
        f = open(filename, "rb")
        data = f.read()
        data64 = base64.b64encode(data)
        str64 = data64.decode('utf-8')
        result_dict["screenshot"] = str64
        f.close()
        if verbose:
            print("screen shot save to "+filename)

    # Close Web Browser
    driver.quit()

    # output result JSON
    print(json.dumps(result_dict, indent=2, ensure_ascii=False ))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="access url")
    parser.add_argument("--screenshot", action="count", help="save screen shot, default window size")
    parser.add_argument("--fullscreenshot", action="count", help="save screen shot, whole web page")
    parser.add_argument("--cmdscreenshot", action="count", help="save screen shot, with chrome command")
    parser.add_argument("--verbose", action="count", help="save document title")
    parser.add_argument("--waitsec", type=int, help="wait page load in seconds")
    parser.add_argument("--seleniumurl", help="selenium service url , like http://selenium-chrome:4444/wd/hub ")
    args = parser.parse_args()
    browser_fetch( url=args.url , verbose=args.verbose, screenshot=args.screenshot, cmdscreenshot=args.cmdscreenshot, fullscreenshot=args.fullscreenshot, waitsec=args.waitsec, seleniumurl=args.seleniumurl)
