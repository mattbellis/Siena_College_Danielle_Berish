#!/bin/tcsh

@ i = 0

while ( $i < 1000 ) 

    set filename = `printf "toy_cocktail_output_%05d.dat" $i`

    python ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/fit_0.py ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_cocktail/$filename >> new_single_poisson.log 

    @ i += 1


    if ( $i % 10 == 0 ) then
        echo $i
     endif

end
