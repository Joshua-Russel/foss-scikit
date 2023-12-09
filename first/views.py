from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
from sklearn.preprocessing import MaxAbsScaler,OneHotEncoder
from sklearn.neighbors import NearestNeighbors

# Create your views here.
def demo1(request):
   return render(request,'samp.html')
def demo2(request):
    name=request.GET['search-input']
    print(name)
    dataset = pd.read_csv('first/dataset/anime_new.csv')

    filtered_data = dataset[dataset["episodes"]=="Unknown"]

    new_ratings=pd.read_csv('first/dataset/anime_updated.csv')
    dataset.update(new_ratings)
    new_filtered_data = dataset[dataset["episodes"]=="Unknown"]

    dataset.loc[(dataset["type"]=="OVA") & (dataset["episodes"]=="Unknown"),"episodes"] = "1"
    dataset.loc[(dataset["type"] == "Movie") & (dataset["episodes"] == "Unknown"),"episodes"] = "1"

    dataset.drop(dataset.loc[dataset["episodes"]=="Unknown"].index, inplace=True)

    dataset["rating"] = dataset["rating"].astype(float)

    dataset.dropna(subset = ["rating"], inplace=True)

    pd.get_dummies(dataset[["type"]]).head()

    dataset["members"] = dataset["members"].astype(float)

# df=dataset.iloc[:,2:4]
# df.genre.unique().tolist()

# anime_features=OneHotEncoder(handle_unknown='ignore')
# anime_features.fit([df.genre.unique(),df.type.unique()])

    anime_features = pd.concat([dataset["genre"].str.get_dummies(sep=","),pd.get_dummies(dataset[["type"]]),dataset[["rating"]],dataset[["members"]],dataset["episodes"]],axis=1)
    dataset["name"] = dataset["name"].map(lambda name:re.sub('[^A-Za-z0-9]+', " ", name))



    max_abs_scaler = MaxAbsScaler()
    anime_features = max_abs_scaler.fit_transform(anime_features)
    nearest_neighbours = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(anime_features)
    distances, indices = nearest_neighbours.kneighbors(anime_features)

    all_anime_names = list(dataset.name.values)

    

  
    found_id =dataset[dataset["name"]==name].index.tolist()[0]
    print("Your Search:",name," | Its  Genre is :",dataset.loc[found_id]["genre"]," || Rating:",dataset.loc[found_id]["rating"],"|| Episodes:",dataset.loc[found_id]["episodes"])
    print("==================================")
    print("RECOMMENDATIONS--")
    print("==================================")
    array=[]
    for id in indices[found_id][1:]:
         array.append(dataset.loc[id]["name"])
    print(array)    
    return render(request,'samp.html',{'array':array})
   
