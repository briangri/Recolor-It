#!/usr/bin/env python
"""The GUI and front end for the Recolor It program"""
#Author: Brian Griffith
#Version: 0.1

import pygtk
pygtk.require('2.0')
import gtk
from library.img import *

class ImagesExample:
    """The main gui container used for Recolor It"""
    # when invoked (via signal delete_event), terminates the application.
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def file_selected(self, widget):
        """Called when a new file is selected. Records the filename and updates"""
        print "Selected filepath: %s" % widget.get_filename()
        self.filename = widget.get_filename()
        Img(self.filename)
        self.update()
        
    def resize(self, height, width, url):
        """returns an image from given url with given size"""
        pixbuf = gtk.gdk.pixbuf_new_from_file(url)
        pixbuf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_BILINEAR)
        return gtk.image_new_from_pixbuf(pixbuf)

    def resized(self, height, width, url):
        """returns a pixbuf based on a url with given size"""
        pixbuf = gtk.gdk.pixbuf_new_from_file(url)
        pixbuf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_BILINEAR)
        return pixbuf
    
    def __init__(self):
        """Initializes the GUI"""
        # create the main window, and attach delete_event signal to terminating
        # the application
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.close_application)
        self.window.set_border_width(10)
        self.window.set_title("Recolor It!")
        self.window.show()
        self.filename = "sample_images/obama.jpg"
        self.myImg = Img(self.filename)
        self.draw()

    def update(self):
        """Updates the front page image and histograms"""
        self.picture.set_from_pixbuf(self.resized(450, 350, self.filename))
        self.rhist.set_from_pixbuf(self.resized(160, 280, "library/0pre.jpg"))
        self.bhist.set_from_pixbuf(self.resized(160, 280, "library/1pre.jpg"))
        self.ghist.set_from_pixbuf(self.resized(160, 280, "library/2pre.jpg"))

    def updateresults(self):
        """updates the results page image and histograms"""
        self.picture2.set_from_pixbuf(self.resized(450, 350, "library/out.jpg"))
        self.rhist2.set_from_pixbuf(self.resized(160, 280, "library/0post.jpg"))
        self.bhist2.set_from_pixbuf(self.resized(160, 280, "library/1post.jpg"))
        self.ghist2.set_from_pixbuf(self.resized(160, 280, "library/2post.jpg"))
        self.notebook.set_current_page(1)
        
        
    def draw(self):
        """draws the main gui"""
        self.notebook = gtk.Notebook()
        
        #create table
        self.table = gtk.Table(5, 2, False)
        self.table.set_row_spacings(10)
        self.table.set_col_spacings(10)
        
        #input button
        filechooserbutton = gtk.FileChooserButton('Select a File')
        filechooserbutton.connect("file-set", self.file_selected)  
        #self.window.add(filechooserbutton)
        #filechooserbutton.show()
        self.table.attach(filechooserbutton, 0, 2, 0, 1)

        #picture
        self.picture = self.resize(450, 350, self.filename)
        self.table.attach(self.picture, 0, 1, 1, 4)

        #histograms
        self.rhist = self.resize(160, 280, "library/0pre.jpg")
        self.table.attach(self.rhist, 1, 2, 1, 2)
        ###addit
        self.ghist = self.resize(160, 280, "library/0pre.jpg")
        self.table.attach(self.ghist, 1, 2, 2, 3)
        ###addit
        self.bhist = self.resize(160, 280, "library/0pre.jpg")
        self.table.attach(self.bhist, 1, 2, 3, 4)

        #text inputs:
        inputarea = gtk.HBox()
        inputarea.set_spacing(10)
        self.table.attach(inputarea, 0, 2, 4, 5)

        label = gtk.Label("Red Shift:")
        inputarea.pack_start(label, gtk.TRUE, gtk.TRUE, 0)
        self.red = gtk.Entry(5)
        inputarea.pack_start(self.red, gtk.TRUE, gtk.TRUE, 0)

        label = gtk.Label("Blue Shift:")
        inputarea.pack_start(label, gtk.TRUE, gtk.TRUE, 0)
        self.blue = gtk.Entry(5)
        inputarea.pack_start(self.blue, gtk.TRUE, gtk.TRUE, 0)

        label = gtk.Label("Green Shift:")
        inputarea.pack_start(label, gtk.TRUE, gtk.TRUE, 0)
        self.green = gtk.Entry(5)
        inputarea.pack_start(self.green, gtk.TRUE, gtk.TRUE, 0)

        self.norm = gtk.Button("Normalize")
        self.norm.connect("clicked", self.normalize, None)
        inputarea.pack_start(self.norm, gtk.TRUE, gtk.TRUE, 0)

        self.shift = gtk.Button("Shift")
        self.shift.connect("clicked", self.shiftit, None)
        inputarea.pack_start(self.shift, gtk.TRUE, gtk.TRUE, 0)

        #table 2
        self.table2 = gtk.Table(5, 2, False)
        self.table2.set_row_spacings(10)
        self.table2.set_col_spacings(10)

        #picture
        self.picture2 = self.resize(450, 350, self.filename)
        self.table2.attach(self.picture2, 0, 1, 1, 4)

        #histograms
        self.rhist2 = self.resize(160, 280, "library/0pre.jpg")
        self.table2.attach(self.rhist2, 1, 2, 1, 2)
        ###addit
        self.ghist2 = self.resize(160, 280, "library/1pre.jpg")
        self.table2.attach(self.ghist2, 1, 2, 2, 3)
        ###addit
        self.bhist2 = self.resize(160, 280, "library/2pre.jpg")
        self.table2.attach(self.bhist2, 1, 2, 3, 4)
        
        self.notebook.append_page(self.table, gtk.Label('Input'))
        self.notebook.append_page(self.table2, gtk.Label('Results'))
        self.notebook.props.border_width = 12
        self.notebook.set_tab_reorderable(self.table, True)
        self.notebook.set_tab_reorderable(self.table2, True)
        self.window.add(self.notebook)
        self.window.show_all()
        
        
    def normalize(self, widget, value=None):
        """generates images and histograms based on the "normalize" algorithm"""
        values =  [int(self.red.get_text()), int(self.green.get_text()),
                   int(self.blue.get_text())]
        print self.filename
        myImg = Img(self.filename)
        myImg.run(values, "N")
        self.updateresults()

    def shiftit(self, widget, value=None):
        """generates images and histograms based on "shift" algorithm"""
        values =  [int(self.red.get_text()), int(self.green.get_text()),
                   int(self.blue.get_text())]
        print self.filename
        myImg = Img(self.filename)
        myImg.run(values, "S")
        self.updateresults()
        
        
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ImagesExample()
    main()

