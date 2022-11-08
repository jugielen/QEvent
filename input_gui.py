from types import NoneType
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
from gi.repository import GLib
from QEvent import QEvent
from MyDates import MyDates


class EditWindow(Gtk.Dialog):
    def __init__(self,parent,title,event):
        super().__init__(title=title,transient_for=parent,flags=0)
        #main_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        main_box=self.get_content_area()
        main_box.set_border_width(20)
        #self.add(main_box)
        self.name=Gtk.Entry()
        self.name.set_text(event.get_name())
        self.location=Gtk.Entry()
        self.location.set_text(event.get_location())
        self.StartDate=DateEntryBox(event.get_start(),"Début de l'évenement")
        self.EndDate=DateEntryBox(event.get_end(),"Fin de l'événement")
        main_box.pack_start(Gtk.Label(label="Nom de l'événement"),False,False,0)
        main_box.pack_start(self.name,False,False,0)
        main_box.pack_start(Gtk.Label(label="Emplacement"),False,False,0)
        main_box.pack_start(self.location,False,False,0)
        main_box.pack_start(self.StartDate,False,False,0)
        main_box.pack_start(self.EndDate,False,False,0)
        self._set_header_bar(title,event)
        self.show_all()

    def _set_header_bar(self,title,event):
        barre=Gtk.HeaderBar()
        barre.set_show_close_button(False)
        barre.set_title(title)
        self.set_titlebar(barre)
        
        confirm_button=Gtk.Button.new_from_icon_name("dialog-apply",Gtk.IconSize.MENU)
        cancel_button=Gtk.Button.new_from_icon_name("dialog-cancel",Gtk.IconSize.MENU)
        confirm_button.connect("clicked",self._on_confirm_clicked,event)
        cancel_button.connect("clicked",self._on_cancel_clicked)
        barre.pack_end(confirm_button)
        barre.pack_end(cancel_button)

    def _on_cancel_clicked(self,button):
        self.destroy()

    def _on_confirm_clicked(self,button,event):
        print("confirm cliked")
        self._get_entries(event)
        self.response(Gtk.ResponseType.OK)
        self.destroy()


    def _get_entries(self,event):
        event.set_name(self.name.get_text())
        event.set_location(self.location.get_text())
        event.set_start(self.StartDate.get_datetime())
        event.set_end=(self.EndDate.get_datetime())
        print(event)

    
class DateEntryBox(Gtk.Box):
    def __init__(self,date,label):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
        self.hour=self._set_hour_button(date.hour)
        self.min=self._set_min_button(date.minute)
        self.date=Gtk.Entry()
        date_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        date_box.pack_start(Gtk.Label(label=label),False,False,0)
        date_box.pack_start(self._set_entry_cal(date),True,False,0)
        self.pack_start(date_box,False,False,0)
        time_box=Gtk.Box(spacing=2)
        time_box.pack_start(self.hour,False,False,0)
        time_box.pack_start(Gtk.Label(label=":"),False,False,0)
        time_box.pack_start(self.min,False,False,0)
        self.pack_start(time_box,False,False,0)

    def get_datetime(self):
        return MyDates.new_from_gui(self.date.get_text(),self.hour.get_value_as_int(),self.min.get_value_as_int())

    def _set_entry_cal(self,date):
        box=Gtk.Box()
        self.date.set_text(date.get_date())
        pop_button=Gtk.Button.new_from_icon_name("arrow-down",Gtk.IconSize.MENU)
        pop_button.connect("clicked",self._on_pop_clicked,pop_button)
        box.pack_start(self.date,False,False,0)
        box.pack_start(pop_button,False,False,0)
        return box

    def _on_pop_clicked(self,button,widget):
        cal=self._cal_popover(widget)
        cal.show_all()

    def _cal_popover(self,widget):
        pop=Gtk.Popover()
        pop.set_position(Gtk.PositionType.TOP)
        pop.set_relative_to(widget)
        cal = Gtk.Calendar()
        sel_date=MyDates.new_from_gui(self.date.get_text(),0,0)
        cal.select_day(sel_date.day)
        cal.select_month(sel_date.month-1,sel_date.year)
        cal.connect("day-selected-double-click",self._on_date_selected,pop)
        pop.add(cal)
        return pop

    def _on_date_selected(self,cal,pop):
        date=MyDates.new_from_gdate(cal.get_date())
        self.date.set_text(date.get_date())
        pop.destroy()

    def _set_hour_button(self,value):
        adjust=Gtk.Adjustment(value=value,lower=0.0,upper=23.0,step_increment=1.0,page_increment=0.0,page_size=0.0)
        spin_hour=Gtk.SpinButton()
        spin_hour.configure(adjust,0.5,0)
        spin_hour.set_wrap(True)
        spin_hour.set_orientation(Gtk.Orientation.VERTICAL)
        return spin_hour

    def _set_min_button(self,value):
        adjust=Gtk.Adjustment(value=value,lower=0.0,upper=59.0,step_increment=5.0,page_increment=0.0,page_size=0.0)
        spin_min=Gtk.SpinButton()
        spin_min.configure(adjust,0.5,0)
        spin_min.set_wrap(True)
        spin_min.set_orientation(Gtk.Orientation.VERTICAL)
        return spin_min
