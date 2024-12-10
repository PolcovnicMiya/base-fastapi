import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.configuration.setting import Environments
from src.infrastructure.smtp.ports import (
    VerifyEmailSMTPRepositoryPort
)
#https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_Dab-G9c5c9tfXkctraPU2wxfC4LmxJ1STQ&s
#https://i.ytimg.com/vi/TANftn7RnuI/hqdefault.jpg
class VerifyEmailSMTPRepositoryAdapter(VerifyEmailSMTPRepositoryPort):
    async def send_verify_code(self, to: str, code: str) -> None:
        print(code)
        html = f"""
        <html>
            <body style="text-align: center;">
                <p><img src="https://i.ytimg.com/vi/TANftn7RnuI/hqdefault.jpg" width="400" height="400" alt="Verification Image"></p>
                <h2>Verification Code</h2>
                <p>Dear user,</p>
                <p>Your verification code is:</p>
                <h3>{code}</h3>
                <p>Please use this code to verify your email address.</p>
                <p>Thank you!</p>
                <br>
                <p>Best regards,</p>
                <p>The ChronoAI Team</p>
            </body>
        </html>
        """
        msg = MIMEMultipart()
        msg['From'] = Environments().smtp.SMTP_EMAIL
        msg['To'] = to
        msg['Subject'] = "Verification code"
        msg.attach(MIMEText(_text=html, _subtype='html', _charset='utf-8'))

        server = smtplib.SMTP(
            Environments().smtp.SMTP_HOST,
            Environments().smtp.SMTP_PORT
        )
        server.starttls()
        server.login(
            user=Environments().smtp.SMTP_EMAIL,
            password=Environments().smtp.SMTP_PASSWORD
        )
        server.send_message(msg=msg)
        server.quit()




