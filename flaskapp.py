from flask import Flask,render_template,request
import time

#easier to read csv file using pandas
import pandas as pd

#to make data to be in an acceptable format in the form of an array as python doesnt have an array
#import numpy as np
from numpy import vstack

#use Kmeans algorithm
from scipy.cluster.vq import kmeans,vq

#to make the the graph
import pygal
from pygal.style import DefaultStyle, DarkGreenBlueStyle
custom_style = DarkGreenBlueStyle(colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53'))





app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cluster')
def cluster():
    # values required
    col1 = request.args.get('col1')
    col2 = request.args.get('col2')
    n_clusters = int(request.args.get('cluster'))

    start = time.time()

    # reading csv file
    csv_data = pd.read_csv('data.csv')
    #csv_data = pd.read_csv('/home/ubuntu/flaskapp/data.csv')

    x = csv_data[col1]
    y =csv_data[col2]


    # forming sets ---- x[1,2,3...] and y[6,7,8....] to data[[1,6],[2,7],[3,8]]
    range_value = len(x)

    data = []
    for i in range(0, range_value):
        element = []
        element.append(float(x[i]))
        element.append(float(y[i]))
        data.append(element)
    print data


    data = vstack(data)

    # creating centroids from data given
    centroids, distortion = kmeans(data, n_clusters)
    ##centroids -> centre point of clusters
    ##distortion -> distance to be considered between and entry and centroid to make the entry belong to a cetroid


    # assigning data entries to a particular cluster, depending on its distortion
    idx, _ = vq(data, centroids)


    #calculating number of points in each cluster
    list = ''
    total_count = 0
    cluster_names = []
    for i in range(n_clusters):

        name = "Cluster " + str(i + 1)
        cluster_names.append(name)

        # count points in each cluster based on data and idx labels
        points = data[idx == i, 0]
        count = 0
        for point in points:
            count += 1

        list += "Total cluster points in {0} is : {1}<br>".format(name, count)
        total_count += count

    ### make list an [] if rendering to an html template.. if displaying on head of graph in html, keep as string only

    print centroids
    # making centroid poins as actual set of points like [1,2]
    centroid_points = []
    for row in centroids:
        cent = []
        cent.append(row[0])
        cent.append(row[1])
        centroid_points.append(cent)

    print centroid_points

    # creating scatter graph

    # creating an object of pygal graphs
    # xy is to show that it is a x-y coordinate graph
    # stroke-False, as we dont need line strokes
    scatter_chart = pygal.XY(stroke=False, style=DefaultStyle, dots_size=2, width=1280, height=720,
                             legend_at_bottom=False, title='K-Means Clustering')

    # adding points for each cluster to scatter plot
    for i in range(0, n_clusters):
        for j in range(0, 1):
            scatter_data = []
            for k in range(0, len(data[idx == i, j]) - 1):
                each_tuple = (data[idx == i, j][k], data[idx == i, j + 1][k])
                scatter_data.append(each_tuple)

            scatter_chart.add(cluster_names[i], scatter_data)

    # adding centroids to scatter plot
    scatter_data = []
    for i in range(len(centroids[:, 0])):
        each_tuple = (centroids[:, 0][i - 1], centroids[:, 1][i - 1])
        scatter_data.append(each_tuple)

    scatter_chart.add("Centroids", scatter_data)

    #below renders the chart as a Flask app return response
    return scatter_chart.render_response()


    #the below line opens a new tab and displays the chart in it.
    #scatter_chart.render_in_browser()


    # #below code is to modify the output page to show the total time as well as total points of all clusters along with rendering the grap as uri
    # html =''
    # html += '<center>Total Tuple Count: ' + str(total_count) + '</center><br>'
    # html += '<center>Centroids: ' + str(centroid_points) + '</center><br>'
    # html += '<center>' + list + '</center><br>'
    # html += '<center>Total Time: ' + str(time.time() - start) + '</center><br>'
    # graph_data = scatter_chart.render_data_uri()
    # html += '<object type="image/svg+xml" data=' + graph_data + ' />'
    #
    #
    # return '''<html>
    #             <head>
    #                 <title>Output cluster</title>
    #                 <link rel="stylesheet" href="static/stylesheets/style.css">
    #             </head>
    #             <body>''' + html + '''<br></body></html>'''


    #OR I can do the below:  h
    # scatter_chart.render_in_browser()
    # return 'The number of clusters is: {0} <br> The total number of points is: {1}<br> The total time takes is {2}'.format(n_clusters,total_count,time.time()-start)



if __name__ == '__main__':
	app.run(debug=True)