// Implementation of the payoff classes
#include "payoffs.h"

// PayOffCall class
PayOffCall::PayOffCall(const double _K): K(_K){		// List Initialization
}

PayOffCall::~PayOffCall(){				// No dynamic memory to delete
}

double PayOffCall::operator()(const double &S) const{
  return   max(S - K, 0.0);				// European call pay-off
}

// PayOffPut class
PayOffPut::PayOffPut(const double _K): K(_K){
}

PayOffPut::~PayOffPut(){				// No dynamic memory to release
}

double PayOffPut::operator()(const double &S) const{	// functor/function object
  return max(K - S, 0.0);
}

// PayOffDoubleDigital class
PayOffDoubleDigital::PayOffDoubleDigital(const double U, const double D): Up(U), Down(D){
}

PayOffDoubleDigital::~PayOffDoubleDigital(){		//   No memory to release
}

double PayOffDoubleDigital::operator()(const double &S) const{
  if (S <= Up && S >= Down)
    return 1.0;
  else
    return 0.0;
}

// PayOffDigitalCall class
PayOffDigitalCall::PayOffDigitalCall(const double _K): K(_K){
}

PayOffDigitalCall::~PayOffDigitalCall(){
}

double PayOffDigitalCall::operator()(const double &S) const{
  if(S > K)
    return 1.0;
  else
    return 0.0;
}

// PayOffDigitalPut class
PayOffDigitalPut::PayOffDigitalPut(const double _K): K(_K){
}

PayOffDigitalPut::~PayOffDigitalPut(){
}

double PayOffDigitalPut::operator()(const double &S) const{
  if(S < K)
    return 1.0;
  else
    return 0.0;
}
