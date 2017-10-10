"""
A Python program for the Neville's algorithm.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

def neville(datax, datay, x):
    """
    Finds an interpolated value using Neville's algorithm.

    Input
      datax: input x's in a list of size n
      datay: input y's in a list of size n
      x: the x value used for interpolation

    Output
      p[0]: the polynomial of degree n
    """
    n = len(datax)
    p = n*[0]
    for k in range(n):
        for i in range(n-k):
            if k == 0:
                p[i] = datay[i]
            else:
                p[i] = ((x-datax[i+k])*p[i]+ \
                        (datax[i]-x)*p[i+1])/ \
                        (datax[i]-datax[i+k])
    return p[0]
