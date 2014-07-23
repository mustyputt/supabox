import xbmc,xbmcgui

#CONSTANTS
heading = sys.argv[1]
anounce = sys.argv[2]

def TextBoxes(heading,anounce):
##
# Shows text window, can be used for FAQ, etc. 
#
# heading = window heading string
# anounce = string or filename in root plugin directory to show
#
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                        self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()

TextBoxes(heading, anounce)
