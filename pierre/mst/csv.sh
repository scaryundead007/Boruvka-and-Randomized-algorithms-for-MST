#! /bin/bash

gawk '
{print $1" "$4" "$6" "$8}
' $1 | \
    gawk '
"r" == $1 { a[int((1+NR)/2)][$1] = $2"	"$3"	"$4 }
"k" == $1 { a[int((1+NR)/2)][$1] = $4 }
END {
  print "v	e	r	k"
  for (n in a) {
    print a[n]["r"]"	"a[n]["k"]
  }
}
' | sed -e 's/\./,/g'
