set terminal pngcairo  transparent enhanced font "arial,12" fontscale 1.0 size 600, 600
set output '../images/fnfa.png'

set samples 1000
set border 1+2+4+8+16+32+64 front lt black linewidth 0.500 dashtype solid
# set border 128+256+512+1024+2048 back lt black linewidth 0.500 dashtype '-'

# set border 4095 back lt black linewidth 0.500 dashtype '-'

# set grid noxtics nomxtics noytics nomytics ztics nomztics nortics nomrtics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set grid xtics ytics ztics


set grid layerdefault   lt 0 linecolor 0 linewidth 0.500,  lt 0 linecolor 0 linewidth 0.500
set key at screen 0.9, 0.8 right top vertical Right noreverse enhanced autotitle box lt black linewidth 1.000 dashtype solid
set key noinvert samplen 4 spacing 1 width 0 height 1
set key opaque
set style increment default
set style data lines
set xyplane at 0

set xtics offset 0,-0.5
set ytics offset 0,-0.5

set ztics 0,20,100
set ytics (2,5,10)
set xtics (20,35,50,75,100)

set xlabel "n"
set xlabel offset 0,-0.5
set ylabel "k"
set ylabel offset 0,-0.5
set zlabel "%"

# set title "Finitely Ambiguous Automata"
unset title

set xrange [ 0 : 100 ] noreverse writeback
set x2range [ 0 : 100 ] noreverse writeback
set yrange [ 0 : 10 ] noreverse nowriteback
set y2range [ 0 : 10 ] noreverse writeback
set zrange [ -1 : 100 ] noreverse writeback

set cbrange [ * : * ] noreverse writeback
set rrange [ * : * ] noreverse writeback
## Last datafile plotted: "silver.dat"

# set view 60, 30, 1, 1
set view 80, 60, 1, 1

set multiplot

set dgrid3d splines

splot \
 \
'pd_fnfa.dat' every ::0::4 using 1:2:3 with lines linecolor rgb "orange" dashtype 1 title "PD", \
'pd_fnfa.dat' every ::5::9 using 1:2:3 with lines linecolor rgb "orange" dashtype 1 title "", \
'pd_fnfa.dat' every ::10::14 using 1:2:3 with lines linecolor rgb "orange" dashtype 1 title "", \
 \
'position_fnfa.dat' every ::0::4 using 1:2:3 with lines linecolor rgb "blue" dashtype 1 title "Position", \
'position_fnfa.dat' every ::5::9 using 1:2:3 with lines linecolor rgb "blue" dashtype 1 title "", \
'position_fnfa.dat' every ::10::14 using 1:2:3 with lines linecolor rgb "blue" dashtype 1 title ""

#'pd_fnfa.dat' every ::0::4 using 1:($2-0.1):3 with lines linecolor rgb "orange" dashtype 1 title "",\
#'pd_fnfa.dat' every ::8::8 using 1:($2-0.1):3 with lines linecolor rgb "orange" dashtype 1 title "",\
#'pd_fnfa.dat' every ::10::14 using 1:($2-0.1):3 with lines linecolor rgb "orange" dashtype 1 title "",\

#'position_fnfa.dat' every ::0::4 using 1:($2-0.1):3 with lines linecolor rgb "blue" dashtype 1 title "",\
#'position_fnfa.dat' every ::8::8 using 1:($2-0.1):3 with lines linecolor rgb "blue" dashtype 1 title "",\
#'position_fnfa.dat' every ::10::14 using 1:($2-0.1):3 with lines linecolor rgb "blue" dashtype 1 title ""

unset dgrid3d
unset key

splot 'pd_fnfa.dat' every ::0::4 using 1:2:3 with points linecolor rgb "black" lw 3 title ""
splot 'pd_fnfa.dat' every ::5::9 using 1:2:3 with points linecolor rgb "black" lw 3 title ""
splot 'pd_fnfa.dat' every ::10::14 using 1:2:3 with points linecolor rgb "black" lw 3 title ""

splot 'position_fnfa.dat' every ::0::4 using 1:2:3 with points linecolor rgb "black" lw 3 title ""
splot 'position_fnfa.dat' every ::5::9 using 1:2:3 with points linecolor rgb "black" lw 3 title ""
splot 'position_fnfa.dat' every ::10::14 using 1:2:3 with points linecolor rgb "black" lw 3 title ""
