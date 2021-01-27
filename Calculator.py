from CalcWindow import *
from GraphWindow import *


def run_gui():
    calc_window = CalcWindow()
    calc_window.window_main.mainloop()


def run_cmd():
    exp = '-e*7^-pi^-3'  # -250700883.2992471
    exp = '-(  -0.5^(3+4) * sqrt( 9 ) / sin(-pi/4))'  # -0.03314563036811942
    exp = '  -.3^pi * sqrt( sin(pi/2) ) + cos(pi/4) /ln(e^2)'  # 0.33078522847446457
    exp = '  -ln(e^(3+6))*.3^pi'  # -0.20491345906928324
    exp = '(-2)^pi'  # illegal -2 ^ pi
    exp = '  .3^e -( -tan(pi/4) ) ^ 4 +-ln(e^2)'  # -2.962097469297049
    exp = '-sin(x)(3)'
    root = get_tree_from_exp(exp)

    r = get_result_from_node(root)

    print('\nresult:\n-------------------------------------------------')

    if gv.err != None:
        print(gv.err)
        gv.err = None
    else:
        print(r)

    print('-------------------------------------------------')


def main():
    if gv.is_test_mode:
        run_cmd()
    else:
        run_gui()

main()