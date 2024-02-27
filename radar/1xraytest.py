from parsraybetlive import raybetlive
from parsreaybetline import raybetline
from pars1xlive import onexlive
from pars1xline import onexline
import time

start = time.time()
x = raybetlive() + raybetline() + onexlive() + onexline()
print(*x, sep='\n')
stop = time.time()
print(stop - start)