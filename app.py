from flask import Flask, render_template, request, url_for
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr,
standard_transformations, implicit_multiplication_application)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    context = {}
    context['defaults'] = {
            'fn': 'x**2',
            'x0': 1,
            'eta': 0.1,
            'numIter': 10,
        }

    x = Symbol('x')
    y = Symbol('y')

    if request.method == 'POST':
        fn_str = str(request.form.get('fn'))
        x0 = Float(request.form.get('x0'))
        eta = Float(request.form.get('eta'))
        num_iter = int(request.form.get('numIter'))

        context['defaults'] = {
            'fn': str(fn_str),
            'x0': float(x0),
            'eta': float(eta),
            'numIter': num_iter,
        }

        fn = parse_expr(fn_str.replace('^', '**'))
        df = diff(fn)

        df_res = []

        for i in range(1, num_iter+1):
            x0 = x0 - eta * df.subs(x, x0).evalf()

            val1 = x0.evalf(3)
            val2 = fn.subs(x, x0).evalf(3)

            df_res.append((val1, val2))


        
        context['df'] = format_helper(str(df))
        context['res'] = df_res

    return render_template('index.html', context=context)

def format_helper(s:str) -> str:
    s = s.replace('**', '^')
    s = s.replace('*', ' * ')
    return s

if __name__ == "__main__":
    with app.test_request_context():
        print(url_for('index'))

    x = Symbol('x')
    print(x)

    fn = parse_expr('2 * x**2')
    print(str(fn))
    df = diff(fn)
    print(Float(df.subs(x, 3).evalf(), 3))
    val = round(df.subs(x, 3).evalf(), 2)

    print(val)