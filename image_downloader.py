import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google_images_download import google_images_download
import tkinter as tk
from tkinter import messagebox

def download_images(keywords, limit):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": keywords,
        "limit": limit,
        "print_urls": True,
        "format": "jpg"
    }
    paths = response.download(arguments)
    return paths

def send_email(recipient_email, subject, body, image_paths):
    # Set your email and password here
    sender_email = "karora22_be22@thapar.edu"
    sender_password = "9464022209"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach images
    for path in image_paths:
        for image in image_paths[path]:
            if os.path.exists(image):
                attachment = open(image, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image)}')
                msg.attach(part)
                attachment.close()

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        messagebox.showinfo("Success", "Images sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")

def on_submit():
    keywords = entry_keywords.get()
    limit = entry_limit.get()
    email = entry_email.get()  # Make sure this is defined before use

    if not keywords or not limit.isdigit() or not email:
        messagebox.showerror("Input Error", "Please fill all fields correctly.")
        return

    limit = int(limit)
    paths = download_images(keywords, limit)
    
    # Send email with images
    send_email(email, "Your Requested Images", f"Here are the images for: {keywords}", paths)

# Setting up the GUI
root = tk.Tk()
root.title("Google Image Downloader")

tk.Label(root, text="Enter Keywords:").grid(row=0, column=0)
entry_keywords = tk.Entry(root)
entry_keywords.grid(row=0, column=1)

tk.Label(root, text="Number of Images:").grid(row=1, column=0)
entry_limit = tk.Entry(root)
entry_limit.grid(row=1, column=1)

tk.Label(root, text="Your Email:").grid(row=2, column=0)
entry_email = tk.Entry(root)  # Define entry_email here
entry_email.grid(row=2, column=1)

submit_button = tk.Button(root, text="Download and Send", command=on_submit)
submit_button.grid(row=3, columnspan=2)

root.mainloop()
