import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
tests = {
 'underline': r'$\underline{\mathbf{X}}$',
 'mathbfX': r'$\mathbf{X}$',
 'dT': r'$d(\underline{\mathbf{X}}) = \underline{\mathbf{W}}^T\,\underline{\mathbf{X}} = w_1x_1 + w_2x_2 + ..... + w_nx_n +$',
 'arrow': r'$\Rightarrow$',
 'cases_l1': r'$>0 \Rightarrow \mathrm{Class\ I}$',
 'cdots': r'$x_1 \atop x_2$',
 'pmatrix': r'$\begin{pmatrix} 1 \\ x_1 \end{pmatrix}$',
}
for name, tex in tests.items():
    fig = plt.figure(figsize=(10,4), dpi=100)
    try:
        fig.text(0.5,0.5, tex, fontsize=14, ha='center')
        fig.canvas.draw()
        print(f'{name}: OK')
    except Exception as e:
        print(f'{name}: FAIL {type(e).__name__}: {str(e)[:90]}')
    plt.close(fig)
