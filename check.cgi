#!/usr/bin/perl

# Copyright (c) CGIROOM.   http://cgiroom.nu
#======================================================================#
# [Ver  2.02] 簡易 Perl CGI Script 実行チェックプログラム
#
# このプログラムによって起きた事にCGIROOMは責任を負いません。
# 利用契約に同意できない方のご利用は、遠慮下さい。

	#=====変数の取得=====#
	local($buf, $key, $val, @buf, $cuntkey);
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$size = 5000;
		$remain = $ENV{'CONTENT_LENGTH'};
		if($remain > $size){&error("サイズオーバー");}
		read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
	} else {
		$query = $ENV{'QUERY_STRING'};
	}

	#=====文字のデコード=====#
	foreach $pair (split(/&/, $query)) {
		($key, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
		$in{$key} = $value;
	}


if($in{'mode'} eq "check"){&check;}
else{
	print "Content-type: text/html\n\n";
	print <<"EOM";
	<form action="check.cgi" method="POST">
	<input type="text" name="cgiroom_cgi" size="15">
	<input type="hidden" name="mode" value="check">
	<input type="submit" value="検査">
	</form>
EOM
}
exit;
#======================================================================#
# ＣＧＩの実行 ＆ 出力
sub check{
$cgiroom_cgi=$in{'cgiroom_cgi'};
$cgiroom_check= (split(/\\|\/|\:/,$0))[-1];
open(CHECK,$cgiroom_cgi) || &cgiroom_error("チェックしようとしたＣＧＩ($cgiroom_cgi)が見つかりません。");
while(<CHECK>){
	last if /^__END__[\r\n]+$/;
	$cgiroom_perl .= $_;
}
close(CHECK);

$cgiroom_perl =~ s/$cgiroom_cgi/$cgiroom_check/g;
eval $cgiroom_perl;
&cgiroom_error("$cgiroom_cgiを実行した結果エラーが報告されました。<hr><pre>$@</pre><hr>CHECK ") if $@ ne "";
exit;
}
sub cgiroom_error{
	print "Content-type: text/html\n\n";
	print "$_[0]<hr size=1><pre>$]</pre><hr size=1><a href=\"http://cgiroom.nu\" target=cgiroom>CGIROOM</a>";
	exit;
}
__END__
1999/07/12  Ver  1.00
1999/10/02  Ver  2.00
2000/09/23  Ver  2.01
2000/10/12  Ver  2.02