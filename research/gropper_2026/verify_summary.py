from math import sqrt,log2
from collections import Counter
n_tokens=25373;n_lines=2952;observed=218;expected=210.86288561112096
pairs=n_tokens-n_lines
print("Observed repeated pair rate:",observed/pairs)
print("Expected within-line null rate:",expected/pairs)
print("Observed/expected:",observed/expected)
assert 174<=observed<=254
correct=34;n=39;p=correct/n;z=1.96
mid=(p+z*z/(2*n))/(1+z*z/n)
rad=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
print("Classifier accuracy:",p,"naive descriptive Wilson 95%:",mid-rad,mid+rad)
def conditional_entropy(s):
    pairs=Counter(zip(s,s[1:]));first=Counter(x for x,y in zip(s,s[1:]));total=len(s)-1
    return -sum((count/total)*log2(count/first[x]) for (x,y),count in pairs.items())
assert conditional_entropy("abababababababab")==conditional_entropy("xyxyxyxyxyxyxyxy")
print("Bijective relabeling toy control: PASS")
print("NOTE: published-output arithmetic + toy invariant, NOT original Gropper replication.")
