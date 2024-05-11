import smtplib
import random


def send_otp():
    from new import user_email
    random_num = random.randint(1000, 9999)
    sender_email = "sdsystems52024@gmail.com"
    rec_email = str(user_email)
    password = str("cnse rube mnho hjpx")
    message = "Your OTP is " + str(random_num)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, rec_email, message)
    print("email sent to ", rec_email)
    return str(random_num)