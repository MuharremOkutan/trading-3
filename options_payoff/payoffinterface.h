/* This is an interface that should be implemented by clients
   (inheriting clients) */
#ifndef _payoff
#define _payoff
#include <algorithm>
using namespace std;

class PayOff{
 public:
  PayOff() {};		/* Empty default constructor */
  virtual ~PayOff() {}; /* virtual destructor, clients can override */
  
  virtual double operator()(const double &S) const = 0; /* Overloading the '()' operator
							   turns the PayOff class into an 
							   abstract function object or functor */
};
#endif
