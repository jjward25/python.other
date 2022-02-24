import pandas as pd
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

## Initial Excel reading and dataframe creation
articleDF = pd.read_excel('C:/Users/Josep/OneDrive/Desktop/Coding/next.nutshell-news/public/NutshellSampleData.xlsx',engine='openpyxl')
#print(articleDF)
inputObj = articleDF.to_dict(orient='index')  ## Turns every row into an object
#print(inputObj)

##########
# Create a master list with objects for each unique section
##########
sectionList = []
## Creates a key:value pair for each section, with an array for categories
for contentRowObj in inputObj.values():
        if contentRowObj['Section'] not in sectionList:
            sectionList.append(contentRowObj['Section'])           
#print(sectionList)

########
# Create arrays of Category object for each section
########
contentObj = {}
for section in sectionList:      
    categoryList = []
    catDupes = []
    for contentRowObj in inputObj.values():
        if contentRowObj['Section'] == section:
            categoryDict = {}   
            categoryDict.setdefault("CategoryName",contentRowObj['Category'])
            categoryDict.setdefault("CategoryPriority",contentRowObj['CategoryPriority'])
            catDupes.append(categoryDict)
            categoryList = [i for n, i in enumerate(catDupes) if i not in catDupes[n + 1:]]
            contentObj[contentRowObj['Section']]=categoryList
        else:
            continue        
print(contentObj)


##########
# For each Category Object, add a list of Post objects; unique objects for each post, with PostName, PostDate, PostPriority, etc. and then a SubHeaderObjArray:[{}]
##########
for categoryObjList in contentObj.values():
    #print(categoryObjList)
    for categoryObj in categoryObjList:
        #print(categoryObj)
        postList = []
        postDupes = []
        postNames = []
        ## Iterate through the dataset rows for category match, then create the post objects to append to the post array
        for contentRowObj in inputObj.values():
            if contentRowObj['Category'] == categoryObj['CategoryName']:
                postDict = {}
                postDict.setdefault("PostName",contentRowObj['PostName'])
                postDict.setdefault("PostPriority",contentRowObj['PostPriority'])
                postDict.setdefault("PostDate",contentRowObj['PostDate'])
                postDict.setdefault("PostUpDate",contentRowObj['PostUpDate'])
                
                if contentRowObj['PostName'] not in postNames:
                   postDupes.append(postDict)
                   postNames.append(contentRowObj['PostName']) ## Fill list w postNames so the next time the postName comes up it's in the list and no object will be created
                else:
                    continue
            else:
                continue

        postList = [i for n, i in enumerate(postDupes) if i not in postList[n + 1:]]  
        categoryObj.setdefault("PostArray",postList)



##########
# For each Post Object, add a list of Subheader objects; unique objects for each subheader, with SHName, SHPriority, etc. and then a BulletObjArray:[{}]
##########
for categoryObjList in contentObj.values():
    
    for categoryObj in categoryObjList:
        
        for postObj in categoryObj['PostArray']:
            shList = []
            shDupes = []
            shNames = []
        ## Iterate through the dataset rows for category match, then create the post objects to append to the post array
            for contentRowObj in inputObj.values():
                if contentRowObj['PostName'] == postObj['PostName']:
                    shDict = {}
                    shDict.setdefault("SubheaderName",contentRowObj['SubheaderName'])
                    shDict.setdefault("SubheaderPriority",contentRowObj['SubheaderPriority'])
            
                    if contentRowObj['SubheaderName'] not in shNames:
                        shDupes.append(shDict)
                        shNames.append(contentRowObj['SubheaderName']) ## Fill list w postNames so the next time the postName comes up it's in the list and no object will be created
                    else:
                        continue
                else:
                    continue

            shList = [i for n, i in enumerate(shDupes) if i not in shList[n + 1:]]  
            postObj.setdefault("SubheaderArray",shList)
            #pp.pprint(sectionList)


##########
# For each Subheader Object, add a list of bullet objects; unique objects for each bullet, with all remaining bullet details
##########
for categoryObjList in contentObj.values():
    
    for categoryObj in categoryObjList:
        
        for postObj in categoryObj['PostArray']:

            for shObj in postObj['SubheaderArray']:  ## For each subheader 
                bulletList = []
                bulletDupes = []
                bulletNames = []
                for contentRowObj in inputObj.values(): ## Iterate through the dataset rows for a subheader match, then create the post objects to append to the post array
                    if contentRowObj['PostName']+contentRowObj['SubheaderName'] == postObj['PostName']+shObj['SubheaderName']:
                        bulletDict = {}
                        bulletDict.setdefault("BulletText",contentRowObj['BulletText'])
                        bulletDict.setdefault("BulletPriority",contentRowObj['BulletPriority'])
                        bulletDict.setdefault("BulletCite",contentRowObj['BulletCite'])
                        bulletDict.setdefault("BulletLink",contentRowObj['BulletLink'])
                        bulletDict.setdefault("BulletPostDate",contentRowObj['BulletPostDate'])
                        bulletDict.setdefault("BulletUpDate",contentRowObj['BulletUpDate'])
                        
                        if contentRowObj['BulletText'] not in bulletNames:
                            bulletDupes.append(bulletDict)
                            bulletNames.append(contentRowObj['BulletText']) 
                        else:
                            continue
                    else:
                        continue

                bulletList = [i for n, i in enumerate(bulletDupes) if i not in bulletList[n + 1:]]  
                shObj.setdefault("BulletArray",bulletList)
                #pp.pprint(sectionList)

pp.pprint(contentObj)
with open("content.json", "w") as write_file:
    json.dump(contentObj, write_file, indent=4)
    