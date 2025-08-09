from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header  # 添加Header解决编码问题
from email.utils import formataddr  # 添加formataddr解决发件人格式问题
from Base.basePath import BasePath as BP
from Base.utils import read_config_ini, make_zip


class HandleEmail:

    def __init__(self):
        config = read_config_ini(BP.CONFIG_FILE)
        email_config = config['邮件发送配置']
        self.host = email_config['host']
        self.port = int(email_config['port'])
        self.send_email = email_config['send_email']
        self.receiver = eval(email_config['receiver'])
        self.pwd = (email_config['pwd'])
        self.sender_name = (email_config['sender'])  # 改为sender_name
        self.subject = (email_config['subject'])

    def add_test(self, text):
        """
        添加文本内容
        """
        return MIMEText(text, "plain", "utf-8")

    def add_accessory(self, file_path):
        """
        添加邮件的附件，附件路径为file_path
        """
        res = MIMEText(open(file_path, 'rb').read(), "base64", "utf-8")
        res.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        return res

    def add_subject_attch(self, attach_info: tuple, send_date=None):
        """
        给邮件添加主题，发件人，收件人
        :param attach_info:附件的内容
        :param send_date:发送的日期
        :return:
        """
        msg = MIMEMultipart('mixed')
        # 使用Header解决主题编码问题
        msg['subject'] = Header(self.subject, 'utf-8')
        # 使用formataddr正确格式化发件人
        msg['From'] = formataddr((self.sender_name, self.send_email))
        # 使用逗号分隔多个收件人
        msg['To'] = ','.join(self.receiver)
        if send_date:
            msg['Date'] = send_date
        else:
            msg['Date'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        if isinstance(attach_info, tuple):
            for i in attach_info:
                msg.attach(i)
        return msg

    def send_email_oper(self, msg):
        """
        发送邮件
        msg: 需要发送的内容
        """
        try:
            # 根据端口选择合适的加密方式
            if self.port == 465:
                smtp = smtplib.SMTP_SSL(self.host, self.port)
            else:
                smtp = smtplib.SMTP(self.host, self.port)
                smtp.starttls()  # 启用加密传输

            smtp.login(self.send_email, self.pwd)
            smtp.sendmail(self.send_email, self.receiver, msg.as_string())
            send_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            print(f"{self.send_email}给{self.receiver}发送邮件成功，发送时间：{send_time}")
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
            raise
        finally:
            # 确保安全关闭连接
            try:
                smtp.quit()
            except:
                pass

    def send_public_email(self, send_date=None, text='', file_type='ALLURE'):
        """
        邮件发送公共方法
        :param send_date: 发送时间
        :param text: 文本信息
        :param file_type: 测试报告的格式，ALLURE，HTML，XML
        :return:
        """
        attach_info = []
        text_plain = self.add_test(text=text)
        attach_info.append(text_plain)
        if file_type == 'ALLURE':
            allure_zip = make_zip(BP.ALLURE_REPORT_DIR, os.path.join(BP.ALLURE_REPORT_DIR, 'allure.zip'))
            file_attach = self.add_accessory(file_path=allure_zip)
            attach_info.append(file_attach)
        elif file_type == 'HTML':
            file_attach = self.add_accessory(file_path=os.path.join(BP.REPORTS_HTML_DIR, 'auto_reports.html'))
            attach_info.append(file_attach)
        elif file_type == 'XML':
            file_attach = self.add_accessory(file_path=os.path.join(BP.REPORTS_XML_DIR, 'auto_reports.xml'))
            attach_info.append(file_attach)
        attach_info = tuple(attach_info)
        msg = self.add_subject_attch(attach_info=attach_info, send_date=send_date)
        self.send_email_oper(msg=msg)


if __name__ == '__main__':
    text = '本邮件由系统自动发出，无需回复！\n各位同事，大家好，以下为本次测试报告!'
    email_sender = HandleEmail()
    email_sender.send_public_email(send_date=None, text=text, file_type='HTML')