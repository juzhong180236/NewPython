"""Script generated by ansys-mapdl-core version 0.59.3"""
from ansys.mapdl.core import launch_mapdl
mapdl = launch_mapdl(loglevel="WARNING")
mapdl.run("/batch")
mapdl.run("/config,noeldb,1     ")  # force off writing results to database
mapdl.get("_wallstrt", "active", "", "time", "wall")
# ANSYS input file written by Workbench version 2021 R1
# File used for geometry attach: D:\Alai\ansys_Alai\AeroFoil\shell_181\1_files\dp0\SYS\DM\SYS.agdb
mapdl.title("1--Static Structural (A5)")
# ****** Begin Custom Load Command Snippet ******
# CT Extensions:
# SDYNA 2021.1
# f463412-bd3e-484b-87e7-cbc0a665e474 wbex
# 
# ****** End   Custom Load Command Snippet ******
mapdl.run("*DIM,_wb_ProjectScratch_dir,string,248")
mapdl.run("_wb_ProjectScratch_dir(1) = 'D:\Alai\ansys_Alai\AeroFoil\shell_181\_ProjectScratch\ScrF078\'")
mapdl.run("*DIM,_wb_SolverFiles_dir,string,248")
mapdl.run("_wb_SolverFiles_dir(1) = 'D:\Alai\ansys_Alai\AeroFoil\shell_181\1_files\dp0\SYS\MECH\'")
mapdl.run("*DIM,_wb_userfiles_dir,string,248")
mapdl.run("_wb_userfiles_dir(1) = 'D:\Alai\ansys_Alai\AeroFoil\shell_181\1_files\user_files\'")
# -- Data in consistent NMM units. See Solving Units in the help system for more information.
mapdl.run("/units,MPA")
mapdl.run("/nopr")
mapdl.run("/wb,file,start              ")  # signify a WB generated input file
mapdl.prep7()
# Turn off shape checking because checks already performed inside WB mesher.
# See help system for more information.
mapdl.shpp("OFF", "", "NOWARN")
mapdl.run("/nolist")
mapdl.run("etcon,set             ")  # allow ANSYS to choose best KEYOP's for 180x elements, resets any applicable keyopt to MAPDL defaults
# ********** Nodes for the whole assembly ***********
mapdl.run("nblock,3,,162")
mapdl.run("(1i9,3e20.9e3)")
mapdl.run("1     2.802000000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("2     0.000000000E+00     0.000000000E+00     0.000000000E+00")
mapdl.run("3     2.802000000E+02     1.600000000E+01     0.000000000E+00")
mapdl.run("4     6.000000000E+01     5.000000000E+01     0.000000000E+00")
mapdl.run("5     0.000000000E+00     5.000000000E+01     0.000000000E+00")
mapdl.run("6     2.723896825E+02     5.738095238E+00     0.000000000E+00")
mapdl.run("7     2.645793651E+02     6.142857143E+00     0.000000000E+00")
mapdl.run("8     2.567690476E+02     6.547619048E+00     0.000000000E+00")
mapdl.run("9     2.489587302E+02     6.952380952E+00     0.000000000E+00")
mapdl.run("10     2.411484127E+02     7.357142857E+00     0.000000000E+00")
mapdl.run("11     2.333380952E+02     7.761904762E+00     0.000000000E+00")
mapdl.run("12     2.255277778E+02     8.166666667E+00     0.000000000E+00")
mapdl.run("13     2.177174603E+02     8.571428571E+00     0.000000000E+00")
mapdl.run("14     2.099071429E+02     8.976190476E+00     0.000000000E+00")
mapdl.run("15     2.020968254E+02     9.380952381E+00     0.000000000E+00")
mapdl.run("16     1.942865079E+02     9.785714286E+00     0.000000000E+00")
mapdl.run("17     1.864761905E+02     1.019047619E+01     0.000000000E+00")
mapdl.run("18     1.786658730E+02     1.059523810E+01     0.000000000E+00")
mapdl.run("19     1.708555556E+02     1.100000000E+01     0.000000000E+00")
mapdl.run("20     1.630452381E+02     1.140476190E+01     0.000000000E+00")
mapdl.run("21     1.552349206E+02     1.180952381E+01     0.000000000E+00")
mapdl.run("22     1.474246032E+02     1.221428571E+01     0.000000000E+00")
mapdl.run("23     1.396142857E+02     1.261904762E+01     0.000000000E+00")
mapdl.run("24     1.318039683E+02     1.302380952E+01     0.000000000E+00")
mapdl.run("25     1.239936508E+02     1.342857143E+01     0.000000000E+00")
mapdl.run("26     1.161833333E+02     1.383333333E+01     0.000000000E+00")
mapdl.run("27     1.083730159E+02     1.423809524E+01     0.000000000E+00")
mapdl.run("28     1.005626984E+02     1.464285714E+01     0.000000000E+00")
mapdl.run("29     9.275238095E+01     1.504761905E+01     0.000000000E+00")
mapdl.run("30     8.494206349E+01     1.545238095E+01     0.000000000E+00")
mapdl.run("31     7.713174603E+01     1.585714286E+01     0.000000000E+00")
mapdl.run("32     6.932142857E+01     1.626190476E+01     0.000000000E+00")
mapdl.run("33     6.151111111E+01     1.666666667E+01     0.000000000E+00")
mapdl.run("34     5.382222222E+01     1.666666667E+01     0.000000000E+00")
mapdl.run("35     4.613333333E+01     1.666666667E+01     0.000000000E+00")
mapdl.run("36     3.844444444E+01     1.666666667E+01     0.000000000E+00")
mapdl.run("37     3.075555556E+01     1.666666667E+01     0.000000000E+00")
mapdl.run("38     2.306666667E+01     1.666666667E+01     0.000000000E+00")
mapdl.run("39     1.537777778E+01     1.666666667E+01     0.000000000E+00")
mapdl.run("40     7.688888889E+00     1.666666667E+01     0.000000000E+00")
mapdl.run("41     2.723626984E+02     1.147619048E+01     0.000000000E+00")
mapdl.run("42     2.645253968E+02     1.228571429E+01     0.000000000E+00")
mapdl.run("43     2.566880952E+02     1.309523810E+01     0.000000000E+00")
mapdl.run("44     2.488507937E+02     1.390476190E+01     0.000000000E+00")
mapdl.run("45     2.410134921E+02     1.471428571E+01     0.000000000E+00")
mapdl.run("46     2.331761905E+02     1.552380952E+01     0.000000000E+00")
mapdl.run("47     2.253388889E+02     1.633333333E+01     0.000000000E+00")
mapdl.run("48     2.175015873E+02     1.714285714E+01     0.000000000E+00")
mapdl.run("49     2.096642857E+02     1.795238095E+01     0.000000000E+00")
mapdl.run("50     2.018269841E+02     1.876190476E+01     0.000000000E+00")
mapdl.run("51     1.939896825E+02     1.957142857E+01     0.000000000E+00")
mapdl.run("52     1.861523810E+02     2.038095238E+01     0.000000000E+00")
mapdl.run("53     1.783150794E+02     2.119047619E+01     0.000000000E+00")
mapdl.run("54     1.704777778E+02     2.200000000E+01     0.000000000E+00")
mapdl.run("55     1.626404762E+02     2.280952381E+01     0.000000000E+00")
mapdl.run("56     1.548031746E+02     2.361904762E+01     0.000000000E+00")
mapdl.run("57     1.469658730E+02     2.442857143E+01     0.000000000E+00")
mapdl.run("58     1.391285714E+02     2.523809524E+01     0.000000000E+00")
mapdl.run("59     1.312912698E+02     2.604761905E+01     0.000000000E+00")
mapdl.run("60     1.234539683E+02     2.685714286E+01     0.000000000E+00")
mapdl.run("61     1.156166667E+02     2.766666667E+01     0.000000000E+00")
mapdl.run("62     1.077793651E+02     2.847619048E+01     0.000000000E+00")
mapdl.run("63     9.994206349E+01     2.928571429E+01     0.000000000E+00")
mapdl.run("64     9.210476190E+01     3.009523810E+01     0.000000000E+00")
mapdl.run("65     8.426746032E+01     3.090476190E+01     0.000000000E+00")
mapdl.run("66     7.643015873E+01     3.171428571E+01     0.000000000E+00")
mapdl.run("67     6.859285714E+01     3.252380952E+01     0.000000000E+00")
mapdl.run("68     6.075555556E+01     3.333333333E+01     0.000000000E+00")
mapdl.run("69     5.316111111E+01     3.333333333E+01     0.000000000E+00")
mapdl.run("70     4.556666667E+01     3.333333333E+01     0.000000000E+00")
mapdl.run("71     3.797222222E+01     3.333333333E+01     0.000000000E+00")
mapdl.run("72     3.037777778E+01     3.333333333E+01     0.000000000E+00")
mapdl.run("73     2.278333333E+01     3.333333333E+01     0.000000000E+00")
mapdl.run("74     1.518888889E+01     3.333333333E+01     0.000000000E+00")
mapdl.run("75     7.594444444E+00     3.333333333E+01     0.000000000E+00")
mapdl.run("76     0.000000000E+00     1.666666667E+01     0.000000000E+00")
mapdl.run("77     0.000000000E+00     3.333333333E+01     0.000000000E+00")
mapdl.run("78     7.500000000E+00     5.000000000E+01     0.000000000E+00")
mapdl.run("79     1.500000000E+01     5.000000000E+01     0.000000000E+00")
mapdl.run("80     2.250000000E+01     5.000000000E+01     0.000000000E+00")
mapdl.run("81     3.000000000E+01     5.000000000E+01     0.000000000E+00")
mapdl.run("82     3.750000000E+01     5.000000000E+01     0.000000000E+00")
mapdl.run("83     4.500000000E+01     5.000000000E+01     0.000000000E+00")
mapdl.run("84     5.250000000E+01     5.000000000E+01     0.000000000E+00")
mapdl.run("85     6.786428571E+01     4.878571429E+01     0.000000000E+00")
mapdl.run("86     7.572857143E+01     4.757142857E+01     0.000000000E+00")
mapdl.run("87     8.359285714E+01     4.635714286E+01     0.000000000E+00")
mapdl.run("88     9.145714286E+01     4.514285714E+01     0.000000000E+00")
mapdl.run("89     9.932142857E+01     4.392857143E+01     0.000000000E+00")
mapdl.run("90     1.071857143E+02     4.271428571E+01     0.000000000E+00")
mapdl.run("91     1.150500000E+02     4.150000000E+01     0.000000000E+00")
mapdl.run("92     1.229142857E+02     4.028571429E+01     0.000000000E+00")
mapdl.run("93     1.307785714E+02     3.907142857E+01     0.000000000E+00")
mapdl.run("94     1.386428571E+02     3.785714286E+01     0.000000000E+00")
mapdl.run("95     1.465071429E+02     3.664285714E+01     0.000000000E+00")
mapdl.run("96     1.543714286E+02     3.542857143E+01     0.000000000E+00")
mapdl.run("97     1.622357143E+02     3.421428571E+01     0.000000000E+00")
mapdl.run("98     1.701000000E+02     3.300000000E+01     0.000000000E+00")
mapdl.run("99     1.779642857E+02     3.178571429E+01     0.000000000E+00")
mapdl.run("100     1.858285714E+02     3.057142857E+01     0.000000000E+00")
mapdl.run("101     1.936928571E+02     2.935714286E+01     0.000000000E+00")
mapdl.run("102     2.015571429E+02     2.814285714E+01     0.000000000E+00")
mapdl.run("103     2.094214286E+02     2.692857143E+01     0.000000000E+00")
mapdl.run("104     2.172857143E+02     2.571428571E+01     0.000000000E+00")
mapdl.run("105     2.251500000E+02     2.450000000E+01     0.000000000E+00")
mapdl.run("106     2.330142857E+02     2.328571429E+01     0.000000000E+00")
mapdl.run("107     2.408785714E+02     2.207142857E+01     0.000000000E+00")
mapdl.run("108     2.487428571E+02     2.085714286E+01     0.000000000E+00")
mapdl.run("109     2.566071429E+02     1.964285714E+01     0.000000000E+00")
mapdl.run("110     2.644714286E+02     1.842857143E+01     0.000000000E+00")
mapdl.run("111     2.723357143E+02     1.721428571E+01     0.000000000E+00")
mapdl.run("112     2.802000000E+02     1.066666667E+01     0.000000000E+00")
mapdl.run("113     2.802000000E+02     5.333333333E+00     0.000000000E+00")
mapdl.run("114     2.724166667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("115     2.646333333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("116     2.568500000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("117     2.490666667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("118     2.412833333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("119     2.335000000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("120     2.257166667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("121     2.179333333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("122     2.101500000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("123     2.023666667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("124     1.945833333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("125     1.868000000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("126     1.790166667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("127     1.712333333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("128     1.634500000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("129     1.556666667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("130     1.478833333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("131     1.401000000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("132     1.323166667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("133     1.245333333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("134     1.167500000E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("135     1.089666667E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("136     1.011833333E+02     0.000000000E+00     0.000000000E+00")
mapdl.run("137     9.340000000E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("138     8.561666667E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("139     7.783333333E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("140     7.005000000E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("141     6.226666667E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("142     5.448333333E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("143     4.670000000E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("144     3.891666667E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("145     3.113333333E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("146     2.335000000E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("147     1.556666667E+01     0.000000000E+00     0.000000000E+00")
mapdl.run("148     7.783333333E+00     0.000000000E+00     0.000000000E+00")
mapdl.run("-1")
mapdl.run("/wb,elem,start            ")  # set before creation of elements
# ********** Elements for Body 1 'Surface Body' ***********
mapdl.et(1, 181)
mapdl.run("keyo,1,3,2")
mapdl.run("eblock,19,solid,,108")
mapdl.run("(19i9)")
mapdl.run("1        1        1        1        0        0        0        0        4        0        1      113        6      114        1")
mapdl.run("1        1        1        1        0        0        0        0        4        0        2      112       41        6      113")
mapdl.run("1        1        1        1        0        0        0        0        4        0        3        3      111       41      112")
mapdl.run("1        1        1        1        0        0        0        0        4        0        4        6        7      115      114")
mapdl.run("1        1        1        1        0        0        0        0        4        0        5       41       42        7        6")
mapdl.run("1        1        1        1        0        0        0        0        4        0        6      111      110       42       41")
mapdl.run("1        1        1        1        0        0        0        0        4        0        7        7        8      116      115")
mapdl.run("1        1        1        1        0        0        0        0        4        0        8       42       43        8        7")
mapdl.run("1        1        1        1        0        0        0        0        4        0        9      110      109       43       42")
mapdl.run("1        1        1        1        0        0        0        0        4        0       10        8        9      117      116")
mapdl.run("1        1        1        1        0        0        0        0        4        0       11       43       44        9        8")
mapdl.run("1        1        1        1        0        0        0        0        4        0       12      109      108       44       43")
mapdl.run("1        1        1        1        0        0        0        0        4        0       13        9       10      118      117")
mapdl.run("1        1        1        1        0        0        0        0        4        0       14       44       45       10        9")
mapdl.run("1        1        1        1        0        0        0        0        4        0       15      108      107       45       44")
mapdl.run("1        1        1        1        0        0        0        0        4        0       16       10       11      119      118")
mapdl.run("1        1        1        1        0        0        0        0        4        0       17       45       46       11       10")
mapdl.run("1        1        1        1        0        0        0        0        4        0       18      107      106       46       45")
mapdl.run("1        1        1        1        0        0        0        0        4        0       19       11       12      120      119")
mapdl.run("1        1        1        1        0        0        0        0        4        0       20       46       47       12       11")
mapdl.run("1        1        1        1        0        0        0        0        4        0       21      106      105       47       46")
mapdl.run("1        1        1        1        0        0        0        0        4        0       22       12       13      121      120")
mapdl.run("1        1        1        1        0        0        0        0        4        0       23       47       48       13       12")
mapdl.run("1        1        1        1        0        0        0        0        4        0       24      105      104       48       47")
mapdl.run("1        1        1        1        0        0        0        0        4        0       25       13       14      122      121")
mapdl.run("1        1        1        1        0        0        0        0        4        0       26       48       49       14       13")
mapdl.run("1        1        1        1        0        0        0        0        4        0       27      104      103       49       48")
mapdl.run("1        1        1        1        0        0        0        0        4        0       28       14       15      123      122")
mapdl.run("1        1        1        1        0        0        0        0        4        0       29       49       50       15       14")
mapdl.run("1        1        1        1        0        0        0        0        4        0       30      103      102       50       49")
mapdl.run("1        1        1        1        0        0        0        0        4        0       31       15       16      124      123")
mapdl.run("1        1        1        1        0        0        0        0        4        0       32       50       51       16       15")
mapdl.run("1        1        1        1        0        0        0        0        4        0       33      102      101       51       50")
mapdl.run("1        1        1        1        0        0        0        0        4        0       34       16       17      125      124")
mapdl.run("1        1        1        1        0        0        0        0        4        0       35       51       52       17       16")
mapdl.run("1        1        1        1        0        0        0        0        4        0       36      101      100       52       51")
mapdl.run("1        1        1        1        0        0        0        0        4        0       37       17       18      126      125")
mapdl.run("1        1        1        1        0        0        0        0        4        0       38       52       53       18       17")
mapdl.run("1        1        1        1        0        0        0        0        4        0       39      100       99       53       52")
mapdl.run("1        1        1        1        0        0        0        0        4        0       40       18       19      127      126")
mapdl.run("1        1        1        1        0        0        0        0        4        0       41       53       54       19       18")
mapdl.run("1        1        1        1        0        0        0        0        4        0       42       99       98       54       53")
mapdl.run("1        1        1        1        0        0        0        0        4        0       43       19       20      128      127")
mapdl.run("1        1        1        1        0        0        0        0        4        0       44       54       55       20       19")
mapdl.run("1        1        1        1        0        0        0        0        4        0       45       98       97       55       54")
mapdl.run("1        1        1        1        0        0        0        0        4        0       46       20       21      129      128")
mapdl.run("1        1        1        1        0        0        0        0        4        0       47       55       56       21       20")
mapdl.run("1        1        1        1        0        0        0        0        4        0       48       97       96       56       55")
mapdl.run("1        1        1        1        0        0        0        0        4        0       49       21       22      130      129")
mapdl.run("1        1        1        1        0        0        0        0        4        0       50       56       57       22       21")
mapdl.run("1        1        1        1        0        0        0        0        4        0       51       96       95       57       56")
mapdl.run("1        1        1        1        0        0        0        0        4        0       52       22       23      131      130")
mapdl.run("1        1        1        1        0        0        0        0        4        0       53       57       58       23       22")
mapdl.run("1        1        1        1        0        0        0        0        4        0       54       95       94       58       57")
mapdl.run("1        1        1        1        0        0        0        0        4        0       55       23       24      132      131")
mapdl.run("1        1        1        1        0        0        0        0        4        0       56       58       59       24       23")
mapdl.run("1        1        1        1        0        0        0        0        4        0       57       94       93       59       58")
mapdl.run("1        1        1        1        0        0        0        0        4        0       58       24       25      133      132")
mapdl.run("1        1        1        1        0        0        0        0        4        0       59       59       60       25       24")
mapdl.run("1        1        1        1        0        0        0        0        4        0       60       93       92       60       59")
mapdl.run("1        1        1        1        0        0        0        0        4        0       61       25       26      134      133")
mapdl.run("1        1        1        1        0        0        0        0        4        0       62       60       61       26       25")
mapdl.run("1        1        1        1        0        0        0        0        4        0       63       92       91       61       60")
mapdl.run("1        1        1        1        0        0        0        0        4        0       64       26       27      135      134")
mapdl.run("1        1        1        1        0        0        0        0        4        0       65       61       62       27       26")
mapdl.run("1        1        1        1        0        0        0        0        4        0       66       91       90       62       61")
mapdl.run("1        1        1        1        0        0        0        0        4        0       67       27       28      136      135")
mapdl.run("1        1        1        1        0        0        0        0        4        0       68       62       63       28       27")
mapdl.run("1        1        1        1        0        0        0        0        4        0       69       90       89       63       62")
mapdl.run("1        1        1        1        0        0        0        0        4        0       70       28       29      137      136")
mapdl.run("1        1        1        1        0        0        0        0        4        0       71       63       64       29       28")
mapdl.run("1        1        1        1        0        0        0        0        4        0       72       89       88       64       63")
mapdl.run("1        1        1        1        0        0        0        0        4        0       73       29       30      138      137")
mapdl.run("1        1        1        1        0        0        0        0        4        0       74       64       65       30       29")
mapdl.run("1        1        1        1        0        0        0        0        4        0       75       88       87       65       64")
mapdl.run("1        1        1        1        0        0        0        0        4        0       76       30       31      139      138")
mapdl.run("1        1        1        1        0        0        0        0        4        0       77       65       66       31       30")
mapdl.run("1        1        1        1        0        0        0        0        4        0       78       87       86       66       65")
mapdl.run("1        1        1        1        0        0        0        0        4        0       79       31       32      140      139")
mapdl.run("1        1        1        1        0        0        0        0        4        0       80       66       67       32       31")
mapdl.run("1        1        1        1        0        0        0        0        4        0       81       86       85       67       66")
mapdl.run("1        1        1        1        0        0        0        0        4        0       82       32       33      141      140")
mapdl.run("1        1        1        1        0        0        0        0        4        0       83       67       68       33       32")
mapdl.run("1        1        1        1        0        0        0        0        4        0       84       85        4       68       67")
mapdl.run("1        1        1        1        0        0        0        0        4        0       85       33       34      142      141")
mapdl.run("1        1        1        1        0        0        0        0        4        0       86       68       69       34       33")
mapdl.run("1        1        1        1        0        0        0        0        4        0       87        4       84       69       68")
mapdl.run("1        1        1        1        0        0        0        0        4        0       88       34       35      143      142")
mapdl.run("1        1        1        1        0        0        0        0        4        0       89       69       70       35       34")
mapdl.run("1        1        1        1        0        0        0        0        4        0       90       84       83       70       69")
mapdl.run("1        1        1        1        0        0        0        0        4        0       91       35       36      144      143")
mapdl.run("1        1        1        1        0        0        0        0        4        0       92       70       71       36       35")
mapdl.run("1        1        1        1        0        0        0        0        4        0       93       83       82       71       70")
mapdl.run("1        1        1        1        0        0        0        0        4        0       94       36       37      145      144")
mapdl.run("1        1        1        1        0        0        0        0        4        0       95       71       72       37       36")
mapdl.run("1        1        1        1        0        0        0        0        4        0       96       82       81       72       71")
mapdl.run("1        1        1        1        0        0        0        0        4        0       97       37       38      146      145")
mapdl.run("1        1        1        1        0        0        0        0        4        0       98       72       73       38       37")
mapdl.run("1        1        1        1        0        0        0        0        4        0       99       81       80       73       72")
mapdl.run("1        1        1        1        0        0        0        0        4        0      100       38       39      147      146")
mapdl.run("1        1        1        1        0        0        0        0        4        0      101       73       74       39       38")
mapdl.run("1        1        1        1        0        0        0        0        4        0      102       80       79       74       73")
mapdl.run("1        1        1        1        0        0        0        0        4        0      103       39       40      148      147")
mapdl.run("1        1        1        1        0        0        0        0        4        0      104       74       75       40       39")
mapdl.run("1        1        1        1        0        0        0        0        4        0      105       79       78       75       74")
mapdl.run("1        1        1        1        0        0        0        0        4        0      106       40       76        2      148")
mapdl.run("1        1        1        1        0        0        0        0        4        0      107       75       77       76       40")
mapdl.run("1        1        1        1        0        0        0        0        4        0      108       78        5       77       75")
mapdl.run("-1")
# Material Id = {B144443B-EC07-44E0-86A3-E3612B1F2EAB}
mapdl.run("/wb,elem,end               ")  # done creating elements
# ********** Send User Defined Coordinate System(s) ***********
mapdl.csys(0)
mapdl.toffst(273.15, "")  # Temperature offset from absolute zero
# ********** Set Reference Temperature ***********
mapdl.tref(22.)
mapdl.run("/wb,mat,start              ")  # starting to send materials
# ********** Send Materials ***********
mapdl.mp("EX", 1, 71000, "")  # tonne s^-2 mm^-1
mapdl.mp("NUXY", 1, 0.33, "")
mapdl.mp("DENS", 1, 2.83e-09, "")  # tonne mm^-3
mapdl.run("/wb,mat,end                ")  # done sending materials
# ********** Send Sheet Properties ***********
mapdl.sectype(1, "shell")
mapdl.secdata(1.15)
mapdl.run("secoff,mid")
# ************************* Model Summary ********************
# Surface Body,	aerofoil,	matid,	1
# ************************* End Model Summary ********************
# get the diagonal of the bounding box. Needed later for other things
mapdl.get("_xmin", "node", "", "mnloc", "x")
mapdl.get("_ymin", "node", "", "mnloc", "y")
mapdl.get("_zmin", "node", "", "mnloc", "z")
mapdl.get("_xmax", "node", "", "mxloc", "x")
mapdl.get("_ymax", "node", "", "mxloc", "y")
mapdl.get("_zmax", "node", "", "mxloc", "z")
mapdl.run("_ASMDIAG=(_xmax-_xmin)*(_xmax-_xmin)+(_ymax-_ymin)*(_ymax-_ymin)+(_zmax-_zmin)*(_zmax-_zmin)")
mapdl.run("_ASMDIAG=SQRT(_ASMDIAG)")
mapdl.run("/wb,contact,start          ")  # starting to send contact
mapdl.run("/wb,contact,end            ")  # done creating contacts
mapdl.run("/golist")
mapdl.run("/wb,load,start             ")  # starting to send loads
# ********** Fixed Supports ***********
mapdl.run("CMBLOCK,_FIXEDSU,NODE,        4")
mapdl.run("(8i10)")
mapdl.run("2         5        76        77")
mapdl.cmsel("s", "_FIXEDSU")
mapdl.d("all", "all")
mapdl.nsel("all")
# ********** Create Displacement Tables and Functions ******
mapdl.run("*DIM,_loadvari43zp,TABLE,2,1,1,TIME,")
# Time values
mapdl.run("_loadvari43zp(1,0,1) = 0.")
mapdl.run("_loadvari43zp(2,0,1) = 1.")
# Load values
mapdl.run("_loadvari43zp(1,1,1) = 0.")
mapdl.run("_loadvari43zp(2,1,1) = 80.")
mapdl.run("*DIM,_loadvari43zn,TABLE,2,1,1,TIME,")
# Time values
mapdl.run("_loadvari43zn(1,0,1) = 0.")
mapdl.run("_loadvari43zn(2,0,1) = 1.")
# Load values
mapdl.run("_loadvari43zn(1,1,1) = 0.")
mapdl.run("_loadvari43zn(2,1,1) = -80.")
mapdl.run("/gst,on,on")
mapdl.run("fini")
mapdl.get("_numnode", "node", 0, "count")
mapdl.get("_numelem", "elem", 0, "count")
mapdl.get("_MAXELEMNUM", "elem", 0, "NUM", "MAX")
mapdl.get("_MAXNODENUM", "node", 0, "NUM", "MAX")
mapdl.get("_MAXELEMTYPE", "etyp", 0, "NUM", "MAX")
mapdl.get("_MAXREALCONST", "real", 0, "NUM", "MAX")
mapdl.run("/go")
mapdl.run("/wb,load,end               ")  # done creating loads
# -- Number of total nodes = %_numnode%
# -- Number of contact elements = 0
# -- Number of spring elements = 0
# -- Number of bearing elements = 0
# -- Number of solid elements = 108
# -- Number of condensed parts = 0
# -- Number of total elements = %_numelem%
mapdl.get("_wallbsol", "active", "", "time", "wall")
# ***************************************************************************
# ************************    SOLUTION       ********************************
# ***************************************************************************
mapdl.run("/solu")
mapdl.antype(0)  # static analysis
mapdl.nlgeom("on")  # Turn on Large Deformation Effects
mapdl.run("_thickRatio=  0     ")  # Ratio of thick parts in the model
mapdl.run("eqsl,sparse,,,,,1")
mapdl.cntr("print", 1)  # print out contact info and also make no initial contact an error
mapdl.dmpoption("emat", "no")  # Don't combine emat file for DANSYS
mapdl.dmpoption("esav", "no")  # Don't combine esav file for DANSYS
mapdl.nldiag("cont", "iter")  # print out contact info each equilibrium iteration
mapdl.rescontrol("define", "last", "last", "", "dele")  # Program Controlled
# ***************************************************
# ****************** SOLVE FOR LS 1 OF 1 ****************
# ** Set Displacements ***
mapdl.run("CMBLOCK,_CM43UZ_ZP,NODE,        4")
mapdl.run("(8i10)")
mapdl.run("1         3       112       113")
mapdl.cmsel("s", "_CM43UZ_ZP")
mapdl.d("all", "uz", "%_loadvari43zp%")
mapdl.nsel("all")
# ** Component For All Non-Zero UZ Displacements ***
mapdl.cmsel("s", "_CM43uz_zp")
mapdl.cm("_DISPNONZEROUZ", "NODE")
mapdl.nsel("all")
mapdl.run("/nopr")
mapdl.run("/gopr")
mapdl.run("/nolist")
mapdl.autots("on")  # Workbench Program Controlled automatic time stepping
mapdl.run("nsub,1,10,1                ")  # due to presence of general nonlinear
mapdl.time(1.)
mapdl.outres("erase")
mapdl.outres("all", "none")
mapdl.outres("nsol", "all", "")
mapdl.outres("rsol", "all")
mapdl.outres("eangl", "all")
mapdl.outres("etmp", "all")
mapdl.outres("veng", "all")
mapdl.outres("strs", "all", "")
mapdl.outres("epel", "all", "")
mapdl.outres("eppl", "all", "")
mapdl.outres("cont", "all", "")
# *********** WB SOLVE COMMAND ***********
# check interactive state
mapdl.get("ANSINTER_", "active", "", "int")
with mapdl.non_interactive:
    mapdl.run("*if,ANSINTER_,ne,0,then")
    mapdl.run("/eof")
    mapdl.run("*endif")
    mapdl.solve()
    # 
    mapdl.run("CEWRITE,file,ce,,INTE")
    # ***************************************************
    # ************** FINISHED SOLVE FOR LS 1 *************
    mapdl.get("_wallasol", "active", "", "time", "wall")
    mapdl.run("/nopr")
    mapdl.get("_numnode", "node", 0, "count")
    mapdl.get("_numelem", "elem", 0, "count")
    mapdl.get("_MAXELEMNUM", "elem", 0, "NUM", "MAX")
    mapdl.get("_MAXNODENUM", "node", 0, "NUM", "MAX", "", "", "INTERNAL")
    mapdl.get("_MAXELEMTYPE", "etyp", 0, "NUM", "MAX")
    mapdl.get("_MAXREALCONST", "real", 0, "NUM", "MAX")
    mapdl.run("/gopr")
    mapdl.run("/post1")
    mapdl.run("xmlo,ENCODING,ISO-8859-1")
    mapdl.run("xmlo,parm")
    mapdl.run("/xml,parm,xml")
    mapdl.run("fini")
    mapdl.run("/gopr")
    mapdl.get("_walldone", "active", "", "time", "wall")
    mapdl.run("_preptime=(_wallbsol-_wallstrt)*3600")
    mapdl.run("_solvtime=(_wallasol-_wallbsol)*3600")
    mapdl.run("_posttime=(_walldone-_wallasol)*3600")
    mapdl.run("_totaltim=(_walldone-_wallstrt)*3600")
    mapdl.get("_dlbratio", "active", 0, "solu", "dlbr")
    mapdl.get("_combtime", "active", 0, "solu", "comb")
    # -- Total number of nodes = %_numnode%
    # -- Total number of elements = %_numelem%
    # -- Element load balance ratio = %_dlbratio%
    # -- Time to combine distributed files = %_combtime%
    mapdl.run("/wb,file,end               ")  # done with WB generated input
mapdl.exit()