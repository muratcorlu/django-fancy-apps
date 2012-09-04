class MailingList(models.Model):
    name = models.CharField(blank=True, max_length=100)
    create_date = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __unicode__(self):
        return u"MailingList"

class Newsletter(models.Model):
    title = models.CharField(blank=True, max_length=100)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return u"Newsletter"

class Subscriber(models.Model):
    list = models.ForeignKey(MailingList)

    def __unicode__(self):
        return u"Subscriber"
