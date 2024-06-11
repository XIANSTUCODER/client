import socket
import threading
import queue
import json
import os
import pandas as pd

#库文件
from command_operator import * 

# 定义命令标记
SEND_MESSAGE = "SEND_MESSAGE"
SEND_IMAGE = "SEND_IMAGE"
SEND_RESET_GPT_HISTORY = "RESET"
END_FLAG = "END"
TaskTable_PATH = "taskTable.xlsx"
image_path = "screenshot/screenshot.png" # 存放截图的路径
encoding = 'utf-8'
def send_message(client_socket, message):
    client_socket.send(message.encode(encoding))

def send_image(client_socket, image_path):
    try:
        file_size = os.path.getsize(image_path)
        send_message(client_socket, str(file_size))# 发送文件大小
        with open(image_path, 'rb') as file:# 打开并发送文件内容
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)
            # 发送图片结束标志
            # client_socket.send(b"I_E")
    except FileNotFoundError:
        print(f"图片文件 '{image_path}' 未找到")
    except Exception as e: 
        print(f"send_image发生异常: {str(e)}")

def receive_message(client_socket):
    return client_socket.recv(1024).decode(encoding)
    # return client_socket.recv(1024)

def handle_server_messages(client_socket, client_message_queue):
    try:
        while True:
            response = receive_message(client_socket)

            # 检查响应类型
            try:
                # json的操作命令响应
                order_list = json.loads(response)
                if isinstance(order_list, list):
                    client_message_queue.put(order_list)
                    # print('order_list is a list')
                
            except json.JSONDecodeError:
                # 普通字符串响应
                client_message_queue.put(response)
    except ConnectionResetError:
        print("连接被重置")
    except Exception as e:
        print(f"handle_server_messages发生异常: {str(e)}")

def client_main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('202.117.3.78', 55555)  # 替换为服务器的实际地址和端口

    try:
        client_socket.connect(server_address)
        print('----------------------成功连接到服务器了！----------------------')
        print("-------步骤：先发送任务消息，再一步一步地截图；若要重新开始任务，就再发一次任务消息，然后在手机上手动返回任务的开始界面-----------")

        # 创建客户端消息队列
        client_message_queue = queue.Queue()

        # 启动处理服务器消息的线程
        server_message_thread = threading.Thread(target=handle_server_messages, args=(client_socket, client_message_queue))
        server_message_thread.start()

        while True:
            print('\n------发送任务消息，请输入"m" ; 发送图片请输入"i"------')
            command = input("发送消息或图片(m/i/END): ")

            #发送任务信息   “m xx”  m + 空格（一个或多个）+ 任务在表中的序号
            if command.startswith('m'):
                send_message(client_socket, SEND_MESSAGE)
                # message = input("请输入消息: ")
                #region 
                # --------------影音视听---------------
                #region  
                # message = "我想看去哔哩哔哩看“守护解放西4””" # b站
                # message = "去哔哩哔哩购买邀请码" # b站
                # message = "去哔哩哔哩看“守护解放西4”并将第一集缓存到手机里" # b站
                # message = "去哔哩哔哩的创作中心查看稿件“神龙大侠之旅结束段”的数据" # b站

                # message = "播放陈奕迅的“十年”，并且收藏" # QQ音乐
                # message = "去QQ音乐中将弹唱版的“姑娘别哭泣”添加到自建歌单“测试”中" # QQ音乐
                # message = "开启QQ音乐的定时关闭，设为45分钟" # QQ音乐
                # message = "去QQ音乐查看我收藏的歌曲" # QQ音乐

                # message = "去Spotify搜索热门华语音乐歌单" # Spotify
                # message = "去Spotify查看我的歌单" # Spotify
                # message = "去Spotify中播放艺人团体“Red Velvet”的歌曲" # Spotify
                # message = "去Spotify中查看我喜欢的歌曲并播放" # Spotify

                # message = "在喜马拉雅找一个儿童的睡前故事播放" # 喜马拉雅
                # message = "去喜马拉雅中开启定时关闭功能，并选择播完3集声音" # 喜马拉雅
                # message = "开启喜马拉雅中的哄睡模式" # 喜马拉雅
                # message = "去喜马拉雅中查看我已过期的优惠券" # 喜马拉雅
                # message = "去喜马拉雅中查看我购买过的内容" # 喜马拉雅

                # message = "去哔哩哔哩漫画领取大会员的漫画福利券" # 哔哩哔哩漫画
                # message = "去哔哩哔哩漫画领取漫画福利券" # 哔哩哔哩漫画
                # message = "关闭哔哩哔哩漫画的自动购买下一话漫画的功能" # 哔哩哔哩漫画
                # message = "去哔哩哔哩漫画看我缓存下来的漫画" # 哔哩哔哩漫画
                # message = "去哔哩哔哩漫画看我的已购漫画" # 哔哩哔哩漫画
                # message = "去哔哩哔哩漫画查看国漫榜" # 哔哩哔哩漫画    
                #endregion
                # --------------聊天社交---------------
                #region
                # message = "去小红书搜索男生冬季穿搭并点赞第一个作品" # 小红书
                # message = "去小红书看我的浏览记录" # 小红书
                # message = "去小红书查看优惠券" # 小红书
                # message = "去小红书查看收礼记录" # 小红书

                # message = "去微信给“咖啡因从咖啡果中来”发消息，提醒她吃早饭" # 微信
                # message = "去看看我的微信朋友圈" # 微信
                # message = "去微信中发一条朋友圈“早上好”，且仅自己可见" # 微信
                # message = "去微信中发一条朋友圈，现拍一张照片，配文“早上好”" # 微信
                # message = "去微信面对面建群" # 微信
                # message = "去微信中进入聊天界面，添加“线条小狗第1弹”表情包" # 微信
                # message = "去微信中切换账号" # 微信
                # message = "去微信中打开贝壳找房" # 微信

                # message = "查看微博中所有@我的消息" # 微博
                # message = "查看微博热搜" # 微博
                # message = "去微博查看我发过的评论" # 微博
                # message = "找到西安交通大学的官方微博并关注" # 微博
                #endregion
                # --------------出行导航---------------
                #region
                
                # message = "我要用高德地图看用公交地铁到西安北站的路线" # 高德地图
                # message = "去高德地图中看卫星地图" # 高德地图
                # message = "去高德地图搜索西安北站并收藏" # 高德地图
                # message = "去高德地图将收藏的西安北站设置备注名为高铁站" # 高德地图

                # message = "去携程旅行预定西安北站附近的酒店双床房" # 携程旅行
                # message = "去携程旅行预定12月14日到12月15日西安永宁门附近的民宿" # 携程旅行
                # message = "去携程旅行预定3月14日到3月15日西安永宁门附近的民宿" # 携程旅行
                # message = "去携程旅行看看北京的旅游景点" # 携程旅行
                # message = "去携程旅行导入别人帮我订的机票" # 携程旅行
                # message = "去携程旅行查看我的旅行路线" # 携程旅行

                # message = "去铁路12306预订11月11日从西安北站到北京西站的火车票" # 铁路12306
                # message = "去铁路12306查看车站大屏" # 铁路12306
                # message = "去铁路12306查看12月27日从长沙到重庆的火车票" # 铁路12306
                # message = "去铁路12306申请临时身份证明" # 铁路12306
                # message = "去铁路12306查看12月6日的G1938次高铁、西安北到徐州东的高铁外卖订餐界面" # 铁路12306
                # message = "去铁路12306查询上海客服中心电话并拨打" # 铁路12306
                # message = "去铁路12306查看待评价的餐饮订单" # 铁路12306

                # message = "去移动交通大学预约班车，早上6：20从思源中心出发的那一趟" # 移动交通大学
                # message = "去移动交通大学查看横向合同立项情况" # 移动交通大学
                # message = "去移动交通大学预约健身房" # 移动交通大学
                
                # message = "在航旅纵横预订11月20日从西安到澳门的往返机票" # 航旅纵横
                # message = "在航旅纵横查看我待出行的行程" # 航旅纵横
                # message = "去航旅纵横查询CA8888航班" # 航旅纵横
                # message = "去航旅纵横将我的行程导入日历中" # 航旅纵横
                # message = "去航旅纵横查看上海浦东机场的机场大屏" # 航旅纵横
                # message = "去航旅纵横查看我的权益包" # 航旅纵横
                # message = "去航旅纵横添加个人的护照信息" # 航旅纵横
                #endregion
                # --------------购物消费---------------
                #region
                
                # message = "去淘宝中搜索罗技键盘并选择第一件商品" # 淘宝
                # message = "查看我淘宝中收藏的宝贝" # 淘宝
                # message = "删除淘宝订单的第一条退款记录" # 淘宝
                # message = "去淘宝给所有订单添加价保" # 淘宝

                # message = "全选盒马购物车中的商品并删除" # 盒马
                # message = "清空盒马的购物车" # 盒马
                # message = "去盒马购买大闸蟹" # 盒马
                # message = "去盒马查看我开过的发票" # 盒马
                # message = "去盒马添加收货地址" # 盒马

                # message = "去拼多多搜索发卡，并选择品牌商品" # 拼多多
                # message = "去拼多多中查看待处理的退款订单" # 拼多多
                # message = "去拼多多中查看我的举报投诉的处理进度" # 拼多多
                # message = "查看我拼多多中收藏的商品" # 拼多多
                #endregion
                # --------------摄影摄像---------------
                #region
                
                # message = "去美图秀秀现拍一张照片并添加滤镜“深夜食堂”" # 美图秀秀
                # message = "去美图秀秀制作一张一寸照" # 美图秀秀
                # message = "去美图秀秀设置我的个人水印" # 美图秀秀
                # message = "去美图秀秀设置不允许他人保存我的图片" # 美图秀秀
                
                # message = "去轻颜查看我用过的特效" # 轻颜
                # message = "将轻颜的闪光灯设置打开" # 轻颜
                # message = "去轻颜将男生妆容适配关闭" # 轻颜
                # message = "" # 
                #endregion
                # --------------金融理财---------------
                #region
                
                # message = "支付宝中查看收款记录" # 支付宝
                # message = "将支付宝余额提现" # 支付宝
                # message = "支付宝中帮我查看本月账单的支出情况" # 支付宝
                # message = "支付宝中帮我交10元电费" # 支付宝
                # message = "在支付宝中取消淘宝的免密支付" # 支付宝

                # message = "查看零钱金额" # 微信
                # message = "打开微信收款码" # 微信
                # message = "用微信交供暖费" # 微信
                # message = "在微信中暂停使用付款码支付功能" # 微信
                
                #endregion
                # --------------美食娱乐---------------
                #region
                
                # message = "去饿了么查找3km内的奶茶店" # 饿了么
                # message = "用饿了么看看炸鸡的外卖，销量优先" # 饿了么
                # message = "去饿了么中新增收货地址" # 饿了么         
                # message = "去饿了么看看我的优惠券" # 饿了么
                # message = "我想吃肯德基的甜品两件套" # 饿了么
                # message = "去饿了么中开通小额免密支付" # 饿了么

                # message = "在美团中到黄焖鸡米饭店点一份大份微辣黄焖鸡米饭" # 美团
                # message = "去美团中查看我的收藏" # 美团
                # message = "去美团中查看3公里内的KTV" # 美团
                # message = "去美团中查看我退款的订单" # 美团

                # message = "去大麦查看我看过的演出票" # 大麦
                # message = "去大麦添加新的观演人" # 大麦
                # message = "去大麦看看我附近的脱口秀的票" # 大麦
                # message = "开启大麦的积分过期提醒" # 大麦
                # message = "去大麦把我看过的德云社演出的官方电子纪念票存入相册" # 大麦
                #endregion
                # --------------体育运动---------------
                #region
                
                # message = "查看/设置运动步数？" # keep
                # message = "去Keep开始行走记录" # keep
                # message = "去Keep查看我的运动装备" # keep
                # message = "去Keep查看“八段锦”系列的课程" # keep
                # message = "去Keep中开启体态评估" # keep

                # message = "去训记中查看二头肌的动作" # 训记
                # message = "去训记中查看我的身体数据" # 训记
                # message = "去训记中观看俯身飞鸟动作演示" # 训记
                # message = "去训记中查看训练的数据统计" # 训记

                # message = "去华为运动健康设置跑步的心率上限值为198次/分钟" # 华为运动健康
                # message = "" # 
                #endregion
                # --------------学习资讯---------------
                #region
                
                # message = "用网易有道词典翻译一下“deep learning”" # 网易有道词典
                # message = "去网易有道词典背今天的单词”" # 网易有道词典
                # message = "去网易有道词典下载离线的牛津词典" # 网易有道词典

                message = "去微信读书将西游记添加到书架中" # 微信读书
                # message = "查看我微信读书的阅读时长" # 微信读书
                # message = "去微信读书设置允许使用音量键翻页" # 微信读书

                # message = "查看今日头条的头条热榜" # 今日头条
                # message = "去查看今日头条的浏览历史" # 今日头条
                # message = "打开今日头条的新闻推送" # 今日头条

                # message = "搜索问题“CS ranking in China”，并打开第一个热门回答" # 知乎
                # message = "去知乎中查看我收藏的内容" # 知乎
                # message = "去知乎中查看我赞过的内容" # 知乎
                #endregion
                # --------------效率办公--------------
                #region                
                
                # message = "将网易邮箱大师中的所有未读邮件标为已读" # 网易邮箱大师
                # message = "去网易邮箱大师设置为收取全部邮件" # 网易邮箱大师

                # message = "在腾讯会议中开一个快速会议，打开视频，并使用个人会议号" # 腾讯会议

                # message = "去系统应用“日历”中给圣诞节添加提醒事项“买礼物”" # 日历
                # message = "在日历中搜索“设置”" # 日历

                # message = "去qq邮箱打开收件箱并查看每日悦读订阅的内容" # qq邮箱
                # message = "去qq邮箱给631080500@qq.com写邮件" # qq邮箱

                # message = "去手机应用“信息”中将查看通知信息" # 信息
                # message = "去系统应用“信息”中删除所有骚扰信息" # 信息

                # message = "给联系人中的阿里巴巴钉钉客服打电话" # 电话

                # message = "将联系人中的阿里巴巴钉钉客服的二维码信息分享给微信的文件传输助手" # 联系人
                
                # message = "在备忘录中的待办添加事项“周日去拔牙”" # 备忘录
                # message = "在备忘录中查看我收藏的笔记" # 备忘录
                
                # message = "打开一个chrome浏览器的无痕浏览窗口" # chrome
                # message = "清除Chrome浏览器的Cookie数据" # chrome
                # message = "将Chrome浏览器的默认搜索引擎设置为Bing" # chrome
                #endregion
                # --------------便捷生活--------------
                #region
                
                # message = "去中国移动充20元话费" # 中国移动
                # message = "去中国移动查询我订阅的套餐" # 中国移动

                # message = "去菜鸟查看我有几个待取包裹" # 菜鸟裹裹
                # message = "去菜鸟开启丰巢小程序的取件授权" # 菜鸟裹裹
                # message = "去菜鸟添加家人账号" # 菜鸟裹裹
                
                # message = "打开支付宝的公交乘车码" # 支付宝
                # message = "去支付宝交电费" # 支付宝
                # message = "去移动交通大学查看我的安全邮箱" # 支付宝
                # message = "去支付宝中的“校园派”小程序中给我的校园卡充值" # 支付宝

                # message = "去系统应用“天气”中查看北京天气" # 天气

                # message = "去系统应用“时钟”中新建一个上午9点半的闹钟" # 时钟
                # message = "去系统应用“时钟”查看纽约的时间" # 时钟
                #endregion
                # --------------功能设置--------------
                #region
                
                # message = "开启个人移动WLAN热点" # 设置
                # message = "打开蓝牙并连接airpods" # 设置
                # message = "去设置中将时间设为24小时制" # 设置
                # message = "去设置中打开电池管理" # 设置

                # message = "我想要将微信界面更改为英文界面" # 微信
                # message = "去微信中在我的发现页添加“搜一搜”功能" # 微信

                # message = "查看支付宝账号的邮箱信息" # 支付宝
                # message = "支付宝的深色模式设置为跟随系统" # 支付宝
                # message = "去支付宝中设置不可通过转账页面添加我" # 支付宝

                # message = "去手机应用“天气”中查看上海市静安区的天气" # 华为天气

                # message = "在联系人界面设置卞艺衡的工作单位为交大" # 联系人
                #endregion
                #endregion
                taskdf = pd.read_excel(TaskTable_PATH, keep_default_na= False) 
                tasklist = taskdf['任务内容'].tolist() # 任务列表
                inputarray = command.split(" ")
                if len(inputarray) == 1:
                    num = input("请输入任务序号：(序号需要大于3)")
                else:
                    num = inputarray[1]
                while not num.isdigit() or tasklist[int(num) - 2] == '' :
                    num = input("请输入有效的任务序号：(序号需要大于3)")
                message = tasklist[int(num) - 2]  
                
                send_message(client_socket, "Q：" + message)
                if message == 'END':
                    break
                
            elif command.startswith('i'):
                send_message(client_socket, SEND_IMAGE)
                
                if longscreenshot_flag:
                    capture_longscreenshot(image_path)
                else:
                    capture_screenshot(image_path)
                send_image(client_socket, image_path)

            elif command.startswith('r'):
                send_message(client_socket, SEND_RESET_GPT_HISTORY)
                continue

            elif command == 'END':
                break
            else:
                print("无效的命令")
                continue
            
            response = client_message_queue.get()
            print(f"收到服务器回复: {response}")
            if response == "图片已接收并存储":
                response = client_message_queue.get()
                print(f"收到服务器回复: {response}")

                if isinstance(response, str):
                    print("response 是字符串类型")
                elif isinstance(response, list):
                    # print(f"order_list: {response}")
                    order_list = response
                    operator(order_list)  # 传递服务器返回的order_list中的每个操作
                    # for order in order_list:
                    #     taped_element_content = order['button_content']
                    
                else:
                    print("response 是其他类型")

    except ConnectionRefusedError:

        print("无法连接到服务器，请检查服务器是否运行。")
    except Exception as e:

        print(f"client_main发生异常: {str(e)}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    client_main()
        