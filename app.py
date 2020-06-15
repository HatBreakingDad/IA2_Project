from flask import Flask, render_template, request, url_for
import csv

app = Flask(__name__)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == 'GET':
        """convert the csv into a basic html table format"""
        dataout = []
        with open("GE_Data.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for line in reader:
                dataout.append(line)
        return render_template('search.html', getdata=dataout, dataLength = 8, resultLength = -1)
    else:
        requestResults = request.form['results']
        search = []
        with open("GE_Data.csv", mode='r', encoding='latin-1') as file:
            reader = csv.reader(file)
            search.append(next(reader))
            categoryList = []
            for line in reader:
                if (requestResults.lower() in ''.join(line).lower()):
                    search.append(line)
                returnCategory = line[len(line)  - 1].replace('product_cat-','').replace('-',' ').title().split(',')
                for i in range(0, len(returnCategory)):
                    if(returnCategory[i] not in categoryList):
                        categoryList.append(returnCategory[i])
            print(categoryList)
        return render_template('search.html', getdata=search, dataLength = 8, resultLength=len(search) - 1)


# @app.route("/form", methods=["POST", "GET"])
# def form():
#     if request.method == 'GET':
#         """convert the csv into a basic html table format"""
#         dataout = []
#         with open("FirstFleet.csv", mode='r', encoding='latin-1') as file:
#             reader = csv.reader(file)
#             for line in reader:
#                 dataout.append(line)
#         return render_template('form.html', getdata=dataout)
#     else:
#         requestResults = request.form['results']
#         dataout = []
#         with open("FirstFleet.csv", mode='r', encoding='latin-1') as file:
#             reader = csv.reader(file)
#             for line in reader:
#                 dataout.append(line)
#         search = []
#         for item in dataout[1:]:
#             if (requestResults.lower() in ' '.join(item).lower()):
#                 search.append(item)
#         return render_template('form.html', getdata=search)


if __name__ == "__main__":
    app.run(debug=True)
