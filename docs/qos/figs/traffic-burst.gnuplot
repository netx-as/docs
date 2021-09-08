set terminal pdfcairo font "Gill Sans,9" linewidth 1 rounded fontscale 1.0
set output "traffic-burst.pdf

# Line style for grid
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set style line 1 lt rgb "#A00000" lw 0.5 pt 1
set style line 2 lt rgb "#00A000" lw 0.5 pt 6
set style line 3 lt rgb "#5060D0" lw 1 pt 2
set style line 4 lt rgb "#F25900" lw 1 pt 9

#set grid back linestyle 81
set border 1 back 

set xtics nomirror
set ytics nomirror

set xrange[0:60]
set yrange[0:150]

set xlabel 'time (s)'
set ylabel 'Bandwidth (Mb/s)'

$data << EOD
0   120   30  0 0xA00000
30  120   0   -20 0xA00000


30  100   30 0 0x5060D0
EOD


plot "$data" i 0 using 1:2:3:4:5 with vectors nohead lw 1 lc rgb variable title "Burst traffic", \
	  ""     i 1 using 1:2:3:4:5 w vectors nohead lw 1 lc rgb variable title "Bandwidth limit"
