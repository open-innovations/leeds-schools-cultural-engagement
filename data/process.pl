#!/usr/bin/perl

use utf8;
use Data::Dumper;
use Cwd qw(abs_path);
use JSON::XS;
use Geo::Coordinates::OSGB qw(ll_to_grid grid_to_ll);

# Get the real base directory for this script
my $basedir = "./";
if(abs_path($0) =~ /^(.*\/)[^\/]*/){ $basedir = $1; }

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

# Load in data
$schoolfile = "leeds_schools_public.csv";
@schools = Load($basedir.$schoolfile);
$edubase = Load($basedir."edubase-leeds.csv","URN");
@osmurls = ("https://raw.githubusercontent.com/open-innovations/west-yorkshire-mapping/main/data/leeds/leeds-amenities-school.geojson","https://raw.githubusercontent.com/open-innovations/west-yorkshire-mapping/main/data/leeds/leeds-amenities-college.geojson");
$osm = {'type'=>'FeatureCollection','features'=>()};
for($o = 0; $o < @osmurls; $o++){
	$geojson = Load($osmurls[$o]);
	for($i = 0; $i < @{$geojson->{'features'}}; $i++){
		push(@{$osm->{'features'}},$geojson->{'features'}[$i]);
	}
}
$n = @{$osm->{'features'}};


@keepfields = (
	{'src'=>'schools','field'=>'urn','rename'=>'URN'},
	{'src'=>'schools','field'=>'school_name','rename'=>'Name'},
	{'src'=>'edubase','field'=>'latitude','rename'=>'Latitude'},
	{'src'=>'edubase','field'=>'longitude','rename'=>'Longitude'},
	{'src'=>'schools','field'=>'type'},
	{'src'=>'schools','field'=>'phase_type_grouping'},
	{'src'=>'schools','field'=>'total_fulltime','rename'=>'total_FT'},
	{'src'=>'schools','field'=>'total_parttime','rename'=>'total_PT'},
	{'src'=>'schools','field'=>'total_pupils'},
	{'src'=>'schools','field'=>'artsmark_progress','empty'=>'?'},
	{'src'=>'schools','field'=>'most_recent_award'},
	{'src'=>'schools','field'=>'artsaward','empty'=>'NO'},
	{'src'=>'edubase','field'=>'StatutoryLowAge'},
	{'src'=>'edubase','field'=>'StatutoryHighAge'}
);


$csv = "";
$geojson = "";
for($s = 0; $s < @schools; $s++){
	$match = -1;
	
	
	$r1 = $schools[$s]->{'urn'};
	for($i = 0; $i < $n; $i++){
		$r2 = $osm->{'features'}[$i]{'properties'}{'other_tags'}{'ref:edubase'};
		if($r1 eq $r2){ $match = $i; last; print "$r1 => $r2\n"; }
	}

	# If we don't have a match we will try matching the edubase reference
	if($match < 0){

		$n1 = cleanSchoolName($schools[$s]->{'school_name'});
		for($i = 0; $i < $n; $i++){
			$n2 = cleanSchoolName($osm->{'features'}[$i]{'properties'}{'name'});
			if($n1 eq $n2){ $match = $i; last; }
		}

	}

	$urn = $schools[$s]->{'urn'};

	($lat,$lon) = grid_to_ll($edubase->{$urn}{'Easting'},$edubase->{$urn}{'Northing'});
	$edubase->{$urn}{'latitude'} = sprintf("%0.5f",$lat);
	$edubase->{$urn}{'longitude'} = sprintf("%0.5f",$lon);


	# Build CSV entry
	$csvrow = "";
	for($k = 0; $k < @keepfields; $k++){
		$v = "";
		if($keepfields[$k]->{'src'} eq "schools"){ $v = $schools[$s]->{$keepfields[$k]->{'field'}}; }
		elsif($keepfields[$k]->{'src'} eq "edubase"){ $v = $edubase->{$urn}{$keepfields[$k]->{'field'}}; }
		if($v eq "" && $keepfields[$k]->{'empty'}){ $v = $keepfields[$k]->{'empty'}; }
		$csvrow .= ($csvrow ? "," : "").($v =~ /\,/ ? "\"".$v."\"" : $v);
	}
	$csv .= "$csvrow\n";

	# Build GeoJSON entry
	$geojson .= ($geojson ? ",\n":"")."\t\t{ \"type\": \"Feature\", \"properties\": {\"URN\":\"$urn\",\"name\":\"$schools[$s]->{'school_name'}\"}, \"geometry\": {";
	if($match < 0){
		warning("$s - $schools[$s]->{'school_name'} NOT FOUND\n");
		$geojson .= "\"type\":\"Point\",\"coordinates\":\[".sprintf("%0.5f",$edubase->{$urn}{'longitude'}).",".sprintf("%0.5f",$edubase->{$urn}{'latitude'})."\]";
	}else{
		#msg("$s - $schools[$s]->{'school_name'}\n");
		$coords = JSON::XS->new->encode($osm->{'features'}[$i]{'geometry'}{'coordinates'});
		$coords =~ s/([0-9]\.[0-9]{5})[0-9]/$1/g;
		$geojson .= "\"type\":\"$osm->{'features'}[$i]{'geometry'}{'type'}\",\"coordinates\":".$coords."";;
	}
	$geojson .= "}}";

}


open(FILE,">",$basedir."../src/_data/viz/schools.csv");
# Build header
for($k = 0; $k < @keepfields; $k++){
	print FILE ($k > 0 ? ",":"").($keepfields[$k]->{'rename'}||$keepfields[$k]->{'field'});
}
print FILE "\n";
print FILE $csv;
close(FILE);

open(FILE,">",$basedir."../src/_data/viz/school-map.geojson");
print FILE "{\n\t\"type\":\"FeatureCollection\",\n\t\"features\":[\n";
print FILE $geojson;
print FILE "\n\t]\n\}\n";
close(FILE);


#########################

sub msg {
	my $str = shift;
	my $dest = shift||STDOUT;
	foreach my $c (keys(%colours)){ $str =~ s/\< ?$c ?\>/$colours{$c}/g; }
	print $dest $str;
}

sub error {
	my $str = shift;
	$str =~ s/(^[\t\s]*)/$1<red>ERROR:<none> /;
	msg($str,STDERR);
}

sub warning {
	my $str = shift;
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
	my $file = shift;
	my $arg = shift;
	my ($str,@lines);
	if(-e $file){
		msg("Processing file from <cyan>$file<none>\n");
		open(FILE,"<:utf8",$file);
		@lines = <FILE>;
		close(FILE);
	}elsif($file =~ /^https?\:/){
		msg("Downloading from <cyan>$file<none>\n");
		@lines = getURL($file);
	}else{
		msg("File <cyan>$file<none> doesn't seem to exist or be a valid URL.\n");
		@lines = ();
	}

	$str = join("",@lines);

	if($file =~ /\.csv$/){
		return parseCSV($str,$arg);
	}elsif($file =~ /\.json$/){
		return parseJSON($str);
	}elsif($file =~ /\.geojson$/){
		return parseGeoJSON($str);
	}else{
		warning("Unknown file type to process \"$file\".\n");
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
				# Trim quotes
				for($c = 0; $c < @cols; $c++){
					$cols[$c] =~ s/(^\"|\"$)//g;
				}
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
	if($@){ warning("Invalid JSON.\n".$str); }
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
