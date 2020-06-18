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
        data = getCSV()[0]
        dataDict = {}
        for i in range(1, len(data)):
            dataDict[data[i][0]] = data[i][1:]
        #Request Form Variables
        #ID -> productID
        id = request.form['productID']
        #Name -> productName
        name = request.form['productName']
        #Stock -> productStock
        stock = request.form['productStock']
        #Image -> image-select-primary
        image = request.form['image-select-primary']
        #Sale Price -> productSale (Need to add $ sign)
        salePrice = '$' + str(request.form['productSale'])
        #Normal Price -> productPrice (Need to add $ sign)
        normalPrice = '$' + str(request.form['productPrice'])
        #Select Category -> productCatSelect
        categories = request.form['productCatSelect']
        print(categories)
        #SKU -> productSKU
        sku = request.form['productSKU']
        print(sku)
        # return render_template('editor.html')


if __name__ == "__main__":
    app.run(debug=True)
