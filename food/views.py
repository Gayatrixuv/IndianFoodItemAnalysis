import base64
import io
import urllib

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS


from django.shortcuts import render, redirect
# import geopandas as gpd

# %matplotlib inline

from .models import Graphs, Data

import csv
def index(request):

    # filename = "C:\\Users\\Gayatri Patil\\Downloads\\indian_food.csv"
    #
    # # initializing the titles and rows list
    # fields = []
    # rows = []
    #
    # # reading csv file
    # with open(filename, 'r') as csvfile:
    #     # creating a csv reader object
    #     csvreader = csv.reader(csvfile)
    #
    #     # extracting field names through first row
    #     fields = next(csvreader)
    #
    #     # extracting each data row one by one
    #     for row in csvreader:
    #         rows.append(row)
    #         d=Data()
    #         d.Name=row[0]
    #         d.Ingredient=row[1]
    #         d.Diet=row[2]
    #         d.PrepTime=row[3]
    #         d.CookTime=row[4]
    #         d.Flavor=row[5]
    #         d.Course=row[6]
    #         d.State=row[7]
    #         d.Region=row[8]
    #
    #         d.save()

    # csv file name

    graph1=Graphs.objects.get(Name='Number of Recipes and States')
    graph2=Graphs.objects.get(Name='Veg Vs Non-Veg Dishes')
    graph3 = Graphs.objects.get(Name='Recipes and Thier Cooking Time')
    graph4 = Graphs.objects.get(Name='Course Wise')
    graph5 = Graphs.objects.get(Name='Flavour Profile')
    graph6 = Graphs.objects.get(Name='Region Profile')
    graph7 = Graphs.objects.get(Name='Most Used Ingrdiants')

    graphs={
        'graph1':graph1,
             'graph2' : graph2,
               'graph3':graph3,
               'graph4':graph4,
               'graph5':graph5,
               'graph6':graph6,
                 'graph7':graph7
    }
    Vegs=Data.objects.filter(Diet='vegetarian')[:10]
    Nonvegs = Data.objects.filter(Diet='non vegetarian')[:10]
    items=Data.objects.all()[:10]
    quickRecipes=Data.objects.filter(CookTime__lte=30)[:10]
    MediumTimeRecipes=Data.objects.filter(CookTime__lte=60,CookTime__gt=30)[:10]
    context={
        'graphs':graphs,
        'items':items,
        'Vegs':Vegs,
        'Nonvegs':Nonvegs,
        'quickRecipes':quickRecipes,
        'MediumTimeRecipes':MediumTimeRecipes,
    }

    # Graphs.objects.all().delete()
    return render(request, 'index.html', context)


def UpdateDashboard(request):

    filename = "C:\\Users\\Gayatri Patil\\Downloads\\indian_food.csv"

    indian_recipes = filename
    df_indian_recipes = pd.read_csv(indian_recipes)
    print("shape", df_indian_recipes.shape, sep=": ")

    sns.set_style('darkgrid')
    matplotlib.rcParams['font.size'] = 14
    matplotlib.rcParams['figure.figsize'] = (9, 5)
    matplotlib.rcParams['figure.facecolor'] = '#00000000'

    df = pd.read_csv("C:\\Users\\Gayatri Patil\\Downloads\\indian_food.csv ")

    recipe_by_state = df_indian_recipes.groupby('state').size().to_frame(name="count").reset_index()
    sns.barplot(x='count', y='state', data=recipe_by_state)

    plt.title("Recipes by State")
    plt.xlabel("State")
    plt.ylabel("Count of recipes")

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    buf.close()
    graph1 = uri

    try:
        graph=Graphs.objects.get(Name="Number of Recipes and States")
    except:
        graph=Graphs()
        graph.Name = 'Number of Recipes and States'


    graph.Image=uri
    graph.save()


    df_diet = df[["diet"]].copy()
    df_diet["count"] = 1
    df_diet = df_diet.groupby("diet").count()
    df_diet.head()
    fig, axes = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw=dict(wspace=0.1, hspace=0.6))
    fig.suptitle("Analisys of diet", fontsize=15)

    g_diet = sns.countplot(data=df, x="diet", order=df['diet'].value_counts().index,
                           ax=axes[0])
    g_diet.set_title("diet countplot")

    g_diet_pie = df_diet.plot.pie(y="count", ax=axes[1])
    g_diet_pie.set_title("diet pie plot")
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    buf.close()
    graph2= uri

    try:
        graph = Graphs.objects.get(Name="Veg Vs Non-Veg Dishes")
    except:
        graph = Graphs()
        graph.Name = 'Veg Vs Non-Veg Dishes'

    graph.Image = uri
    graph.save()

    df_cook_time = (df_indian_recipes.prep_time + df_indian_recipes.cook_time).to_frame('total_time').reset_index()
    plt.hist(df_cook_time['total_time'],np.arange(5, 150, 10))
    plt.title("Cooking time")
    plt.ylabel("Number of recipes")
    plt.xlabel("Time in minutes")
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    buf.close()
    graph3 = uri

    try:
        graph = Graphs.objects.get(Name="Recipes and Thier Cooking Time")
    except:
        graph = Graphs()
        graph.Name = 'Recipes and Thier Cooking Time'

    graph.Image = uri
    graph.save()

    # plt.figure(figsize=(10, 15))
    # plt.title("state vs cooking time for veg/non veg")
    # sns.barplot(x='cook_time', y='state', data=df, hue='diet')
    # fig = plt.gcf()
    # buf = io.BytesIO()
    # fig.savefig(buf, format='png')
    # buf.seek(0)
    # string = base64.b64encode(buf.read())
    # uri = urllib.parse.quote(string)
    # plt.close()
    # buf.close()
    # graph7 =uri
    #
    # try:
    #     graph = Graphs.objects.get(Name="State VS Cooking Time")
    # except:
    #     graph = Graphs()
    #     graph.Name = 'State VS Cooking Time'
    #
    # graph.Image = uri
    # graph.save()

    df_course = df_indian_recipes.course.value_counts().reset_index()
    sns.barplot(x='course', y='index', data=df_course)
    plt.title("Cuisines")
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    buf.close()
    graph4 = uri

    try:
        graph = Graphs.objects.get(Name="Course Wise")
    except:
        graph = Graphs()
        graph.Name = 'Course Wise'

    graph.Image = uri
    graph.save()

    fig, axes = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw=dict(wspace=0.1, hspace=0.6))
    fig.suptitle("Analisys of flavor profile", fontsize=15)

    g_flavor_profile = sns.countplot(data=df, x="flavor_profile", ax=axes[0],
                                     order=df['flavor_profile'].value_counts().index)
    g_flavor_profile.set_title("flavor profile countplot")
    df_flavor_profile = df[["flavor_profile"]].copy()
    df_flavor_profile["count"] = 1
    df_flavor_profile = df_flavor_profile.groupby("flavor_profile").count()
    g_flavor_profile_pie = df_flavor_profile.plot.pie(y="count", ax=axes[1])
    g_flavor_profile_pie.set_title("flavor profile pie plot")
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    buf.close()
    graph5 =uri

    try:
        graph = Graphs.objects.get(Name="Flavour Profile")
    except:
        graph = Graphs()
        graph.Name = 'Flavour Profile'

    graph.Image = uri
    graph.save()

    fig, axes = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw=dict(wspace=0.1, hspace=0.6))
    fig.suptitle("Analisys of region", fontsize=15)

    g_region = sns.countplot(data=df, x="region", order=df['region'].value_counts().index, ax=axes[0])
    g_region.set_title("region countplot")

    g_region = sns.countplot(data=df, x="region", hue="flavor_profile", ax=axes[1],
                             order=df['region'].value_counts().index)
    g_region.legend_._loc = 1
    g_region.set_title("taste countplot per region")

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    buf.close()
    graph6=uri

    try:
        graph = Graphs.objects.get(Name="Region Profile")
    except:
        graph = Graphs()
        graph.Name = 'Region Profile'

    graph.Image = uri
    graph.save()

    comment_words = ''
    for i in df.ingredients:
        i = str(i)
        separate = i.split()
        for j in range(len(separate)):
            separate[j] = separate[j].lower()

        comment_words += " ".join(separate) + " "
    wordcloud_spam = WordCloud(background_color="white").generate(comment_words)
    # Displaying the WordCloud
    plt.figure(figsize=(9, 9), facecolor=None)
    plt.imshow(wordcloud_spam)
    plt.axis("off")
    plt.tight_layout(pad=0)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close()
    buf.close()
    graph7 = uri

    try:
        graph = Graphs.objects.get(Name="Most Used Ingrdiants")
    except:
        graph = Graphs()
        graph.Name = 'Most Used Ingrdiants'

    graph.Image = uri
    graph.save()

    return redirect('index')





