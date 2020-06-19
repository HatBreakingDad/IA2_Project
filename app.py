import csv
import json

from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)


def getCSV():
    with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        returnCatList = []
        returnData = []
        for line in reader:
            returnData.append(line)
            # We read the product's categories as is, but we later remove the product_cat prefix and dashing to improve user readability
            returnCategory = line[len(line) - 1].split(',')
            for i in range(0, len(returnCategory)):
                if(returnCategory[i] not in returnCatList):
                    returnCatList.append(returnCategory[i])
        return returnData, sorted(returnCatList[1:])


def editorSetup():
    fileReturn = getCSV()
    data = fileReturn[0]
    categoryList = fileReturn[1]
    IDList = []
    DictID = {}
    for i in range(1, len(data)):
        IDList.append(data[i][0])
        DictID[data[i][0]] = data[i][1:]
    return data, sorted(IDList), DictID, categoryList


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == 'GET':
        data = getCSV()
        return render_template('search.html', getdata=data[0], dataLength=8, resultLength=-1, categories=data[1])
    else:
        requestResults = request.form['results']
        catSelect = request.form.get('categoryselect')
        stockSelect = request.form.get('stockselect')
        search = []

        fileReturn = getCSV()
        reader = fileReturn[0]
        categoryList = fileReturn[1]

        if (requestResults == "" and catSelect is None and stockSelect is None):
            search = fileReturn[0]
            return render_template('search.html', getdata=search, dataLength=8, resultLength=len(search) - 1, categories=categoryList)

        search.append(reader.pop(0))

        for line in reader:
            if requestResults != "" and requestResults not in ''.join(line):
                continue
            if stockSelect is not None and stockSelect not in line[2]:
                continue
            if catSelect is not None and catSelect not in line[7]:
                continue
            search.append(line)

        return render_template('search.html', getdata=search, dataLength=8, resultLength=len(search) - 1, categories=categoryList)


@app.route("/editor", methods=["POST", "GET"])
def editor():
    if request.method == "GET":
        templateValues = editorSetup()
        return render_template('editor.html', getdata=templateValues[0], IDList=templateValues[1], DictID=templateValues[2], categories=templateValues[3])
    else:
        # Request Form Variables
        # ID -> productID
        id = request.form['productID']
        # Name -> productName
        name = request.form['productName']
        # Stock -> productStock
        stock = request.form['productStock']
        # Image -> image-select-primary
        image = request.form['image-select-primary']
        # Sale Price -> productSale (Need to add $ sign)
        salePrice = ""
        if request.form['productSale'] != "":
            salePrice = '$' + str(request.form['productSale'])
        # Normal Price -> productPrice (Need to add $ sign)
        normalPrice = ""
        if request.form['productPrice'] != "":
            normalPrice = '$' + str(request.form['productPrice'])
        # SKU -> productSKU
        sku = request.form['productSKU']

        for key in request.form:
            print(request.form[key])

        file = csv.reader(open('GE_Data.csv', encoding="utf-8-sig", newline=''))
        lines = list(file)

        writeArray = []

        for i in range(0, len(lines)):
            if id == lines[i][0]:
                categories = ','.join(request.form.getlist('productCatSelect'))
                if len(categories) <= 0:
                    categories = lines[i][7]
                writeArray = [id, name, stock, image, salePrice, normalPrice, sku, categories]
                lines[i] = writeArray

        with open("GE_Data.csv", mode='w+', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(lines)

        templateValues = editorSetup()
        return render_template('editor.html', getdata=templateValues[0], IDList=templateValues[1], DictID=templateValues[2], categories=templateValues[3])


if __name__ == "__main__":
    app.run(debug=True)
