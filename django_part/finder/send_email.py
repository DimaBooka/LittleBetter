import smtplib


def send_email():
    """

    Sends emails in case something goes wrong.

    """
    smtpObj = smtplib.SMTP('smtp.rambler.ru', 587)
    smtpObj.starttls()
    smtpObj.login('dimazarj2009@rambler.ru', 'samsung789')
    smtpObj.sendmail("dimazarj2009@rambler.ru", "dimazarj2009@rambler.ru", "REPAIR IT!!!")
    smtpObj.quit()
