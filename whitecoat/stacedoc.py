# Import smtplib for the actual sending function
import smtplib
from config import *

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def sendemail():
  COMMASPACE = ', '
  # Create the container (outer) email message.
  html =("""\
  <html>
    <head>
      <title></title>
    </head>
    <body>
    <p><span class="sg-image" data-imagelibrary="%7B%22width%22%3A%22480%22%2C%22height%22%3A%22360%22%2C%22alignment%22%3A%22center%22%2C%22border%22%3A%22%22%2C%22src%22%3A%22https%3A//scontent.fsnc1-1.fna.fbcdn.net/hphotos-frc3/v/t1.0-9/941452_10151639299760862_1484269825_n.jpg%3Foh%3Da7b75af00133013b5aa8e5350e6f5074%26oe%3D566EFFBE%22%2C%22alt_text%22%3A%22%22%2C%22classes%22%3A%7B%22sg-image%22%3A1%7D%7D" style="float: none; display: block; text-align: center;"><img height="360" src="https://scontent.fsnc1-1.fna.fbcdn.net/hphotos-frc3/v/t1.0-9/941452_10151639299760862_1484269825_n.jpg?oh=a7b75af00133013b5aa8e5350e6f5074&amp;oe=566EFFBE" style="width: 480px; height: 360px;" width="480" /></span></p>

    <p style="text-align: center;">If you have anything to update STACE on today, 
      <span style="font-size:18px; font-family:tahoma,geneva,sans-serif;">
        <a href="{}">Edit it here!</a>
        <a href="{}">
        {}</a>
        </span></span>
    </p>

    </body>
    </html>
  """).format(STACEDOC_URL,STACEDOC_URL,STACEDOC_URL)
  msg = MIMEMultipart()
  part2 = MIMEText(html, 'html')
  msg.attach(part2)
  today = str(datetime.now().strftime('%A, %b %d'))
  msg['Subject'] = 'STACEDoc Alert for %s' % today
  # me == the sender's email address
  # family = the list of all recipients' email addresses
  FROMADDR = "%s <%s>" % ("Eunice", "eunicekokor@gmail.com")
  friend_array = FRIENDS.split(",")
  msg['To'] = COMMASPACE.join(friend_array)
  msg.preamble = 'If you have anything to update STACE on, edit the doc!'

  # # Assume we know that the image files are all in PNG format
  # for file in pngfiles:
  # # Open the files in binary mode.  Let the MIMEImage class automatically
  # # guess the specific image type.
  #     fp = open(file, 'rb')
  #     img = MIMEImage(fp.read())
  #     fp.close()
  #     msg.attach(img)

  # Send the email via our own SMTP server.
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.set_debuglevel(1)
  server.ehlo()
  server.starttls()
  server.login(LOGIN, PASSWORD)
  server.sendmail(FROMADDR, FRIENDS, msg.as_string())
  server.quit()

sendemail()
