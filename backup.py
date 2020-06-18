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
        return returnData, returnCatList[1:]


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == 'GET':
        """convert the csv into a basic html table format"""
        fileReturn = getCSV()
        data = fileReturn[0]
        categoryList = fileReturn[1]
        return render_template('search.html', getdata=data, dataLength=8, resultLength=-1, categories=categoryList)
    else:
        requestResults = request.form['results']
        catSelect = request.form.get('categoryselect')
        stockSelect = request.form.get('stockselect')
        search = []

        if (requestResults is "" and catSelect is None and stockSelect is None):
            fileReturn = getCSV()
            search = fileReturn[0]
            categoryList = fileReturn[1]
            return render_template('search.html', getdata=search, dataLength=8, resultLength=len(search) - 1, categories=categoryList)

        with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            search.append(next(reader))

            for line in reader:
                returnCategory = line[len(
                    line) - 1].replace('product_cat-', '').title().split(',')
                if requestResults is not "" and requestResults not in line:
                    continue
                if stockSelect is not None and stockSelect not in line[2]:
                    continue
                if catSelect is not None and catSelect not in line[7]:
                    continue
                # returnCategory = line[len(
                #     line) - 1].replace('product_cat-', '').title().split(',')
                # for i in range(0, len(returnCategory)):
                #     if(returnCategory[i] not in categoryList):
                #         categoryList.append(returnCategory[i])

        return render_template('search.html', getdata=search, dataLength=8, resultLength=len(search) - 1, categories=categoryList)

 # Working on making a csv function and beginning early stages of development for editor


@app.route("/editor", methods=["POST", "GET"])
def editor():
    if request.method == "GET":
        fileReturn = getCSV()
        data = fileReturn[0]
        categoryList = fileReturn[1]
        IDList = []
        DictID = {}
        for i in range(1, len(data)):
            IDList.append(data[i][0])
            DictID[data[i][0]] = data[i][1:]
        return render_template('editor.html', getdata=data, IDList=IDList, DictID=DictID, categories=categoryList)
    else:
        fileReturn = getCSV()
        data = fileReturn[0]
        categoryList = fileReturn[1]
        IDList = []
        dataDict = {}
        for i in range(1, len(data)):
            IDList.append(data[i][0])
            dataDict[data[i][0]] = data[i][1:]
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
        salePrice = '$' + str(request.form['productSale'])
        # Normal Price -> productPrice (Need to add $ sign)
        normalPrice = '$' + str(request.form['productPrice'])
        # SKU -> productSKU
        sku = request.form['productSKU']
        print(sku)
        # return render_template('editor.html')
        file = csv.reader(open('GE_Data.csv'))
        lines = list(file)
        for line in lines:
            if id == line[0]:
                writeArray = []
                try:
                    # Select Category -> productCatSelect (We are getting it in a try statement as the user may not have selected any categories)
                    categories = request.form.getlist('productCatSelect')
                    if len(categories) == 0:
                        writeArray = [id, name, stock, image,
                                      salePrice, normalPrice, sku, line[7]]
                    else:
                        writeArray = [id, name, stock, image,
                                      salePrice, normalPrice, sku, categories]
                except:
                    writeArray = [id, name, stock, image,
                                  salePrice, normalPrice, sku, line[7]]
                line = writeArray
                print(line)
        # with open("GE_Data.csv", mode='a+', encoding='utf-8-sig') as file:
        #     writer = csv.writer(file)
        #     writer = csv.writer(file)
        #     print(csv.writer(file).values)
        #     writeArray = [id, name, stock, image, salePrice, normalPrice, sku, categories]
        return "<br>Ok<br>"


if __name__ == "__main__":
    app.run(debug=True)
