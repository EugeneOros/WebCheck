import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def create_message(price, link):
    return "<h1>Hey!\n Price of one of your monitored items has dropped below the maximal_price you've set!\n</h1>" \
           "<h4>Price of this item: <a href=" + str(link) +"> click!</a> is now " + str(price) + ".\n\n\n</h4>" \
            "To unsubscribe this link remove it from your monitored items list. \n " \
            "This message was generated automatically by 'WebCheck'"


def send_email(email_to, link, price):
    messageHTML = create_message(price, link)
    messagePlain = 'Changes were found To check click here'
    message = MIMEMultipart('alternative')
    message['From'] = 'my.pro9ram@gmail.com'
    message['To'] = email_to
    message['Subject'] = "Price of one of monitored items changed!"

    message.attach(MIMEText(messagePlain, 'plain'))
    message.attach(MIMEText(messageHTML, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('my.pro9ram@gmail.com', '<myProgram>')
    text = message.as_string()
    server.sendmail('my.pro9ram@gmail.com', email_to, text)
    server.close()


if __name__ == "__main__":
    send_email( "oogyano@gmail.com", "https://allegro.pl/oferta/apple-iphone-8-64gb-wybor-kolorow-gratisy-7857564686?bi_m=mpage&", 200.0)
