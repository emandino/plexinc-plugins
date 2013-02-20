HTTP_DESKTOP_UA = {
    'Host':'www.fshare.vn',
    'Accept-Encoding':'gzip, deflate',
    'Referer':'https://www.fshare.vn/login.php',
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'
}


MY_URL="https://raw.github.com/trungk43/plexinc-plugins/master/"
MASTER_URL="https://raw.github.com/trungk43/plexinc-plugins/master/master.xml"

###################################################################################################
def Start():
  Plugin.AddPrefixHandler("/video/fshare-plugin", MainMenu, "FShare")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  Plugin.AddViewGroup("List2", viewMode="List", mediaType="items")
  Plugin.AddViewGroup("List3", viewMode="List", mediaType="items")

  ObjectContainer.title1     = "FShare"
  ObjectContainer.view_group = "InfoList"

  Dict.Reset()
  Authenticate()

####################################################################################################

def ValidatePrefs():
  Authenticate()

####################################################################################################
def MainMenu():
  oc = ObjectContainer(view_group="List")

  if 'loggedIn' in Dict and Dict['loggedIn'] == True:
    oc.add(DirectoryObject(key=Callback(MainMenu1), title="fslink.us"))
    oc.add(DirectoryObject(key=Callback(MyHD), title="My HD"))

  oc.add(PrefsObject(title = L('Preferences')))
  
  return oc
  
  
####################################################################################################
def MainMenu1():
  oc = ObjectContainer(view_group="List")

  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/series/'), title="series"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/series/us-tv-series/'), title="us-series"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/18/'), title="18+"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/3d/'), title="3d"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/western/'), title="Western"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/war/'), title="War"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/animation/'), title="Animation"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/mystery/'), title="Mystery"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/comedy/'), title="Comedy"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/action/'), title="Action"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/crime/'), title="Crime"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/horror/'), title="Horror"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/romance/'), title="Romance"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/history/'), title="History"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/adventure/'), title="Adventure"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/thriller/'), title="Thriller"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/documentary/'), title="Documentary"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/drama/'), title="Drama"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/fantasy/'), title="Fantasy"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/family/'), title="Family"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/thuyet-minh-tieng-viet/'), title="Thuyet minh"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/tvb/'), title="TVB"))
  oc.add(DirectoryObject(key=Callback(MainMenu2,url='http://fslink.us/category/phim-2/vietnamese/'), title="vietnamese"))


  return oc

####################################################################################################
# sample link http://fslink.us/category/phim-2/series/us-tv-series/
def MainMenu2(url):
  oc = ObjectContainer(view_group="List")

  page = HTML.ElementFromURL(url)

  videos = page.xpath("//h3[@class='entry-title']//a")
  for video in videos:
    oc.add(DirectoryObject(key=Callback(MoviesList,url=video.get('href')), title=video.text))
  
  pages = page.xpath("//div[@class='wp-pagenavi']//a")
  for link in pages:
    oc.add(DirectoryObject(key=Callback(MainMenu2,url=link.get('href')), title=link.text))
  
  return oc

####################################################################################################
# FShare folder
# sample link http://www.fshare.vn/folder/T72QCQK06T/
def MainMenu3(url):
  oc = ObjectContainer(view_group="List")

  page = HTML.ElementFromURL(url)

  videos = page.xpath("//li[@class]//a[contains(@href, 'fshare.vn/file/')]")
  for video in videos:
    oc.add(VideoClipObject(
      url=video.get('href'), 
      title=page.xpath("//a[contains(@href, '"+video.get('href')+"')]//span")[0].text,
      thumb = None,
      duration = None )
      )  
  
  return oc

####################################################################################################
def MyHD():
  oc = ObjectContainer(view_group="List")

  page = XML.ElementFromURL(MASTER_URL)

  cats = page.xpath("//category")
  for cat in cats:
    oc.add(DirectoryObject(key=Callback(MainMenuMyHD,url=MY_URL+cat.get('file')), title=cat.get('title')))

  return oc

####################################################################################################
# MyHD folder
def MainMenuMyHD(url):
  oc = ObjectContainer(title2='fslink')

  page = XML.ElementFromURL(url)

  videos = page.xpath("//movie")
  for video in videos:
    url1=video.xpath(".//url")[0].text
    if url1.find('file') > 0:
      oc.add(VideoClipObject(
        url=url1, 
        title=video.xpath(".//title")[0].text,
        thumb = None,
        duration = None )
        )  
    else:
      oc.add(DirectoryObject(key=Callback(MainMenu3,url=url1), title=video.xpath(".//title")[0].text))

  return oc
  
####################################################################################################
# sample link http://fslink.us/2013/02/03/cuoc-chien-no-le-spartacus-war-of-the-damned-2013-phan-4-3/
def MoviesList(url):

  oc = ObjectContainer(title2='fslink')

  page = HTML.ElementFromURL(url)

  videos = page.xpath("//a[contains(@href, 'fshare.vn/file/')]")
  for video in videos:
    oc.add(VideoClipObject(
      url=video.get('href'), 
      title=video.text,
      thumb = None,
      duration = None )
      )  

  folders = page.xpath("//a[contains(@href, 'fshare.vn/folder/')]")
  for folder in folders:
    if len(folder.xpath(".//strong"))>0:
	  title1=folder.xpath(".//strong")[0].text
    else:
	  title1=folder.text
    oc.add(DirectoryObject(key=Callback(MainMenu3,url=folder.get('href')), title=title1))

  return oc
  
####################################################################################################
## AUTHENTICATION
####################################################################################################
 
def Authenticate():

  # Only when username and password are set
  Dict['loggedIn'] = False
  if Prefs['fshare_user'] and Prefs['fshare_passwd']:
    try:
      headers = HTTP_DESKTOP_UA

      req = HTTP.Request('http://www.fshare.vn/logout.php').content
      
      req = HTTP.Request('https://www.fshare.vn/login.php', headers=headers, timeout=5, values=dict(
        login_useremail = Prefs['fshare_user'],
        login_password = Prefs['fshare_passwd'],
        url_refe = "https://www.fshare.vn/index.php"
      ))
	  
      cookies = HTTP.CookiesForURL('https://www.fshare.vn/') 
      if cookies.find('fshare_userid=-1')<0:
        Dict['loggedIn'] = True
        Log("Login Successful")
      else:
        Dict['loggedIn'] = False
        Log("Login Failed")
      return True

    except:
      Dict['loggedIn'] = False
      Log("Login Failed")
      return False

  else:
    return False