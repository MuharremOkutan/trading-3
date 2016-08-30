/* Definition of the payoff classes */
#ifndef _payoffs_h
#define _payoffs_h

#include "payoffinterface.h"

/* PayOffCall class */
class PayOffCall : public PayOff{
 private:
  double K;						/* call option's strike price */

 public:
  PayOffCall(const double _K=0.0);
  virtual ~PayOffCall();				/* can be inherited further */
  virtual double operator()(const double &S) const;	/* overriden from baseclass
							    payoff is max(S-K, 0) */
};

/* PayOffPut class */
class PayOffPut : public PayOff{
 private:
  double K;						/* Put's Strike price */
  
 public:
  PayOffPut(const double _K=0.0);
  virtual ~PayOffPut();
  virtual double operator()(const double &S) const;	/* Overriden from base class) 
							   pay-off is max(K-S, 0)*/
};

/* PayOffDoubleDigital */
class PayOffDoubleDigital : public PayOff{
 private:
  double Up;							/* upper strike price */
  double Down;							/* lower strike price */
  
 public:
  PayOffDoubleDigital(const double U=0.0, const double D=0.0);	/* two strike parameters */
  virtual ~PayOffDoubleDigital();

  virtual double operator()(const double &S) const;	/* pay-off is 1 if spot within strike
							 barriers, 0 otherwise */
};

/* PayOffDigitalCall class */
class PayOffDigitalCall : public PayOff{
 private:
  double K;

 public:
  PayOffDigitalCall(const double _K=0.0);
  virtual ~PayOffDigitalCall();
  virtual double operator()(const double &S) const;
};

/* PayOffDigitalPut class */
class PayOffDigitalPut: public PayOff{
 private:
  double K;

 public:
  PayOffDigitalPut(const double _K=0.0);
  virtual ~PayOffDigitalPut();
  virtual double operator()(const double &S) const;
};
#endif
