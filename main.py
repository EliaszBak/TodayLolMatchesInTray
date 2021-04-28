
import wx
import wx.adv
import webbrowser
from lolMatches import getMatches

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'icon.png'

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class LolMatchesPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("blue")
        #first column
        self.sources_list = wx.ListCtrl(self,style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.sources_list1 = wx.ListCtrl(self,style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.sources_list.InsertColumn(0, "Matches", width=350)
        self.sources_list1.InsertColumn(1, "Tournament", width=250)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.sources_list, 0, wx.ALL | wx.EXPAND)
        sizer.Add(self.sources_list1, 1, wx.ALL | wx.EXPAND)

        # sizer.Add(self.news_list, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)
        self.todayMatches()
        self.sources_list.Bind(wx.EVT_LIST_ITEM_SELECTED , self.OnLinkSelected)

    def todayMatches(self):
        for r in getMatches():
            date = r['DateTime UTC']
            date = date.split(' ')
            str = r['Team1'] + ' VS. ' + r['Team2'] + ' at ' + date[1]
            self.sources_list.InsertItem(0, str)
            self.sources_list1.InsertItem(0, r['ShownName'])


# /    def getNewsDescription(self):
#         for post in self.page['data']['children']:
#             # print(post['url'])
#             index = 0
#             self.news_list.InsertItem(index, post['data']['url'])
#             self.news_list.SetItem(index, 1, post['data']['permalink'])
#             index +=1

    def OnSourceSelected(self, event):
         source = event.GetText().replace(" ", "-")

    def OnLinkSelected(self, event):
          webbrowser.open('https://lolesports.com/live/')


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self,frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.myapp_frame = frame
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        create_menu_item(menu, 'Today\'s matches', self.onLolMatches)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print ('Tray icon was left-clicked.')

    def on_exit(self, event):
        self.myapp_frame.Close()

    def onLolMatches(self, event):
        frame = wx.Frame(parent=None, title='TodaysLolMatches', size=(640,300))
        LolMatchesPanel(frame)
        frame.Show()

class My_Application(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1,1))
        panel = wx.Panel(self)
        self.myapp = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    #----------------------------------------------------------------------
    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        self.myapp.RemoveIcon()
        self.myapp.Destroy()
        self.Destroy()

if __name__ == "__main__":
    MyApp = wx.App()
    My_Application()
    MyApp.MainLoop()