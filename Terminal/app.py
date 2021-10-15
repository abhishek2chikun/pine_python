from flask import Flask
from flask import render_template, redirect
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask('__main__')

@app.route('/')
def index():
	return render_template('desk.html')
@app.route('/pine')
def pine():
	return render_template('desk2.html')
@app.route('/screener')
def screener():
	return redirect('http://localhost:8501', code=301)



@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == '__main__':
	app.run(debug=True)