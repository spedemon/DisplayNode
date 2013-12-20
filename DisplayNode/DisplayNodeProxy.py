
# Display Node - Python and Javascript plotting and data visualisation. 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# 20 Oct 2013, Helsinki 



from DisplayNodeServer import DisplayNodeServer
from DisplayNodeServer import PROXY_ADDRESS,PROXY_PORT,WEB_ADDRESS,WEB_PORT
from xmlrpclib import Server, Binary  
import webbrowser
import sys
import socket

import platform 
if platform.system() == "None": 
    from multiprocessing import Process
    import signal
    USE_MULTIPROCESSING = True
else:
    import thread
    USE_MULTIPROCESSING = False

socket.setdefaulttimeout(2)

WIDTH  = 900 #FIXME: obtain display specific width and height form the server
HEIGHT = 500

class DisplayNode(): 
    def __init__(self,proxy_address=(PROXY_ADDRESS,PROXY_PORT), web_address=(WEB_ADDRESS,WEB_PORT)): 
        self._proxy = Server('http://%s:%s'%proxy_address) 
        self.start_server(proxy_address,web_address) 
        self.data = None
        self.type = None
        self.url = None
        self.width = 0
        self.height = 0
        # FIXME: use introspection to define the methods (for autocompletion) 

    def start_server(self,proxy_address,web_address): 
        if not self.is_server_responding(): 
            self._server = DisplayNodeServer(proxy_address,web_address)
            if USE_MULTIPROCESSING: 
                print "Multiprocessing version! "
                self._server_process = Process( target=self.__run_server_forever, args=() )
                self._server_process.start()
            else: 
                thread.start_new_thread( self.__run_server_forever, () )
    
    def __run_server_forever(self): 
        if USE_MULTIPROCESSING: 
            signal.signal(signal.SIGINT, self.__signal_handler_interrupt)
        self._server.serve_forever() 

    def __signal_handler_interrupt(self, signal, frame):
        print 'Shutting down DisplayNode server. '
        sys.exit(0)
    
    def is_server_responding(self): 
        try:
            alive = self._proxy.is_alive(1) 
        except: 
            alive = False
        return alive 

    def display(self,content_type,data={},open_browser=False,new_tab=False,autoraise=False): 
        # if image: send png content
        if content_type=="image": 
            from StringIO import StringIO
            buf = StringIO()
            data.convert("RGB").save(buf,format="PNG") 
            data = Binary(buf.getvalue()) 
            buf.close() 
        url = self._proxy.display({'type':content_type,'data':data}) 
        if open_browser:
            if new_tab:  
                webbrowser.open_new_tab(url) 
            else:
                webbrowser.open(url,autoraise=autoraise) 
        self.data = data
        self.type = content_type
        self.url = url
        self.width = WIDTH  #FIXME: obtain width and height from the server
        self.height = HEIGHT
        return self

    def display_in_browser(self,content_type,data={},new_tab=False,autoraise=False): 
        self.display(content_type,data,open_browser=True,new_tab=new_tab,autoraise=autoraise)
        return None 

    def _repr_html_(self): 
        # This method is for ipython notebook integration through Rich Display
        return '<iframe src=%s width=%d height=%d frameborder=0></iframe>'%(self.url,self.width,self.height)


if __name__ == "__main__": 
    D = DisplayNodeServer()
    D.display('graph','') 

