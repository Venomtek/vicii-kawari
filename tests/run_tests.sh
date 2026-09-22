#!/bin/bash

# Change to no to view output of both VICE and sim
HIDE_WINDOWS=yes

# Where is the parent dir of vicii-vice-3.4 ?
VICII_PARENT=/home/rrossi/src/kawari

cp ../hdl/sine.bin .
cp ../hdl/colors.bin .
cp ../hdl/luma_rev4.bin .

if [ "$1" = "" ]
then
   input="tests.txt"
   total=`wc -l < $input`
else
   echo "$1 PAL" > /tmp/test.txt
   input=/tmp/test.txt
   total=1
fi

if [ "$HIDE_WINDOWS" = "yes" ]
then
   SDLDRIVER=dummy
else
   SDLDRIVER=
fi

current=0
while read -r line
do
    stringarray=($line)

    i=${stringarray[0]}

    j=`basename $i`
    k=`dirname $i`

    if [ "${stringarray[1]}" == "NTSC" ]
    then
        standard="-ntsc"
        model="6567"
        chip="0"
        resolution="520x263"
        color=kawari-ntsc.vpl
    elif [ "${stringarray[1]}" == "NTSCOLD" ]
    then
        standard="-ntsc"
        model="6567r56a"
        chip="2"
        resolution="512x262"
        color=kawari-ntsc.vpl
    else
        standard="-pal"
        model="6569"
        chip="1"
        resolution="512x312"
        color=kawari-pal.vpl
    fi

    delay="6"
    if [[ $i == +(*spritecrunch*) ]]
    then
        delay="8"
    elif [[ $i == +(*reg_timing*) ]]
    then
        delay="14"
    elif [[ $i == +(*lightpen*) ]]
    then
        delay="16"
    elif [[ $i == +(*lft-safe-vsp*) ]]
    then
        delay="19"
    elif [[ $i == +(*spritescan*) ]]
    then
        delay="19"
    elif [[ $i == +(*sprite0move*) ]]
    then
        delay="19"
    elif [[ $i == +(*spritevssprite*) ]]
    then
        delay="19"
    fi

    killall -9 x64sc > /dev/null 2> /dev/null

    echo -n "$i "
    pushd ${VICII_PARENT}/vicii-vice-3.4 > /dev/null
        SDL_RENDER_DRIVER=software SDL_VIDEODRIVER=$SDLDRIVER \
            ./src/x64sc -sounddev dummy $standard -VICIImodel $model \
                -drive8type 1541 \
                -VICIIborders 2 \
                -VICIIextpal -VICIIpalette data/C64/$color \
        "${VICII_PARENT}/vicii-kawari/tests/$i" 1> /dev/null 2> vice.log &
    popd > /dev/null
    sleep $delay
    rm -f screenshot.bmp
    SDL_RENDER_DRIVER=software SDL_VIDEODRIVER=$SDLDRIVER \
            ../simulator/obj_dir/Vtop \
               -k -q -w -z -x -c $chip > sim.log 2> /dev/null
    sleep 1

    mv ${VICII_PARENT}/vicii-vice-3.4/vice.log $k/vice_$j.log
    mv sim.log $k/sim_$j.log

    convert screenshot.bmp -interpolate Integer -filter point -resize $resolution $k/fpga_$j.png > /dev/null 2> /dev/null
    mv ${VICII_PARENT}/vicii-vice-3.4/screenshot.png $k/vice_$j.png

    current=$((current + 1))
    percent=$((current * 100 / $total))
    echo "$current / $total ($percent%)"

done < "$input"
