// This file contains an implementation of the VanillaOption class as
// described in the vanillaoption.h header file
#include "vanillaoption.h"

VanillaOption::VanillaOption(){
  initialize();
}

VanillaOption::VanillaOption(const double &_K, const double &_r,
			     const double &_T, const double &_S,
			     const double &_sigma){
  K = _K;
  r = _r;
  T = _T;
  S = _S;
  sigma = _sigma;
}

VanillaOption::VanillaOption(const VanillaOption &option){
  K = option.getK();
  r = option.getr();
  T = option.getT();
  S = option.getS();
  sigma = option.getsigma();
}

VanillaOption& VanillaOption::operator=(const VanillaOption &option){
  if(&option != this){
    copy(option);
    return *this;
  }
  return *this;		// trying to copy same object
}

VanillaOption::~VanillaOption(){
  // We don't have any dynamic memory allocated from the heap to
  // release, hence the empty constructor.
}

double VanillaOption::getK() const{
  return K;
}

double VanillaOption::getr() const{
  return r;
}

double VanillaOption::getT() const{
  return T;
}

double VanillaOption::getS() const{
  return S;
}

double VanillaOption::getsigma() const{
  return sigma;
}

double VanillaOption::calculateCallPrice()const{
  double sigma_root_T = sigma * sqrt(T);
  double d1 = (log(S/K) + (r + pow(sigma, 2)/2) * T) / sigma_root_T;
  double d2 = d1 - sigma_root_T;
  
  return S * cndf(d1) - K * exp(r * T) * cndf(d2);	// value of call
}

double VanillaOption::calculatePutPrice() const{
  double sigma_root_T = sigma * sqrt(T);
  double d1 = (log(S/K) + (r + pow(sigma, 2)) * T) / sigma_root_T;
  double d2 = d1 - sigma_root_T;

  return (K * exp(-r*T) * (1 - cndf(d2))) - S * exp(-T) * 1 - cndf(d1);	// TODO: value of put
}

double VanillaOption::cndf(const double &x) const{
  const double l = 1.0 / (1.0 + 0.2316419*x);
  const double l_sum = l * (0.319381530 + l*(-0.356563782 + l*(1.781477937 + 
							       l*(-1.821255978 + 1.330274429*l))));
  if( x >= 0.0){
    return (1.0 - (1.0/(pow(2 * M_PI, 0.5))) *exp(-0.5*x*x) * l_sum);
  }
  else{
    return 1.0 - cndf(-x);
  }
}
  
void VanillaOption::initialize(){
  K = 500.0;	// strike price
  r = 0.02;	// 2% interest rate
  T = 0.5;	// contract's time to maturity (0.5 year)
  S = 500.0;	// Underlying's asset price (option at the money: spot == strike)
  sigma = 0.2;
}

void VanillaOption::copy(const VanillaOption &option){
  K = option.getK();	// We need accessor method to retrieve passed option's data
  r = option.getr();
  T = option.getT();
  S = option.getS();
  sigma = option.getsigma();
}
