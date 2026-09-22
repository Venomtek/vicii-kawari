all: simple list.txt index.html

simple: simple/simple.prg

simple/simple.prg: simple/simple.bas
	petcat -w2 -o simple/simple.prg -- simple/simple.bas

index.html: report_gen.py
	python3 report_gen.py > index.html

list.txt:
	find VICII -name '*.prg' -type f > list.txt
	find . -name '*.vsf' -type f >> list.txt
	find glitches -name '*.prg' -type f >> list.txt

clean:
	rm -f list.txt
	rm -f index.html

clean_results:
	find . -name 'vice_*.png' -exec rm -f {} \;
	find . -name 'vice_*.log' -exec rm -f {} \;
	find . -name 'fpga_*.png' -exec rm -f {} \;

publish:
	sudo mkdir -p /var/www/html/tests/VICII
	sudo mkdir -p /var/www/html/tests/snapshots
	sudo mkdir -p /var/www/html/tests/glitches
	sudo cp -R VICII/* /var/www/html/tests/VICII
	sudo cp -R snapshots/* /var/www/html/tests/snapshots
	sudo cp -R glitches/* /var/www/html/tests/glitches
	sudo cp index.html /var/www/html
	sudo chown -R root:root  /var/www/html/*
	sudo chmod -R oug+rw /var/www/html/*
	sudo find /var/www/html -type d -exec chmod oug+x {} \;

host:
	@cd /var/www/html; python3 -m http.server
