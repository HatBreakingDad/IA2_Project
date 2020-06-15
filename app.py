from flask import Flask, render_template, request, url_for
import csv

app = Flask(__name__)


@app.route("/pictures", methods=["POST", "GET"])
def pictures():
    if request.method == 'GET':
        """convert the csv into a basic html table format"""
        dataout = []
        with open("primeimages.csv", mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for line in reader:
                dataout.append(line)
        return render_template('pictures.html', getdata=dataout)
    else:
        requestResults = request.form['results']
        dataout = []
        with open("primeimagescsv", mode='r', encoding='latin-1') as file:
            reader = csv.reader(file)
            for line in reader:
                dataout.append(line)
        search = [[], []]
        for item in dataout:
            if (requestResults.lower() in ' '.join(item).lower()):
                search.append(item)
        return render_template('pictures.html', getdata=search)


@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == 'GET':
        """convert the csv into a basic html table format"""
        dataout = []
        with open("FirstFleet.csv", mode='r', encoding='latin-1') as file:
            reader = csv.reader(file)
            for line in reader:
                dataout.append(line)
        return render_template('form.html', getdata=dataout)
    else:
        requestResults = request.form['results']
        dataout = []
        with open("FirstFleet.csv", mode='r', encoding='latin-1') as file:
            reader = csv.reader(file)
            for line in reader:
                dataout.append(line)
        search = []
        for item in dataout[1:]:
            if (requestResults.lower() in ' '.join(item).lower()):
                search.append(item)
        return render_template('form.html', getdata=search)


if __name__ == "__main__":
    app.run(debug=True)
