/* This class describes a vanilla option class */
#ifndef _vanilla_option_h
#define _vanilla_option_h
#define _USE_MATH_DEFINES	/* imports constant definitions from cmath lib */	
#include <string>
#include <cmath>		/* sqrt, log, pow, exp */
using namespace std;

class VanillaOption{

 public:
  VanillaOption();				/* default constructor, no params */
  VanillaOption(const double &_K, const double &_r,
		const double &_T, const double &_S,
		const double &_sigma);		/* parameter constructor */
  VanillaOption(const VanillaOption &option);	/* copy constructor */
  VanillaOption &operator=(const VanillaOption &option);	/* Assignment overloading */
  virtual ~VanillaOption();					/* destructor */
  double getK() const;
  double getr() const;
  double getT() const;
  double getS() const;
  double getsigma() const;
  double calculateCallPrice() const;
  double calculatePutPrice() const;
  double cndf(const double &x) const;
  string optionState() const;			/* in/out/at the money */
 private:
  double K;		/* strike price */
  double r;		/* risk-free rate */
  double T;		/* contract's maturity time */
  double S;		/* Underlying asset price */
  double sigma;		/* Volatility of underlying asset */

  void initialize();
  void copy(const VanillaOption &option);
};
#endif
