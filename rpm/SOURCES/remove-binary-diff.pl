#!/usr/bin/perl -w
# A script to remove those terrible binary diffs from the patches which
# screw up everything and rain on my parade.

use strict;

my @args=@ARGV;
my @current_patch;
my $is_binary = 0;
my $cnt = 0;

while(my $row = <>) {
	# diff marks the start of a new file to check
	if ($row =~ /^diff --git.*?(\S+)$/) {
		if (!$is_binary) {
			foreach my $line (@current_patch) {
				print $line;
			}
		}
		$is_binary = 0;
		@current_patch = ();
	} elsif ($row =~ /Binary files (.)* differ$/) {
		$is_binary = 1;
	} elsif ($row =~ /GIT binary patch/) {
		$is_binary = 1;
	}
	push (@current_patch, $row);
}

if (!$is_binary) {
	foreach my $line (@current_patch) {
		print $line;
	}
}
