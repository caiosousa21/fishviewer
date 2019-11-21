import json
from urllib.request import urlopen
import pandas as pd
import requests
from rdflib import Graph, Namespace, URIRef, Literal
from bs4 import BeautifulSoup
from os import path
from PIL import Image

def LoadRDF(limit):
    # Load JSON
    url = 'https://fishbase.ropensci.org/species?limit='+str(limit)
    f = urlopen(url)
    data = json.load(f)
    fishesData = data['data']
    f.close()


    # Getting Fish image
    def getFish(fishName=None):
        url = ('https://www.google.com/search?q=' + fishName + '+fish&tbm=isch')
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        img = soup.findAll("img")
        img = img[1]
        return img['src']

    #Build fish object
    def buildFishbase(argFish=None):
        fish = {}
        fish['SpecCode'] = argFish["SpecCode"]
        fish['Species'] = argFish["Species"]
        fish['Genus'] = argFish["Genus"]
        fish['image'] = getFish(argFish['Species'])
        fish['Subfamily'] = argFish["Subfamily"]
        fish['Comments'] = argFish["Comments"]
        fish['Siblings'] = 'None'
        return fish

    #Check if there are other species with the same genus
    def checkSibling(specCode=None, genus=None):
        siblings = []
        siblings.append(specCode)
        for f in fishesData:
            if f['SpecCode'] != specCode and f['Genus'] == genus:
                siblings.append(f['SpecCode'])
        return siblings

    #Build DataFrame
    rowsFishbase = []

    for f in fishesData:
        rowsFishbase.append(buildFishbase(f))
        fishbasedf = pd.DataFrame(rowsFishbase)

    #Defining Graph and types
    g = Graph()
    fishing = Namespace('https://fishbase.ropensci.org/#')
    sf = Namespace('https://fishbase.ropensci.org/siblings#')
    img = Namespace('https://www.google.com/search?q=#')

    # Siblings
    i = 1
    for index, row in fishbasedf.iterrows():
        siblings = checkSibling(row['SpecCode'], row['Genus'])
        dRef = URIRef('sf'+str(i))
        if len(siblings) > 1:
            g.add((dRef, sf.sibling, Literal(siblings)))
            g.add((URIRef(str(row['SpecCode'])), fishing.family, Literal(dRef)))
            i = i+1

    #Fishbase
    for index, row in fishbasedf.iterrows():
        dRef = URIRef(str(row['SpecCode']))
        g.add((dRef, fishing.species, Literal(row['Species'])))
        g.add((dRef, fishing.genus, Literal(row['Genus'])))
        g.add((dRef, img.images, Literal(row['image'])))
        g.add((dRef, fishing.subfamily, Literal(row['Subfamily'])))
        g.add((dRef, fishing.comments, Literal(row['Comments'])))


    # Exportando para um arquivo
    g.serialize(destination=f'fishbase.txt', format='turtle')
    print(f'Grafos RDF em fishbase.txt')


def queryGraph():
    g = Graph()
    filename = 'fishbase.txt'
    g.parse(filename, format='turtle')
    ans = g.query(
        """SELECT ?x ?y ?z
          WHERE {
          ?a ns1:species ?x .
          ?a ns2:images ?y  .
          ?a ns1:family ?z  .
          }"""
    )
    for item in ans:
        print ('Species: ' + item.x + '\nImage Source: ' + item.y + '\nFamily code : ' + item.z + '\n')
        img = Image.open(requests.get(str(x.y), stream=True).raw)
        img.show()


    ans = g.query(
        """SELECT ?x
          WHERE {
          ?a ns3:sibling ?x .
          }"""
    )
    for item in ans:
        print('Siblings: ' + item.x + '\n')

#Get limit
try:
    if path.exists("fishbase.txt") :
        inpt = input("Would you like to generate a new RDF file? (y:yes / anything else:no): ")
        if inpt == 'y':
            limit = input("Enter the number of species you'd like to see: ")
            limit = int(limit)
            LoadRDF(limit)
        else:
            print("Proceeding then.")
    else:
        limit = input("Enter the number of species you'd like to see: ")
        limit = int(limit)
        LoadRDF(limit)
    queryGraph()
except ValueError as e:
    if not limit:
        print("Empty!")
    else:
        print("Invalid input!")


