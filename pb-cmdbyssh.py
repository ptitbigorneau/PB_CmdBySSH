#!/usr/bin/python
# -*- coding: utf-8 -*- 

__author__  = 'PtitBigorneau'
__version__ = 'beta3'

import wx
import os, sys, ConfigParser, time
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    import paramiko
from contextlib import contextmanager

def fexist(File):
    
    try:
    
        file(File)
     
        return True
   
    except:
  
        return False 

def testssh(host, port, user, pwd):
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
    
        ssh.connect(host, int(port), username=user, password=pwd, timeout=1)
      
        return True
   
    except:
        
        return False
      
def testcfg(file):
    
    try:
    
        cfg = ConfigParser.ConfigParser()
        cfg.read(file)
        section = cfg.sections()
        
        for x in section:
            
            cname = cfg.get(x,"name")
            chost = cfg.get(x,"host")
            cport = cfg.get(x,"port")
            cuser = cfg.get(x,"user")
            cpwd = cfg.get(x,"pwd")
            lcmd1 = cfg.get(x,"namecmd1")
            lcmd2 = cfg.get(x,"namecmd2")
            ccmd1 = cfg.get(x,"cmd1")
            ccmd2 = cfg.get(x,"cmd2")
     
        return True
   
    except:
  
        return False

def cara(test):
   
    try:
            
        if fexist('test.cfg') == True:

            os.remove('test.cfg')

        cfg = ConfigParser.ConfigParser()
        cfg.read('test.cfg')
        cfg.add_section('section')
        cfg.set('section', 'test', test)
        cfg.write(open('test.cfg','w'))   
        os.remove('test.cfg')

        return True
   
    except:
  
        return False

def mesError(Error):

    texte =" %s invalid value"%(Error)

    dlg = wx.MessageDialog(None, texte, 'Error !', style = wx.OK | wx.ICON_ERROR)
    retour = dlg.ShowModal()
    dlg.Destroy() 

class MyFrame2(wx.Frame):

    file = 'pb-cmdbyssh.cfg'

    def __init__(self, titre):    
         
        wx.Frame.__init__(self, None, -1, title = titre, size=(650,680))
        
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
     
        section = []
        if (fexist(self.file) == False) or (testcfg(self.file) == False):

            self.configs = ['']
            x=0

            chost = ''
            cport = ''
            cuser = ''
            cpwd = ''
            lcmd1 = ''
            lcmd2 = ''
            ccmd1 = ''
            ccmd2 = ''
            self.testvide = 'vide'

        if (fexist(self.file) == True) and (testcfg(self.file) == True):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)

            section = cfg.sections()

            if len(cfg.sections())==0:

                self.configs = ['']

                x=0
                chost = ''
                cport = ''
                cuser = ''
                cpwd = ''
                lcmd1 = ''
                lcmd2 = ''
                ccmd1 = ''
                ccmd2 = ''
                
                self.testvide = 'vide'

            else:
 
                self.testvide = 'nonvide'
                
                for x in section:
              
                    namesection.append(cfg.get(x,"name"))
               
                self.configs = namesection
                x = len(cfg.sections()) - 1
                self.csection = section[x]
                chost = cfg.get(section[x],"host")
                cport = cfg.get(section[x],"port")
                cuser = cfg.get(section[x],"user")
                cpwd = cfg.get(section[x],"pwd")
                lcmd1 = cfg.get(section[x],"namecmd1")
                lcmd2 = cfg.get(section[x],"namecmd2")
                ccmd1 = cfg.get(section[x],"cmd1")
                ccmd2 = cfg.get(section[x],"cmd2")
     

        menuFile = wx.Menu(style = wx.MENU_TEAROFF) 
        menuFile.Append(101, "&New task\tCtrl+N", "New task")
        menuFile.Append(104, "&Save\tCtrl+S", "Save task")
        menuFile.Append(102, "&Edit\tCtrl+E", "Edit task")
        menuFile.Append(103, "&Delete\tCtrl+D", "Delete task")
       

        menuFile.AppendSeparator() 
        menuFile.Append(105, "&Quit\tCtrl+Q", "Quit PB-CmdBySSH Configuration") 

        menuHelp = wx.Menu()
        menuHelp.Append(106, "About","About PB-CmdBySSH")

        menuBarre = wx.MenuBar() 
        menuBarre.Append(menuFile, "&File")
        menuBarre.Append(menuHelp, "?")

        self.barre = wx.StatusBar(self, -1) 
        self.barre.SetFieldsCount(2) 
        self.barre.SetStatusWidths([-1, -1]) 

        self.SetStatusBar(self.barre)

        self.SetMenuBar(menuBarre)        

        toolbar = self.CreateToolBar()
        toolbar.AddSeparator()
        toolbar.AddLabelTool(101, 'New', wx.Bitmap('./new.bmp'),shortHelp='New', longHelp="New task")
        toolbar.AddLabelTool(104, '', wx.Bitmap('./enr.bmp'),shortHelp='Save', longHelp="Save task")
        toolbar.AddLabelTool(102, '', wx.Bitmap('./modif.bmp'),shortHelp='Edit', longHelp="Edit task")
        toolbar.AddLabelTool(103, '', wx.Bitmap('./effa.bmp'),shortHelp='Delete', longHelp="Delete task")
        
        toolbar.AddSeparator()
        toolbar.AddLabelTool(105, '', wx.Bitmap('./exit.bmp'),shortHelp='Quit', longHelp="Quit PB-CmdBySSH Configuration")
        toolbar.AddSeparator()
        toolbar.Realize()

        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(10, 10)
        
        sizer = wx.GridBagSizer(5, 5)

        font = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        fontc = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.BOLD)

        text1 = wx.StaticText(panel, label="Configuration PB-CmdBySSH")
        sizer.Add(text1, pos=(0, 0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM, 
            border=20)

        font3 = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD)
        text1.SetFont(font3)

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('confpbcmdbyssh.gif'))
        sizer.Add(icon, pos=(0, 4), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, 
            border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        self.tconfig = wx.ComboBox(panel,1,self.configs[x], choices=self.configs, style=wx.CB_READONLY)
        sizer.Add(self.tconfig, pos=(2, 1), span=(1, 3), 
            flag=wx.TOP|wx.EXPAND, border=10)
        self.tconfig.SetFont(fontc)
        
        button2 = wx.Button(panel,1, label="Edit")
        sizer.Add(button2, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=8)        

        self.host = wx.StaticText(panel, label=" Host :                      ")
        sizer.Add(self.host, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)
        self.host.SetFont(font)


        self.thost = wx.TextCtrl(panel, value=chost)
        sizer.Add(self.thost, pos=(3, 1), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)
        
        self.port = wx.StaticText(panel, label=" Port :        ")
        sizer.Add(self.port, pos=(3, 2), flag=wx.LEFT|wx.TOP, border=10)
        self.port.SetFont(font)


        self.tport = wx.TextCtrl(panel, value=cport)
        sizer.Add(self.tport, pos=(3, 3), span=(1, 1), flag=wx.TOP|wx.EXPAND, border=10)

        ident = wx.StaticText(panel, label=" Login :                     ")
        sizer.Add(ident, pos=(4, 0), flag=wx.LEFT|wx.TOP, border=10)
        ident.SetFont(font)

        
        self.tident = wx.TextCtrl(panel, value=cuser)
        sizer.Add(self.tident, pos=(4, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, 
            border=5)
        
        pwd = wx.StaticText(panel, label=" Password :        ")
        sizer.Add(pwd, pos=(5, 0), flag=wx.LEFT|wx.TOP, border=10)
        pwd.SetFont(font)

        
        self.tpwd = wx.TextCtrl(panel, value=cpwd)
        sizer.Add(self.tpwd, pos=(5, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, 
            border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(7, 0), span=(1, 5), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        namecmd1 = wx.StaticText(panel, label=" Button 1 :                ")
        sizer.Add(namecmd1, pos=(8, 0), flag=wx.LEFT|wx.TOP, border=10) 
        namecmd1.SetFont(font)
        
        self.tnamecmd1 = wx.TextCtrl(panel, value=lcmd1)
        sizer.Add(self.tnamecmd1, pos=(8, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, 
            border=5)

        cmd1 = wx.StaticText(panel, label=" Command :             ")
        sizer.Add(cmd1, pos=(10, 0), flag=wx.LEFT|wx.TOP, border=10)
        cmd1.SetFont(font)

        self.tcmd1 = wx.TextCtrl(panel, value=ccmd1)
        sizer.Add(self.tcmd1, pos=(10, 1), span=(1, 3),flag=wx.TOP|wx.EXPAND, 
            border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(12, 0), span=(1, 5), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        namecmd2 = wx.StaticText(panel, label=" Button 2 :                ")
        sizer.Add(namecmd2, pos=(13, 0), flag=wx.LEFT|wx.TOP, border=10)
        namecmd2.SetFont(font)

        self.tnamecmd2 = wx.TextCtrl(panel, value=lcmd2)
        sizer.Add(self.tnamecmd2, pos=(13, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, 
            border=5)
 
        cmd2 = wx.StaticText(panel, label=" Command :             ")
        sizer.Add(cmd2, pos=(15, 0), flag=wx.LEFT|wx.TOP, border=10)
        cmd2.SetFont(font)
        
        self.tcmd2 = wx.TextCtrl(panel, value=ccmd2)
        sizer.Add(self.tcmd2, pos=(15, 1), span=(1, 3),flag=wx.TOP|wx.EXPAND, 
            border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(17, 0), span=(1, 5), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        button3 = wx.Button(panel,2, label="Save")
        sizer.Add(button3, pos=(18, 3), flag=wx.TOP|wx.RIGHT, border=5)

        button4 = wx.Button(panel,3, label="Delete")
        sizer.Add(button4, pos=(18, 4), flag=wx.TOP|wx.RIGHT, border=5)

        sizer.AddGrowableCol(1)
        
        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#f0f0f0") 
        
        self.Bind(wx.EVT_COMBOBOX, self.Changetask)
        self.Bind(wx.EVT_BUTTON, self.Clickmodif, id=1)
        self.Bind(wx.EVT_BUTTON, self.Clickenr, id=2)
        self.Bind(wx.EVT_BUTTON, self.Clickeff, id=3)
        
        wx.EVT_MENU(self, 101, self.Clicknew)
        wx.EVT_MENU(self, 104, self.Clickenr)
        wx.EVT_MENU(self, 102, self.Clickmodif)
        wx.EVT_MENU(self, 103, self.Clickeff)
        wx.EVT_MENU(self, 105, self.Quit)
        wx.EVT_MENU(self, 106, self.About)

    def Changetask(self, evt):
        
        selec = evt.GetSelection()
      
        if (fexist(self.file) == True) and (testcfg(self.file) == True) and (self.testvide != 'vide'):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)

            section = cfg.sections()
            for x in section:
              
                namesection.append(cfg.get(x,"name"))
            
            self.csection = section[int(selec)]
            chost = cfg.get(section[int(selec)],"host")
            cport = cfg.get(section[int(selec)],"port")
            cuser = cfg.get(section[int(selec)],"user")
            cpwd = cfg.get(section[int(selec)],"pwd")
            lcmd1 = cfg.get(section[int(selec)],"namecmd1")
            lcmd2 = cfg.get(section[int(selec)],"namecmd2")
            ccmd1 = cfg.get(section[int(selec)],"cmd1")
            ccmd2 = cfg.get(section[int(selec)],"cmd2")

            self.thost.SetValue(chost)
            self.tport.SetValue(cport)
            self.tident.SetValue(cuser)
            self.tpwd.SetValue(cpwd)
            self.tnamecmd1.SetValue(lcmd1)
            self.tnamecmd2.SetValue(lcmd2)
            self.tcmd1.SetValue(ccmd1)
            self.tcmd2.SetValue(ccmd2)
            evt.Skip()

        return

    def Clickenr(self, evt):

        if testcfg(self.file) == False:

            dlg = wx.MessageDialog(self, "Error File configuration !", "Error !" , style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 

            return

        if self.testvide == 'vide':

            texte = "Not Task has save !"
        
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()

            return

        csection = self.csection

        chost = self.thost.GetValue()
        cport = self.tport.GetValue()
        cuser = self.tident.GetValue()
        cpwd =  self.tpwd.GetValue()
        lcmd1 = self.tnamecmd1.GetValue()
        lcmd2 = self.tnamecmd2.GetValue()
        cmd1 =  self.tcmd1.GetValue()
        cmd2 =  self.tcmd2.GetValue()
       
        if cara(chost) == False:

            mesError('HOST')
            self.thost.SetValue('')
            evt.Skip()
            return

        if cara(cport) == False:

            mesError('PORT')
            self.tport.SetValue('')
            evt.Skip()
            return

        if not cport.isdigit():

            mesError('PORT')
            self.tport.SetValue('')
            evt.Skip()
            return
        
        if cara(cuser) == False:

            self.tident.SetValue('')
            evt.Skip()
            mesError('LOGIN')
            return        

        if cara(cpwd) == False:

            self.tpwd.SetValue('')
            evt.Skip()
            mesError('Password')
            return        

        if cara(lcmd1) == False:

            self.tnamecmd1.SetValue('')
            evt.Skip()
            mesError('Command Name 1')
            return        

        if cara(lcmd2) == False:

            self.tnamecmd2.SetValue('')
            evt.Skip()            
            mesError('Command Name 2')
            return        
        
        if cara(cmd1) == False:

            self.tcmd1.SetValue('')
            evt.Skip()            
            mesError('Command 1')
            return

        if cara(cmd2) == False:

            self.tcmd2.SetValue('')
            evt.Skip()
            mesError('Command 2')
            return

        cfg = ConfigParser.ConfigParser()
        cfg.read(self.file)
        
        cfg.set(csection,"host",chost)
        cfg.set(csection,"port",cport)
        cfg.set(csection,"user",cuser)
        cfg.set(csection,"pwd",cpwd)
        cfg.set(csection,"namecmd1",lcmd1)
        cfg.set(csection,"cmd1",cmd1)
        cfg.set(csection,"namecmd2",lcmd2)
        cfg.set(csection,"cmd2",cmd2)

        cfg.write(open(self.file,'w'))

        texte = "Task successfully registered"

        dlg = wx.MessageDialog(self, texte, style = wx.OK)
        retour = dlg.ShowModal()
        dlg.Destroy()
 
        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-CmdBySSH")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)

    def Clickeff(self, evt):
        
        if self.testvide == 'vide':

            texte = "Not Task has Delete !"
        
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()

            return        

        csection = self.csection
        
        self.configs = self.configs.remove(self.tconfig.GetLabel())

        cfg = ConfigParser.ConfigParser()
        cfg.read(self.file)
        cfg.remove_section(csection)
        cfg.write(open(self.file,'w'))
        
        texte = "Task successfully deleted"
        
        dlg = wx.MessageDialog(self, texte, style = wx.OK)
        retour = dlg.ShowModal()
        dlg.Destroy() 
        
        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-CmdBySSH")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)

    def Clicknew(self, evt):
        
        addTask = wx.TextEntryDialog(self, 'Task has execute : ', 'New Task')
        addTask.ShowModal()
        ccname = addTask.GetValue()
               
        if cara(ccname) == False:
        
            texte = "invalid value !"
        
            dlg = wx.MessageDialog(self, texte, "Error !", style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return
        
        if fexist('test.cfg') == True:

            os.remove('test.cfg')        
        
        if ccname == "":

            return

        section = []
        if (fexist(self.file) == False) or (testcfg(self.file) == False):

            section = "task1"

        if (fexist(self.file) == True) and (testcfg(self.file) == True):
            
            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)

            if len(cfg.sections())==0:

                section = "task1"
            
            else:
 
                n = 1
                section = "task%s"%(n)

                while section in cfg.sections():

                    n = n + 1
                    section = "task%s"%(n)     
        
        cfg = ConfigParser.ConfigParser()
        cfg.read(self.file)
        cfg.add_section(section)
        cfg.set(section, 'name', ccname)
        cfg.set(section, 'host', '')
        cfg.set(section, 'port', '22')
        cfg.set(section, 'user', '')
        cfg.set(section, 'pwd', '')
        cfg.set(section, 'namecmd1', '')
        cfg.set(section, 'cmd1', '')
        cfg.set(section, 'namecmd2', '')
        cfg.set(section, 'cmd2', '')

        cfg.write(open(self.file,'w'))

        texte = "New Task added successfully"
        
        dlg = wx.MessageDialog(self, texte, style = wx.OK)
        retour = dlg.ShowModal()
        dlg.Destroy()

        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-CmdBySSH")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)

    def Clickmodif(self, evt):
        
        if self.testvide == 'vide':

            self.Clicknew(evt)              

            return               
         
        addTask = wx.TextEntryDialog(self, 'Task has execute : ', 'Edit Task')
        addTask.ShowModal()
        ccname = addTask.GetValue()
               
        if cara(ccname) == False:
        
            texte = "invalid value !"
        
            dlg = wx.MessageDialog(self, texte, "Error !",style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return
        
        if fexist('test.cfg') == True:

            os.remove('test.cfg')        
        
        if ccname == "":

            return
        
        csection = self.csection

        cfg = ConfigParser.ConfigParser()
        cfg.read(self.file)
        
        cfg.set(csection,"name",ccname)


        cfg.write(open(self.file,'w'))

        texte = "Task successfully modified"

        dlg = wx.MessageDialog(self, texte, style = wx.OK)
        retour = dlg.ShowModal()
        dlg.Destroy()
 
        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-CmdBySSH")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)

    def Quit(self, evt):

        if fexist('test.cfg') == True:

            os.remove('test.cfg')
        
        self.Destroy()
        self.frame=Myframe(titre="PB-CmdBySSH")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame.SetIcon(icone)
       
        self.frame.Show(True)
        self.Show(False)

    def About(self, evt):

        description = """
            Envois de Commands a distance par SSH            
           ( Python 2.7, wxPython )
"""
       
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO))
        info.SetName('PB-CmdBySSh')
        info.SetVersion('beta3')
        info.SetDescription(description)
        info.SetCopyright('(C) 2011 PtitBigorneau')
        info.SetWebSite('http://www.ptitbigorneau.fr')
             
        wx.AboutBox(info)


class Myframe(wx.Frame):

    file = 'pb-cmdbyssh.cfg'

    def __init__(self, titre):    

        wx.Frame.__init__(self, None, -1, title = titre, size=(650,680))
        
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
        
        colorpwd = "red"
        color = "black"

        section = []
        if (fexist(self.file) == False) or (testcfg(self.file) == False):

            configs = ['']

            self.testvide = 'vide'            
            chost = ''
            cport = ''
            cuser = ''
            self.ctestpwd = ''
            lcmd1 = 'Button 1'
            lcmd2 = 'Button 2'
            ccmd1 = ''
            ccmd2 = ''
            if fexist(self.file) == False:
            
                cstatus = "Not File configuration"
            
            if testcfg(self.file) == False:
  
                cstatus = "Error in File configuration"            
            
            color = "red"

        if (fexist(self.file) == True) and (testcfg(self.file) == True):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)

            section = cfg.sections()

            if len(cfg.sections())==0:

                configs = ['']

                chost = ''
                cport = ''
                cuser = ''
                self.ctestpwd = ''
                lcmd1 = 'Button 1'
                lcmd2 = 'Button 2'
                ccmd1 = ''
                ccmd2 = ''
                cstatus = 'File configuration empty'
                color = "red"
                self.testvide = 'vide'

            else:
 
                self.testvide = 'nonvide'
                
                for x in section:
              
                    namesection.append(cfg.get(x,"name"))
               
                configs = namesection
                chost = cfg.get(section[0],"host")
                cport = cfg.get(section[0],"port")
                cuser = cfg.get(section[0],"user")
                cpwd = cfg.get(section[0],"pwd")
                lcmd1 = cfg.get(section[0],"namecmd1")
                lcmd2 = cfg.get(section[0],"namecmd2")
                ccmd1 = cfg.get(section[0],"cmd1")
                ccmd2 = cfg.get(section[0],"cmd2")
                cstatus = 'Information'
                cstatus2 = ''

                self.pwd = cpwd
                
                if testssh(chost, cport, cuser, cpwd) == True:

                    self.ctestpwd = "ok"
                    colorpwd ="green"

                if testssh(chost, cport, cuser, cpwd) == False:

                    self.ctestpwd = "Error"
                    colorpwd = "red"

        menuFile = wx.Menu(style = wx.MENU_TEAROFF) 
        menuFile.Append(wx.ID_OPEN, "&Configuration\tCtrl+C", "Configurer CmdBySSH") 
        menuFile.Append(wx.ID_EXIT, "&Quit\tCtrl+Q", "Quit CmdBySSH") 

        menuHelp = wx.Menu()
        menuHelp.Append(wx.ID_ABOUT, "About","About CmdBySSH")

        menuBarre = wx.MenuBar() 
        menuBarre.Append(menuFile, "&File")
        menuBarre.Append(menuHelp, "?")

        self.barre = wx.StatusBar(self, -1) 
        self.barre.SetFieldsCount(2) 
        self.barre.SetStatusWidths([-1, -1]) 

        self.SetStatusBar(self.barre)

        self.SetMenuBar(menuBarre)        

        toolbar = self.CreateToolBar()
        toolbar.AddSeparator()
        toolbar.AddLabelTool(wx.ID_OPEN, '', wx.Bitmap('./conf.bmp'),shortHelp='Configuration', longHelp="Configurer CmdBySSH")
        toolbar.AddSeparator()
        toolbar.AddLabelTool(wx.ID_EXIT, '', wx.Bitmap('./exit.bmp'),shortHelp='Quit', longHelp="Quit CmdBySSH")
        toolbar.AddSeparator()
        toolbar.Realize()

        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(10, 10)
        sizer = wx.GridBagSizer(5, 5)

        font = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(12, wx.NORMAL, wx.NORMAL, wx.BOLD)
        fontc = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.BOLD)

        text1 = wx.StaticText(panel, label="PB-CmdBySSH")
        sizer.Add(text1, pos=(0, 0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM, 
            border=20)

        font3 = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD)
        text1.SetFont(font3)

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('pb-cmdbyssh.jpg'))
        sizer.Add(icon, pos=(0, 4), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, 
            border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        tconfig = wx.ComboBox(panel,1,configs[0], choices=configs, style=wx.CB_READONLY)
        sizer.Add(tconfig, pos=(2, 1), span=(1, 3), 
            flag=wx.TOP|wx.EXPAND, border=5)
        tconfig.SetFont(fontc)

        cmd1 = wx.StaticText(panel, label=" Button 1 :             ")
        sizer.Add(cmd1, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)
        cmd1.SetFont(font)
        
        self.button4 = wx.Button(panel, 1, label=lcmd1)
        sizer.Add(self.button4, pos=(4, 1), span=(1, 3), 
            flag=wx.TOP|wx.EXPAND, border=5)

        cmd2 = wx.StaticText(panel, label=" Button 2 :             ")
        sizer.Add(cmd2, pos=(6, 0), flag=wx.TOP|wx.LEFT, border=10)
        cmd2.SetFont(font)
        
        self.button5 = wx.Button(panel, 2, label=lcmd2)
        sizer.Add(self.button5, pos=(6, 1), span=(1, 3), 
            flag=wx.TOP|wx.EXPAND, border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(8, 0), span=(1, 5), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        tstatus = wx.StaticText(panel, label=cstatus)
        sizer.Add(tstatus, pos=(9, 2),span=(1, 2), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)
        tstatus.SetForegroundColour(color)
        tstatus.SetFont(font2)

        thost = wx.StaticText(panel, label=" Host :                    ")
        sizer.Add(thost, pos=(10, 0), flag=wx.TOP|wx.LEFT, border=10)
        font5 = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        thost.SetFont(font)
        
        self.host = wx.StaticText(panel, label=chost + ":" + cport)
        sizer.Add(self.host, pos=(10, 1), flag=wx.TOP|wx.LEFT, border=10)

        tuser = wx.StaticText(panel, label=" Login :                   ")
        sizer.Add(tuser, pos=(11, 0), flag=wx.TOP|wx.LEFT, border=10)
        tuser.SetFont(font)

        self.user = wx.StaticText(panel, label=cuser)
        sizer.Add(self.user, pos=(11, 1), flag=wx.TOP|wx.LEFT, border=10)

        ttestpwd = wx.StaticText(panel, label=" Connect :           ")
        sizer.Add(ttestpwd, pos=(12, 0), flag=wx.TOP|wx.LEFT, border=10)
        ttestpwd.SetFont(font)

        
        self.testpwd = wx.StaticText(panel, label=self.ctestpwd)
        sizer.Add(self.testpwd, pos=(12, 1), flag=wx.TOP|wx.LEFT, border=10)

        self.testpwd.SetForegroundColour(colorpwd)
        self.testpwd.SetFont(font)

        tccmd1 = wx.StaticText(panel, label=" Command 1 :       ")
        sizer.Add(tccmd1, pos=(13, 0), flag=wx.TOP|wx.LEFT, border=10)
        tccmd1.SetFont(font)
        
        self.cmd1 = wx.StaticText(panel, label=ccmd1)
        sizer.Add(self.cmd1, pos=(13, 1), flag=wx.TOP|wx.LEFT, border=10)

        tccmd2 = wx.StaticText(panel, label=" Command 2 :       ")
        sizer.Add(tccmd2, pos=(14, 0), flag=wx.TOP|wx.LEFT, border=10)
        tccmd2.SetFont(font)
        
        self.cmd2 = wx.StaticText(panel, label=ccmd2)
        sizer.Add(self.cmd2, pos=(14, 1), flag=wx.TOP|wx.LEFT, border=10)
        
        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(16, 0), span=(1, 5), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        tcmdlibre = wx.StaticText(panel, label=" Free Command : ")
        sizer.Add(tcmdlibre, pos=(17, 0), flag=wx.TOP|wx.LEFT, border=10)
        tcmdlibre.SetFont(font)
        
        self.cmdlibre = wx.TextCtrl(panel, value='')
        sizer.Add(self.cmdlibre, pos=(17, 1), span=(1, 3),flag=wx.TOP|wx.EXPAND, 
            border=5)

        buttonenvoyer = wx.Button(panel,3, label="Send")
        sizer.Add(buttonenvoyer, pos=(17, 4), flag=wx.TOP|wx.RIGHT, border=5) 

        sizer.AddGrowableCol(2)
        
        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#f0f0f0") 
        
        self.Bind(wx.EVT_COMBOBOX, self.Changetask)
        self.Bind(wx.EVT_BUTTON, self.Clickbutton1, id=1)
        self.Bind(wx.EVT_BUTTON, self.Clickbutton2, id=2)
        self.Bind(wx.EVT_BUTTON, self.Clickenvois, id=3)

        wx.EVT_MENU(self, wx.ID_OPEN, self.Configuration)
        wx.EVT_MENU(self, wx.ID_EXIT, self.Quit)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.About)

    def Configuration(self, evt):

        self.Destroy()
        self.frame2=MyFrame2(titre="Configuration PB-CmdBySSH")
        icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

        self.frame2.SetIcon(icone)
       
        self.frame2.Show(True)
        self.Show(False)

    def Quit(self, evt):

        self.Destroy()

    def Changetask(self, evt):
        
        colorpwd = "red"
        color = "black"
        selec = evt.GetSelection()
        
        if (fexist(self.file) == True) and (testcfg(self.file) == True)and (self.testvide != 'vide'):
            
            namesection = []

            cfg = ConfigParser.ConfigParser()
            cfg.read(self.file)

            section = cfg.sections()
            
            for x in section:
              
                namesection.append(cfg.get(x,"name"))
            
            chost = cfg.get(section[int(selec)],"host")
            cport = cfg.get(section[int(selec)],"port")
            cuser = cfg.get(section[int(selec)],"user")
            cpwd = cfg.get(section[int(selec)],"pwd")
            lcmd1 = cfg.get(section[int(selec)],"namecmd1")
            lcmd2 = cfg.get(section[int(selec)],"namecmd2")
            ccmd1 = cfg.get(section[int(selec)],"cmd1")
            ccmd2 = cfg.get(section[int(selec)],"cmd2")
            self.pwd = cpwd

            if testssh(chost, cport, cuser, cpwd) == True:

                self.ctestpwd = "ok"
                colorpwd = "green"

            if testssh(chost, cport, cuser, cpwd) == False:

                self.ctestpwd = "Error"
                colorpwd = "red"

            self.testpwd.SetForegroundColour(colorpwd)
            self.host.SetLabel(chost + ":" + cport)
            self.user.SetLabel(cuser)
            self.testpwd.SetLabel(self.ctestpwd)
            self.button4.SetLabel(lcmd1)
            self.button5.SetLabel(lcmd2)
            self.cmd1.SetLabel(ccmd1)
            self.cmd2.SetLabel(ccmd2)
            evt.Skip()

        return

    def Clickbutton1(self, evt):
        
        if self.ctestpwd=="":
            
            return        

        if (self.testvide == 'vide') or (self.ctestpwd=="Error"):
            
            dlg = wx.MessageDialog(self, "Error Login !" , style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return

        cmd1 = self.cmd1.GetLabel()
        hostport1 = self.host.GetLabel()
        user1 = self.user.GetLabel()        
        pwd1 = self.pwd
        hostport1 = hostport1.split(':')
        host1 = hostport1[0]
        port1 = hostport1[1]
        
        texte = "Command %s executed successfully"%(cmd1)
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if self.cmd1.GetLabel() !='':
        
            try:
 
                ssh.connect(host1, int(port1), username=user1, password=pwd1, timeout=1)

                ssh.exec_command(cmd1)
            
            finally:

                ssh.close()
                 
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()      

    def Clickbutton2(self, evt):
        
        if self.ctestpwd=="":
            
            return                

        if (self.testvide == 'vide') or (self.ctestpwd=="Error"):
            
            dlg = wx.MessageDialog(self, "Error Login !" , style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return        

        cmd2 = self.cmd2.GetLabel()
        hostport2 = self.host.GetLabel()
        user2 = self.user.GetLabel()        
        pwd2 = self.pwd
        hostport2 = hostport2.split(':')
        host2 = hostport2[0]
        port2 = hostport2[1]        

        texte = "Command %s executed successfully"%(cmd2)
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if self.cmd1.GetLabel() !='':
        
            try:
 
                ssh.connect(host2, int(port2), username=user2, password=pwd2, timeout=1)

                ssh.exec_command(cmd2)
            
            finally:

                ssh.close()
                 
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()

    def Clickenvois(self, evt):
        
        if self.ctestpwd=="":
            
            return        

        if (self.testvide == 'vide') or (self.ctestpwd=="Error"):
            
            dlg = wx.MessageDialog(self, "Error Login !" , style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            
            return

        cmdlibre = self.cmdlibre.GetLabel()

        hostport1 = self.host.GetLabel()
        user1 = self.user.GetLabel()        
        pwd1 = self.pwd
        hostport1 = hostport1.split(':')
        host1 = hostport1[0]
        port1 = hostport1[1]

        texte = "Command %s executed successfully"%(cmdlibre)
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if cara(cmdlibre) == False:
        
            texte = "invalid value !"
        
            dlg = wx.MessageDialog(self, texte, "Error !",style = wx.OK | wx.ICON_ERROR)
            retour = dlg.ShowModal()
            dlg.Destroy() 
            self.cmdlibre.SetLabel('')
            evt.Skip()

            return
        
        if self.cmdlibre.GetLabel() !='':
        
            try:
 
                ssh.connect(host1, int(port1), username=user1, password=pwd1, timeout=1)

                ssh.exec_command(cmdlibre)
            
            finally:

                ssh.close()
                 
            dlg = wx.MessageDialog(self, texte, style = wx.OK)
            retour = dlg.ShowModal()
            dlg.Destroy()      

            self.cmdlibre.SetLabel('')
            evt.Skip()

    def About(self, evt):

        description = """
            Envois de Commands a distance par SSH            
           ( Python 2.7, wxPython )
"""
       
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO))
        info.SetName('PB-CmdBySSh')
        info.SetVersion('beta3')
        info.SetDescription(description)
        info.SetCopyright('(C) 2011 PtitBigorneau')
        info.SetWebSite('http://www.ptitbigorneau.fr')
               
        wx.AboutBox(info)

if __name__ == '__main__':

    app = wx.App()
    frame=Myframe(titre="PB-CmdBySSH")
    icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

    frame.SetIcon(icone)
    frame.Show()

    app.MainLoop()





