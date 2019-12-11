from flask import Flask, render_template

import pygal
import psycopg2

app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template('inventory.html')

@app.route('/about')
def about_page():
    #x = 'JB'

    return render_template('About.html')

@app.route('/contact')
def cpntact_page():
    return render_template('contact us.html')

@app.route('/dashboard')
def piechart():

    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1234' ")

    cur = conn.cursor()

    cur.execute("""SELECT to_char(to_timestamp(date_part('month',sales.created_at)::text,'MM'),'Month') as month, round(sum(inventories.selling_price*sales.quantity))
from public.inventories
join sales on sales.inv_id = inventories.id
group by extract (month from sales.created_at)
order by extract (month from sales.created_at) asc
""")

    rows = cur.fetchall()
    print(type(rows))
    t =[]
    r =[]

    for it in rows:
        print(it)
        t.append(it[0])
        r.append(it[1])

    print(t)
    print(r)

    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1234' ")

    cur1 = conn.cursor()

    cur.execute("""SELECT type,count(type)
	FROM public.sales 
	join public.inventories on inventories.id = sales.inv_id
	group by type
""")

    records = cur.fetchall()
    print(type(records))

    for each in records:
        print(each)

    #ratios = [('Men', 9 ),('Ladies', 5)]
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add(records[0][0],records[0][1])
    pie_chart.add(records[1][0],records[1][1])
    # pie_chart.add('Chrome', 36.3)
    # pie_chart.add('Safari', 4.5)
    # pie_chart.add('Opera', 2.3)
    pie_chart.render()
    pie_data = pie_chart.render_data_uri()

    # data = [
    #     {'month': 'January', 'total': 22},
    #     {'month': 'February', 'total': 27},
    #     {'month': 'March', 'total': 23},
    #     {'month': 'April', 'total': 20},
    #     {'month': 'May', 'total': 12}]
    # x = []
    # y = []
    # for each in data:
    #     print(each['month'])
    #     x.append(each['month'])
    #     y.append(int(each['total']))
    #     # l = [x.append(each['month'])]
    #     # k = [y.append(each['total'])]
    # print(x)
    # print(y)

    graph = pygal.Line()
    graph.title = 'Total monthly sales'
    graph.x_labels = t
    # graph.add = ('total', y)

    graph.add('Sales', r)
    # graph.add('C++', [5, 51, 54, 102, 150, 201])
    # graph.add('All others combined!', [5, 15, 21, 55, 92, 105])
    graph_data = graph.render_data_uri()

    return render_template('dashboard.html', pie_data=pie_data, graph_data=graph_data)

if __name__ == '__main__':
    app.run()
