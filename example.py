from numpy import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager
from ProbitScale import ProbitScale
import matplotlib.scale as mscale
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.special import erf
from scipy.special import erfinv
import copy


def ecdf(x):
    """Compute the empirical cumulative distribution function"""

    x_sorted = copy.copy(x)
    x_sorted.sort()
    
    x_l = len(x_sorted)
    ecdf_x = ones(x_l)

    for i in arange(0, x_l):
        ecdf_x[i] = (i/float(x_l))
    return x_sorted,ecdf_x


class ProbVar:

    def __init__(self, a, b, n, name, pa=0.1, pb=0.9, lognormal=False, Plot=True):

        mscale.register_scale(ProbitScale)

        if Plot:
            fig = plt.figure(facecolor="white")
            ax1 = fig.add_subplot(121, axisbelow=True)
            ax2 = fig.add_subplot(122, axisbelow=True)
            ax1.set_xlabel(name)
            ax1.set_ylabel("Probability Less Than")
            prop = matplotlib.font_manager.FontProperties(size=8)
         
        if lognormal:

            sigma = (log(b) - log(a))/((erfinv(2*pb-1)-erfinv(2*pa-1))*(2**0.5))
            mu = log(a)-erfinv(2*pa-1)*sigma*(2**0.5)
            cdf = arange(0.001, 1.000, 0.001)
            ppf = map(lambda v: lognorm.ppf(v, sigma, scale=exp(mu)), cdf)
            
            x = lognorm.rvs(sigma, scale=exp(mu), size=n)
 
            print "generating lognormal %s, p50 %0.3f, size %s" % (name, exp(mu), n)
            x_s, ecdf_x = ecdf(x)
 
            best_fit = lognorm.cdf(x, sigma, scale=exp(mu))
            if Plot:
                ax1.set_xscale('log')
                ax2.set_xscale('log')
            hist_y = lognorm.pdf(x_s, std(log(x)), scale=exp(mu))

        else:
            
            sigma = (b - a)/((erfinv(2*pb-1)-erfinv(2*pa-1))*(2**0.5))
            mu = a-erfinv(2*pa-1)*sigma*(2**0.5)
            cdf = arange(0.001, 1.000, 0.001)
            ppf = map(lambda v: norm.ppf(v, mu, scale=sigma), cdf)
 
            print "generating normal %s, p50 %0.3f, size %s" % (name, mu, n)
            x = norm.rvs(mu, scale=sigma, size=n)
            x_s,ecdf_x = ecdf(x)
            best_fit = norm.cdf((x-mean(x))/std(x))
            hist_y = norm.pdf(x_s, loc=mean(x), scale=std(x))
            pass

        if Plot:
            ax1.plot(ppf, cdf, 'r-', linewidth=2)
            ax1.set_yscale('probit')
            ax1.plot(x_s, ecdf_x, 'o')
            ax1.plot(x, best_fit, 'r--', linewidth=2)

            n, bins, patches = ax2.hist(x, normed=1, facecolor='green', alpha=0.75)
            bincenters = 0.5*(bins[1:]+bins[:-1])
            ax2.plot(x_s, hist_y, 'r--', linewidth=2)
            ax2.set_xlabel(name)
            ax2.set_ylabel("Fraction")
            ax1.grid(b=True, which='both', color='black', linestyle='-', linewidth=1)
            #ax1.grid(b=True, which='major', color='black', linestyle='--')
            ax2.grid(True)

        return



if __name__=="__main__":

    no_samples = 1000
    rv_lognorm = ProbVar(0.6, 0.75, no_samples, "SGgas", pa=0.1, pb=0.5, lognormal=True, Plot=True)
    rv_norm = ProbVar(0.6, 0.75, no_samples, "SGgas", pa=0.1, pb=0.5, lognormal=False, Plot=True)

    plt.show()
    
