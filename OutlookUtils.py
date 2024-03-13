import win32com.client as win32
from datetime import datetime


class OutlookUtils:
    """outlook工具类"""
    mapi = None
    mapi = None
    account = None
    SORT_BY = {
        "Subject": "[Subject]",  # 邮件主题
        "From": "[From]",  # 发件人
        "To": "[To]",  # 收件人
        "CC": "[CC]",  # 抄送
        "BCC": "[BCC]",  # 密送
        "Size": "[Size]",  # 邮件大小
        "Importance": "[Importance]",  # 重要性（高、低）
        # 敏感性（Normal、Personal、Private、Confidential）
        "Sensitivity": "[Sensitivity]",
        "Date": "[Date]",  # 发送日期
        "ReceivedTime": "[ReceivedTime]",  # 接收日期和时间
        "Unread": "[Unread]",  # 是否未读
    }
    EMAIL_ATTRIBUTE = {
        "Subject": "Subject",  # 邮件主题
        "From": "SenderName",  # 发件人
        "To": "To",  # 收件人
        "CC": "CC",  # 抄送
        "BCC": "BCC",  # 密送
        "Size": "Size",  # 邮件大小
        "Body": "Body",  # 正文
        "Importance": "Importance",  # 重要性（高、低）
        "Sensitivity": "Sensitivity",  # 敏感性（Normal、Personal、Private、Confidential）
        "ReceivedTime": "ReceivedTime",  # 接收日期和时间
        "Attachments": "Attachments",  # 附件
    }

    def __init__(self, account: str = None) -> None:
        self.outlook = win32.Dispatch('outlook.application')
        self.mapi = self.outlook.GetNamespace('MAPI')
        if account is not None:
            self.account = account

    def login(self, account: str):
        """登录对应账号

        Args:
            account (str): 账号
        """
        self.account = account

    def get_local_accounts(self) -> list:
        """获取本地保存的outlook账号

        Returns:
            list: 本地保存的outlook账号列表
        """
        return [str(accounts) for accounts in self.mapi.Accounts]

    def get_outlook_folder(self) -> list:
        """获取对应账号的信箱

        Returns:
            list: 对应账号中所有信箱的列表
        """
        return [str(folder) for idx, folder in enumerate(self.mapi.Folders(self.account).Folders)]

    def get_the_last_email(self, folder_name: str) -> win32.CDispatch:
        """获取邮箱的最后一封邮件(一般最新的邮件都是在最后的)

        Args:
            folder_name (str): 信箱名

        Returns:
            win32.CDispatch: 对应的邮件
        """
        messages = self.mapi.Folders(self.account).Folders(folder_name).Items
        return messages.GetLast()

    def get_email_and_sort(self, folder_name: str, sort_by: str = "[ReceivedTime]", descending: bool = True, return_number: int = 10) -> list:
        """按照一定的规则排列邮件并返回

        Args:
            folder_name (str): 信箱名
            sort_by (str, optional): 排列规则. Defaults to "[ReceivedTime]".
            descending (bool, optional): 排列顺序,为True则从高到底. Defaults to True.
            return_number (int, optional): 返回的邮件数量. Defaults to 10.

        Returns:
            list: 对应的邮件列表
        """
        messages = self.mapi.Folders(self.account).Folders(folder_name).Items
        messages.Sort(sort_by, Descending=descending)
        if len(messages) < return_number:
            return list(messages)
        else:
            return list(messages)[:return_number]

    def get_email_by(self, folder_name: str, pattern: str, by: str = "Subject", fuzzy_query: bool = True, received_time_pattern: str = None) -> list:
        """按照一定的规则搜索邮件

        Args:
            folder_name (str): 信箱名
            pattern (str): 搜索邮件的规则
            by (str, optional): 按什么来搜索. Defaults to "Subject".
            fuzzy_query (bool, optional): 是否为模糊搜索. Defaults to True.
            received_time_pattern (str, optional): 在参数'by'是ReceivedTime时,邮件的收信时间以什么模式转换并匹配. Defaults to None.

        Returns:
            list: 搜索后的邮件
        """
        messages = self.mapi.Folders(self.account).Folders(folder_name).Items
        messages.Sort("[ReceivedTime]", Descending=True)
        search_list = []
        for email in messages:
            match by:
                case "Subject":
                    if fuzzy_query and pattern in email.Subject:
                        search_list.append(email)
                    elif pattern == email.Subject:
                        search_list.append(email)
                case "SenderName":
                    if fuzzy_query and pattern in email.SenderName:
                        search_list.append(email)
                    elif pattern == email.SenderName:
                        search_list.append(email)
                case "To":
                    if fuzzy_query and pattern in email.To:
                        search_list.append(email)
                    elif pattern == email.To:
                        search_list.append(email)
                case "CC":
                    if fuzzy_query and pattern in email.CC:
                        search_list.append(email)
                    elif pattern == email.CC:
                        search_list.append(email)
                case "BCC":
                    if fuzzy_query and pattern in email.BCC:
                        search_list.append(email)
                    elif pattern == email.BCC:
                        search_list.append(email)
                case "Size":
                    if pattern == email.Size:
                        search_list.append(email)
                case "Body":
                    if fuzzy_query and pattern in email.Body:
                        search_list.append(email)
                    elif pattern == email.Body:
                        search_list.append(email)
                case "Importance":
                    if pattern == email.Importance:
                        search_list.append(email)
                case "Sensitivity":
                    if pattern == email.Sensitivity:
                        search_list.append(email)
                case "ReceivedTime":
                    if fuzzy_query and pattern in str(email.ReceivedTime):
                        search_list.append(email)
                    elif pattern == datetime.strptime(str(email.ReceivedTime), "%Y-%m-%d %H:%M:%S.%f%z").strftime(received_time_pattern):
                        search_list.append(email)
                case "Attachments":
                    if fuzzy_query and pattern in [attachment.FileName for attachment in email.Attachments]:
                        search_list.append(email)
                    elif pattern is [attachment.FileName for attachment in email.Attachments]:
                        search_list.append(email)
                case _:
                    if fuzzy_query and pattern in str(email):
                        search_list.append(email)
                    elif pattern == str(email):
                        search_list.append(email)
        return search_list

    def get_email_info(self, email: win32.CDispatch, attribute: str = "Subject") -> str | int | list:
        """获取邮件信息

        Args:
            email (win32.CDispatch): 邮件
            attribute (str, optional): 邮件属性. Defaults to "Subject".

        Returns:
            str|int|list: 邮件对应信息
        """
        match attribute:
            case "Subject":
                return email.Subject
            case "SenderName":
                return email.SenderName
            case "To":
                return email.To
            case "CC":
                return email.CC
            case "BCC":
                return email.BCC
            case "Size":
                return email.Size
            case "Body":
                return email.Body
            case "Importance":
                return email.Importance  # int
            case "Sensitivity":
                return email.Sensitivity  # int
            case "ReceivedTime":
                return datetime.strptime(str(email.ReceivedTime), "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S")
            case "Attachments":
                return [attachment.FileName for attachment in email.Attachments]
            case _:
                return str(email)

    def send_email(self, subject: str, body: str, recipients: list, cc_recipients: list = None, attachment_paths: list = None, resolve_all_recipients=False, display_mail=False):
        """发送邮件

        Args:
            subject (str): 主题
            body (str): 邮件正文
            recipients (list): 收件人列表
            cc_recipients (list, optional): 抄送人列表. Defaults to None.
            attachment_paths (list, optional): 附件列表. Defaults to None.
            resolve_all_recipients (bool, optional): 是否解析所有收件人. Defaults to False.
            display_mail (bool, optional): 是否显示邮件. Defaults to False.
        """
        mail = self.outlook.CreateItem(0)  # 0 表示创建邮件
        mail.Subject = subject
        mail.Body = body
        for recipient in recipients:
            mail.Recipients.Add(recipient)
        if cc_recipients:
            for cc in cc_recipients:
                recipient = mail.Recipients.Add(cc)
                recipient.Type = 2  # 设置收件人类型为抄送(CC)
        if attachment_paths:
            for attachment_path in attachment_paths:
                mail.Attachments.Add(attachment_path)
        if resolve_all_recipients:
            # 解析所有收件人
            mail.Recipients.ResolveAll()
        if display_mail:
            # 显示邮件
            mail.Display()
        mail.Send()
