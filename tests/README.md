Prerequisites

    sudo apt-get install imagemagick

Make sure the roms are read by VICE correctly. This version
used to test Kawari expects these:

    d1541II  -> dos1541ii-251968-03.bin
    kernal   -> kernal-901227-03.bin
    basic    -> basic-901226-01.bin
    chargen  -> chargen-901225-01.bin

Use links or copy files to the correct names in .config/vice/C64 and DRIVES
folders.

To generate a full report

    make clean
    ./test_all.sh
    make
    make publish

To clean local dir of all results

    make clean_results

NOTE: colors.bin and sine.bin must be in this dir for tests script to run
