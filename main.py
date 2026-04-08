import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk, GObject
from wonderwords import RandomWord
from random import randrange

# data = [
#     {"name": "USS Enterprise", "image": "enterprise.png", "registry": "NCC-1701"},
#     {"name": "USS Reliant", "image": "reliant.png", "registry": "NCC-1864"},
#     {"name": "USS Defiant", "image": "defiant.png", "registry": "NX-74205"},
# ]

class Starship(GObject.Object):
    def __init__(self, name, image, registry):
        super().__init__()
        self._name = name
        self._image = image
        self._registry = registry

    @GObject.Property(type=str)
    def name(self):
        return self._name

    @GObject.Property(type=str)
    def image(self):
        return self._image

    @GObject.Property(type=str)
    def registry(self):
        return self._registry

Gio.Resource._register(Gio.Resource.load("gresources.gresource"))

@Gtk.Template(resource_path="/com/github/jasper-zanjani/gtk-starships/template.ui")
class CustomAvatar(Adw.Bin):
    __gtype_name__ = "CustomAvatar"
    image = Gtk.Template.Child()
    name = Gtk.Template.Child()
    registry = Gtk.Template.Child()

class MyApp(Adw.Application):
    random_word = RandomWord()
    def do_activate(self):
        builder = Gtk.Builder()
        builder.add_from_file("main.ui")
        if not self.props.active_window:
            win = builder.get_object("main")

        win.set_application(self)
        win.present()

        def on_factory_setup(_factory, list_item):
            custom_avatar = CustomAvatar()
            list_item.set_child(custom_avatar)

        def on_factory_bind(_factory, list_item):
            custom_avatar = list_item.get_child()
            model_item = list_item.get_item()
            paintable = Gdk.Texture.new_from_filename(model_item.image)
            custom_avatar.image.set_from_paintable(paintable)
            custom_avatar.name.set_label(model_item.name)
            custom_avatar.registry.set_label(model_item.registry)
               
        gridview = builder.get_object("gridview")
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", on_factory_setup)
        factory.connect("bind", on_factory_bind)
        gridview.set_factory(factory)

        data_model = Gio.ListStore(item_type=Starship)
        # for item in data:
        #     gobject = Starship(name=item['name'], image=item['image'], registry=item['registry'])
        #     data_model.append(gobject)
        for i in range(100):
            name = self.random_word.word(include_parts_of_speech=['adjectives'])
            gobject = Starship(name=f"USS {name.title()}", image="enterprise-stripped.png", registry=f"NCC-{randrange(10000)}")
            data_model.append(gobject)
        selection_model = Gtk.SingleSelection.new(data_model)
        gridview.set_model(selection_model)

if __name__ == '__main__':
    app = MyApp()
    app.run()
