
from src.configuration.setting import Environments


print(Environments().smtp.SMTP_EMAIL,Environments().smtp.SMTP_HOST,Environments().smtp.SMTP_PASSWORD,Environments().smtp.SMTP_PORT)