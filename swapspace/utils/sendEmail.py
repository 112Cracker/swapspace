from django.core.mail import send_mail

from swapspace.settings import EMAIL_FROM

from user.models import EmailRecord
import random

HOST = "http://74739114.ngrok.io"
def generateRandomCode(codeLength=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    randCode = ''
    for i in range(codeLength):
        randomIndex = random.randint(0, length)
        randCode += chars[randomIndex]

    return randCode


def sendEmail(email_to, sendType='register', requestMsg=''):
    randCode = generateRandomCode(12)

    emailRecord = EmailRecord(code=randCode, email=email_to, sendType=sendType)
    emailRecord.save()

    if sendType == 'register':
        print("Sending a registration email for user account activation.")
        subject = 'SwapSpace Registration Activation Link'
        body = """Please click the link below to activate your account:\n
               {0}/activate/{1}
               """.format(HOST, randCode)

        status = send_mail(subject, body, EMAIL_FROM, [email_to])
        if status:
            print('Registration password email sent successfully')
            pass

    elif sendType == 'forget':
        print("Sending a reset-pwd email to: %s"%(email_to))
        subject = 'SwapSpace Forget Password Reset Link'
        body = """Please click the link below to reset your account password:\n
               {0}/reset/{1}
               """.format(HOST, randCode)

        status = send_mail(subject, body, EMAIL_FROM, [email_to])
        if status:
            print('Reset password email sent successfully')
            pass

    elif sendType == 'request':
        print("Sending an email to notify user of an incoming request.")
        subject = 'Your SwapSpace item has been Requested for exchange! Come back to ACCEPT!'
        body = requestMsg
        # need to add link
        status = send_mail(subject, body, EMAIL_FROM, [email_to])
        if status:
            print('Request item email sent successfully')
            pass

    elif sendType == 'accept':
        print("Sending an email to notify user of newly accepted request. ")
        subject = 'Your SwapSpace item exchange request has been Accepted! Come back to CONFIRM!'
        body = requestMsg
        # need to add link
        status = send_mail(subject, body, EMAIL_FROM, [email_to])
        if status:
            print('Accept item email sent successfully')
            pass

    elif sendType == 'confirm':
        print("Sending an email to notify user of newly confirmed request.")
        subject = 'Your SwapSpace item exchange request has been Confirmed! Come back to RATE this exchange!'
        body = requestMsg
        # need to add link
        status = send_mail(subject, body, EMAIL_FROM, [email_to])
        if status:
            print('Confirm item email sent successfully')
            pass

    elif sendType == 'cancel':
        print("Sending an email to notify user of newly cancelled exchange.")
        subject = 'Your SwapSpace item exchange request has been Cancelled.'
        body = requestMsg
        status = send_mail(subject, body, EMAIL_FROM, [email_to])
        if status:
            print('Request item email sent successfully')
            pass
