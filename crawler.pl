use strict;
use warnings;
use POSIX qw(strftime);
use feature 'state';
use WWW::Mechanize;

sub genDate {
    return my $date = strftime "$_[0]", localtime time()-($_[1]*24*60*60);
}

my $mech = WWW::Mechanize->new();
my @all_urls;
my %news_links;
my $total_berita = 0;
my $url = "";
my $fileName = "output.txt";

my $total_days = int($ARGV[0]) or die "Anda tidak memasukkan argument untuk hari !\n";
open FileOutput, ">$fileName";

print "- Mulai -\n";

for (my $i = 0; $i <= $total_days-1; $i++) {
    my $date = genDate("%Y-%m-%d", $i); 

    #melakukan operasi split terhadap string hasil dari
    #operasi genDate(). Setiap angka dipisahkan menurut tanda '-'
    (my $year, my $month, my $day) = split /-/, $date;
    print "Crawling data pada $date\n";
    print "   Loading...\n";
    
    for (my $page = 0; $page <= 15; $page++) {
        $url ="https://indeks.kompas.com/?site=all&date=$year-$month-$day&page=$page";
        $mech->get($url);
        @all_urls = $mech->links();
        foreach my $link (@all_urls) {
            my $url = $link->url;
            $news_links{$url} = 1;
            $total_berita++;
        }
        sleep(rand(5));
    }
}
print "- Selesai -\nBerhasil mendapatkan ". $total_berita ." tautan.\n";

my $jumlah_article = 0;
foreach my $url(keys (%news_links)) {
    if($url =~ m[read\/\d*]) { #menggunakan regex
        print FileOutput "$url\n";
        $jumlah_article++;
        # if ($jumlah_article == 1000) {
        #     last;
        # }
    }
}
print "URL yang tersimpan sebanyak ". $jumlah_article ." url\n\n";
close FileOutput;