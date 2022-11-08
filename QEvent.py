import DBQE
from MyDates import MyDates

class QEvent():

    labels=["Date","Fin","Nom","Location"]

    def __init__(self,start=MyDates.today(),end=MyDates.tomorrow(),name="Nom",location="Emplacement",id=None):
        self.start=start
        self.end=end
        self.name=name
        self.location=location
        self.id=id

    #Return list of labels as str    
    @classmethod
    def get_labels(cls):
        return cls.labels

    @classmethod
    def new_from_tuple(cls,event):
        return cls(MyDates.new_from_gui(event[1]),MyDates.new_from_gui(event[2]),event[3],event[4],event[0])

    @classmethod
    def get_next_x(cls):
        x="10"
        today=MyDates.now().strftime("%Y-%m-%d %H-%M-%S")
        return cls._tuple_to_QE(DBQE.get_next_x_db(today,x))

    @classmethod
    def _tuple_to_QE(cls,events_lst):
        agenda=[]
        for event in events_lst:
            print("event")
            agenda.append(cls(MyDates.new_from_sql(event[1]),MyDates.new_from_sql(event[2]),event[3],event[4],event[0]))
        return agenda
    
    @classmethod
    def get_all(cls):
        return cls._tuple_to_QE(DBQE.get_all_db())


    def __str__(self):
        qe_str="{} at {} from {} to {}"
        return(qe_str.format(self.name,self.location,self.start,self.end))

    def __iter__(self):
        return self._gen_QE()
    
    def _gen_QE(self):
        yield self.start
        yield self.end
        yield self.name
        yield self.location

    def _tuple(self):
        if self.id==None:
            return tuple((self.start.strftime("%Y-%m-%d %H-%M-%S"),self.end.strftime("%Y-%m-%d %H-%M-%S"),self.name,self.location))
        else:
            return tuple((self.start.strftime("%Y-%m-%d %H-%M-%S"),self.end.strftime("%Y-%m-%d %H-%M-%S"),self.name,self.location,self.id))


    #get methods for QEvent
    def get_id(self):
        return self.id
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_name(self):
        return self.name
    def get_location(self):
        return self.location

    #set methods for QEvent
    def set_id(self,id):
        self.id=id
    def set_start(self,start):
        self.start=start
    def set_end(self,end):
        self.end=end
    def set_name(self,name):
        self.name=name
    def set_location(self,location):
        self.location=location

    
#save new event in DB and get proper id
    def save(self):
        return DBQE.commit_to_db(self._tuple())

    def update(self):
        return DBQE.update_db(self._tuple())
    
    def delete(self):
        return DBQE.delete_from_db(self.id)






