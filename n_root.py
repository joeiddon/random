def n_rt(z, n, its, x=None):
    x = x or z
    return x if not its else n_rt(z, n, its-1, x - (x**n-z)/(n*x**(n-1)))
