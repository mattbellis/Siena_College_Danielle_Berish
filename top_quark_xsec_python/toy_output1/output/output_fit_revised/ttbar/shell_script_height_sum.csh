#!/bin/tcsh

@ i = 0

while ( $i < 1000 )
    
    set filename = `printf "toy_output_ttbar_njets4_%05d.dat" $i`

    python ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_fit_revised/height_sum.py ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_ttbar/$filename 

    @ i += 1

end 
