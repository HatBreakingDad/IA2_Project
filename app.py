from flask import Flask, render_template, request, url_for, redirect
import csv

app = Flask(__name__)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == 'GET':
        """convert the csv into a basic html table format"""
        dataout = []
        with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            categoryList = []
            for line in reader:
                dataout.append(line)
                returnCategory = line[len(
                    line) - 1].replace('product_cat-', '').replace('-', ' ').title().split(',')
                for i in range(0, len(returnCategory)):
                    if(returnCategory[i] not in categoryList):
                        categoryList.append(returnCategory[i])
        return render_template('search.html', getdata=dataout, dataLength=8, resultLength=-1, categories=categoryList)
    else:
        requestResults = request.form['results']
        search = []
        with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            search.append(next(reader))

            #I'm working on checking if the products have the correct categories selected
            request.form.get('categoryselect')
            request.form.get('stockselect')
            print(request.form)
            if 'stock' in request.form:
                print(request.form.getlist['stock'])
            else:
                print('Stock not in form.')
            if 'category' in request.form:
                print(request.form.getlist['category'])
            else:
                print('Category not in form')
            categoryList = []
            for line in reader:
                if (requestResults.lower() in ''.join(line).lower()):
                    search.append(line)
                returnCategory = line[len(
                    line) - 1].replace('product_cat-', '').title().split(',')
                for i in range(0, len(returnCategory)):
                    if(returnCategory[i] not in categoryList):
                        categoryList.append(returnCategory[i])
        return render_template('search.html', getdata=search, dataLength=8, resultLength=len(search) - 1, categories=categoryList)


@app.route("/stock", methods=["POST", "GET"])
def stock():
    if request.method == 'GET':
        """convert the csv into a basic html table format"""
        dataout = []
        with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for line in reader:
                dataout.append(line)
        return render_template('stock.html', getdata=dataout, dataLength=8)
    else:
        requestResults = request.form['results']
        print(requestResults)
        redirect(url_for('search'), code=307)


if __name__ == "__main__":
    app.run(debug=True)
