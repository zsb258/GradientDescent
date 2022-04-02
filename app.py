from flask import Flask, render_template, request, url_for
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr,
standard_transformations, implicit_multiplication_application)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    context = {}
    context['defaults'] = {
            'fn': 'x^2',
            'x0': 1,
            'y0': 0,
            'eta': 0.1,
            'numIter': 10,
            'numVar1': 'checked',
            'numVar2': '',
        }

    if request.method == 'POST':
        x = Symbol('x')
        y = Symbol('y')

        fn_str = str(request.form.get('fn'))
        num_var = int(request.form.get('numVar'))
        x0 = Float(request.form.get('x0'))
        y0 = Float(request.form.get('y0'))
        eta = Float(request.form.get('eta'))
        num_iter = int(request.form.get('numIter'))

        # managing defaults form values in new page view
        context['defaults'] = {
            'fn': fn_str,
            'x0': float(x0),
            'y0': float(y0),
            'eta': float(eta),
            'numIter': num_iter,
        }
        if num_var == 1:
            context['defaults']['numVar1'] = 'checked'
            context['defaults']['numVar2'] = ''
        else:
            context['defaults']['numVar1'] = ''
            context['defaults']['numVar2'] = 'checked'

        fn = parse_expr(fn_str.replace('^', '**'))

        try:
            if num_var == 1:
                df = diff(fn)

                res = []
                for _ in range(1, num_iter+1):
                    x0 = x0 - eta * df.subs(x, x0).evalf()

                    x_val = x0.evalf(4)
                    y_val = '-'
                    f_val = fn.subs(x, x0).evalf(4)
                    res.append((x_val, y_val, f_val))
                
                context['dfx'] = format_helper(str(df))
                context['dfy'] = '-'

            else:
                dfx = diff(fn, x)
                dfy = diff(fn, y)

                res = []
                for _ in range(1, num_iter+1):
                    x0 = x0 - eta * dfx.subs(x, x0).evalf()
                    y0 = y0 - eta * dfy.subs(y, x0).evalf()

                    x_val = x0.evalf(4)
                    y_val = y0.evalf(4)
                    f_val = fn.subs({x: x0, y: y0}).evalf(4)
                    res.append((x_val, y_val, f_val))
                
                context['dfx'] = format_helper(str(dfx))
                context['dfy'] = format_helper(str(dfy))

            context['res'] = res
        
        except Exception:
            context['status'] = 'Your inputs are invalid. Please try again.'


    return render_template('index.html', context=context)


def format_helper(s:str) -> str:
    s = s.replace('**', '^')
    s = s.replace('*', ' * ')
    return s

if __name__ == "__main__":
    with app.test_request_context():
        print(url_for('index'))

    x = Symbol('x')
    y = Symbol('y')
    print(x)

    fn = parse_expr('2 * x**2 + y')
    print(str(fn))
    df = diff(fn, x)
    print(Float(df.subs({x: 4, y: 2}).evalf(), 4))
    val = round(df.subs(x, 4).evalf(), 2)

    print(val)