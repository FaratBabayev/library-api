def notify(kind, title="", email="", send=True):
    if not send:
        return

    if kind == "checkout":
        subject = "Book checked out"
        body = "You checked out " + title
    elif kind == "renew":
        subject = "Loan renewed"
        body = "You renewed " + title
    else:
        subject = "Library notice"
        body = title

    with open("outbox.txt", "a") as f:
        f.write(
            "TO: " + email +
            " | SUBJECT: " + subject +
            " | BODY: " + body + "\n"
        )
def notify_return(email, title, fine):
    with open("outbox.txt", "a") as f:
        f.write(
            "TO: " + email +
            " | SUBJECT: Book returned | BODY: You returned " + title +
            ". Fine: $" + str(round(float(fine), 2)) + "\n"
        )

def notify_fine_paid(email, amount):
    with open("outbox.txt", "a") as f:
        f.write(
            "TO: " + email +
            " | SUBJECT: Fine paid | BODY: We received $" +
            str(round(float(amount), 2)) + "\n"
        )