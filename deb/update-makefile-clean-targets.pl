#!/usr/bin/env perl

use v5.10.1;
use strict;
use warnings;

sub cols ($);

use List::Util qw/ uniq /;
my @goals;
while (<>) {
    s/\s*\\\s*$//;
    push @goals, grep { !/^\s*$/ } split /\s+/, $_;
}

my %all_goals;
{
    my @all_goals = grep { !/^\s*$/ } map { s/.*?://; s/:$//; $_ } split /\n+/, `grep -E '^[-a-zA-Z0-9_]+-clean:' *.mk Makefile`;
    warn "all goals: ", scalar @all_goals;
    %all_goals = map { $_ => 1 } @all_goals;
}

warn "old: ", scalar @goals;
@goals = uniq @goals;
warn "new: ", scalar @goals;
#print join " ", @goals;

for my $goal (@goals) {
    if ($goal !~ /-clean$/) {
        die "bad target: $goal";
    }
    my $val = delete %all_goals{$goal};
    if (!$val) {
        die "clean target $goal not defined";
    }
}

if (%all_goals) {
    for my $g (sort keys %all_goals) {
        if ($g !~ /-clean$/) {
            die "bad target: $g";
        }
        push @goals, $g;
    }
}

my $line = "clean:";
while (@goals) {
    my $goal = shift @goals;
    my $new = "$line $goal";
    if (cols($new) > 80) {
        unshift @goals, $goal;
        print $line, " \\\n";
        $line = "\t\t";
    } else {
        $line = $new;
    }
}

if ($line ne "\t\t") {
    print "$line\n";
} else {
    print "\n";
}

sub cols ($) {
    my $s = shift;
    $s .= " \\\n";
    $s =~ s/\t/        /g;
    length $s;
}
