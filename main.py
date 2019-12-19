from flask import Flask, render_template,request,redirect,url_for,flash

import pygal
import psycopg2

from flask_sqlalchemy import SQLAlchemy
# from config.Config import Development
from config.Config import Production

app = Flask(__name__)
app.config.from_object(Production)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@127.0.0.1:5432/postgres'
# app.config['SECRET_KEY'] = 'Jaye7eus'
# app.config['DEBUG'] = True
db = SQLAlchemy(app)

from models.inventories import Inventories

@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def hello_world():

    records = Inventories.fetch_all_records()

    print(type(records))

    return render_template('index.html', records=records)


@app.route('/add_inventory', methods=['POST', 'GET'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']
        stock = request.form['stock']

        # print(Name)
        # print(Type)
        # print(buying_price)
        # print(selling_price)
        # print(Stock)

        record = Inventories(name=name,type=type,buying_price=buying_price,selling_price=selling_price,
                         stock=stock)

        # record.add_records(record)
        db.session.add(record)
        db.session.commit()

    return redirect(url_for('hello_world'))


@app.route('/test/<name>')
def test(name):

    return name

@app.route('/sale_product/<int:id>', methods=['POST','GET'])
def make_sales(id):

    record = Inventories.fetch_one_record(id)
    if record:
        print(id)
        if request.method =='POST' :
            quantity = request.form['quantity']
            new_stock= record.stock - int(quantity)

            record.stock = new_stock
            db.session.commit()

            # sales = Sales(inv_id=id)

            flash ('Sale made successfully','success')


            print(quantity)
    return redirect(url_for('hello_world'))

@app.route('/view_sales/int:id')
def viewsales(id):
    record = Inventories.fetch_one_record(id)

    return render_template('sales.html', record=record)


@app.route('/delete/<int:id>')
def delete(id):
    record = Inventories.fetch_one_record(id)
    # print(record.id)
    # print(record.name)
    db.session.delete(record)
    db.session.commit()
    # flash('Item successfully deleted from inventory','danger')

    return redirect(url_for('hello_world'))

@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit(id):
    record = Inventories.fetch_one_record(id)
    if request.method == 'POST':
        record.name = request.form['name']
        record.type = request.form['type']
        record.buying_price = request.form['buying_price']
        record.selling_price = request.form['selling_price']
        record.stock = request.form['stock']

        db.session.commit()

        return redirect(url_for('hello_world'))
    return render_template('edit.html',record=record)

@app.route('/about')
def about_page():
    #x = 'JB'

    return render_template('About.html')

@app.route('/contact')
def contact_page():
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

    cur = conn.cursor()

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
