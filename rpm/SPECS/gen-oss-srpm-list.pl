#!/usr/bin/env perl

use v5.10.1;
use strict;
use warnings;

sub shell ($);
sub cd ($);

my $old_list = <<_EOC_;
https://openresty.org/download/perl-Lemplate-0.15-3.fc29.src.rpm
https://openresty.org/download/perl-Test-Nginx-0.29-2.fc28.src.rpm
https://openresty.org/download/openresty-zlib-1.2.11-4.fc28.src.rpm
https://openresty.org/download/openresty-zlib-asan-1.2.11-17.fc28.src.rpm
https://openresty.org/download/openresty-pcre-8.44-2.fc28.src.rpm
https://openresty.org/download/openresty-pcre-asan-8.44-5.fc28.src.rpm
https://openresty.org/download/openresty-openssl111-1.1.1k-1.fc28.src.rpm
https://openresty.org/download/openresty-openssl111-debug-1.1.1k-1.fc28.src.rpm
https://openresty.org/download/openresty-openssl111-asan-1.1.1k-1.fc28.src.rpm
https://openresty.org/download/openresty-openssl-1.1.0l-3.fc28.src.rpm
https://openresty.org/download/openresty-openssl-debug-1.1.0l-3.fc28.src.rpm
https://openresty.org/download/openresty-openssl-asan-1.1.0l-3.fc28.src.rpm
https://openresty.org/download/openresty-1.19.3.2-1.fc28.src.rpm
https://openresty.org/download/openresty-debug-1.19.3.2-1.fc28.src.rpm
https://openresty.org/download/openresty-valgrind-1.19.3.1-2.fc28.src.rpm
https://openresty.org/download/openresty-asan-1.19.3.1-5.fc28.src.rpm
_EOC_

open my $in, "<", \$old_list
    or die $!;

my @wanted_files;
my %wanted_files;
while (<$in>) {
    next if /^\s*$/;
    chomp;
    if (!m{/([^/]+\.src\.rpm)$}) {
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
    say "https://openresty.org/download/$fname";
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
