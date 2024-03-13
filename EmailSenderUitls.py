"""邮件工具类 EmailSenderUitls"""
import smtplib,imghdr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import traceback


def sendEmail_Text(sender: str, sender_password: str, receiver_list: list, title: str, content: str, smtp_server: str) -> bool:
    """发送纯文本邮件

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件, 可以为多个, 用列表填充
        title (str): 邮件标题
        content (str): 邮件正文内容
        smtp_server (str): 邮件发送的服务器

    Returns:
       bool: 是否发送成功, 成功为True, 不成功为False
    """
    message = MIMEText(content, 'plain', 'utf-8')  # 发送内容 （文本内容, 发送格式, 编码格式）
    message['From'] = sender  # 发送地址
    message['To'] = ','.join(receiver_list)  # 接受地址
    message['Subject'] = Header(title, 'utf-8')  # 邮件标题

    try:
        smtp = smtplib.SMTP(smtp_server, 25)  # 创建SMTP对象
        smtp.starttls()  # 启用TLS加密
        smtp.login(sender, sender_password)  # 登录邮箱账号
        smtp.sendmail(sender, receiver_list, message.as_string())  # 发送账号信息
        return True
    except smtplib.SMTPException as e:
        traceback.print_exc(e)
        return False
    finally:
        smtp.quit()

def sendEmail_Html(sender: str, sender_password: str, receiver_list: list, title: str, content_html: str, smtp_server: str) -> bool:
    """发送HTML格式邮件, 强烈推荐用这个发送纯文本邮件

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件, 可以为多个, 用列表填充
        title (str): 邮件标题
        content_html (str): 邮件正文内容, HTML格式, 这会在邮件上显示格式
        smtp_server (str): 邮件发送的服务器

    Returns:
        bool: 是否发送成功, 成功为True, 不成功为False
    """
    message = MIMEText(content_html, 'html', 'utf-8')  # 发送内容 （文本内容, 发送格式, 编码格式）
    message['From'] = sender  # 发送地址
    message['To'] = ','.join(receiver_list)  # 接受地址
    message['Subject'] = Header(title, 'utf-8')  # 邮件标题

    try:
        smtp = smtplib.SMTP(smtp_server, 25)  # 创建SMTP对象
        smtp.starttls()  # 启用TLS加密
        smtp.login(sender, sender_password)  # 登录邮箱账号
        smtp.sendmail(sender, receiver_list, message.as_string())  # 发送账号信息
        return True
    except smtplib.SMTPException as e:
        traceback.print_exc(e)
        return False
    finally:
        smtp.quit()

def sendEmail_file(sender: str, sender_password: str, receiver_list: list, title: str, content_html: str, file_path_list: list, file_name_list: list, smtp_server: str) -> bool:
    """发送HTML格式邮件, 并带上附件

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件, 可以为多个, 用列表填充
        title (str): 邮件标题
        content_html (str): 邮件正文内容, HTML格式, 这会在邮件上显示格式
        file_path_list (list): 附件路径, 只是路径不包括附件名, 如src/main/, !!!必须用列表存!!!, eg.['src/main/','src/jar/']
        file_name_list (list): 附件名称, !!!必须用列表存!!!, 每个附件名称的下标与路径列表对应, eg.['1.txt','2.jar'], 与附件路径例子组合成src/main/1.txt；src/jar/2.jar
        smtp_server (str): 邮件发送的服务器

    Returns:
        bool: 是否发送成功, 成功为True, 不成功为False
    """
    message = MIMEMultipart()  # 创建一个带附件的实例
    message['From'] = sender  # 发送地址
    message['To'] = ','.join(receiver_list)  # 接受地址
    message['Subject'] = Header(title, 'utf-8')  # 邮件标题
    message.attach(MIMEText(content_html, 'html', 'utf-8'))  # 添加邮件正文内容

    i = 0
    while (i < len(file_path_list)):
        with open(file_path_list[i] + file_name_list[i], 'rb') as file:
            if(imghdr.what(file_path_list[i] + file_name_list[i]) is not None):
                appendix = MIMEImage(file.read())
                appendix["Content-Type"] = 'application/octet-stream'  # 此处为固定的格式, 可以在浏览器中查看到相关信息
                appendix["Content-Disposition"] = f'attachment; filename="{file_name_list[i]}"'  # 这里的 filename 命名任意, 即在邮件中显示的名称
                message.attach(appendix)
            else:
                appendix = MIMEText(file.read(), 'base64', 'utf-8')  # 构造附件, 传送文件
                appendix["Content-Type"] = 'application/octet-stream'  # 此处为固定的格式, 可以在浏览器中查看到相关信息
                appendix["Content-Disposition"] = f'attachment; filename="{file_name_list[i]}"'  # 这里的 filename 命名任意, 即在邮件中显示的名称
                message.attach(appendix)  # 添加附件
            file.close()
        i = i + 1

    try:
        smtp = smtplib.SMTP(smtp_server, 25)  # 创建SMTP对象
        smtp.starttls()  # 启用TLS加密
        smtp.login(sender, sender_password)  # 登录邮箱账号
        smtp.sendmail(sender, receiver_list, message.as_string())  # 发送账号信息
        return True
    except smtplib.SMTPException as e:
        traceback.print_exc(e)
        return False
    finally:
        smtp.quit()

def sendEmail_image(sender: str, sender_password: str, receiver_list: list, title: str, content_html: str, file_path_list: list, file_name_list: list, image_path_list: list,
                    image_name_list: list, smtp_server: str) -> bool:
    """发送HTML格式邮件, 正文内嵌图片, 并带上附件。

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件, 可以为多个, 用列表填充
        title (str): 邮件标题
        content_html (str): 邮件正文内容, HTML格式, 这会在邮件上显示格式, 注意img标准中src格式为cid:xxx, xxx与形参image_name_list中的参数相同, 例如:<img src=\"cid:TestImage.jpg\"></p>, 那么image_name_list里面应该就有TestImage.jpg
        file_path_list (list): 附件路径, 只是路径不包括附件名, 如src/main/, !!!必须用列表存!!!, eg.['src/main/','src/jar/']
        file_name_list (list): 附件名称, !!!必须用列表存!!!, 每个附件名称的下标与路径列表对应, eg.['1.txt','2.jar'], 与附件路径例子组合成src/main/1.txt；src/jar/2.jar
        image_path_list (list): 图片路径, 只是路径不包括附件名, 如src/main/, !!!必须用列表存!!!, eg.['src/main/','src/jar/']
        image_name_list (list): 图片名称, !!!必须用列表存!!!, 每个附件名称的下标与路径列表对应, eg.['1.png','2.jpg'], 与附件路径例子组合成src/main/1.png；src/jar/2.jpg
        smtp_server (str): 邮件发送的服务器

    Returns:
        bool: 是否发送成功, 成功为True, 不成功为False
    """
    message = MIMEMultipart()  # 创建一个带附件的实例
    message['From'] = sender  # 发送地址
    message['To'] = ','.join(receiver_list)  # 接受地址
    message['Subject'] = Header(title, 'utf-8')  # 邮件标题
    message.attach(MIMEText(content_html, 'html', 'utf-8'))  # 添加邮件正文内容

    i = 0
    while (i < len(file_path_list)):
        with open(file_path_list[i] + file_name_list[i], 'rb') as file:
            appendix = MIMEText(file.read(), 'base64', 'utf-8')  # 构造附件, 传送文件
            appendix["Content-Type"] = 'application/octet-stream'  # 此处为固定的格式, 可以在浏览器中查看到相关信息
            appendix["Content-Disposition"] = f'attachment; filename="{file_name_list[i]}"'  # 这里的 filename 命名任意, 即在邮件中显示的名称
            message.attach(appendix)  # 添加附件
            file.close()
        i = i + 1

    i = 0
    while (i < len(image_path_list)):
        with open(image_path_list[i] + image_name_list[i], 'rb') as file:
            msgImage = MIMEImage(file.read())  # 添加图片附件
            msgImage.add_header('Content-ID', image_name_list[i])  # 这个id用于上面html获取图片
            message.attach(msgImage)
            file.close()
        i = i + 1

    try:
        smtp = smtplib.SMTP()  # 创建SMTP对象
        smtp.connect(smtp_server)  # 连接服务器
        smtp.login(sender, sender_password)  # 登录邮箱账号
        smtp.sendmail(sender, receiver_list, message.as_string())  # 发送账号信息
        return True
    except smtplib.SMTPException as e:
        traceback.print_exc(e)
        return False
    finally:
        smtp.quit()