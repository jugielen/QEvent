import gi,sys
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from QEvent import QEvent
from input_gui import EditWindow

class EventLabel(Gtk.Label):
    def __init__(self,event):
        super().__init__()
        self.event=event
        self.set_markup("<big>"+str(event)+"</big>")
        self.set_xalign(0.0)

    def get_event(self):
        return self.event


class EventsBox(Gtk.FlowBox):
    def __init__(self,events):
        super().__init__()
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self._display_events(events)
    
    def _display_events(self,events):
        #add event to main_box with labels
        for event in events:
            print(event.get_id())
            event_label=EventLabel(event)
            self.add(event_label)
            sep=Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            self.add(sep)

    def refresh(self):
        for widget in self:
            widget.destroy()
        self.events=QEvent.get_next_x()
        self._display_events()
       


#main window, display next ten events by default
class ApplicationWindow(Gtk.ApplicationWindow):
    def __init__(self,application):
        Gtk.Window.__init__(self,application=application)
        main_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        self.add(main_box)
        main_box.set_border_width(20)
        self.events=QEvent.get_next_x()
        self.ebox=EventsBox(self.events)
        main_box.add(self.ebox)       
        self.set_header_bar("Simple Life Organizer")
        self.show_all()

    def set_header_bar(self,title):
        barre=Gtk.HeaderBar()
        barre.set_show_close_button(True)
        barre.set_title(title)
        self.set_titlebar(barre)
        add_button=Gtk.Button.new_from_icon_name("add",Gtk.IconSize.MENU)
        edit_button=Gtk.Button.new_from_icon_name("edit",Gtk.IconSize.MENU)
        del_button=Gtk.Button.new_from_icon_name("edit-delete",Gtk.IconSize.MENU)
        edit_button.connect("clicked",self.edit_event)
        del_button.connect("clicked",self.del_event)
        add_button.connect("clicked",self.add_event)
        barre.pack_start(add_button)
        barre.pack_start(edit_button)
        barre.pack_start(del_button)

    def refresh(self):
        self.ebox.destroy()
        self.events=QEvent.get_next_x()
        self.ebox=EventsBox(self.events)
        self.get_child().add(self.ebox)  
        self.show_all()

    #si add_event_clicked
    def add_event(self,button):
        new_event=QEvent()
        add_event_win=EditWindow(self,"Nouvel Evénement",new_event)
        confirm=add_event_win.run()
        add_event_win.show_all()
        if confirm==Gtk.ResponseType.OK:
            saved=new_event.save()
            if saved:
                notif=NotifBar(Gtk.MessageType.INFO,"Evénement sauvegardé")
            else:
                notif=NotifBar(Gtk.MessageType.ERROR,"Erreur - événement non sauvegardé")
            self.get_child().add(notif)
            self.get_child().reorder_child(notif,0)
            self.refresh()
            self.show_all()
        elif confirm==Gtk.ResponseType.CANCEL:
            pass
        add_event_win.destroy()

    #si edit clicked
    def edit_event(self,button):
        print("Edit_clicked")
        event_selected=self.ebox.get_selected_children()
        event=event_selected[0].get_child().get_event()
        edit_event_win=EditWindow(self,"Edit Event",event)
        confirm=edit_event_win.run()
        if confirm==Gtk.ResponseType.OK:
            saved=event.update()
            self.refresh()
            self.show_all()
        elif confirm==Gtk.ResponseType.CANCEL:
            pass
        edit_event_win.destroy()

    #si delete clicked
    def del_event(self,button):
        event_selected=self.ebox.get_selected_children()
        event=event_selected[0].get_child().get_event()
        dialog_content="Voulez-vous vraiment supprimer cet événement?\n"+str(event)
        del_win=DialogWin(self,"Are your sure ?",dialog_content)
        confirm=del_win.run()
        if confirm==Gtk.ResponseType.OK:
            del_confirm=event.delete()
            self.refresh()
            self.show_all()

        elif Gtk.ResponseType.CANCEL:
            pass
        del_win.destroy()

#Dialog window with custom title and label
class DialogWin(Gtk.Dialog):

    def __init__(self,parent,title,dialog_content):
        super().__init__(title=title, transient_for=parent, flags=0)
        
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)

        label_confirm=Gtk.Label(dialog_content)

        box = self.get_content_area()
        box.pack_start(label_confirm, True,True,0)
        self.show_all()

#entry window to add or edit events
class EntryWindow(Gtk.Dialog):
    def __init__(self,parent,title,event):
        self.event=event
        super().__init__(title=title, transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OK,Gtk.ResponseType.OK)
        box=self.get_content_area()
        box.set_border_width(20)
        list_label=QEvent.get_labels()
        box_label=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        self.box_entry=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        box.pack_start(box_label,True, True,0)
        box.pack_start(self.box_entry,False, True,0)

        i=0

        for el in event:
            event_label=Gtk.Label(label=list_label[i])
            entry=Gtk.Entry()
            entry.set_text(str(el))
            box_label.pack_start(event_label,True, True,0)
            self.box_entry.pack_start(entry,True,True,0)
            i+=1
 
        self.show_all()

    def return_event(self):
        tuple_event=tuple((self.event.get_id(),))
        for entry in self.box_entry:
            tuple_event=tuple_event+tuple((entry.get_text(),))
        return QEvent.new_from_tuple(tuple_event)





class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        window = ApplicationWindow(self)

def start_gui():
    application = Application()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)


class NotifBar(Gtk.InfoBar):
    def __init__(self,type,notif):
        super().__init__(self)
        self.set_message_type(type)
        self.set_show_close_button(True)
        self.get_content_area().add(Gtk.Label(label=notif))
        self.connect("response", self._on_infobar_response)

    def _on_infobar_response(self, infobar, respose_id):
        self.destroy()
    
