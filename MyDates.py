import datetime

class MyDates(datetime.datetime):

    @classmethod
    def tomorrow(cls):
        return cls.today()+datetime.timedelta(days=1)

    @classmethod
    def new_from_sql(cls,str):
        return cls.strptime(str,"%Y-%m-%d %H-%M-%S")

    @classmethod
    def new_from_gui(cls,str,hour,min):
        date=cls.strptime(str,"%d-%m-%y")
        return date.replace(hour=hour,minute=min)

    @classmethod
    def new_from_gdate(cls,tuple):
        return cls(tuple[0],tuple[1]+1,tuple[2])

    #return date as str
    def get_date(self):
        return self.strftime("%d-%m-%y")

    def __str__(self):
        return self.strftime("%d %B %Y %H:%M")
