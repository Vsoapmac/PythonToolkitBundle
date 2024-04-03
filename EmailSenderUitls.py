"""邮件工具类 EmailSenderUitls"""
import smtplib, os, traceback
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders


def send_text_email(sender: str, sender_password: str, receiver_list: list, CC_list: list,
                    title: str, content: str, smtp_server: str, smtp_port: int, start_tls: bool=True):
    """发送纯文本邮件

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件
        CC_list (list): 抄送人邮件列表, 为空列表则不抄送
        title (str): 邮件标题
        content (str): 邮件正文内容
        smtp_server (str): 邮件发送的服务器
        smtp_port (int, optional): 邮件发送的端口
        start_tls (bool, optional): 是否启用TLS加密. Defaults to True.
    """
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = ','.join(receiver_list)
    message['Cc'] = ','.join(CC_list)
    message['Subject'] = Header(title, 'utf-8')

    try:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        if start_tls:
            smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.sendmail(sender, receiver_list, message.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        raise Exception(f"Send email fail", traceback.format_exc(e))

def send_html_email(sender: str, sender_password: str, receiver_list: list, CC_list: list,
                    title: str, content_html: str, smtp_server: str, smtp_port: int, start_tls: bool=True):
    """发送HTML格式邮件

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件
        CC_list (list): 抄送人邮件列表, 为空列表则不抄送
        title (str): 邮件标题
        content_html (str): 邮件正文内容, HTML格式, 这会在邮件上显示对应的格式
        smtp_server (str): 邮件发送的服务器
        smtp_port (int, optional): 邮件发送的端口
        start_tls (bool, optional): 是否启用TLS加密. Defaults to True.
    """
    message = MIMEText(content_html, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = ','.join(receiver_list)
    message['Cc'] = ','.join(CC_list)
    message['Subject'] = Header(title, 'utf-8')

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        if start_tls:
            smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.sendmail(sender, receiver_list, message.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        raise Exception(f"Send email fail, {traceback.format_exc(e)}")

def send_email_with_embedded_images(sender: str, sender_password: str, receiver_list: list, CC_list: list,
                    title: str, content_html: str, smtp_server: str, image_paths: list, 
                    smtp_port: int, start_tls: bool=True):
    """发送HTML格式邮件, 并在文章中内嵌图片

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件
        CC_list (list): 抄送人邮件列表, 为空列表则不抄送
        title (str): 邮件标题
        content_html (str): 邮件正文内容, HTML格式, 这会在邮件上显示对应的格式
        smtp_server (str): 邮件发送的服务器
        image_paths (list): 图片的路径列表, 图片会被内嵌到邮件中
        smtp_port (int, optional): 邮件发送的端口
        start_tls (bool, optional): 是否启用TLS加密. Defaults to True.
        
    Example:
        >>> sender = 'your_email@example.com' # 发送人邮件地址
        >>> sender_password = 'your_password' # 发送人邮件密码或授权码, 请替换为实际值
        >>> receiver_list = ['receiver1@example.com', 'receiver2@example.com'] # 接收人邮件列表, 请替换为实际值
        >>> CC_list = ['cc1@example.com', 'cc2@example.com'] # 抄送人邮件列表, 为空列表则不抄送, 请替换为实际值
        >>> title = 'Test Email with Embedded Images' # 邮件标题, 请替换为实际值
        >>> smtp_server = 'smtp.example.com' # 邮件发送的服务器, 请替换为实际值
        >>> image_paths = ['path/to/image1.jpg', 'path/to/image2.jpg'] # 图片路径列表
        >>> smtp_port = 999 # 邮件发送的端口, 请替换为实际值
        >>> # 邮件正文内容, HTML格式, 这会在邮件上显示对应的格式, 使用内嵌图片时加入<img src="cid:图片文件名.png" alt="alt名">在文章内, 会在文章中显示对应的图片, 请替换为实际值
        >>> content_html = '''<p>This is a test email with embedded images.</p><img src="cid:image1.png" alt="Image 1"><img src="cid:image2.png" alt="Image 2">''' 
        >>> send_email_with_embedded_images(sender, sender_password, receiver_list, CC_list, title, content_html, smtp_server, image_paths)
    """
    # 设置邮件内容
    message = MIMEMultipart('related')
    message['From'] = sender
    message['To'] = ','.join(receiver_list)
    message['Cc'] = ','.join(CC_list)
    message['Subject'] = Header(title, 'utf-8')

    # 添加 HTML 正文
    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)
    msg_alternative.attach(MIMEText(content_html, 'html', 'utf-8'))
    
    # 为每个图片创建一个 MIME image 对象，并将其添加到邮件中
    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            img_data = f.read()
        # 获取图片文件名作为 CID (Content ID)
        image_name = os.path.basename(image_path)
        cid = '<' + image_name + '>'
        # 创建一个 MIME image 对象并设置相应的 headers
        img = MIMEImage(img_data)
        img.add_header('Content-ID', cid)
        img.add_header('Content-Disposition', 'inline', filename=image_name)
        # 将 MIME image 对象添加到邮件中
        message.attach(img)

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        if start_tls:
            smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.sendmail(sender, receiver_list, message.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        raise Exception(f"Send email fail, {traceback.format_exc(e)}")

def send_html_with_attachment(sender: str, sender_password: str, receiver_list: list, CC_list: list,
                    title: str, content_html: str, smtp_server: str, file_path_list: list, 
                    smtp_port: int, start_tls: bool=True):
    """发送HTML格式邮件, 并附带附件

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件
        CC_list (list): 抄送人邮件列表, 为空列表则不抄送
        title (str): 邮件标题
        content_html (str): 邮件正文内容, HTML格式, 这会在邮件上显示对应的格式
        smtp_server (str): 邮件发送的服务器
        file_path_list (list): 附件的路径列表, 附件会被附带在邮件中
        smtp_port (int, optional): 邮件发送的端口
        start_tls (bool, optional): 是否启用TLS加密. Defaults to True.
    """
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ','.join(receiver_list)
    message['Cc'] = ','.join(CC_list)
    message['Subject'] = Header(title, 'utf-8')
    message.attach(MIMEText(content_html, 'html', 'utf-8'))
    
    # 遍历所有附件并添加到邮件中
    for file_path in file_path_list:
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
        message.attach(part)
    
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        if start_tls:
            smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.sendmail(sender, receiver_list, message.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        raise Exception(f"Send email fail, {traceback.format_exc(e)}")

def send_email_with_embedded_images_and_attachments(sender: str, sender_password: str, receiver_list: list, CC_list: list,
                    title: str, content_html: str, smtp_server: str, file_path_list: list, image_paths: list, 
                    smtp_port: int, start_tls: bool=True):
    """发送HTML格式邮件, 并在文章中内嵌图片且附带附件

    Args:
        sender (str): 发送人邮件
        sender_password (str): 发送人邮件的密码或授权码
        receiver_list (list): 接收人邮件
        CC_list (list): 抄送人邮件列表, 为空列表则不抄送
        title (str): 邮件标题
        content_html (str): 邮件正文内容, HTML格式, 这会在邮件上显示对应的格式
        smtp_server (str): 邮件发送的服务器
        file_path_list (list): 附件的路径列表, 附件会被附带在邮件中
        image_paths (list): 图片的路径列表, 图片会被内嵌到邮件中
        smtp_port (int, optional): 邮件发送的端口
        start_tls (bool, optional): 是否启用TLS加密. Defaults to True.
    """
    # 创建邮件的根部分
    message = MIMEMultipart('mixed')
    message['From'] = sender
    message['To'] = ','.join(receiver_list)
    message['Cc'] = ','.join(CC_list)
    message['Subject'] = Header(title, 'utf-8')

    # 添加包含 HTML 和内嵌图片的邮件部分
    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)

    # 添加 HTML 正文
    msg_alternative.attach(MIMEText(content_html, 'html', 'utf-8'))

    # 添加内嵌图片
    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            img_data = f.read()
        image_name = os.path.basename(image_path)
        cid = '<' + image_name + '>'
        img = MIMEImage(img_data, name=image_name)
        img.add_header('Content-ID', cid)
        msg_alternative.attach(img)

    # 遍历所有附件并添加到邮件中
    for file_path in file_path_list:
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_name}')
        message.attach(part)

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        if start_tls:
            smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.sendmail(sender, receiver_list, message.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        raise Exception(f"Send email fail, {traceback.format_exc(e)}")
