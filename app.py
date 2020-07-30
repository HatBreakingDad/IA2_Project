from flask import Flask, render_template, request, url_for, redirect
import csv

# GetData is not used in editor.html template and is unnecessarily returned in the editorSetup function.
app = Flask(__name__)

"""
    Description
    
    Args:
        
    Returns:
        
    """


def getCSV():
    # Open the file in read mode using utf-8-sig encoding -> allow for a wider range of characters
    with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        returnCatList = []
        returnData = []
        for line in reader:
            returnData.append(line)
            # We read the product's categories as is, but we later remove the product_cat prefix and dashing to improve user readability
            returnCategory = line[len(line) - 1].split(',')
            for i in range(0, len(returnCategory)):
                # Creating a category list that will be displayed in the search bar. It checks if a category is already in the list and if
                # adds it to the list. It also makes sure that blank categories aren't added to the list.
                if(returnCategory[i] not in returnCatList and returnCategory[i] != ""):
                    returnCatList.append(returnCategory[i])
        return returnData, sorted(returnCatList[1:])


def editorSetup():
    fileReturn = getCSV()
    data = fileReturn[0]
    categoryList = fileReturn[1]
    idList = []
    dictID = {}
    for i in range(1, len(data)):
        idList.append(int(data[i][0]))
        dictID[data[i][0]] = data[i][1:]
    return data, sorted(idList), dictID, categoryList

# Bottom two links redirect to home just in case the user forgets how to get to the homepage


@app.route("/index")
def index():
    return redirect(url_for('main'))


@app.route("/home")
def home():
    return redirect(url_for('main'))


@app.route("/")
def main():
    return render_template('home.html')


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == 'GET':
        data = getCSV()
        # Returning data, length of each row, result length (-1 tells template no responses were found) and list of categories
        return render_template('search.html', getdata=data[0], dataLength=8, resultLength=-1, categories=data[1])
    else:
        searchTerm = request.form['results']
        catSelect = request.form.get('categoryselect')
        stockSelect = request.form.get('stockselect')
        search = []

        fileReturn = getCSV()
        reader = fileReturn[0]
        categoryList = fileReturn[1]

        if (searchTerm == "" and catSelect is None and stockSelect is None):
            search = reader
            return render_template('search.html', getdata=search, dataLength=8, resultLength=-1, categories=categoryList)

        # Adding header row
        search.append(reader.pop(0))

        # The following for loop goes through the current product data and matches it with the criteria provided by the user
        for line in reader:
            # If the user did use a search term and the term is not in the result, skip this csv line
            if searchTerm != "" and searchTerm not in ''.join(line):
                continue
            # If the user did use a stock filter and the stock condition was not in the result, skip this csv line
            if stockSelect is not None and stockSelect not in line[2]:
                continue
            # If the user did use a category filter and the category was not in the result, skip this csv line
            if catSelect is not None and catSelect not in line[7]:
                continue
            # If the compiler has made it here, it means the result fulfils all of the user filters and hence, the csv line is appended to the results list
            search.append(line)

        return render_template('search.html', getdata=search, dataLength=8, resultLength=len(search) - 1, categories=categoryList, searchTerm=searchTerm)


@app.route("/editor", methods=["POST", "GET"])
def editor():
    if request.method == "GET":
        templateValues = editorSetup()
        return render_template('editor.html', getdata=templateValues[0], idList=templateValues[1], dictID=templateValues[2], categories=templateValues[3], success=0)
    else:
        # Request Form Variables
        print(request.form['formSubmit'])
        print(type(request.form['formSubmit']))
        if request.form['formSubmit'] == '0':
            print('Yesman')
            templateValues = editorSetup()
            with open("GE_Data.csv", mode='w+', encoding='utf-8-sig', newline='') as dataStore:
                writer = csv.writer(dataStore, delimiter=",")
                lines = []
                with open("BackupData.csv", mode='r', encoding='utf-8-sig') as dataBackup:
                    reader = csv.reader(dataBackup)
                    for line in reader:
                        lines.append(line)
                writer.writerows(lines)
            return render_template('editor.html', getdata=templateValues[0], idList=templateValues[1], dictID=templateValues[2], categories=templateValues[3], success=3)
        id = request.form['productID']
        name = request.form['productName']
        stock = request.form['productStock']
        image = request.form['image-select-primary']
        # Sale Price -> productSale (Need to add $ sign for CSV)
        salePrice = '$' + str(request.form['productSale'])
        # Normal Price -> productPrice (Need to add $ sign for CSV)
        normalPrice = '$' + str(request.form['productPrice'])
        sku = request.form['productSKU']

        file = csv.reader(
            open('GE_Data.csv', encoding="utf-8-sig", newline=''))
        # Doing this instead of getCSV function as it is more efficient as I do not need the categories value
        lines = list(file)

        writeList = []

        for i in range(0, len(lines)):
            if id == lines[i][0]:
                categories = ','.join(request.form.getlist('productCatSelect'))
                # If the user selected no categories, simply use the current ones
                if len(categories) <= 0:
                    categories = lines[i][7]
                writeList = [id, name, stock, image,
                              salePrice, normalPrice, sku, categories]
                # Checking if clientside accidently sent emtpy field.
                for item in writeList:
                    if not item:
                        templateValues = editorSetup()
                        return render_template('editor.html', getdata=templateValues[0], idList=templateValues[1], dictID=templateValues[2], categories=templateValues[3], success=1)
                # What we do here is check if any changes were made to the line, if not, we don't bother writing the form submitted line
                # as it won't make a difference. I did try to implement something like this using js and html, however I was unable to
                # succesfully make something that would work https://www.sitepoint.com/detect-html-form-changes/ (is what I looked at)
                if lines[i] == writeList:
                    templateValues = editorSetup()
                    return render_template('editor.html', getdata=templateValues[0], idList=templateValues[1], dictID=templateValues[2], categories=templateValues[3], success=1)
                lines[i] = writeList

        # Now writing all rows (including edited row) back to file. I would like to find a more efficient solution that only replaces
        # the edited line
        with open("GE_Data.csv", mode='w+', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(lines)

        templateValues = editorSetup()
        return render_template('editor.html', getdata=templateValues[0], idList=templateValues[1], dictID=templateValues[2], categories=templateValues[3], success=2)


if __name__ == "__main__":
    app.run(debug=True)
