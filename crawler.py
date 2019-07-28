import re
##I've picked urllib parse over request because it's much simpler and according to most reports at least twice as fast
import urllib.request




#input
search = input("What term are you searching?")


#google result page
try:
    url= "https://www.google.com/search?q="+search
    

    headers={}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    string = str(resp.read())




    
except Exception as e:
    print(str(e))





search_results = re.findall(r'href="https:\/\/\w{2,3}\..{0,20}\.\w{2,5}[^"]{0,40}"',string)
del string


list_of_libraries=[]
for x in search_results:
    
    #to clear all the unnecessary google links
    if re.search('www.google',x):
        continue

    #to make the names for the normal files
    v = re.sub('href="','',x)
    l = re.sub('"','',v)
    try:
        url= str(l)
        headers={}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        responseData = resp.read()
        
        prefilename = str(re.sub(r'https://','',l))
        pre_filename = str(re.sub(r'/','_',prefilename))
        filename = str(re.sub(r'\?','_',pre_filename))
        saveFile = open(filename+'.html','w')
        saveFile.write(str(responseData))
        saveFile.close()


    
    except Exception as e:
        print(str(e))

    file = open(filename+'.html','r')
    string = file.read()
    file.close()
    
    #finding the javascript libraries
    library_check = re.findall(r'<script\ssrc=".{0,40}\.js',string)

    #to clean the directories
    cleaned_libraries = []
    for y in library_check:

        xyz=re.findall(r'\/[^\/]+\.js',y)
        vz = str(xyz).replace("['/",'').replace("']",'')
        
        ##deduplication algorithm for the same JavaScript libraroes with different names
        cleaned_libraries.append(re.sub(r'\.min','_',str(vz)))

    for y in cleaned_libraries:    
        list_of_libraries.append(y)


#creating a set of libraries so I may use it to rank the libraries by use
the_set_of_libraries = set(list_of_libraries)
library_rankings ={}

#instead of this I'd use numpy or Counter() but the task is without third party libraries
#they would also speed up the code
for x in the_set_of_libraries:
    number = 0
    for y in list_of_libraries:
        if x==y:
            number+=1
    name = x
    library_rankings.update({name:number})


library_rankings_top = sorted(library_rankings)


#printing the top 5 most used libraries in the search
print("Top five most used libraries:")
for x in range(0,5):
    print(str(x+1)+" "+library_rankings_top[x])




