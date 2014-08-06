'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

class BillionUploads(HostResolver):
    implements = [HostResolver]
    
    name = 'billionuploads'
    
    match_list = ['billionuploads.com']
    
    def Resolve(self, url):
    
        try:
            
            #Show dialog box so user knows something is happening
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving ' + self.name.upper() + ' Link...')
            dialog.update(0)
            
            common.addon.log( self.name.upper() + ' - Link: %s' % url )
            
            import os            
            cookie_file = os.path.join(common.cookies_path, 'billionuploads.lwp')
            
            import cookielib
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)

            import urllib, urllib2, re
            normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            headers = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Language', 'en-US,en;q=0.5'),
                ('Accept-Encoding', ''),
                ('DNT', '1'),
                ('Connection', 'keep-alive'),
                ('Pragma', 'no-cache'),
                ('Cache-Control', 'no-cache')
            ]
            normal.addheaders = headers
            class NoRedirection(urllib2.HTTPErrorProcessor):
                # Stop Urllib2 from bypassing the 503 page.
                def http_response(self, request, response):
                    code, msg, hdrs = response.code, response.msg, response.info()
                    return response
                https_response = http_response
            opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = normal.addheaders
            response = opener.open(url).read()
            decoded = re.search('(?i)var z="";var b="([^"]+?)"', response)
            if decoded:
                decoded = decoded.group(1)
                z = []
                for i in range(len(decoded)/2):
                    z.append(int(decoded[i*2:i*2+2],16))
                decoded = ''.join(map(unichr, z))
                incapurl = re.search('(?i)"GET","(/_Incapsula_Resource[^"]+?)"', decoded)
                if incapurl:
                    incapurl = 'http://billionuploads.com'+incapurl.group(1)
                    opener.open(incapurl)
                    cj.save(cookie_file,True)
                    response = opener.open(url).read()
            captcha = re.search('(?i)<iframe src="(/_Incapsula_Resource[^"]+?)"', response)
            if captcha:
                captcha = 'http://billionuploads.com'+captcha.group(1)
                opener.addheaders.append(('Referer', url))
                response = opener.open(captcha).read()
                formurl = 'http://billionuploads.com'+re.search('(?i)<form action="(/_Incapsula_Resource[^"]+?)"', response).group(1)
                resource = re.search('(?i)src=" (/_Incapsula_Resource[^"]+?)"', response)
                if resource:
                    import random
                    resourceurl = 'http://billionuploads.com'+resource.group(1) + str(random.random())
                    opener.open(resourceurl)
                recaptcha = re.search('(?i)<script type="text/javascript" src="(https://www.google.com/recaptcha/api[^"]+?)"', response)
                if recaptcha:
                    response = opener.open(recaptcha.group(1)).read()
                    challenge = re.search('''(?i)challenge : '([^']+?)',''', response)
                    if challenge:
                        challenge = challenge.group(1)
                        captchaimg = 'https://www.google.com/recaptcha/api/image?c=' + challenge
    #                     site = re.search('''(?i)site : '([^']+?)',''', response).group(1)
    #                     reloadurl = 'https://www.google.com/recaptcha/api/reload?c=' + challenge + '&' + site + '&reason=[object%20MouseEvent]&type=image&lang=en'
                        img = xbmcgui.ControlImage(550,15,300,57,captchaimg)
                        wdlg = xbmcgui.WindowDialog()
                        wdlg.addControl(img)
                        wdlg.show()
                        
                        import xbmc
                        kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
                        kb.doModal()
                        capcode = kb.getText()
                        if (kb.isConfirmed()):
                            userInput = kb.getText()
                            if userInput != '': capcode = kb.getText()
                            elif userInput == '':
                                common.addon.log(self.name.upper() + ' - Image-Text not entered')
                                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Image-Text not entered.[/COLOR]')                
                                return None
                        else: return None
                        wdlg.close()
                        captchadata = {}
                        captchadata['recaptcha_challenge_field'] = challenge
                        captchadata['recaptcha_response_field'] = capcode
                        opener.addheaders = headers
                        opener.addheaders.append(('Referer', captcha))
                        resultcaptcha = opener.open(formurl,urllib.urlencode(captchadata)).info()
                        opener.addheaders = headers
                        response = opener.open(url).read()
                        
            ga = re.search('(?i)"text/javascript" src="(/ga[^"]+?)"', response)
            if ga:
                jsurl = 'http://billionuploads.com'+ga.group(1)
                p  = "p=%7B%22appName%22%3A%22Netscape%22%2C%22platform%22%3A%22Win32%22%2C%22cookies%22%3A1%2C%22syslang%22%3A%22en-US%22"
                p += "%2C%22userlang%22%3A%22en-US%22%2C%22cpu%22%3A%22WindowsNT6.1%3BWOW64%22%2C%22productSub%22%3A%2220100101%22%7D"
                opener.open(jsurl, p)
                response = opener.open(url).read()
    #         pid = re.search('(?i)PID=([^"]+?)"', response)
    #         if pid:
    #             normal.addheaders += [('Cookie','D_UID='+pid.group(1)+';')]
    #             opener.addheaders = normal.addheaders
            if re.search('(?i)url=/distil_r_drop.html', response) and filename:
                url += '/' + filename
                response = normal.open(url).read()
            jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
            if jschl:
                jschl = jschl[0]    
                maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')
                domain_url = re.compile('(https?://.+?/)').findall(url)[0]
                domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
                final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
                html = normal.open(url).read()
            else: html = response
            
            if dialog.iscanceled(): return None
            dialog.update(25)
            
            #Check page for any error msgs            
            if re.search('This server is in maintenance mode', html):
                common.addon.log(self.name.upper() + ' - Site in maintenance mode')
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Site is in maintenance mode.[/COLOR]')
                return None
            if re.search('File Not Found', html):
                common.addon.log(self.name.upper() + ' - File not found')
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]File not found.[/COLOR]')                
                return None

            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', html)
            for name, value in r: data[name] = value
            if not data:
                common.addon.log(self.name.upper() + ' - Data not found')
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Data not found.[/COLOR]')                
                return None
            
            if dialog.iscanceled(): return None
            
            captchaimg = re.search('<img src="((?:http://|www\.)?BillionUploads.com/captchas/.+?)"', html)            
            if captchaimg:

                img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
                
                import xbmc
                kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
                kb.doModal()
                capcode = kb.getText()
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '': capcode = kb.getText()
                    elif userInput == '':
                        common.addon.log(self.name.upper() + ' - Image-Text not entered')
                        common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Image-Text not entered.[/COLOR]')                
                        return None
                else: return None
                wdlg.close()
                
                data.update({'code':capcode})
            
            if dialog.iscanceled(): return None
            dialog.update(50)
            
            data.update({'submit_btn':''})
            enc_input = re.compile('decodeURIComponent\("(.+?)"\)').findall(html)
            if enc_input:
                dec_input = urllib2.unquote(enc_input[0])
                r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', dec_input)
                for name, value in r:
                    data[name] = value
            extradata = re.compile("append\(\$\(document.createElement\('input'\)\).attr\('type','hidden'\).attr\('name','(.*?)'\).val\((.*?)\)").findall(html)
            if extradata:
                for attr, val in extradata:
                    if 'source="self"' in val:
                        val = re.compile('<textarea[^>]*?source="self"[^>]*?>([^<]*?)<').findall(html)[0]
                    data[attr] = val.strip("'")
            r = re.findall("""'input\[name="([^"]+?)"\]'\)\.remove\(\)""", html)
            
            for name in r: del data[name]
            
            normal.addheaders.append(('Referer', url))
            html = normal.open(url, urllib.urlencode(data)).read()
            cj.save(cookie_file,True)
            
            if dialog.iscanceled(): return None
            dialog.update(75)
            
            def custom_range(start, end, step):
                while start <= end:
                    yield start
                    start += step

            def checkwmv(e):
                s = ""
                i=[]
                u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
                for z in range(0, len(u)):
                    for n in range(u[z][0],u[z][1]):
                        i.append(chr(n))
                t = {}
                for n in range(0, 64): t[i[n]]=n
                for n in custom_range(0, len(e), 72):
                    a=0
                    h=e[n:n+72]
                    c=0
                    for l in range(0, len(h)):            
                        f = t.get(h[l], 'undefined')
                        if f == 'undefined': continue
                        a = (a<<6) + f
                        c = c + 6
                        while c >= 8:
                            c = c - 8
                            s = s + chr( (a >> c) % 256 )
                return s

            dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)
            if dll:
                dl = dll[0].split('GvaZu')[1]
                dl = checkwmv(dl);
                dl = checkwmv(dl);
            else:
                alt = re.compile('<source src="([^"]+?)"').findall(html)
                if alt:
                    dl = alt[0]
                else:
                    common.addon.log(self.name.upper() + ' - File not found')
                    common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]File not found.[/COLOR]')
                    return None
            
            if dialog.iscanceled(): return None
            dialog.update(100)                    

            return dl
            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None
        finally:
            dialog.close()