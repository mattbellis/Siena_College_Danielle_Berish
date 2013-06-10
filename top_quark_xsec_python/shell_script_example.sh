#!/bin/tcsh

@ i = 0

while ( $i < 100 ) 

    set filename = `printf "file%03d.txt" $i`
    echo $filename

    @ i += 1

end
