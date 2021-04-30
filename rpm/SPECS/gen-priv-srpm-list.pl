#!/usr/bin/env perl

use v5.10.1;
use strict;
use warnings;

sub shell ($);
sub cd ($);

my $old_list = <<_EOC_;
openresty-plzip-1.8-3.fc28.src.rpm
openresty-yajl-2.1.0.4-2.fc28.src.rpm
openresty-tar-1.32-3.fc28.src.rpm
openresty-binutils-2.33.1.1-4.fc28.src.rpm
openresty-elfutils-0.177.12-6.fc28.src.rpm
openresty-util-linux-2.35.1.3-2.fc28.src.rpm
openresty-utils-0.17-2.fc28.src.rpm
openresty-saas-zlib-1.2.11-2.fc28.src.rpm
openresty-saas-pcre-8.44-3.fc28.src.rpm
openresty-saas-openssl111-1.1.1i-3.fc28.src.rpm
openresty-python3-3.7.9-15.fc28.src.rpm
openresty-python3-cython-0.28.5-6.fc28.src.rpm
openresty-python3-setuptools-39.2.0-5.fc28.src.rpm
openresty-python3-goto-1.2.1-3.fc28.src.rpm
openresty-python3-numpy-1.16.4-11.fc28.src.rpm
openresty-stap-4.5.0.5-6.fc28.src.rpm
openresty-gdb-10.1-3.fc28.src.rpm
openresty-plus-hyperscan-5.0.0-11.fc28.src.rpm
openresty-pcap-1.9.1-3.fc28.src.rpm
openresty-tcpdump-4.9.3.3-2.fc28.src.rpm
openresty-maxminddb-1.4.2.4-2.fc28.src.rpm
openresty-maxminddb-debug-1.4.2.4-2.fc28.src.rpm
openresty-maxminddb-asan-1.4.2.4-4.fc28.src.rpm
openresty-saas-1.19.3.1.3-2.fc28.src.rpm
openresty-plus-openssl111-1.1.1i-2.fc28.src.rpm
openresty-plus-openssl111-debug-1.1.1i-2.fc28.src.rpm
openresty-plus-openssl111-asan-1.1.1i-3.fc28.src.rpm
openresty-plus-1.19.3.1.6-2.fc28.src.rpm
openresty-plus-debug-1.19.3.1.6-2.fc28.src.rpm
openresty-plus-asan-1.19.3.1.28-2.fc28.src.rpm
openresty-postgresql12-12.5-4.fc28.src.rpm
openresty-postgresql12-ip4r-2.4.1-2.fc28.src.rpm
openresty-postgresql12-orsl-0.02-2.fc28.src.rpm
openresty-postgresql12-timescaledb-1.7.4-2.fc28.src.rpm
openresty-postgresql-9.6.20-5.fc28.src.rpm
openresty-postgresql-ip4r-2.4.1-3.fc28.src.rpm
openresty-postgresql-orsl-0.02-2.fc28.src.rpm
openresty-postgresql-timescaledb-1.7.4-1.fc28.src.rpm
openresty-odb-0.23-2.fc28.src.rpm
openresty-odb-debug-0.23-2.fc28.src.rpm
lua-resty-jsonb-0.0.5-1.fc28.src.rpm
openresty-firejail-0.9.62-2.fc28.src.rpm
openresty-coreutils-8.32-3.fc28.src.rpm
openresty-python3-xray-stats-0.0.3-1.fc28.src.rpm
openresty-nodejs-15.4.0-4.fc28.src.rpm
openresty-perl-5.24.4-1.fc28.src.rpm
openresty-perl-B-Flags-0.17-1.fc28.src.rpm
openresty-perl-ExtUtils-Config-0.008-1.fc28.src.rpm
openresty-perl-ExtUtils-Helpers-0.026-1.fc28.src.rpm
openresty-perl-ExtUtils-InstallPaths-0.012-1.fc28.src.rpm
openresty-perl-Module-Build-Tiny-0.039-1.fc28.src.rpm
openresty-perl-Readonly-2.05-1.fc28.src.rpm
openresty-perl-IPC-Run-20200505.0-1.fc28.src.rpm
openresty-perl-IO-Tty-1.16-2.fc28.src.rpm
openresty-perl-Opcodes-0.14-1.fc28.src.rpm
openresty-perl-B-C-1.57-1.fc28.src.rpm
openresty-saas-zlib-1.2.11-3.fc28.src.rpm

openresty-saas-1.19.3.1.7-2.fc28.src.rpm
openresty-utils-0.20-3.fc28.src.rpm
openresty-odb-0.23-3.fc28.src.rpm
openresty-odb-debug-0.23-3.fc28.src.rpm

openresty-keepalived-2.2.1-1.fc28.src.rpm
_EOC_

open my $in, "<", \$old_list
    or die $!;

my @wanted_files;
my %wanted_files;
while (<$in>) {
    next if /^\s*$/;
    chomp;
    if (!m{^([^/]+\.src\.rpm)$}) {
        die "error: line $.: $_\n";
    }
    my $fname = $1;
    if ($fname =~ m{^(\S+)-([.\w]+)-(\d+)\.(\w+)\.src\.rpm$}) {
        my $basename = $1;
        #warn $basename;
        if (!defined $wanted_files{$basename}) {
            $wanted_files{$basename} = 1;
            push @wanted_files, $basename;
        }

    } else {
        die "error: line $.: bad src.rpm file name: $fname\n";
    }
}

close $in;

cd $ENV{HOME} . "/packaging/SRPMS";
shell "clean-old-rpms.pl 1 1";

my @files = glob "*.src.rpm";
for my $file (@files) {
    if ($file =~ m{^(\S+)-([.\w]+)-(\d+)\.(\w+)\.src\.rpm$}) {
        my $basename = $1;
        #warn "$basename: $file\n";
        next if !exists $wanted_files{$basename};
        $wanted_files{$basename} = $file;
    }
}

for my $basename (@wanted_files) {
    my $fname = $wanted_files{$basename};
    if ($fname eq '1') {
        die "Package $basename not found.\n";
    }
    say $fname;
}

sub shell ($) {
    my $cmd = shift;
    system($cmd) == 0
        or die "Cannot run cmd '$cmd': $?\n";
}

sub cd ($) {
    my $dir = shift;
    chdir $dir or die "Cannot chdir to '$dir': $!\n";
}
