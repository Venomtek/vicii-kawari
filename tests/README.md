Prerequisites

    sudo apt-get install imagemagick python3-pil

To compare all matching FPGA and VICE PRG screenshots recursively (allowing up to four pixels of horizontal and vertical displacement):

    ./compare_screenshots.py

An alternate search directory or offset limit can be supplied when needed:

    ./compare_screenshots.py path/to/screenshots --max-offset 1

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
    make all
    make publish
    make host

To clean local dir of all results

    make clean_results

