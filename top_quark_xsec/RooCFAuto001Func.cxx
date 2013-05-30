/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "RooCFAuto001Func.h" 
#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <math.h> 
#include "TMath.h" 

ClassImp(RooCFAuto001Func) 

 RooCFAuto001Func::RooCFAuto001Func(const char *name, const char *title, 
                        RooAbsReal& _nt_kappa,
                        RooAbsReal& _beta_nt) :
   RooAbsReal(name,title), 
   nt_kappa("nt_kappa","nt_kappa",this,_nt_kappa),
   beta_nt("beta_nt","beta_nt",this,_beta_nt)
 { 
 } 


 RooCFAuto001Func::RooCFAuto001Func(const RooCFAuto001Func& other, const char* name) :  
   RooAbsReal(other,name), 
   nt_kappa("nt_kappa",this,other.nt_kappa),
   beta_nt("beta_nt",this,other.beta_nt)
 { 
 } 



 Double_t RooCFAuto001Func::evaluate() const 
 { 
   // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
   return pow(nt_kappa,beta_nt) ; 
 } 



