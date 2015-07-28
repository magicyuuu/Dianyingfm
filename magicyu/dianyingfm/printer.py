# -*- coding: utf-8 -*-#
import sys

class Printer(object):
    def __init__(self):
        self.xmlstr = '<?xml version="1.0" encoding="utf-8"?>\n'
        self.item = [self.xmlstr]

    def start(self):
        self.item.append('<items>\n')

    def end(self):
        self.item.append('</items>\n')

    def sendToWorkFlow(self):
        sys.stdout.write("".join(self.item))

    def reset(self):
        self.item = [self.xmlstr]

    def add_item(self, title, subtitle, arg, icon, valid=False):
        it = '  <item valid="%s"><title>%s</title><subtitle>%s</subtitle><arg>%s</arg><icon>%s</icon></item>\n' % (
        'yes' if valid else 'no', title, subtitle, arg, icon)
        self.item.append(it)