#!/usr/bin/perl

use Data::Dumper;
use JSON::XS;


my %colours = (
	'black'=>"\033[0;30m",
	'red'=>"\033[0;31m",
	'green'=>"\033[0;32m",
	'yellow'=>"\033[0;33m",
	'blue'=>"\033[0;34m",
	'magenta'=>"\033[0;35m",
	'cyan'=>"\033[0;36m",
	'white'=>"\033[0;37m",
	'none'=>"\033[0m"
);

@osmurls = ("https://raw.githubusercontent.com/open-innovations/west-yorkshire-mapping/main/data/leeds/leeds-amenities-school.geojson","https://raw.githubusercontent.com/open-innovations/west-yorkshire-mapping/main/data/leeds/leeds-amenities-college.geojson");
$schoolfile = "leeds_schools_public.csv";

#print Dumper Load($osmurl);
@schools = Load($schoolfile);
$osm = {'type'=>'FeatureCollection','features'=>()};
for($o = 0; $o < @osmurls; $o++){
	$geojson = Load($osmurls[$o]);
	for($i = 0; $i < @{$geojson->{'features'}}; $i++){
		push(@{$osm->{'features'}},$geojson->{'features'}[$i]);
	}
}

$n = @{$osm->{'features'}};

for($s = 0; $s < @schools; $s++){
	$match = -1;
	$n1 = cleanSchoolName($schools[$s]->{'school_name'});
	for($i = 0; $i < $n; $i++){
		$n2 = cleanSchoolName($osm->{'features'}[$i]{'properties'}{'name'});
		if($n1 eq $n2){ $match = $i; last; }
	}
	msg("$s = $schools[$s]->{'school_name'}\n");

	# If we don't have a match we will try matching the edubase reference
	if($match < 0){

		$r1 = $schools[$s]->{'urn'};
		for($i = 0; $i < $n; $i++){
			$r2 = $osm->{'features'}[$i]{'properties'}{'other_tags'}{'ref:edubase'};
			if($r1 eq $r2){ $match = $i; last; print "$r1 => $r2\n"; }
		}
		msg("\tRef:edubase $match ($r1)\n");


		# If we have no match we try matching by postcode
		if($match < 0){

			warning("\tNo EDUBASE code\n");

			$p1 = cleanPostcode($schools[$s]->{'school_postcode'});
			for($i = 0; $i < $n; $i++){
				$p2 = cleanPostcode($osm->{'features'}[$i]{'properties'}{'other_tags'}{'addr:postcode'});
				if($schools[$s]->{'school_postcode'} eq $osm->{'features'}[$i]{'properties'}{'other_tags'}{'addr:postcode'}){ $match = $i; last; }
			}
			if($match < 0){
				warning("\tNo postcode match for $schools[$s]->{'school_name'}\n");
			}else{
				msg("\tPostcode: $match ($schools[$s]->{'school_name'} / $osm->{'features'}[$match]{'properties'}{'name'})\n");
			}
		}


	}
}


#########################

sub msg {
	my $str = $_[0];
	my $dest = $_[1]||STDOUT;
	foreach my $c (keys(%colours)){ $str =~ s/\< ?$c ?\>/$colours{$c}/g; }
	print $dest $str;
}

sub error {
	my $str = $_[0];
	$str =~ s/(^[\t\s]*)/$1<red>ERROR:<none> /;
	msg($str,STDERR);
}

sub warning {
	my $str = $_[0];
	$str =~ s/(^[\t\s]*)/$1$colours{'yellow'}WARNING:$colours{'none'} /;
	print STDERR $str;
}

sub cleanSchoolName {
	my $name = shift;
	$name = lc($name);
	$name =~ s/^the //g;
	$name =~ s/\.//g;
	return $name;
}
sub cleanPostcode {
	my $pc = shift;
	$pc = lc($pc);
	$pc =~ s/ //g;
	return $pc;
}
sub getURL {
	my $url = $_[0];
	my @lines = `wget -q -e robots=off  --no-check-certificate -O- "$url"`;
	return @lines;
}

sub Load {
	my $file = $_[0];
	my ($str,@lines);
	if(-e $file){
		msg("\tProcessing file from <cyan>$file<none>\n");
		open(FILE,"<:utf8",$file);
		@lines = <FILE>;
		close(FILE);
	}elsif($file =~ /^https?\:/){
		msg("\tDownloading from <cyan>$file<none>\n");
		@lines = getURL($file);
	}else{
		msg("\tFile <cyan>$file<none> doesn't seem to exist or be a valid URL.\n");
		@lines = ();
	}

	$str = join("",@lines);

	if($file =~ /\.csv$/){
		return parseCSV($str);
	}elsif($file =~ /\.json$/){
		return parseJSON($str);
	}elsif($file =~ /\.geojson$/){
		return parseGeoJSON($str);
	}else{
		warning("\tUnknown file type to process \"$file\".\n");
	}
}

sub parseCSV {
	my $str = shift;
	my $col = shift;

	my (@rows,@cols,@header,$r,$c,@features,$data,$key,$k,$f);

	@rows = split(/[\r\n]+/,$str);

	for($r = 0; $r < @rows; $r++){
		@cols = split(/,(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))/,$rows[$r]);
		if($r < 1){
			# Header
			if(!@header){
				@header = @cols;
			}else{
				for($c = 0; $c < @cols; $c++){
					$header[$c] .= "\n".$cols[$c];
				}
			}
		}else{
			$data = {};
			for($c = 0; $c < @cols; $c++){
				$cols[$c] =~ s/(^\"|\"$)//g;
				$data->{$header[$c]} = $cols[$c];
			}
			push(@features,$data);
		}
	}
	if($col && $col ne ""){
		$data = {};
		for($r = 0; $r < @features; $r++){
			$data->{$features[$r]->{$col}} = $features[$r];
		}
		return $data;
	}else{
		return @features;
	}
}

sub parseJSON {
	my ($str,$json);
	$str = shift;

	if(!$str){ $str = "{}"; }
	eval {
		$json = JSON::XS->new->decode($str);
	};
	if($@){ warning("\tInvalid JSON.\n".$str); }
	if(ref($json) eq "ARRAY"){
		return {'array'=>\@{$json}};
	}else{
		return $json;
	}
}

sub parseGeoJSON {
	my ($str,$json,$f,$nf);
	$str = shift;
	$json = parseJSON($str);
	
	$nf = @{$json->{'features'}};
	for($f = 0; $f < $nf; $f++){
		if($json->{'features'}[$f]{'properties'}{'other_tags'}){
			$json->{'features'}[$f]{'properties'}{'other_tags'} = parseTagString($json->{'features'}[$f]{'properties'}{'other_tags'});
		}
	}
	return $json;
}

sub parseTagString {
	my $str = shift;
	my (@parts,$p,$json,$k,$v);
	@parts = split(/,(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))/,$str);
	for($p = 0; $p < @parts; $p++){
		($k,$v) = split(/\=\>/,$parts[$p]);
		$k =~ s/(^\"|\"$)//g;
		$v =~ s/(^\"|\"$)//g;
		$json->{$k} = $v;
	}
	return $json;
}
