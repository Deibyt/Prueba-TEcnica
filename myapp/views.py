from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

from django.shortcuts import render
from django.db import connection
from bokeh.plotting import figure
from bokeh.models import Legend
from bokeh.embed import components
from bokeh.palettes import Spectral6
from numpy import cumsum, pi
import plotly.graph_objects as go
from django.shortcuts import render
import plotly.graph_objs as go

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from django.shortcuts import HttpResponseRedirect


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile')  # profile
        else:
            msg = 'Error al ingresar, por favor verifiqué su usuario y contraseña'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')


def signout(request):
    logout(request)
    return redirect('/')

def calcular_suma_costos(request):
    # Realizar la consulta a la base de datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_empresa, SUM(costo) FROM info_riesgo_empresas GROUP BY id_empresa")

        # Obtener los resultados de la consulta
        results = cursor.fetchall()

    # Crear una lista con los valores de las sumas
    sumas = [float(result[1]) for result in results]  # Convertir a valor numérico

    # Crear una lista con los nombres de las empresas como cadenas de texto
    empresas = [f"Empresa {str(result[0])}" for result in results]

    # Crear los datos para el gráfico de pastel
    data = go.Pie(labels=empresas, values=sumas)

    # Crear el diseño del gráfico de pastel
    layout = go.Layout(title="Suma de Costos por Empresa")

    # Crear la figura que contiene el gráfico de pastel y el diseño
    fig = go.Figure(data=data, layout=layout)

    # Convertir la figura en un componente HTML
    div = fig.to_html(full_html=False)

    # Renderizar la plantilla con los resultados y el gráfico de pastel
    return render(request, 'profile.html', {'results': results, 'div': div})



def calcular_suma_emp1(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT categoria_evento, SUM(impacto_reputacion) AS total_impacto_reputacion, SUM(sistemas_afectados) AS total_sistemas_afectados, SUM(nivel_gravedad) AS total_nivel_gravedad FROM info_riesgo_empresas WHERE categoria_evento IN ('Evento A', 'Evento B', 'Evento C') AND id_empresa = 1 GROUP BY categoria_evento")
        resultados = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas

    figs = []

    for resultado in resultados:
        categoria_evento = resultado[0]
        total_impacto_reputacion = resultado[1]
        total_sistemas_afectados = resultado[2]
        total_nivel_gravedad = resultado[3]

        fig = go.Figure(data=[
            go.Bar(name='Impacto en la Reputación', x=['Impacto en la Reputación'], y=[total_impacto_reputacion]),
            go.Bar(name='Sistemas Afectados', x=['Sistemas Afectados'], y=[total_sistemas_afectados]),
            go.Bar(name='Nivel de Gravedad', x=['Nivel de Gravedad'], y=[total_nivel_gravedad])
        ])

        fig.update_layout(barmode='group', title=f'Gráficas de Barras - {categoria_evento}', yaxis=dict(range=[0, 100]))

        fig_html = fig.to_html(full_html=False)
        figs.append(fig_html)

    mostrar_tabla = True  # Variable para indicar si se debe mostrar la tabla

    return render(request, 'profile.html', {'resultados': resultados, 'columnas': column_names, 'figs': figs, 'mostrar_tabla': mostrar_tabla})

def calcular_suma_emp2(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT categoria_evento, SUM(impacto_reputacion) AS total_impacto_reputacion, SUM(sistemas_afectados) AS total_sistemas_afectados, SUM(nivel_gravedad) AS total_nivel_gravedad FROM info_riesgo_empresas WHERE categoria_evento IN ('Evento A', 'Evento B', 'Evento C') AND id_empresa = 2 GROUP BY categoria_evento")
        resultados = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas

    figs = []

    for resultado in resultados:
        categoria_evento = resultado[0]
        total_impacto_reputacion = resultado[1]
        total_sistemas_afectados = resultado[2]
        total_nivel_gravedad = resultado[3]

        fig = go.Figure(data=[
            go.Bar(name='Impacto en la Reputación', x=['Impacto en la Reputación'], y=[total_impacto_reputacion]),
            go.Bar(name='Sistemas Afectados', x=['Sistemas Afectados'], y=[total_sistemas_afectados]),
            go.Bar(name='Nivel de Gravedad', x=['Nivel de Gravedad'], y=[total_nivel_gravedad])
        ])

        fig.update_layout(barmode='group', title=f'Gráficas de Barras - {categoria_evento}', yaxis=dict(range=[0, 100]))

        fig_html = fig.to_html(full_html=False)
        figs.append(fig_html)

    mostrar_tabla = True  # Variable para indicar si se debe mostrar la tabla

    return render(request, 'profile.html', {'resultados': resultados, 'columnas': column_names, 'figs': figs, 'mostrar_tabla': mostrar_tabla})

def calcular_suma_emp3(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT categoria_evento, SUM(impacto_reputacion) AS total_impacto_reputacion, SUM(sistemas_afectados) AS total_sistemas_afectados, SUM(nivel_gravedad) AS total_nivel_gravedad FROM info_riesgo_empresas WHERE categoria_evento IN ('Evento A', 'Evento B', 'Evento C') AND id_empresa = 3 GROUP BY categoria_evento")
        resultados = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas

    figs = []

    for resultado in resultados:
        categoria_evento = resultado[0]
        total_impacto_reputacion = resultado[1]
        total_sistemas_afectados = resultado[2]
        total_nivel_gravedad = resultado[3]

        fig = go.Figure(data=[
            go.Bar(name='Impacto en la Reputación', x=['Impacto en la Reputación'], y=[total_impacto_reputacion]),
            go.Bar(name='Sistemas Afectados', x=['Sistemas Afectados'], y=[total_sistemas_afectados]),
            go.Bar(name='Nivel de Gravedad', x=['Nivel de Gravedad'], y=[total_nivel_gravedad])
        ])

        fig.update_layout(barmode='group', title=f'Gráficas de Barras - {categoria_evento}', yaxis=dict(range=[0, 100]))

        fig_html = fig.to_html(full_html=False)
        figs.append(fig_html)

    mostrar_tabla = True  # Variable para indicar si se debe mostrar la tabla

    return render(request, 'profile.html', {'resultados': resultados, 'columnas': column_names, 'figs': figs, 'mostrar_tabla': mostrar_tabla})


def calcular_suma_emp4(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT categoria_evento, SUM(impacto_reputacion) AS total_impacto_reputacion, SUM(sistemas_afectados) AS total_sistemas_afectados, SUM(nivel_gravedad) AS total_nivel_gravedad FROM info_riesgo_empresas WHERE categoria_evento IN ('Evento A', 'Evento B', 'Evento C') AND id_empresa = 4 GROUP BY categoria_evento")
        resultados = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas

    figs = []

    for resultado in resultados:
        categoria_evento = resultado[0]
        total_impacto_reputacion = resultado[1]
        total_sistemas_afectados = resultado[2]
        total_nivel_gravedad = resultado[3]

        fig = go.Figure(data=[
            go.Bar(name='Impacto en la Reputación', x=['Impacto en la Reputación'], y=[total_impacto_reputacion]),
            go.Bar(name='Sistemas Afectados', x=['Sistemas Afectados'], y=[total_sistemas_afectados]),
            go.Bar(name='Nivel de Gravedad', x=['Nivel de Gravedad'], y=[total_nivel_gravedad])
        ])

        fig.update_layout(barmode='group', title=f'Gráficas de Barras - {categoria_evento}', yaxis=dict(range=[0, 100]))

        fig_html = fig.to_html(full_html=False)
        figs.append(fig_html)

    mostrar_tabla = True  # Variable para indicar si se debe mostrar la tabla

    return render(request, 'profile.html', {'resultados': resultados, 'columnas': column_names, 'figs': figs, 'mostrar_tabla': mostrar_tabla})


def calcular_suma_emp5(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT categoria_evento, SUM(impacto_reputacion) AS total_impacto_reputacion, SUM(sistemas_afectados) AS total_sistemas_afectados, SUM(nivel_gravedad) AS total_nivel_gravedad FROM info_riesgo_empresas WHERE categoria_evento IN ('Evento A', 'Evento B', 'Evento C') AND id_empresa = 5 GROUP BY categoria_evento")
        resultados = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas

    figs = []

    for resultado in resultados:
        categoria_evento = resultado[0]
        total_impacto_reputacion = resultado[1]
        total_sistemas_afectados = resultado[2]
        total_nivel_gravedad = resultado[3]

        fig = go.Figure(data=[
            go.Bar(name='Impacto en la Reputación', x=['Impacto en la Reputación'], y=[total_impacto_reputacion]),
            go.Bar(name='Sistemas Afectados', x=['Sistemas Afectados'], y=[total_sistemas_afectados]),
            go.Bar(name='Nivel de Gravedad', x=['Nivel de Gravedad'], y=[total_nivel_gravedad])
        ])

        fig.update_layout(barmode='group', title=f'Gráficas de Barras - {categoria_evento}', yaxis=dict(range=[0, 100]))

        fig_html = fig.to_html(full_html=False)
        figs.append(fig_html)

    mostrar_tabla = True  # Variable para indicar si se debe mostrar la tabla

    return render(request, 'profile.html', {'resultados': resultados, 'columnas': column_names, 'figs': figs, 'mostrar_tabla': mostrar_tabla})

def calificar_riesgos_emp_g(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT calificador_riesgos, SUM(costo) AS total_costos FROM info_riesgo_empresas GROUP BY calificador_riesgos")
        resultados = cursor.fetchall()

    # Obtener los valores de los calificadores de riesgos y los totales de costos
    calificadores_riesgos = [resultado[0] for resultado in resultados]
    totales_costos = [resultado[1] for resultado in resultados]

    # Crear el gráfico de líneas
    fig = go.Figure(data=go.Scatter(x=calificadores_riesgos, y=totales_costos, mode='lines'))

    # Establecer el título del gráfico
    fig.update_layout(title='Total de Costos por Calificador de Riesgos', xaxis_title='Calificador de Riesgos', yaxis_title='Total de Costos')

    # Convertir el gráfico en un componente HTML
    div = fig.to_html(full_html=False)

    # Renderizar la plantilla con el gráfico de líneas
    return render(request, 'profile.html', {'div': div})

def calificar_riesgos_emp1(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT calificador_riesgos, nivel_gravedad, COUNT(*) AS cantidad_casos
            FROM info_riesgo_empresas
            WHERE id_empresa = 1
            GROUP BY calificador_riesgos, nivel_gravedad
        """)
        resultados = cursor.fetchall()

    # Obtener los valores de los calificadores de riesgos, niveles de gravedad y cantidades de casos
    calificadores_riesgos = [resultado[0] for resultado in resultados]
    niveles_gravedad = [resultado[1] for resultado in resultados]
    cantidades_casos = [resultado[2] for resultado in resultados]

    # Crear el gráfico de burbujas
    fig = go.Figure(data=go.Scatter(
        x=calificadores_riesgos,
        y=niveles_gravedad,
        mode='markers',
        marker=dict(
            size=cantidades_casos,
            sizemode='diameter',
            sizeref=0.1,
            sizemin=1,
            color=cantidades_casos,
            colorscale='Viridis',
            showscale=True
        )
    ))

    # Establecer el título del gráfico
    fig.update_layout(title='Calificador de Riesgos (Empresa 1)', xaxis_title='Calificador de Riesgos', yaxis_title='Nivel de Gravedad')

    # Convertir el gráfico en un componente HTML
    div = fig.to_html(full_html=False)

    # Renderizar la plantilla con el gráfico de burbujas
    return render(request, 'profile.html', {'div': div})

def calificar_riesgos_emp2(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT calificador_riesgos, nivel_gravedad, COUNT(*) AS cantidad_casos
            FROM info_riesgo_empresas
            WHERE id_empresa = 2
            GROUP BY calificador_riesgos, nivel_gravedad
        """)
        resultados = cursor.fetchall()

    # Obtener los valores de los calificadores de riesgos, niveles de gravedad y cantidades de casos
    calificadores_riesgos = [resultado[0] for resultado in resultados]
    niveles_gravedad = [resultado[1] for resultado in resultados]
    cantidades_casos = [resultado[2] for resultado in resultados]

    # Crear el gráfico de burbujas
    fig = go.Figure(data=go.Scatter(
        x=calificadores_riesgos,
        y=niveles_gravedad,
        mode='markers',
        marker=dict(
            size=cantidades_casos,
            sizemode='diameter',
            sizeref=0.1,
            sizemin=1,
            color=cantidades_casos,
            colorscale='Viridis',
            showscale=True
        )
    ))

    # Establecer el título del gráfico
    fig.update_layout(title='Calificador de Riesgos (Empresa 2)', xaxis_title='Calificador de Riesgos', yaxis_title='Nivel de Gravedad')

    # Convertir el gráfico en un componente HTML
    div = fig.to_html(full_html=False)

    # Renderizar la plantilla con el gráfico de burbujas
    return render(request, 'profile.html', {'div': div})

def calificar_riesgos_emp3(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT calificador_riesgos, nivel_gravedad, COUNT(*) AS cantidad_casos
            FROM info_riesgo_empresas
            WHERE id_empresa = 3
            GROUP BY calificador_riesgos, nivel_gravedad
        """)
        resultados = cursor.fetchall()

    # Obtener los valores de los calificadores de riesgos, niveles de gravedad y cantidades de casos
    calificadores_riesgos = [resultado[0] for resultado in resultados]
    niveles_gravedad = [resultado[1] for resultado in resultados]
    cantidades_casos = [resultado[2] for resultado in resultados]

    # Crear el gráfico de burbujas
    fig = go.Figure(data=go.Scatter(
        x=calificadores_riesgos,
        y=niveles_gravedad,
        mode='markers',
        marker=dict(
            size=cantidades_casos,
            sizemode='diameter',
            sizeref=0.1,
            sizemin=1,
            color=cantidades_casos,
            colorscale='Viridis',
            showscale=True
        )
    ))

    # Establecer el título del gráfico
    fig.update_layout(title='Calificador de Riesgos (Empresa 3)', xaxis_title='Calificador de Riesgos', yaxis_title='Nivel de Gravedad')

    # Convertir el gráfico en un componente HTML
    div = fig.to_html(full_html=False)

    # Renderizar la plantilla con el gráfico de burbujas
    return render(request, 'profile.html', {'div': div})

def calificar_riesgos_emp4(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT calificador_riesgos, nivel_gravedad, COUNT(*) AS cantidad_casos
            FROM info_riesgo_empresas
            WHERE id_empresa = 4
            GROUP BY calificador_riesgos, nivel_gravedad
        """)
        resultados = cursor.fetchall()

    # Obtener los valores de los calificadores de riesgos, niveles de gravedad y cantidades de casos
    calificadores_riesgos = [resultado[0] for resultado in resultados]
    niveles_gravedad = [resultado[1] for resultado in resultados]
    cantidades_casos = [resultado[2] for resultado in resultados]

    # Crear el gráfico de burbujas
    fig = go.Figure(data=go.Scatter(
        x=calificadores_riesgos,
        y=niveles_gravedad,
        mode='markers',
        marker=dict(
            size=cantidades_casos,
            sizemode='diameter',
            sizeref=0.1,
            sizemin=1,
            color=cantidades_casos,
            colorscale='Viridis',
            showscale=True
        )
    ))

    # Establecer el título del gráfico
    fig.update_layout(title='Calificador de Riesgos (Empresa 4)', xaxis_title='Calificador de Riesgos', yaxis_title='Nivel de Gravedad')

    # Convertir el gráfico en un componente HTML
    div = fig.to_html(full_html=False)

    # Renderizar la plantilla con el gráfico de burbujas
    return render(request, 'profile.html', {'div': div})


def calificar_riesgos_emp5(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT calificador_riesgos, nivel_gravedad, COUNT(*) AS cantidad_casos
            FROM info_riesgo_empresas
            WHERE id_empresa = 5
            GROUP BY calificador_riesgos, nivel_gravedad
        """)
        resultados = cursor.fetchall()

    # Obtener los valores de los calificadores de riesgos, niveles de gravedad y cantidades de casos
    calificadores_riesgos = [resultado[0] for resultado in resultados]
    niveles_gravedad = [resultado[1] for resultado in resultados]
    cantidades_casos = [resultado[2] for resultado in resultados]

    # Crear el gráfico de burbujas
    fig = go.Figure(data=go.Scatter(
        x=calificadores_riesgos,
        y=niveles_gravedad,
        mode='markers',
        marker=dict(
            size=cantidades_casos,
            sizemode='diameter',
            sizeref=0.1,
            sizemin=1,
            color=cantidades_casos,
            colorscale='Viridis',
            showscale=True
        )
    ))

    # Establecer el título del gráfico
    fig.update_layout(title='Calificador de Riesgos (Empresa 5)', xaxis_title='Calificador de Riesgos', yaxis_title='Nivel de Gravedad')

    # Convertir el gráfico en un componente HTML
    div = fig.to_html(full_html=False)

    # Renderizar la plantilla con el gráfico de burbujas
    return render(request, 'profile.html', {'div': div})


def mostrar_datos_emp1(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM info_riesgo_empresas WHERE id_empresa = 1")
        resultados = cursor.fetchall()

    # Renderizar la plantilla con los datos
    return render(request, 'profile.html', {'resultados': resultados})

def mostrar_datos_emp2(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM info_riesgo_empresas WHERE id_empresa = 2")
        resultados = cursor.fetchall()

    # Renderizar la plantilla con los datos
    return render(request, 'profile.html', {'resultados': resultados})

def mostrar_datos_emp3(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM info_riesgo_empresas WHERE id_empresa = 3")
        resultados = cursor.fetchall()

    # Renderizar la plantilla con los datos
    return render(request, 'profile.html', {'resultados': resultados})

def mostrar_datos_emp4(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM info_riesgo_empresas WHERE id_empresa = 4")
        resultados = cursor.fetchall()

    # Renderizar la plantilla con los datos
    return render(request, 'profile.html', {'resultados': resultados})

def mostrar_datos_emp5(request):
    # Ejecutar la consulta SQL para obtener los datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM info_riesgo_empresas WHERE id_empresa = 5")
        resultados = cursor.fetchall()

    # Renderizar la plantilla con los datos
    return render(request, 'profile.html', {'resultados': resultados})

def modelo_riesgos_emp1(request):
    id_empresa = 1
    with connection.cursor() as cursor:
        cursor.execute("SELECT nivel_gravedad, impacto_reputacion FROM pruebaTecnica.info_riesgo_empresas  where id_empresa = 1")
        data = cursor.fetchall()

    X = np.array([row[0] for row in data])
    y = np.array([row[1] for row in data])

    # Escalar los datos numéricos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, 1))

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    low_prob = sum(y_pred < 4) / len(y_pred)
    medium_prob = sum((y_pred >= 4) & (y_pred < 8)) / len(y_pred)
    high_prob = sum(y_pred >= 8) / len(y_pred)

    return render(request, 'profile.html',
                  {'id_empresa': id_empresa, 'low_prob': low_prob, 'medium_prob': medium_prob, 'high_prob': high_prob})

def modelo_riesgos_emp2(request):
    id_empresa = 2
    with connection.cursor() as cursor:
        cursor.execute("SELECT nivel_gravedad, impacto_reputacion FROM pruebaTecnica.info_riesgo_empresas  where id_empresa = 2")
        data = cursor.fetchall()

    X = np.array([row[0] for row in data])
    y = np.array([row[1] for row in data])

    # Escalar los datos numéricos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, 1))

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    low_prob = sum(y_pred < 4) / len(y_pred)
    medium_prob = sum((y_pred >= 4) & (y_pred < 8)) / len(y_pred)
    high_prob = sum(y_pred >= 8) / len(y_pred)

    return render(request, 'profile.html',
                  {'id_empresa': id_empresa, 'low_prob': low_prob, 'medium_prob': medium_prob, 'high_prob': high_prob})

def modelo_riesgos_emp3(request):
    id_empresa = 3
    with connection.cursor() as cursor:
        cursor.execute("SELECT nivel_gravedad, impacto_reputacion FROM pruebaTecnica.info_riesgo_empresas  where id_empresa = 3")
        data = cursor.fetchall()

    X = np.array([row[0] for row in data])
    y = np.array([row[1] for row in data])

    # Escalar los datos numéricos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, 1))

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    low_prob = sum(y_pred < 4) / len(y_pred)
    medium_prob = sum((y_pred >= 4) & (y_pred < 8)) / len(y_pred)
    high_prob = sum(y_pred >= 8) / len(y_pred)

    return render(request, 'profile.html',
                  {'id_empresa': id_empresa, 'low_prob': low_prob, 'medium_prob': medium_prob, 'high_prob': high_prob})
def modelo_riesgos_emp4(request):
    id_empresa = 4
    with connection.cursor() as cursor:
        cursor.execute("SELECT nivel_gravedad, impacto_reputacion FROM pruebaTecnica.info_riesgo_empresas  where id_empresa = 4")
        data = cursor.fetchall()

    X = np.array([row[0] for row in data])
    y = np.array([row[1] for row in data])

    # Escalar los datos numéricos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, 1))

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    low_prob = sum(y_pred < 4) / len(y_pred)
    medium_prob = sum((y_pred >= 4) & (y_pred < 8)) / len(y_pred)
    high_prob = sum(y_pred >= 8) / len(y_pred)

    return render(request, 'profile.html',
                  {'id_empresa': id_empresa, 'low_prob': low_prob, 'medium_prob': medium_prob, 'high_prob': high_prob})


def modelo_riesgos_emp5(request):
    id_empresa = 5
    with connection.cursor() as cursor:
        cursor.execute("SELECT nivel_gravedad, impacto_reputacion FROM pruebaTecnica.info_riesgo_empresas  where id_empresa = 5")
        data = cursor.fetchall()

    X = np.array([row[0] for row in data])
    y = np.array([row[1] for row in data])

    # Escalar los datos numéricos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, 1))

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    low_prob = sum(y_pred < 4) / len(y_pred)
    medium_prob = sum((y_pred >= 4) & (y_pred < 8)) / len(y_pred)
    high_prob = sum(y_pred >= 8) / len(y_pred)

    return render(request, 'profile.html', {'id_empresa': id_empresa, 'low_prob': low_prob*100, 'medium_prob': medium_prob*100, 'high_prob': high_prob*100})

def calificar_riesgos_emp(request):
    # Aquí puedes colocar el código necesario para calificar los riesgos de la empresa
    # y generar el mensaje que deseas mostrar en la plantilla
    return render(request, 'profile.html')  # Reemplaza 'profile.html' con tu plantilla adecuada
