from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import pickle
import pandas as pd

import matplotlib.pyplot as plt, mpld3


app = Flask(__name__)
app.config['SECRET_KEY'] = "Espero que saquemos 10 con esta pagina web"

#Form class
class ModelInputForm(FlaskForm):
    dureza = IntegerField('Dureza', validators=[DataRequired()])
    asp = IntegerField('Aspiraciones', validators=[DataRequired()])
    calidad = IntegerField('Calidad estimada', validators=[DataRequired()])
    tasa_prod = IntegerField('Tasa de Produccion', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Create a route decorator
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    nombre = ['Jose Andres Meyer','Antonio Patjane Ceballos', 'Luis Gabriel Martinez']
    return render_template('nosotros.html', nombre = nombre)

@app.route('/prediccion', methods = ["GET", "POST"])
def prediccion():
    if request.method == 'POST':
        result = request.form
        nombre_archivo='rfregresor.pkl'
        archivo_entrada= open(nombre_archivo, 'rb')
        reg_model= pickle.load(archivo_entrada)
        archivo_entrada.close()
        dureza = float(request.form['dureza'])
        asp = float(request.form['asp'])
        calidad = float(request.form['calidad'])
        tasa_prod = float(request.form['tasa_prod'])
        inputs = [dureza, asp, calidad, tasa_prod]
        r = reg_model.predict(([inputs]))
        EC = r[0][1]*40.4
        EE = r[0][0]*34.5
        price = EE + 0.724*EC
        
        df = pd.read_csv('calidad_costo_df.csv')
        fig = plt.figure()
        plt.scatter(df['Calidad'], df['Costo'])
        plt.scatter(calidad,price, c='red')
        plt.legend(['Puntos en nuestra base de datos','Punto de prediccion'])
        plt.xlabel('Calidad')
        plt.ylabel('Costo')
        html_graph = mpld3.fig_to_html(fig)
        
        return render_template('prediction.html', 
        inputs = inputs,
        EC = EC,
        EE = EE,
        price = price,
        html_graph = html_graph)

@app.route('/modelo', methods=['GET', 'POST'])
def modelo():
    dureza = None
    asp = None
    calidad = None
    tasa_prod = None

    form = ModelInputForm()
    r = [[0,0]]
    price = 0.0

    if form.validate_on_submit():
        dureza = form.dureza.data
        asp = form.asp.data
        calidad = form.calidad.data
        tasa_prod = form.tasa_prod.data

        # form.dureza.data = 0
        # form.asp.data = 0
        # form.calidad.data = 0
        # form.tasa_prod.data = 0
        
    return render_template('modelo.html', 
        # dureza = dureza
        # asp = asp,
        # calidad = calidad,
        # tasa_prod = tasa_prod,
         form = form
        )

if __name__ == "__main__":
    app.run()