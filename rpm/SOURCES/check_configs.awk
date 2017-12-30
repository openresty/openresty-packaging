#!/usr/bin/awk -f

/is not set/ {
                split ($0, a, "#");
                split(a[2], b);
                if (NR==FNR) {
                        configs[b[1]]="is not set";
                } else {
                        if (configs[b[1]] != "" && configs[b[1]] != "is not set")
                                print "Found # "b[1] " is not set, after generation, had " b[1] " " configs[b[1]] " in Fedora tree";
                }
}

/=/     {
                split ($0, a, "=");
                if (NR==FNR) {
                        configs[a[1]]=a[2];
                } else {
                        if (configs[a[1]] != "" && configs[a[1]] != a[2])
                                print "Found "a[1]"="configs[a[1]]"  after generation, had " a[1]"="a[2]" in Fedora tree";
                }
}
