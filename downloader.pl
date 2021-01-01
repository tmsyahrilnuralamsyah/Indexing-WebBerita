use strict;
use warnings;
use LWP::Simple;

my $filename = './output.txt';
open(my $fh, '<', $filename);

my $x=0;
while (my $row = <$fh>) {
    my $filename = "./download/Kompas-". $x .".html";
    getstore($row, $filename);
    $x++;
    sleep(rand(5));
}
print "Selesai"