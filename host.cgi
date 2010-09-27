#!/usr/bin/perl

##### 開発記録など ############

##### 設定 ####################
# このｃｇｉのファイルの名前
$this_cgi = 'host.cgi';

# オーナーパスの設定(変更してください)
$ona_pas = '';

# 許可管理者名
$kanre_name = '';

$ona_id = '';

$hozon_fail = 'in_host.cgi';

#=====================
&loadformdata;	#フォーム入力
&getoin;

sub getoin{

	print "Content-type:text/html;\n\n";
	print <<EOF ;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<title>許可ホスト変更</title>
</head>
<body>
EOF

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq "" || $host eq $addr) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr; #koko2007/05/18
	}
	if ($host eq "") { $host = $addr; }

	if($FORM{'name'} eq $kanre_name && $FORM{'id'} eq $ona_id && $FORM{'pas'} eq $ona_pas && $FORM{'kanri'} eq $FORM{'kensa'}){
		open (IN, "< $hozon_fail") or die;
		eval{ flock (IN, 1); };
		$f_host = <IN>;
		@host_kiroku = <IN>;
		close (IN);
		&get_time;
		if($#host_kiroku >= 24){$#host_kiroku = 24;}
		unshift @host_kiroku,"$FORM{'host_in'}<>$jikan<>\n";
		open (OUT, "> $hozon_fail") or die;
		eval{ flock (OUT, 2); };
		print OUT "$FORM{'host_in'}\n";
		print OUT @host_kiroku ;
		close (OUT);
	}
	$kensa = sprintf("%04d",int(rand(10000)));
	print <<EOF ;
<h2 align="center">許可ホスト変更</h2><br>

<div align="center"><form action="$this_cgi" method="post">
名前：<input type="text" name="name"><br>
ＩＤ：<input type="text" name="id"><br>
パスワード：<input type="password" name="pas"><br>
確認：<input type=text name="kensa"> <font color=#ff0000>$kensa</font>を左に入れてください
<input type=hidden name=kanri value=$kensa><br>
現在のホスト $host<br>
設定ホスト：<input type=text name="host_in" value="$host"><br>
<input type=submit value=" 送 信 "><br>
</form><br>
EOF

	foreach (@host_kiroku){
		($host_disp,$time_disp) = split(/<>/);
		print "$host_disp , $time_disp<br>";
	}
	print "</div></body></html>\n";
	exit;
}

### フォーム受信 ##########
sub loadformdata {
	$max_size = 200;
	my ($query,$pair);
	if($ENV{'REQUEST_METHOD'} eq 'POST') {
		read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
	} else {
		$query = $ENV{'QUERY_STRING'};
		if ($get_no ==1 && $query ne ""){&err2("エラー・GET 禁止");}
	}
	my ($saizu)=length $query;
	if ($saizu > $max_size){&err2("エラー・サイズオーバー");}
	
	foreach $pair (split(/&/, $query)) {
		my ($key, $value) = split(/=/, $pair);
	
	# 文字のデコード
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
	
#		$value = jcode::sjis($value);	# euc? sjis? jcode.plが必要
		$value =~ s/&/&amp;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/"/&quot;/g;
		$value =~ s/\x0D\x0A/<br>/g;
	#	$value =~ tr/\t/ /; #2007/05/06
	
		$FORM{$key} = $value;
	}
}

### 現在の時間出し ###############
sub get_time{
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time) ;	#一括取り入れ
	$year += 1900;	# $year = $year + 1900 と同じ
	++$mon ;
	@youbi=('日','月','火','水','木','金','土');

	$mond = sprintf("%02d",$mon);
	$mdayd = sprintf("%02d",$mday);
	$hourd = sprintf("%02d",$hour);
	$mind = sprintf("%02d",$min);
	$secd = sprintf("%02d",$sec);

	$jikan = "$year年$mond月$mdayd日$youbi[$wday]曜日$hourd時$mind分$secd秒";

#	$countup = 1;

}

