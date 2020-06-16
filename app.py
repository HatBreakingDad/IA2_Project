from flask import Flask, render_template, request, url_for, redirect
import csv

app = Flask(__name__)


def getCSV():
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
        return categoryList, dataout
        # return categoryList
        # return dataout


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

        # return categoryList
        # return dataout
        return render_template('search.html', getdata=dataout, dataLength=8, resultLength=-1, categories=categoryList)
    else:
        requestResults = request.form['results']
        search = []
        with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            search.append(next(reader))

            # I'm working on checking if the products have the correct categories selected
            catSelect = request.form.get('categoryselect')
            stockSelect = request.form.get('stockselect')

            categoryList = []
            for line in reader:
                returnCategory = line[len(
                    line) - 1].replace('product_cat-', '').title().split(',')
                if (requestResults.lower() in ''.join(line).lower()):
                    if catSelect != None:  # If there is category
                        if stockSelect != None:  # If there is stock
                            # Check if product is correct
                            if catSelect in returnCategory and stockSelect in line[2]:
                                search.append(line)  # Add line if so
                        else:  # Else, if there is no stock
                            if catSelect in returnCategory:  # And if the category is correct
                                search.append(line)  # Then append the line
                    else:  # Else, if there is no category
                        if stockSelect != None:  # But if there is stock
                            if stockSelect in line[2]:  # Check if stock valid
                                search.append(line)  # If it is, append line
                        else:
                            # Else, if stock and category do not exist, append line
                            search.append(line)
                for i in range(0, len(returnCategory)):
                    if(returnCategory[i] not in categoryList):
                        categoryList.append(returnCategory[i])
        return render_template('search.html', getdata=search, dataLength=8, resultLength=len(search) - 1, categories=categoryList)

 #Working on making a csv function and beginning early stages of development for editor
@app.route("/editor", methods=["POST", "GET"])
def editor():
    if request.method == "POST":
        return render_template('editor.html', getdata=dataout, datalength=8)
    else:
        return render_template('editor.html', getdata=dataout, dataLength=8)

        # @app.route("/stock", methods=["POST", "GET"])
        # def stock():
        #     if request.method == 'GET':
        #         """convert the csv into a basic html table format"""
        #         dataout = []
        #         with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
        #             reader = csv.reader(file)
        #             for line in reader:
        #                 dataout.append(line)
        #         return render_template('stock.html', getdata=dataout, dataLength=8)
        #     else:
        #         requestResults = request.form['results']
        #         print(requestResults)
        # redirect(url_for('search'), code=307)


if __name__ == "__main__":
    app.run(debug=True)
