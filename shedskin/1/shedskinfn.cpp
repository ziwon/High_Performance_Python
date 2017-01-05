#include "builtin.hpp"
#include "shedskinfn.hpp"

namespace __shedskinfn__ {

str *const_0;


list<__ss_int> *output;
str *__name__;



list<__ss_int> *calculate_z(__ss_int maxiter, list<complex> *zs, list<complex> *cs) {
    /**
    Calculate output list using Julia update rule
    */
    __ss_bool __2, __3;
    __ss_int __0, __1, i, n;
    complex c, z;
    list<__ss_int> *output;

    output = ((new list<__ss_int>(1,0)))->__mul__(len(zs));

    FAST_FOR(i,0,len(zs),1,0,1)
        n = 0;
        z = zs->__getfast__(i);
        c = cs->__getfast__(i);

        while (((n<maxiter) and (__abs(z)<((double)(2))))) {
            z = ((z*z)+c);
            n = (n+1);
        }
        output->__setitem__(i, n);
    END_FOR

    return output;
}

void __init() {
    const_0 = new str("__main__");

    __name__ = new str("__main__");

    if (__eq(__name__, const_0)) {
        output = calculate_z(1, (new list<complex>(1,mcomplex(0.0, 0.0))), (new list<complex>(1,mcomplex(0.0, 0.0))));
    }
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__shedskinfn__::__init);
}
