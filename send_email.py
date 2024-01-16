class EmailSender:
    pass
    # with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
    #     connection.starttls()
    #     result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
    #     connection.sendmail(
    #         from_addr=YOUR_EMAIL,
    #         to_addrs=YOUR_EMAIL,
    #         msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
    #     )
