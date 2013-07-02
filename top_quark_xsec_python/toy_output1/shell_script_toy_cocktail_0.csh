#!/usr/bin/tcsh


#foreach i (`seq -w 0 100`)

#    echo python toy_cocktail.py toy_output/output_ttbar/toy_output_ttbar_njets4_$i.dat toy_output/output_wjets/toy_output_wjets_njets4_000.dat toy_output/output_qcd/toy_output_qcd_njets4_000.dat toy_output/output_t/toy_output_t_njets4_000.dat toy_output/output_tbar/toy_output_tbar_njets4_000.dat  > log.log
    
#end

@ i = 0

while ( $i < 1000 ) 
    set filename_0 = `printf "toy_output_ttbar_njets4_%05d.dat" $i` 
    set filename_1 = `printf "toy_output_wjets_njets4_%05d.dat" $i`    
    set filename_2 = `printf "toy_output_qcd_njets4_%05d.dat" $i`
    set filename_3 = `printf "toy_output_t_njets4_%05d.dat" $i`
    set filename_4 = `printf "toy_output_tbar_njets4_%05d.dat" $i`

    python ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/toy_cocktail_0.py  ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_ttbar/$filename_0  ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_wjets/$filename_1  ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_qcd/$filename_2  ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_t/$filename_3  ~/Siena_College_Danielle_Berish/top_quark_xsec_python/toy_output1/output/output_tbar/$filename_4 > log.log  
    
    @ i += 1

    if ( $i % 10 == 0 ) then
        echo $i
    endif

end
