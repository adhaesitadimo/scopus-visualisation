import os
from dataset import Dataset
from flask import Flask, request, render_template, send_from_directory
from flask import send_from_directory, send_file


app = Flask(__name__)
Data = Dataset()

@app.route('/')
def hello():
    from_year = request.args.get('from_year')
    to_year = request.args.get('to_year')
    coef = request.args.get('coef')
    components_num = request.args.get('components_num')
    print(coef)
    if from_year and to_year:
        Data.gen_graph(from_year=int(from_year),
                       to_year=int(to_year),
                       coef=float(coef)/100,
                       components_num=int(components_num))
    return Data.render_graph()


@app.route('/download')
def download():
    file_format = request.args.get('format')
    print(file_format)
    Data.download_graph(file_format)
    try:
        return send_file(os.path.join(os.cwd, 'output.'+file_format), as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'icon/favicon.ico')
    except Exception as ex:
        return ex
