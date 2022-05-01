Youtube Analysis and Prediction 
==============================

 Youtube Categorical Analysis By using Trending Youtube video statistics for several countries

 Originally  we used  [this dataset](https://www.kaggle.com/datasnaek/youtube-new) on Kaggle, which has about 6 months worth of trending YouTube videos on it. This dataset has the most relevant information from videos that are currently trending on YouTube in a specified set of countries[Canda, USA, France, Japan, Korea, Mixico, Russia, Denemark ].

 But this dataset also don't have the mose important info __in our opinion__ the length of each video so have scrapping this info from youtube by using video id

Our Steps
------------
1. Mapping  Category_id with Category title for each conuntry , Because This data also includes a category_id field, which varies between regions. To retrieve the categories for a specific video, find it in the associated JSON. One such file is included for each of the five regions in the dataset. 

2. Then we merging all Countries datasets in one dataset

3. Randomly we choosen nearly __10K__ videos to scrappe thier lenght 

4. Our final step we have done some Exploratroy Data Analysis 


How to run this app
------------
1. First, clone this repository and open a terminal inside the root folder.

2. Create and activate a new virtual environment (recommended) by running the following:
```
python3 -m venv myvenv
source myvenv/bin/activate
```

3. Install requirements
```
pip install -r requirements.txt
```

4. Change directory to src folder

```
cd src/
```

5. Run the app
```
python app.py

```

6. Open a browser at http://127.0.0.1:8050
--------

