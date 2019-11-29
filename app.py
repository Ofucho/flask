from flask import Flask, render_template

import pygal

app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template('inventory.html')

@app.route('/about')
def about_page():
    x = 'JB'

    return render_template('About.html', x=x)

@app.route('/contact')
def cpntact_page():
    return render_template('contact us.html')

@app.route('/dashboard')
def piechart():
    ratios = [('Men', 9 ),('Ladies', 5)]
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add(ratios[0][0],ratios[0][1])
    pie_chart.add(ratios[1][0],ratios[1][1])
    # pie_chart.add('Chrome', 36.3)
    # pie_chart.add('Safari', 4.5)
    # pie_chart.add('Opera', 2.3)
    pie_chart.render()
    pie_data = pie_chart.render_data_uri()

    graph = pygal.Line()
    graph.title = '% Change Coolness of programming languages over time.'
    graph.x_labels = ['2011', '2012', '2013', '2014', '2015', '2016']
    graph.add('Python', [15, 31, 89, 200, 356, 900])
    # graph.add('Java', [15, 45, 76, 80, 91, 95])
    # graph.add('C++', [5, 51, 54, 102, 150, 201])
    # graph.add('All others combined!', [5, 15, 21, 55, 92, 105])
    graph_data = graph.render_data_uri()

    return render_template('dashboard.html', pie_data=pie_data,graph_data=graph_data)

if __name__ == '__main__':
    app.run()
